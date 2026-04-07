from __future__ import annotations

from pathlib import Path

from hermeneia.config.profile import ProfileResolver
from hermeneia.config.schema import parse_project_config
from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.indexes import FeatureStore
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.parser import ParseRequest
from hermeneia.rules.base import RuleContext


def _parse(language_pack, source: str):
    return MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )


def _annotate(language_pack, profile, document):
    return (
        SpaCyDocumentAnnotator(language_pack.parser_model)
        .annotate(document, profile)
        .document
    )


def test_passive_voice_rule_emits(registry, language_pack, research_profile) -> None:
    document = _parse(language_pack, "The theorem was proved by contradiction.\n")
    document = _annotate(language_pack, research_profile, document)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.passive_voice"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.passive_voice"


def test_transition_quality_rule_emits_without_support(
    registry, language_pack, research_profile
) -> None:
    source = "However, this conclusion remains asserted.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["discourse.transition_quality"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "discourse.transition_quality"


def test_sentence_redundancy_rule_emits_on_adjacent_restatement(
    registry, language_pack, research_profile
) -> None:
    source = (
        "The argument controls the leading term in the expansion.\n"
        "The argument controls the leading term in the expansion.\n"
    )
    document = _parse(language_pack, source)
    document = _annotate(language_pack, research_profile, document)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.sentence_redundancy"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.sentence_redundancy"


def test_paragraph_redundancy_rule_emits_on_duplicate_paragraphs(
    registry, language_pack, research_profile
) -> None:
    source = (
        "The contraction argument controls the nonlinear residual term.\n\n"
        "The contraction argument controls the nonlinear residual term.\n"
    )
    document = _parse(language_pack, source)
    document = _annotate(language_pack, research_profile, document)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.paragraph_redundancy"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.paragraph_redundancy"


def test_heading_capitalization_rule_emits_for_mixed_styles(
    registry, language_pack, research_profile
) -> None:
    source = "# Intro\n\n## Main Result\n\n## main derivation\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.heading_capitalization"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.heading_capitalization"


def test_jargon_density_rule_emits_for_learner_profile(registry, language_pack) -> None:
    config = parse_project_config(
        {
            "profile": {"name": "pedagogical", "audience": "learner"},
            "rules": {"active": ["audience.jargon_density"]},
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    source = "The homomorphism and isomorphism induce a stochastic asymptotic cohomology argument.\n"
    document = _parse(language_pack, source)
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(profile.rules["audience.jargon_density"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "audience.jargon_density"


def test_math_proof_marker_rule_emits_without_proof_opener(
    registry, language_pack, research_profile
) -> None:
    source = "The estimate follows.\n\n$\\square$\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.proof_marker"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.proof_marker"


def test_math_prose_math_rule_emits_on_paraphrased_relation(
    registry, language_pack, research_profile
) -> None:
    source = "The gain is given by the product of x times y.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.prose_math"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.prose_math"
