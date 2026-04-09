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


def test_nominalization_rule_can_disable_lexicalized_exception(registry, language_pack) -> None:
    source = "The documentation is clear.\n"
    document = _parse(language_pack, source)

    default_config = parse_project_config({"rules": {"active": ["surface.nominalization"]}})
    default_profile = ProfileResolver(registry).resolve(default_config, language_pack)
    default_context = RuleContext(
        default_profile, language_pack, FeatureStore(document, document.indexes)
    )
    default_rule = registry.instantiate(default_profile.rules["surface.nominalization"])
    assert default_rule.check(document, default_context) == []

    strict_config = parse_project_config(
        {
            "rules": {
                "active": ["surface.nominalization"],
                "overrides": {
                    "surface.nominalization": {
                        "options": {"allow_lexicalized_noun_exception": False}
                    }
                },
            }
        }
    )
    strict_profile = ProfileResolver(registry).resolve(strict_config, language_pack)
    strict_context = RuleContext(
        strict_profile, language_pack, FeatureStore(document, document.indexes)
    )
    strict_rule = registry.instantiate(strict_profile.rules["surface.nominalization"])
    violations = strict_rule.check(document, strict_context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.nominalization"


def test_nominalization_rule_can_disable_adjective_position_exception(registry, language_pack) -> None:
    source = "Configuration file stores values.\n"

    default_config = parse_project_config({"rules": {"active": ["surface.nominalization"]}})
    default_profile = ProfileResolver(registry).resolve(default_config, language_pack)
    default_document = _annotate(language_pack, default_profile, _parse(language_pack, source))
    default_context = RuleContext(
        default_profile, language_pack, FeatureStore(default_document, default_document.indexes)
    )
    default_rule = registry.instantiate(default_profile.rules["surface.nominalization"])
    assert default_rule.check(default_document, default_context) == []

    strict_config = parse_project_config(
        {
            "rules": {
                "active": ["surface.nominalization"],
                "overrides": {
                    "surface.nominalization": {
                        "options": {
                            "allow_adjective_position_exception": False,
                            "allow_lexicalized_noun_exception": False,
                        }
                    }
                },
            }
        }
    )
    strict_profile = ProfileResolver(registry).resolve(strict_config, language_pack)
    strict_document = _annotate(language_pack, strict_profile, _parse(language_pack, source))
    strict_context = RuleContext(
        strict_profile, language_pack, FeatureStore(strict_document, strict_document.indexes)
    )
    strict_rule = registry.instantiate(strict_profile.rules["surface.nominalization"])
    violations = strict_rule.check(strict_document, strict_context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.nominalization"


def test_vague_procedural_nominalization_rule_emits(registry, language_pack, research_profile) -> None:
    source = "The comparison remains inconclusive.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.vague_procedural_nominalization"])
    violations = rule.check(document, context)
    assert len(violations) == 1


def test_abstract_framing_rule_covers_forbidden_literal_strings(
    registry, language_pack, research_profile
) -> None:
    source = "The operator is responsible for the contraction.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.abstract_framing"])
    violations = rule.check(document, context)
    assert len(violations) == 1


def test_vague_procedural_nominalization_rule_accepts_explicit_arguments(
    registry, language_pack, research_profile
) -> None:
    source = "The comparison between X and Y remains inconclusive.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.vague_procedural_nominalization"])
    assert rule.check(document, context) == []


def test_concrete_subject_rule_emits(registry, language_pack, research_profile) -> None:
    source = "This section derives the factorization.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.concrete_subject"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.concrete_subject"


def test_lexicalized_compound_exception_is_configurable(registry, language_pack) -> None:
    source = "Open-source command-line utility improves workflow.\n"
    document = _parse(language_pack, source)

    default_config = parse_project_config(
        {"rules": {"active": ["surface.abstract_compound_modifier"]}}
    )
    default_profile = ProfileResolver(registry).resolve(default_config, language_pack)
    default_context = RuleContext(
        default_profile, language_pack, FeatureStore(document, document.indexes)
    )
    default_rule = registry.instantiate(default_profile.rules["surface.abstract_compound_modifier"])
    assert default_rule.check(document, default_context) == []

    strict_config = parse_project_config(
        {
            "rules": {
                "active": ["surface.abstract_compound_modifier"],
                "overrides": {
                    "surface.abstract_compound_modifier": {
                        "options": {"allow_lexicalized_exception": False}
                    }
                },
            }
        }
    )
    strict_profile = ProfileResolver(registry).resolve(strict_config, language_pack)
    strict_context = RuleContext(
        strict_profile, language_pack, FeatureStore(document, document.indexes)
    )
    strict_rule = registry.instantiate(strict_profile.rules["surface.abstract_compound_modifier"])
    violations = strict_rule.check(document, strict_context)
    assert len(violations) == 1


def test_sentence_economy_rules_emit(registry, language_pack, research_profile) -> None:
    document = _parse(
        language_pack,
        (
            "It provides the following benefits: speed and precision.\n"
            "In order to prove convergence, we bound the residual.\n"
            "We track alpha, beta, gamma, delta, epsilon, and zeta.\n"
            "Optimization regularization stabilization calibration pipeline fails.\n"
        ),
    )
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))

    verbose = registry.instantiate(research_profile.rules["surface.verbose_preamble"])
    redundant = registry.instantiate(research_profile.rules["surface.redundant_leadin"])
    long_enum = registry.instantiate(research_profile.rules["surface.long_inline_enumeration"])
    stacked = registry.instantiate(research_profile.rules["surface.stacked_nominalization_chain"])

    assert len(verbose.check(document, context)) == 1
    assert len(redundant.check(document, context)) == 1
    assert len(long_enum.check(document, context)) == 1
    assert len(stacked.check(document, context)) == 1


def test_double_framing_rule_emits(registry, language_pack, research_profile) -> None:
    source = (
        "This section provides the following points:\n\n"
        "- This point establishes the baseline.\n"
        "- This point explains the normalization.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.double_framing"])
    violations = rule.check(document, context)
    assert len(violations) == 1


def test_information_architecture_rules(registry, language_pack, research_profile) -> None:
    opening_missing = _parse(language_pack, "- [A](#a)\n- [B](#b)\n")
    opening_context = RuleContext(
        research_profile, language_pack, FeatureStore(opening_missing, opening_missing.indexes)
    )
    opening_rule = registry.instantiate(research_profile.rules["structure.opening_sentence_presence"])
    assert len(opening_rule.check(opening_missing, opening_context)) == 1

    prose_outside = _parse(
        language_pack,
        "This is a substantial opening paragraph that should be placed under a heading.\n\n# Setup\n",
    )
    prose_context = RuleContext(
        research_profile, language_pack, FeatureStore(prose_outside, prose_outside.indexes)
    )
    prose_rule = registry.instantiate(research_profile.rules["structure.prose_outside_heading"])
    assert len(prose_rule.check(prose_outside, prose_context)) == 1

    heading_skip = _parse(language_pack, "# Top\n\n### Deep\n")
    skip_context = RuleContext(
        research_profile, language_pack, FeatureStore(heading_skip, heading_skip.indexes)
    )
    skip_rule = registry.instantiate(research_profile.rules["structure.heading_level_skip"])
    assert len(skip_rule.check(heading_skip, skip_context)) == 1
