from __future__ import annotations

from pathlib import Path

from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext


def _parse(language_pack, source: str):
    return MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )


def test_nominalization_rule_emits_on_weak_support_verb(
    registry, language_pack, research_profile
) -> None:
    source = "The construction is a stable mechanism for approximation.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.nominalization"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    violation = violations[0]
    assert violation.rule_id == "surface.nominalization"
    assert violation.evidence is not None
    assert violation.evidence.features["signal_type"] == "weak_support_verb"


def test_nominalization_rule_emits_on_abstract_noun_phrase(
    registry, language_pack, research_profile
) -> None:
    source = "The composition of f with g yields a contraction.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.nominalization"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    violation = violations[0]
    assert violation.rule_id == "surface.nominalization"
    assert violation.evidence is not None
    assert violation.evidence.features["signal_type"] == "abstract_noun_phrase"
