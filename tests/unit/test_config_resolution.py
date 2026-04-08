from __future__ import annotations

from dataclasses import replace

import pytest
from pydantic import BaseModel, Field

from hermeneia.config.defaults import PROFILE_PRESETS, ProfilePreset
from hermeneia.config.profile import CliOverrides, ProfileResolver
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


class _NestedOptionsRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="test.deep_merge",
        label="Deep merge test rule",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "limits": {"soft": 1, "hard": 3},
            "phrases": {"allow": ["default"], "deny": ["default-deny"]},
            "mode": "default",
        },
    )

    def check_source(self, lines, doc, ctx):  # noqa: ARG002
        return []


def test_parse_project_config_rejects_unknown_fields() -> None:
    with pytest.raises(ConfigError, match="Unknown field 'unexpected' in root"):
        parse_project_config({"unexpected": {}})


def test_parse_project_config_rejects_non_boolean_runtime_flag() -> None:
    with pytest.raises(ConfigError, match="runtime.strict_validation"):
        parse_project_config({"runtime": {"strict_validation": 1}})


def test_parse_project_config_rejects_non_boolean_runtime_debug_flag() -> None:
    with pytest.raises(ConfigError, match="runtime.debug"):
        parse_project_config({"runtime": {"debug": "yes"}})


def test_parse_project_config_rejects_unknown_embedding_backend() -> None:
    with pytest.raises(
        ConfigError,
        match="runtime.embeddings.backend",
    ):
        parse_project_config({"runtime": {"embeddings": {"backend": "bogus"}}})


