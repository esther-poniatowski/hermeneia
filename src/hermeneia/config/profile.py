"""Resolved profile construction with strict merge semantics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Mapping

from hermeneia.config.defaults import PROFILE_PRESETS, ProfilePreset
from hermeneia.config.schema import ProjectConfig, RuleOverrideConfig
from hermeneia.engine.registry import RuleRegistry
from hermeneia.language.base import LanguagePack
from hermeneia.rules.base import ResolvedProfile, ResolvedRuleSettings, Severity

COMMA_SEPARATOR = ", "


@dataclass(frozen=True)
class CliOverrides:
    """Clioverrides."""

    profile_name: str | None = None
    rule_ids: tuple[str, ...] = ()
    disabled_rule_ids: tuple[str, ...] = ()
    reporting_format: str | None = None
    enable_experimental: bool | None = None


class ProfileResolver:
    """Merge rule defaults, language defaults, profile defaults, and overrides."""

    def __init__(self, registry: RuleRegistry) -> None:
        """Init."""
        self._registry = registry

    def resolve(
        self,
        config: ProjectConfig,
        language_pack: LanguagePack,
        cli: CliOverrides | None = None,
    ) -> ResolvedProfile:
        """Resolve."""
        cli = cli or CliOverrides()
        preset = self._resolve_preset(cli.profile_name or config.profile.name)
        self._validate_rule_id_references(config, cli, preset, language_pack)
        explicit_rule_ids = self._explicit_rule_ids(config, cli)

        active_rule_ids = self._resolve_active_rules(config, preset, cli)
        resolved_rules: dict[str, ResolvedRuleSettings] = {}
        for rule_id in active_rule_ids:
            registration = self._registry.get(rule_id)
            if (
                registration.metadata.profiles_active
                and preset.name not in registration.metadata.profiles_active
                and rule_id not in explicit_rule_ids
            ):
                continue
            if not self._language_pack_supports_rule(language_pack, rule_id):
                raise ValueError(
                    f"Rule '{rule_id}' is not supported by language pack "
                    f"'{language_pack.code}'"
                )
            if language_pack.code not in registration.metadata.supported_languages:
                raise ValueError(
                    f"Rule '{rule_id}' does not support language '{language_pack.code}'"
                )
            if registration.metadata.experimental and not self._experimental_enabled(
                config, cli
            ):
                continue
            merged = self._merge_rule_settings(
                rule_id,
                preset,
                config.rules.overrides.get(rule_id),
                language_pack,
            )
            merged_options = _merge_options(
                registration.metadata.default_options,
                merged.options,
            )
            options = _validate_options_model(
                rule_id, registration.rule_cls, merged_options
            )
            resolved_rules[rule_id] = ResolvedRuleSettings(
                metadata=registration.metadata,
                enabled=merged.enabled if merged.enabled is not None else True,
                severity=merged.severity or registration.metadata.default_severity,
                weight=(
                    merged.weight
                    if merged.weight is not None
                    else registration.metadata.default_weight
                ),
                options=options,
                extra_patterns=merged.extra_patterns,
                silenced_patterns=merged.silenced_patterns,
            )

        profile = config.profile
        return ResolvedProfile(
            profile_name=preset.name,
            audience=profile.audience or preset.audience,
            genre=profile.genre or preset.genre,
            section=profile.section or preset.section,
            register=profile.register or preset.register,
            language=language_pack.code,
            strict_validation=config.runtime.strict_validation,
            enable_experimental=self._experimental_enabled(config, cli),
            rules=resolved_rules,
        )

    def _resolve_preset(self, profile_name: str) -> ProfilePreset:
        """Resolve preset."""
        try:
            return PROFILE_PRESETS[profile_name]
        except KeyError as exc:
            raise ValueError(
                "Unknown profile "
                f"'{profile_name}'. Expected one of: "
                f"{COMMA_SEPARATOR.join(sorted(PROFILE_PRESETS))}"
            ) from exc

    def _resolve_active_rules(
        self,
        config: ProjectConfig,
        preset: ProfilePreset,
        cli: CliOverrides,
    ) -> tuple[str, ...]:
        """Resolve active rules."""
        if cli.rule_ids:
            active = set(cli.rule_ids)
        elif config.rules.active is not None:
            active = set(config.rules.active)
        else:
            active = set(preset.active_rules)
        active -= set(config.rules.disabled)
        active -= set(cli.disabled_rule_ids)
        return tuple(sorted(active))

    def _merge_rule_settings(
        self,
        rule_id: str,
        preset: ProfilePreset,
        user_override: RuleOverrideConfig | None,
        language_pack: LanguagePack,
    ) -> RuleOverrideConfig:
        """Merge rule settings."""
        merged = RuleOverrideConfig()
        merged = _merge_override(
            merged,
            _mapping_to_override(
                rule_id=rule_id,
                raw=language_pack.rule_defaults.get(rule_id, {}),
                source="language pack defaults",
            ),
        )
        merged = _merge_override(
            merged,
            _mapping_to_override(
                rule_id=rule_id,
                raw=preset.rule_overrides.get(rule_id, {}),
                source=f"profile preset '{preset.name}'",
            ),
        )
        if user_override is not None:
            merged = _merge_override(merged, user_override)
        return merged

    def _experimental_enabled(self, config: ProjectConfig, cli: CliOverrides) -> bool:
        """Experimental enabled."""
        if cli.enable_experimental is not None:
            return cli.enable_experimental
        return config.runtime.experimental_rules

    def _validate_rule_id_references(
        self,
        config: ProjectConfig,
        cli: CliOverrides,
        preset: ProfilePreset,
        language_pack: LanguagePack,
    ) -> None:
        """Validate rule id references."""
        self._raise_unknown_rule_ids("rules.active", config.rules.active or ())
        self._raise_unknown_rule_ids("rules.disabled", config.rules.disabled)
        self._raise_unknown_rule_ids("rules.overrides", config.rules.overrides)
        self._raise_unknown_rule_ids("cli --rule", cli.rule_ids)
        self._raise_unknown_rule_ids("cli --disable-rule", cli.disabled_rule_ids)
        self._raise_unknown_rule_ids(
            f"profile preset '{preset.name}' active_rules",
            preset.active_rules,
        )
        self._raise_unknown_rule_ids(
            f"profile preset '{preset.name}' rule_overrides",
            preset.rule_overrides,
        )
        self._raise_unknown_rule_ids(
            f"language pack '{language_pack.code}' rule_defaults",
            language_pack.rule_defaults,
        )
        self._raise_unknown_rule_ids(
            f"language pack '{language_pack.code}' supported_rules",
            language_pack.supported_rules,
        )
        supported = language_pack.supported_rules
        if supported:
            defaults_outside_support = sorted(
                rule_id
                for rule_id in language_pack.rule_defaults
                if rule_id not in supported
            )
            if defaults_outside_support:
                raise ValueError(
                    f"language pack '{language_pack.code}' rule_defaults declare unsupported "
                    "rule ids: " + ", ".join(defaults_outside_support)
                )

    def _raise_unknown_rule_ids(self, source: str, rule_ids: Iterable[str]) -> None:
        """Raise unknown rule ids."""
        unknown = sorted(
            rule_id for rule_id in rule_ids if rule_id not in self._registry
        )
        if unknown:
            raise ValueError(
                f"Unknown rule ids in {source}: {COMMA_SEPARATOR.join(unknown)}"
            )

    def _language_pack_supports_rule(
        self, language_pack: LanguagePack, rule_id: str
    ) -> bool:
        """Language pack supports rule."""
        supported_rules = language_pack.supported_rules
        if not supported_rules:
            return True
        return rule_id in supported_rules

    def _explicit_rule_ids(
        self,
        config: ProjectConfig,
        cli: CliOverrides,
    ) -> frozenset[str]:
        """Explicit rule ids."""
        explicit: set[str] = set()
        explicit.update(cli.rule_ids)
        if config.rules.active is not None:
            explicit.update(config.rules.active)
        return frozenset(explicit)


def _merge_override(
    base: RuleOverrideConfig, incoming: RuleOverrideConfig
) -> RuleOverrideConfig:
    """Merge override."""
    return RuleOverrideConfig(
        enabled=incoming.enabled if incoming.enabled is not None else base.enabled,
        severity=incoming.severity or base.severity,
        weight=incoming.weight if incoming.weight is not None else base.weight,
        options=_merge_options(base.options, incoming.options),
        extra_patterns=base.extra_patterns + incoming.extra_patterns,
        silenced_patterns=base.silenced_patterns + incoming.silenced_patterns,
    )


def _merge_options(*mappings: object) -> dict[str, object]:
    """Merge options."""
    merged: dict[str, object] = {}
    for mapping in mappings:
        if isinstance(mapping, Mapping):
            merged = _deep_merge_mapping(merged, mapping)
    return merged


def _deep_merge_mapping(
    base: Mapping[str, object],
    incoming: Mapping[str, object],
) -> dict[str, object]:
    """Deep merge mapping."""
    merged: dict[str, object] = {
        key: _clone_option_value(value) for key, value in base.items()
    }
    for key, value in incoming.items():
        current = merged.get(key)
        merged[key] = _merge_option_values(current, value)
    return merged


def _merge_option_values(current: object, incoming: object) -> object:
    """Merge option values."""
    if isinstance(current, Mapping) and isinstance(incoming, Mapping):
        return _deep_merge_mapping(current, incoming)
    return _clone_option_value(incoming)


def _clone_option_value(value: object) -> object:
    """Clone option value."""
    if isinstance(value, Mapping):
        return {key: _clone_option_value(item) for key, item in value.items()}
    if isinstance(value, list):
        return [_clone_option_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(_clone_option_value(item) for item in value)
    return value


def _mapping_to_override(
    rule_id: str,
    raw: object,
    source: str,
) -> RuleOverrideConfig:
    """Mapping to override."""
    if not raw:
        return RuleOverrideConfig()
    if not isinstance(raw, Mapping):
        raise ValueError(f"{source} override for rule '{rule_id}' must be a mapping")
    allowed_fields = frozenset(
        {
            "enabled",
            "severity",
            "weight",
            "options",
            "extra_patterns",
            "silenced_patterns",
        }
    )
    unknown = sorted(key for key in raw if key not in allowed_fields)
    if unknown:
        raise ValueError(
            f"{source} override for rule '{rule_id}' has unknown fields: "
            f"{COMMA_SEPARATOR.join(unknown)}"
        )
    enabled = raw.get("enabled")
    if enabled is not None and not isinstance(enabled, bool):
        raise ValueError(
            f"{source} override for rule '{rule_id}' field 'enabled' must be a boolean"
        )
    severity = raw.get("severity")
    options_raw = raw.get("options", {})
    if options_raw is None:
        options_raw = {}
    if not isinstance(options_raw, Mapping):
        raise ValueError(
            f"{source} override for rule '{rule_id}' field 'options' must be a mapping"
        )
    options = {}
    for key, value in options_raw.items():
        if not isinstance(key, str):
            raise ValueError(
                f"{source} override for rule '{rule_id}' field 'options' keys must be strings"
            )
        options[key] = value
    weight_raw = raw.get("weight")
    if weight_raw is not None and (
        isinstance(weight_raw, bool) or not isinstance(weight_raw, (int, float))
    ):
        raise ValueError(
            f"{source} override for rule '{rule_id}' field 'weight' must be numeric"
        )
    weight = float(weight_raw) if weight_raw is not None else None
    extra_patterns = _string_tuple(
        raw.get("extra_patterns", ()),
        f"{source} override for rule '{rule_id}' field 'extra_patterns'",
    )
    silenced_patterns = _string_tuple(
        raw.get("silenced_patterns", ()),
        f"{source} override for rule '{rule_id}' field 'silenced_patterns'",
    )
    return RuleOverrideConfig(
        enabled=enabled,
        severity=Severity(severity) if severity is not None else None,
        weight=weight,
        options=options,
        extra_patterns=extra_patterns,
        silenced_patterns=silenced_patterns,
    )


def _string_tuple(raw: object, field_label: str) -> tuple[str, ...]:
    """String tuple."""
    if raw is None:
        return ()
    if not isinstance(raw, (list, tuple)):
        raise ValueError(f"{field_label} must be a sequence of strings")
    if not all(isinstance(item, str) for item in raw):
        raise ValueError(f"{field_label} must be a sequence of strings")
    return tuple(raw)


def _validate_options_model(
    rule_id: str,
    rule_cls: type[object],
    options: dict[str, object],
) -> dict[str, object]:
    """Validate options model."""
    options_model = getattr(rule_cls, "options_model", None)
    if options_model is None:
        return options
    validator = getattr(options_model, "model_validate", None)
    if not callable(validator):
        raise ValueError(
            f"Rule '{rule_id}' declares options_model without model_validate(...)"
        )
    try:
        model = validator(options)
    except Exception as exc:
        raise ValueError(f"Invalid options for rule '{rule_id}': {exc}") from exc
    dumper = getattr(model, "model_dump", None)
    if not callable(dumper):
        raise ValueError(
            f"Rule '{rule_id}' options_model must return a model with model_dump(...)"
        )
    dumped = dumper()
    if not isinstance(dumped, dict):
        raise ValueError(
            f"Rule '{rule_id}' options_model.model_dump() must return dict"
        )
    return dumped
