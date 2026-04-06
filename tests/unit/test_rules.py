from __future__ import annotations

from pathlib import Path

from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import Token
from hermeneia.document.parser import ParseRequest
from hermeneia.engine.detector import RuleDetector
from hermeneia.rules.base import RuleContext


def test_contraction_rule_triggers_through_detector(
    registry, language_pack, research_profile
) -> None:
    source = "It's fine.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    document = (
        SpaCyDocumentAnnotator(language_pack.parser_model)
        .annotate(document, research_profile)
        .document
    )
    detector = RuleDetector(registry)
    features = FeatureStore(document, document.indexes)
    violations = detector.detect(document, research_profile, language_pack, features)
    assert any(violation.rule_id == "surface.contraction" for violation in violations)


def test_subject_verb_distance_rule_abstains_without_dependencies(
    registry, language_pack, research_profile
) -> None:
    source = "The central claim, after several subordinate details, remains uncertain.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    sentence = document.indexes.sentences[0]
    actual_sentence = document.sentence_by_id(sentence.id)
    assert actual_sentence is not None
    actual_sentence.tokens = [
        Token("The", "the", None, None, None, actual_sentence.span, 0, 3),
        Token("central", "central", None, None, None, actual_sentence.span, 4, 11),
        Token("claim", "claim", None, None, None, actual_sentence.span, 12, 17),
    ]
    rule = registry.instantiate(research_profile.rules["discourse.subject_verb_distance"])
    ctx = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    assert rule.check(document, ctx) == []


def test_claim_calibration_rule_emits_without_support(
    registry, language_pack, research_profile
) -> None:
    source = "This clearly proves the theorem.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["audience.claim_calibration"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "audience.claim_calibration"
