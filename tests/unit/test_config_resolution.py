from __future__ import annotations

from dataclasses import replace

import pytest
from pydantic import BaseModel, Field

from hermeneia.config.defaults import PROFILE_PRESETS, ProfilePreset
from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import ConfigError, parse_project_config
from hermeneia.rules.base import (
    Layer,
    RuleKind,
    RuleMetadata,
    Severity,
    SourcePatternRule,
    Tractability,
)


class _OptionsModel(BaseModel):
    max_words: int = Field(ge=1)


class _OptionsValidatedRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="test.options_model",
        label="Options model test rule",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"max_words": 5},
    )
    options_model = _OptionsModel

    def check_source(self, lines, doc, ctx):  # noqa: ARG002
        return []


class _NoDumpOptionsModel:
    @classmethod
    def model_validate(cls, options):  # noqa: ANN001
        _ = options
        return object()


class _OptionsNoDumpRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="test.options_nodump",
        label="Options no-dump rule",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={},
    )
    options_model = _NoDumpOptionsModel

    def check_source(self, lines, doc, ctx):  # noqa: ARG002
        return []


def test_parse_project_config_rejects_unknown_fields() -> None:
    with pytest.raises(ConfigError, match="Unknown field 'unexpected' in root"):
        parse_project_config({"unexpected": {}})


def test_parse_project_config_rejects_non_boolean_runtime_flag() -> None:
    with pytest.raises(ConfigError, match="runtime.strict_validation"):
        parse_project_config({"runtime": {"strict_validation": 1}})


def test_parse_project_config_rejects_non_numeric_override_weight() -> None:
    with pytest.raises(
        ConfigError, match="rules.overrides.surface.sentence_length.weight"
    ):
        parse_project_config(
            {
                "rules": {
                    "overrides": {
                        "surface.sentence_length": {
                            "weight": "heavy",
                        }
                    }
                }
            }
        )


def test_parse_project_config_rejects_unknown_override_field() -> None:
    with pytest.raises(
        ConfigError,
        match="Unknown field 'unexpected' in rules.overrides.surface.sentence_length",
    ):
        parse_project_config(
            {
                "rules": {
                    "overrides": {
                        "surface.sentence_length": {
                            "unexpected": 1,
                        }
                    }
                }
            }
        )


def test_parse_project_config_rejects_legacy_top_level_override_option_key() -> None:
    with pytest.raises(
        ConfigError,
        match="Unknown field 'max_words' in rules.overrides.surface.sentence_length",
    ):
        parse_project_config(
            {
                "rules": {
                    "overrides": {
                        "surface.sentence_length": {
                            "max_words": 18,
                        }
                    }
                }
            }
        )


def test_parse_project_config_preserves_profile_register_alias() -> None:
    config = parse_project_config({"profile": {"register": "pedagogical"}})
    assert config.profile.register == "pedagogical"


def test_profile_resolution_applies_merge_precedence(registry, language_pack) -> None:
    config = parse_project_config(
        {
            "profile": {"name": "research"},
            "rules": {
                "overrides": {
                    "surface.sentence_length": {
                        "options": {"max_words": 18},
                        "severity": "info",
                    }
                }
            },
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    settings = profile.rules["surface.sentence_length"]
    assert settings.options["max_words"] == 18
    assert settings.severity.value == "info"


def test_profile_resolution_rejects_unknown_active_rule(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {"rules": {"active": ["surface.sentence_length", "unknown.rule"]}}
    )
    with pytest.raises(ValueError, match="Unknown rule ids: unknown.rule"):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_unknown_override_rule(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {"rules": {"overrides": {"unknown.rule": {"options": {"max_words": 12}}}}}
    )
    with pytest.raises(ValueError, match="Unknown rule ids in overrides: unknown.rule"):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_accepts_options_mapping_override(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {
            "rules": {
                "overrides": {
                    "surface.sentence_length": {
                        "options": {"max_words": 17},
                        "severity": "info",
                    }
                }
            }
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    settings = profile.rules["surface.sentence_length"]
    assert settings.options["max_words"] == 17
    assert settings.severity.value == "info"


def test_profile_resolution_validates_rule_options_model(
    registry, language_pack
) -> None:
    registry.add(_OptionsValidatedRule)
    config = parse_project_config(
        {
            "rules": {
                "active": ["test.options_model"],
                "overrides": {"test.options_model": {"options": {"max_words": 0}}},
            }
        }
    )
    with pytest.raises(
        ValueError, match="Invalid options for rule 'test.options_model'"
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_options_model_without_model_dump(
    registry, language_pack
) -> None:
    registry.add(_OptionsNoDumpRule)
    config = parse_project_config({"rules": {"active": ["test.options_nodump"]}})
    with pytest.raises(
        ValueError,
        match="Rule 'test.options_nodump' options_model must return a model with model_dump",
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_legacy_language_default_shape(
    registry, language_pack
) -> None:
    bad_pack = replace(
        language_pack,
        rule_defaults={"surface.sentence_length": {"max_words": 18}},
    )
    config = parse_project_config({"rules": {"active": ["surface.sentence_length"]}})
    with pytest.raises(
        ValueError,
        match="language pack defaults override for rule 'surface.sentence_length' has unknown fields: max_words",
    ):
        ProfileResolver(registry).resolve(config, bad_pack)


def test_profile_resolution_rejects_legacy_profile_default_shape(
    registry, language_pack, monkeypatch
) -> None:
    bad_preset = ProfilePreset(
        name="legacy-preset",
        audience="specialist",
        genre="research_note",
        section="body",
        register="formal",
        active_rules=("surface.sentence_length",),
        rule_overrides={"surface.sentence_length": {"max_words": 20}},
    )
    monkeypatch.setitem(PROFILE_PRESETS, "legacy-preset", bad_preset)
    config = parse_project_config({"profile": {"name": "legacy-preset"}})
    with pytest.raises(
        ValueError,
        match="profile preset 'legacy-preset' override for rule 'surface.sentence_length' has unknown fields: max_words",
    ):
        ProfileResolver(registry).resolve(config, language_pack)
