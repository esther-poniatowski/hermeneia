from __future__ import annotations

from pathlib import Path

from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext


def test_definition_before_use_emits_for_undefined_first_symbol(
    registry, language_pack, research_profile
) -> None:
    source = "Then $x$ is bounded by the hypothesis.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["audience.definition_before_use"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    violation = violations[0]
    assert violation.rule_id == "audience.definition_before_use"
    assert violation.evidence is not None
    assert violation.evidence.features["symbols"] == ("x",)


def test_definition_before_use_skips_symbol_with_local_definition_marker(
    registry, language_pack, research_profile
) -> None:
    source = "Let $x$ denote the control variable.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["audience.definition_before_use"])
    assert rule.check(document, context) == []


def test_definition_before_use_only_checks_first_use(
    registry, language_pack, research_profile
) -> None:
    source = "Let $x$ denote the control variable. Then $x$ is bounded.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["audience.definition_before_use"])
    assert rule.check(document, context) == []


def test_definition_before_use_accepts_symbol_defined_by_colon_frame(
    registry, language_pack, research_profile
) -> None:
    source = "The control variable is: $x$.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["audience.definition_before_use"])
    assert rule.check(document, context) == []


def test_definition_before_use_accepts_symbol_defined_by_measurement_frame(
    registry, language_pack, research_profile
) -> None:
    source = "The instability index is measured by $I$.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["audience.definition_before_use"])
    assert rule.check(document, context) == []
