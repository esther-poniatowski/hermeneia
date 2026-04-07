"""Resolved profile construction with strict merge semantics."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from hermeneia.config.defaults import PROFILE_PRESETS, ProfilePreset
from hermeneia.config.schema import ProjectConfig, RuleOverrideConfig
from hermeneia.engine.registry import RuleRegistry
from hermeneia.language.base import LanguagePack
from hermeneia.rules.base import ResolvedProfile, ResolvedRuleSettings, Severity


@dataclass(frozen=True)
class CliOverrides:
    profile_name: str | None = None
    rule_ids: tuple[str, ...] = ()
    disabled_rule_ids: tuple[str, ...] = ()
    reporting_format: str | None = None
    enable_experimental: bool | None = None


class ProfileResolver:
    """Merge rule defaults, language defaults, profile defaults, and overrides."""

    def __init__(self, registry: RuleRegistry) -> None:
        self._registry = registry

    def resolve(
        self,
        config: ProjectConfig,
        language_pack: LanguagePack,
        cli: CliOverrides | None = None,
    ) -> ResolvedProfile:
        cli = cli or CliOverrides()
        preset = self._resolve_preset(cli.profile_name or config.profile.name)
        self._validate_override_rule_ids(config.rules.overrides)
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
            if language_pack.code not in registration.metadata.supported_languages:
                raise ValueError(f"Rule '{rule_id}' does not support language '{language_pack.code}'")
            if registration.metadata.experimental and not self._experimental_enabled(config, cli):
                continue
            merged = self._merge_rule_settings(
                rule_id,
                preset,
                config.rules.overrides.get(rule_id),
                language_pack,
            )
            merged_options = _merge_options(
                registration.metadata.default_options,
                language_pack.rule_defaults.get(rule_id, {}),
                preset.rule_overrides.get(rule_id, {}),
                merged.options,
            )
            options = _validate_options_model(rule_id, registration.rule_cls, merged_options)
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
        try:
            return PROFILE_PRESETS[profile_name]
        except KeyError as exc:
            raise ValueError(f"Unknown profile '{profile_name}'. Expected one of: {', '.join(sorted(PROFILE_PRESETS))}") from exc

    def _resolve_active_rules(
        self,
        config: ProjectConfig,
        preset: ProfilePreset,
        cli: CliOverrides,
    ) -> tuple[str, ...]:
        if cli.rule_ids:
            active = set(cli.rule_ids)
        elif config.rules.active is not None:
            active = set(config.rules.active)
        else:
            active = set(preset.active_rules)
        active -= set(config.rules.disabled)
        active -= set(cli.disabled_rule_ids)
        unknown = sorted(rule_id for rule_id in active if rule_id not in self._registry)
        if unknown:
            raise ValueError(f"Unknown rule ids: {', '.join(unknown)}")
        return tuple(sorted(active))

    def _merge_rule_settings(
        self,
        rule_id: str,
        preset: ProfilePreset,
        user_override: RuleOverrideConfig | None,
        language_pack: LanguagePack,
    ) -> RuleOverrideConfig:
        merged = RuleOverrideConfig()
        merged = _merge_override(merged, _mapping_to_override(language_pack.rule_defaults.get(rule_id, {})))
        merged = _merge_override(merged, _mapping_to_override(preset.rule_overrides.get(rule_id, {})))
        if user_override is not None:
            merged = _merge_override(merged, user_override)
        return merged

    def _experimental_enabled(self, config: ProjectConfig, cli: CliOverrides) -> bool:
        if cli.enable_experimental is not None:
            return cli.enable_experimental
        return config.runtime.experimental_rules

    def _validate_override_rule_ids(
        self, overrides: Mapping[str, RuleOverrideConfig]
    ) -> None:
        unknown = sorted(rule_id for rule_id in overrides if rule_id not in self._registry)
        if unknown:
            raise ValueError(f"Unknown rule ids in overrides: {', '.join(unknown)}")

    def _explicit_rule_ids(
        self,
        config: ProjectConfig,
        cli: CliOverrides,
    ) -> frozenset[str]:
        explicit: set[str] = set()
        explicit.update(cli.rule_ids)
        if config.rules.active is not None:
            explicit.update(config.rules.active)
        return frozenset(explicit)


def _merge_override(base: RuleOverrideConfig, incoming: RuleOverrideConfig) -> RuleOverrideConfig:
    return RuleOverrideConfig(
        enabled=incoming.enabled if incoming.enabled is not None else base.enabled,
        severity=incoming.severity or base.severity,
        weight=incoming.weight if incoming.weight is not None else base.weight,
        options=_merge_options(base.options, incoming.options),
        extra_patterns=base.extra_patterns + incoming.extra_patterns,
        silenced_patterns=base.silenced_patterns + incoming.silenced_patterns,
    )


def _merge_options(*mappings: object) -> dict[str, object]:
    merged: dict[str, object] = {}
    for mapping in mappings:
        if isinstance(mapping, Mapping):
            merged.update(mapping)
    return merged


def _mapping_to_override(raw: object) -> RuleOverrideConfig:
    if not raw:
        return RuleOverrideConfig()
    if not isinstance(raw, Mapping):
        raise ValueError("Internal rule defaults must be mappings")
    severity = raw.get("severity")
    options = {
        key: value
        for key, value in raw.items()
        if key
        not in {
            "enabled",
            "severity",
            "weight",
            "extra_patterns",
            "silenced_patterns",
            "profiles_active",
            "abstain_when_flags",
            "evidence_fields",
            "suggestion_mode",
        }
    }
    return RuleOverrideConfig(
        enabled=raw.get("enabled"),
        severity=Severity(severity) if severity is not None else None,
        weight=float(raw["weight"]) if "weight" in raw else None,
        options=options,
        extra_patterns=tuple(raw.get("extra_patterns", ())),
        silenced_patterns=tuple(raw.get("silenced_patterns", ())),
    )


def _validate_options_model(
    rule_id: str,
    rule_cls: type[object],
    options: dict[str, object],
) -> dict[str, object]:
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
        return options
    dumped = dumper()
    if not isinstance(dumped, dict):
        raise ValueError(f"Rule '{rule_id}' options_model.model_dump() must return dict")
    return dumped
