from __future__ import annotations

import pytest

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import ConfigError, parse_project_config


def test_parse_project_config_rejects_unknown_fields() -> None:
    with pytest.raises(ConfigError, match="Unknown field 'unexpected' in root"):
        parse_project_config({"unexpected": {}})


def test_profile_resolution_applies_merge_precedence(registry, language_pack) -> None:
    config = parse_project_config(
        {
            "profile": {"name": "research"},
            "rules": {
                "overrides": {
                    "surface.sentence_length": {
                        "max_words": 18,
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


def test_profile_resolution_rejects_unknown_active_rule(registry, language_pack) -> None:
    config = parse_project_config(
        {"rules": {"active": ["surface.sentence_length", "unknown.rule"]}}
    )
    with pytest.raises(ValueError, match="Unknown rule ids: unknown.rule"):
        ProfileResolver(registry).resolve(config, language_pack)
