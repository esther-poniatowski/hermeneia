"""Strict configuration parsing and validation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping

from hermeneia.config.defaults import DEFAULT_PROFILE
from hermeneia.rules.base import Severity


class ConfigError(ValueError):
    """Raised when a configuration file is structurally invalid."""


@dataclass(frozen=True)
class ProfileConfig:
    name: str = DEFAULT_PROFILE
    audience: str | None = None
    genre: str | None = None
    section: str | None = None
    register: str | None = None


@dataclass(frozen=True)
class LanguageConfig:
    code: str = "en"
    pack: str | None = None


@dataclass(frozen=True)
class RuntimeConfig:
    strict_validation: bool = True
    experimental_rules: bool = False
    external_rule_modules: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuleOverrideConfig:
    enabled: bool | None = None
    severity: Severity | None = None
    weight: float | None = None
    options: Mapping[str, object] = field(default_factory=dict)
    extra_patterns: tuple[str, ...] = ()
    silenced_patterns: tuple[str, ...] = ()


@dataclass(frozen=True)
class RulesConfig:
    active: tuple[str, ...] | None = None
    disabled: tuple[str, ...] = ()
    overrides: Mapping[str, RuleOverrideConfig] = field(default_factory=dict)


@dataclass(frozen=True)
class ScoringConfig:
    aggregation: str = "hierarchical"
    output: tuple[str, ...] = ("layer_scores", "global_score", "violation_list")


@dataclass(frozen=True)
class SuggestionConfig:
    enabled: bool = True
    default_mode: str = "tactic_only"


@dataclass(frozen=True)
class ReportingConfig:
    format: str = "text"
    sort_by: str = "severity_desc"


@dataclass(frozen=True)
class ProjectConfig:
    profile: ProfileConfig = ProfileConfig()
    language: LanguageConfig = LanguageConfig()
    runtime: RuntimeConfig = RuntimeConfig()
    rules: RulesConfig = RulesConfig()
    scoring: ScoringConfig = ScoringConfig()
    suggestions: SuggestionConfig = SuggestionConfig()
    reporting: ReportingConfig = ReportingConfig()


def parse_project_config(raw: Mapping[str, object] | None) -> ProjectConfig:
    """Validate a raw mapping and return the typed config object."""

    if raw is None:
        return ProjectConfig()
    _ensure_fields(raw, {"profile", "language", "runtime", "rules", "scoring", "suggestions", "reporting"}, "root")
    return ProjectConfig(
        profile=_parse_profile(_mapping(raw.get("profile"), "profile")),
        language=_parse_language(_mapping(raw.get("language"), "language")),
        runtime=_parse_runtime(_mapping(raw.get("runtime"), "runtime")),
        rules=_parse_rules(_mapping(raw.get("rules"), "rules")),
        scoring=_parse_scoring(_mapping(raw.get("scoring"), "scoring")),
        suggestions=_parse_suggestions(_mapping(raw.get("suggestions"), "suggestions")),
        reporting=_parse_reporting(_mapping(raw.get("reporting"), "reporting")),
    )


def _parse_profile(raw: Mapping[str, object]) -> ProfileConfig:
    _ensure_fields(raw, {"name", "audience", "genre", "section", "register"}, "profile")
    return ProfileConfig(
        name=_string(raw.get("name"), "profile.name", DEFAULT_PROFILE),
        audience=_optional_string(raw.get("audience"), "profile.audience"),
        genre=_optional_string(raw.get("genre"), "profile.genre"),
        section=_optional_string(raw.get("section"), "profile.section"),
        register=_optional_string(raw.get("register"), "profile.register"),
    )


def _parse_language(raw: Mapping[str, object]) -> LanguageConfig:
    _ensure_fields(raw, {"code", "pack"}, "language")
    return LanguageConfig(
        code=_string(raw.get("code"), "language.code", "en"),
        pack=_optional_string(raw.get("pack"), "language.pack"),
    )


def _parse_runtime(raw: Mapping[str, object]) -> RuntimeConfig:
    _ensure_fields(raw, {"strict_validation", "experimental_rules", "external_rule_modules"}, "runtime")
    return RuntimeConfig(
        strict_validation=_bool(raw.get("strict_validation"), "runtime.strict_validation", True),
        experimental_rules=_bool(raw.get("experimental_rules"), "runtime.experimental_rules", False),
        external_rule_modules=_string_tuple(raw.get("external_rule_modules"), "runtime.external_rule_modules"),
    )


def _parse_rules(raw: Mapping[str, object]) -> RulesConfig:
    _ensure_fields(raw, {"active", "disabled", "overrides"}, "rules")
    overrides_raw = _mapping(raw.get("overrides"), "rules.overrides", allow_none=True)
    overrides: dict[str, RuleOverrideConfig] = {}
    for rule_id, value in overrides_raw.items():
        if not isinstance(rule_id, str):
            raise ConfigError("rules.overrides keys must be rule ids")
        overrides[rule_id] = _parse_rule_override(_mapping(value, f"rules.overrides.{rule_id}"))
    active = raw.get("active")
    return RulesConfig(
        active=None if active is None else _string_tuple(active, "rules.active"),
        disabled=_string_tuple(raw.get("disabled"), "rules.disabled"),
        overrides=overrides,
    )


def _parse_rule_override(raw: Mapping[str, object]) -> RuleOverrideConfig:
    legacy_option_fields = {
        "threshold",
        "max_words",
        "max_distance",
        "lookback_sentences",
        "minimum_score",
        "require_leadin",
        "max_distinct_acronyms",
    }
    _ensure_fields(
        raw,
        {
            "enabled",
            "severity",
            "weight",
            "options",
            "extra_patterns",
            "silenced_patterns",
            *legacy_option_fields,
        },
        "rule override",
    )
    options_raw = _mapping(raw.get("options"), "rule override.options", allow_none=True)
    options: dict[str, object] = {}
    for key, value in options_raw.items():
        if not isinstance(key, str):
            raise ConfigError("rule override.options keys must be strings")
        options[key] = value
    for key in legacy_option_fields:
        if key in raw:
            options[key] = raw[key]
    severity_value = raw.get("severity")
    return RuleOverrideConfig(
        enabled=_optional_bool(raw.get("enabled"), "rule override.enabled"),
        severity=None if severity_value is None else Severity(str(severity_value)),
        weight=_optional_float(raw.get("weight"), "rule override.weight"),
        options=options,
        extra_patterns=_string_tuple(raw.get("extra_patterns"), "rule override.extra_patterns"),
        silenced_patterns=_string_tuple(raw.get("silenced_patterns"), "rule override.silenced_patterns"),
    )


def _parse_scoring(raw: Mapping[str, object]) -> ScoringConfig:
    _ensure_fields(raw, {"aggregation", "output"}, "scoring")
    return ScoringConfig(
        aggregation=_string(raw.get("aggregation"), "scoring.aggregation", "hierarchical"),
        output=_string_tuple(raw.get("output"), "scoring.output") or ("layer_scores", "global_score", "violation_list"),
    )


def _parse_suggestions(raw: Mapping[str, object]) -> SuggestionConfig:
    _ensure_fields(raw, {"enabled", "default_mode"}, "suggestions")
    return SuggestionConfig(
        enabled=_bool(raw.get("enabled"), "suggestions.enabled", True),
        default_mode=_string(raw.get("default_mode"), "suggestions.default_mode", "tactic_only"),
    )


def _parse_reporting(raw: Mapping[str, object]) -> ReportingConfig:
    _ensure_fields(raw, {"format", "sort_by"}, "reporting")
    return ReportingConfig(
        format=_string(raw.get("format"), "reporting.format", "text"),
        sort_by=_string(raw.get("sort_by"), "reporting.sort_by", "severity_desc"),
    )


def _ensure_fields(raw: Mapping[str, object], allowed: set[str], scope: str) -> None:
    for field_name in raw:
        if field_name not in allowed:
            raise ConfigError(f"Unknown field '{field_name}' in {scope}")


def _mapping(raw: object, scope: str, allow_none: bool = False) -> Mapping[str, object]:
    if raw is None:
        if allow_none:
            return {}
        return {}
    if not isinstance(raw, Mapping):
        raise ConfigError(f"{scope} must be a mapping")
    return raw


def _string(raw: object, scope: str, default: str) -> str:
    if raw is None:
        return default
    if not isinstance(raw, str):
        raise ConfigError(f"{scope} must be a string")
    return raw


def _optional_string(raw: object, scope: str) -> str | None:
    if raw is None:
        return None
    if not isinstance(raw, str):
        raise ConfigError(f"{scope} must be a string")
    return raw


def _bool(raw: object, scope: str, default: bool) -> bool:
    if raw is None:
        return default
    if not isinstance(raw, bool):
        raise ConfigError(f"{scope} must be a boolean")
    return raw


def _optional_bool(raw: object, scope: str) -> bool | None:
    if raw is None:
        return None
    if not isinstance(raw, bool):
        raise ConfigError(f"{scope} must be a boolean")
    return raw


def _optional_float(raw: object, scope: str) -> float | None:
    if raw is None:
        return None
    if not isinstance(raw, (int, float)):
        raise ConfigError(f"{scope} must be numeric")
    return float(raw)


def _string_tuple(raw: object, scope: str) -> tuple[str, ...]:
    if raw is None:
        return ()
    if not isinstance(raw, list):
        raise ConfigError(f"{scope} must be a list of strings")
    if not all(isinstance(item, str) for item in raw):
        raise ConfigError(f"{scope} must be a list of strings")
    return tuple(raw)