def test_parse_project_config_accepts_sentence_transformers_embedding_backend() -> None:
    config = parse_project_config(
        {
            "runtime": {
                "embeddings": {
                    "backend": "sentence_transformers",
                    "model": "sentence-transformers/all-MiniLM-L6-v2",
                }
            }
        }
    )
    assert config.runtime.embeddings.backend == "sentence_transformers"
    assert config.runtime.embeddings.model == "sentence-transformers/all-MiniLM-L6-v2"


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
    with pytest.raises(
        ValueError, match="Unknown rule ids in rules.active: unknown.rule"
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_legacy_literary_parallelism_rule_id(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {"rules": {"active": ["paragraph.literary_parallelism"]}}
    )
    with pytest.raises(
        ValueError,
        match=(
            "Unknown rule ids in rules.active: paragraph.literary_parallelism"
        ),
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_unknown_override_rule(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {"rules": {"overrides": {"unknown.rule": {"options": {"max_words": 12}}}}}
    )
    with pytest.raises(
        ValueError, match="Unknown rule ids in rules.overrides: unknown.rule"
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_unknown_disabled_rule(
    registry, language_pack
) -> None:
    config = parse_project_config({"rules": {"disabled": ["unknown.rule"]}})
    with pytest.raises(
        ValueError, match="Unknown rule ids in rules.disabled: unknown.rule"
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_unknown_cli_rule_id(
    registry, language_pack
) -> None:
    config = parse_project_config({})
    with pytest.raises(
        ValueError, match="Unknown rule ids in cli --rule: unknown.rule"
    ):
        ProfileResolver(registry).resolve(
            config, language_pack, cli=CliOverrides(rule_ids=("unknown.rule",))
        )


def test_profile_resolution_rejects_unknown_cli_disabled_rule_id(
    registry, language_pack
) -> None:
    config = parse_project_config({})
    with pytest.raises(
        ValueError,
        match="Unknown rule ids in cli --disable-rule: unknown.rule",
    ):
        ProfileResolver(registry).resolve(
            config,
            language_pack,
            cli=CliOverrides(disabled_rule_ids=("unknown.rule",)),
        )


def test_profile_resolution_rejects_unknown_rule_in_profile_active_rules(
    registry, language_pack, monkeypatch
) -> None:
    bad_preset = ProfilePreset(
        name="bad-active",
        audience="specialist",
        genre="research_note",
        section="body",
        register="formal",
        active_rules=("unknown.rule",),
        rule_overrides={},
    )
    monkeypatch.setitem(PROFILE_PRESETS, "bad-active", bad_preset)
    config = parse_project_config({"profile": {"name": "bad-active"}})
    with pytest.raises(
        ValueError,
        match="Unknown rule ids in profile preset 'bad-active' active_rules: unknown.rule",
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_unknown_rule_in_profile_overrides(
    registry, language_pack, monkeypatch
) -> None:
    bad_preset = ProfilePreset(
        name="bad-overrides",
        audience="specialist",
        genre="research_note",
        section="body",
        register="formal",
        active_rules=("surface.sentence_length",),
        rule_overrides={"unknown.rule": {"options": {"max_words": 20}}},
    )
    monkeypatch.setitem(PROFILE_PRESETS, "bad-overrides", bad_preset)
    config = parse_project_config({"profile": {"name": "bad-overrides"}})
    with pytest.raises(
        ValueError,
        match="Unknown rule ids in profile preset 'bad-overrides' rule_overrides: unknown.rule",
    ):
        ProfileResolver(registry).resolve(config, language_pack)


def test_profile_resolution_rejects_unknown_rule_in_language_defaults(
    registry, language_pack
) -> None:
    bad_pack = replace(
        language_pack,
        rule_defaults={"unknown.rule": {"options": {"max_words": 18}}},
    )
    config = parse_project_config({})
    with pytest.raises(
        ValueError,
        match="Unknown rule ids in language pack 'en' rule_defaults: unknown.rule",
    ):
        ProfileResolver(registry).resolve(config, bad_pack)


def test_profile_resolution_rejects_unknown_rule_in_language_supported_rules(
    registry, language_pack
) -> None:
    bad_pack = replace(
        language_pack,
        supported_rules=frozenset({"unknown.rule"}),
    )
    config = parse_project_config({})
    with pytest.raises(
        ValueError,
        match="Unknown rule ids in language pack 'en' supported_rules: unknown.rule",
    ):
        ProfileResolver(registry).resolve(config, bad_pack)


def test_profile_resolution_rejects_rule_not_supported_by_language_pack(
    registry, language_pack
) -> None:
    restricted_pack = replace(
        language_pack,
        supported_rules=frozenset({"surface.sentence_length"}),
        rule_defaults={},
    )
    config = parse_project_config(
        {"rules": {"active": ["surface.passive_voice"]}}
    )
    with pytest.raises(
        ValueError,
        match="Rule 'surface.passive_voice' is not supported by language pack 'en'",
    ):
        ProfileResolver(registry).resolve(config, restricted_pack)


def test_profile_resolution_allows_rule_when_language_pack_supports_it(
    registry, language_pack
) -> None:
    restricted_pack = replace(
        language_pack,
        supported_rules=frozenset({"surface.sentence_length"}),
        rule_defaults={},
    )
    config = parse_project_config(
        {"rules": {"active": ["surface.sentence_length"]}}
    )
    profile = ProfileResolver(registry).resolve(config, restricted_pack)
    assert "surface.sentence_length" in profile.rules


def test_profile_resolution_rejects_language_default_for_unsupported_rule(
    registry, language_pack
) -> None:
    restricted_pack = replace(
        language_pack,
        supported_rules=frozenset({"surface.sentence_length"}),
        rule_defaults={
            "surface.sentence_length": {"options": {"max_words": 18}},
            "surface.passive_voice": {"options": {}},
        },
    )
    config = parse_project_config(
        {"rules": {"active": ["surface.sentence_length"]}}
    )
    with pytest.raises(
        ValueError,
        match="language pack 'en' rule_defaults declare unsupported rule ids: surface.passive_voice",
    ):
        ProfileResolver(registry).resolve(config, restricted_pack)


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


def test_profile_resolution_deep_merges_nested_options_mappings(
    registry, language_pack, monkeypatch
) -> None:
    registry.add(_NestedOptionsRule)
    deep_preset = ProfilePreset(
        name="deep-merge-test",
        audience="specialist",
        genre="research_note",
        section="body",
        register="formal",
        active_rules=("test.deep_merge",),
        rule_overrides={
            "test.deep_merge": {
                "options": {
                    "limits": {"hard": 4},
                    "phrases": {"deny": ["profile-deny"]},
                }
            }
        },
    )
    monkeypatch.setitem(PROFILE_PRESETS, "deep-merge-test", deep_preset)
    merged_pack = replace(
        language_pack,
        rule_defaults={
            **language_pack.rule_defaults,
            "test.deep_merge": {
                "options": {
                    "limits": {"soft": 2},
                    "phrases": {"allow": ["language-allow"]},
                    "lexicon": {"extra": ["l1"]},
                }
            },
        },
    )
    config = parse_project_config(
        {
            "profile": {"name": "deep-merge-test"},
            "rules": {
                "overrides": {
                    "test.deep_merge": {
                        "options": {
                            "limits": {"hard": 10, "user": 9},
                            "phrases": {"allow": ["user-allow"]},
                            "lexicon": {"extra": ["u1", "u2"]},
                            "mode": "user",
                        }
                    }
                }
            },
        }
    )
    profile = ProfileResolver(registry).resolve(config, merged_pack)
    options = profile.rules["test.deep_merge"].options
    assert options["limits"] == {"soft": 2, "hard": 10, "user": 9}
    assert options["phrases"] == {
        "allow": ["user-allow"],
        "deny": ["profile-deny"],
    }
    assert options["lexicon"] == {"extra": ["u1", "u2"]}
    assert options["mode"] == "user"
