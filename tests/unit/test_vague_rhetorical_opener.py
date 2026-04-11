from __future__ import annotations

from pathlib import Path

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext


def _parse(language_pack, source: str):
    return MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )


def _rule_from_profile(registry, language_pack, config_payload: dict[str, object]):
    config = parse_project_config(config_payload)
    profile = ProfileResolver(registry).resolve(config, language_pack)
    settings = profile.rules["paragraph.vague_rhetorical_opener"]
    rule = registry.instantiate(settings)
    return profile, rule


def test_vague_rhetorical_opener_emits_for_default_phrase(registry, language_pack) -> None:
    profile, rule = _rule_from_profile(
        registry,
        language_pack,
        {
            "runtime": {"experimental_rules": True},
            "rules": {"active": ["paragraph.vague_rhetorical_opener"]},
        },
    )
    document = _parse(language_pack, "In this context, the sequence converges.\n")
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.vague_rhetorical_opener"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features.get("opener") == "in this context"


def test_vague_rhetorical_opener_honors_silenced_patterns(registry, language_pack) -> None:
    profile, rule = _rule_from_profile(
        registry,
        language_pack,
        {
            "runtime": {"experimental_rules": True},
            "rules": {
                "active": ["paragraph.vague_rhetorical_opener"],
                "overrides": {
                    "paragraph.vague_rhetorical_opener": {"silenced_patterns": ["in this context"]}
                },
            },
        },
    )
    document = _parse(language_pack, "In this context, the sequence converges.\n")
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    assert rule.check(document, context) == []


def test_vague_rhetorical_opener_supports_extra_patterns(registry, language_pack) -> None:
    profile, rule = _rule_from_profile(
        registry,
        language_pack,
        {
            "runtime": {"experimental_rules": True},
            "rules": {
                "active": ["paragraph.vague_rhetorical_opener"],
                "overrides": {
                    "paragraph.vague_rhetorical_opener": {"extra_patterns": ["for clarity"]}
                },
            },
        },
    )
    document = _parse(language_pack, "For clarity, we show the estimate.\n")
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].evidence is not None
    assert violations[0].evidence.features.get("opener") == "for clarity"
