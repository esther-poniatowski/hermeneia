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
    detection = detector.detect(document, research_profile, language_pack, features)
    assert any(violation.rule_id == "vocabulary.contraction" for violation in detection.violations)
    assert detection.diagnostics == ()


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
    rule = registry.instantiate(research_profile.rules["syntax.subject_verb_distance"])
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
    rule = registry.instantiate(research_profile.rules["evidence.claim_calibration"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "evidence.claim_calibration"


def test_claim_calibration_rule_abstains_on_heavy_math_masking(
    registry, language_pack, research_profile
) -> None:
    source = "$x$ $y$ $z$ $w$ clearly proves the claim.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["evidence.claim_calibration"])
    assert rule.check(document, context) == []


def test_passive_voice_rule_extracts_actor_for_by_phrase(
    registry, language_pack, research_profile
) -> None:
    source = "The theorem was proved by the authors.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    document = (
        SpaCyDocumentAnnotator(language_pack.parser_model)
        .annotate(document, research_profile)
        .document
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["syntax.passive_voice"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    evidence = violations[0].evidence
    assert evidence is not None
    assert evidence.features.get("actor") == "the authors"


def test_generic_one_rule_emits_on_subject_one_dependency(
    registry, language_pack, research_profile
) -> None:
    source = "One derives the estimate from Lemma 2.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    sentence_ref = document.indexes.sentences[0]
    sentence = document.sentence_by_id(sentence_ref.id)
    assert sentence is not None
    sentence.tokens = [
        Token("One", "one", "PRON", "nsubj", 1, sentence.span, 0, 3),
        Token("derives", "derive", "VERB", "ROOT", None, sentence.span, 4, 11),
        Token("the", "the", "DET", "det", 3, sentence.span, 12, 15),
        Token("estimate", "estimate", "NOUN", "dobj", 1, sentence.span, 16, 24),
    ]
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["reference.generic_one"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    evidence = violations[0].evidence
    assert evidence is not None
    assert evidence.features.get("phrase") == "one"
    assert evidence.features.get("signal") == "subject_dependency"


def test_personal_pronoun_rule_emits_on_we_subject(
    registry, language_pack, research_profile
) -> None:
    source = "We now derive the estimate.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["reference.personal_pronoun"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "reference.personal_pronoun"
