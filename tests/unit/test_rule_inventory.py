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


def test_transition_quality_rule_emits_on_unmarked_shift(
    registry, language_pack, research_profile
) -> None:
    source = (
        "The estimator controls the leading residual term.\n"
        "We now classify boundary regularity across unrelated domains.\n"
    )
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


def test_lexical_repetition_rule_emits_on_nonadjacent_restatement(
    registry, language_pack, research_profile
) -> None:
    source = (
        "The mapping controls the leading residual term.\n"
        "This sentence introduces notation for the boundary set.\n"
        "The mapping controls the leading residual term.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.lexical_repetition"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.lexical_repetition"


def test_concept_reference_drift_rule_emits_on_label_churn(
    registry, language_pack, research_profile
) -> None:
    source = (
        "The method updates parameters with a projected step.\n"
        "The approach updates parameters with a projected step.\n"
        "The framework updates parameters with a projected step.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.concept_reference_drift"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.concept_reference_drift"


def test_reformulation_inflation_rule_emits_on_restatement_marker(
    registry, language_pack, research_profile
) -> None:
    source = (
        "The estimate bounds the residual term uniformly.\n"
        "In other words, the estimate bounds the residual term uniformly.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.reformulation_inflation"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.reformulation_inflation"


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


def test_surface_abstract_framing_rule_emits(registry, language_pack, research_profile) -> None:
    source = "The fact that the residual decays implies stability.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.abstract_framing"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.abstract_framing"


def test_surface_abstract_compound_modifier_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "This is a context-dependent strategy for calibration.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.abstract_compound_modifier"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.abstract_compound_modifier"


def test_surface_abstract_compound_modifier_rule_emits_on_spaced_suffix_form(
    registry, language_pack, research_profile
) -> None:
    source = "We use a context dependent strategy for calibration.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.abstract_compound_modifier"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.abstract_compound_modifier"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["signal"] == "spaced_suffix"


def test_surface_assumption_hypothesis_framing_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "Under the compactness assumption, the sequence converges.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.assumption_hypothesis_framing"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.assumption_hypothesis_framing"


def test_surface_indefinite_reference_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "Everything improves somehow in the argument.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.indefinite_reference"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.indefinite_reference"


def test_math_display_ambiguous_rule_emits(registry, language_pack, research_profile) -> None:
    source = "$$ a $$ $$\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.display_ambiguous"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.display_ambiguous"


def test_math_display_unclosed_rule_emits_and_closed_display_passes(
    registry, language_pack, research_profile
) -> None:
    unclosed = _parse(language_pack, "$$\na+b\n")
    context = RuleContext(research_profile, language_pack, FeatureStore(unclosed, unclosed.indexes))
    rule = registry.instantiate(research_profile.rules["math.display_unclosed"])
    unclosed_violations = rule.check(unclosed, context)
    assert len(unclosed_violations) == 1
    assert unclosed_violations[0].rule_id == "math.display_unclosed"

    closed = _parse(language_pack, "$$\na+b\n$$\n")
    closed_context = RuleContext(
        research_profile, language_pack, FeatureStore(closed, closed.indexes)
    )
    assert rule.check(closed, closed_context) == []


def test_math_inline_math_rule_emits_on_equation_like_inline(
    registry, language_pack, research_profile
) -> None:
    source = "We use $a = b + c$ in the argument.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.inline_math"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.inline_math"


def test_math_shorthand_rule_emits_on_input_magnitude_alias(
    registry, language_pack, research_profile
) -> None:
    source = "$$\n\\rho := \\|\\mathbf{u}\\|\n$$\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.shorthand"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.shorthand"


def test_math_imperative_opening_rule_emits_on_fix(
    registry, language_pack, research_profile
) -> None:
    source = "Fix x in X.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.imperative_opening"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.imperative_opening"


def test_surface_heading_link_rule_emits(registry, language_pack, research_profile) -> None:
    source = "[Main result](#main-result)\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.heading_link"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.heading_link"


def test_surface_see_link_rule_emits(registry, language_pack, research_profile) -> None:
    source = "See [Lemma 2](#^lemma-two).\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.see_link"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.see_link"


def test_surface_raw_anchor_rule_emits(registry, language_pack, research_profile) -> None:
    source = "Use ^lemma-two for the cross-reference.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.raw_anchor"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.raw_anchor"


def test_surface_generic_link_text_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "[Lemma (Boundary bound)](#^lemma-two)\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.generic_link_text"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.generic_link_text"


def test_surface_generic_link_text_rule_emits_on_procedural_term(
    registry, language_pack, research_profile
) -> None:
    source = "[normality specialization](#^note-specialization)\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.generic_link_text"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.generic_link_text"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["signal"] == "procedural_term"


def test_surface_generic_link_text_rule_uses_configurable_reference_labels(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {
            "rules": {
                "active": ["surface.generic_link_text"],
                "overrides": {
                    "surface.generic_link_text": {
                        "options": {"reference_labels": ["fact"]},
                    }
                },
            }
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    source = "[Fact 2](#^fact-two)\n"
    document = _parse(language_pack, source)
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(profile.rules["surface.generic_link_text"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.generic_link_text"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["signal"] == "citation_label"


def test_surface_numbered_case_rule_emits(registry, language_pack, research_profile) -> None:
    source = "Case 1: the residual is bounded.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.numbered_case"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.numbered_case"


def test_surface_case_scaffolding_rule_emits_on_plural_case_form(
    registry, language_pack, research_profile
) -> None:
    source = "In the non-normal cases, the residual term grows.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.case_scaffolding"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.case_scaffolding"


def test_structure_section_opener_block_kind_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "# Setup\n\n$$\na=b\n$$\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.section_opener_block_kind"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.section_opener_block_kind"


def test_math_assumption_motivation_order_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "Assume the sequence is bounded.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.assumption_motivation_order"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.assumption_motivation_order"


def test_math_proof_placement_context_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "Lemma 2. The bound holds.\n\nProof.\nThe argument is standard.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.proof_placement_context"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.proof_placement_context"


def test_math_display_followup_interpretation_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = (
        "We derive the bound:\n\n$$\na=b+c+d+e+f+g\n$$\n\n"
        "The claim is immediate.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["math.display_followup_interpretation"]
    )
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.display_followup_interpretation"


def test_math_consecutive_display_blocks_without_bridge_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "Values are:\n\n$$\na=b\n$$\n\n$$\nc=d\n$$\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["math.consecutive_display_blocks_without_bridge"]
    )
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.consecutive_display_blocks_without_bridge"


def test_math_display_followup_interpretation_rule_accepts_interpretive_followup(
    registry, language_pack, research_profile
) -> None:
    source = (
        "We derive the bound:\n\n$$\na=b+c+d+e+f+g\n$$\n\n"
        "The equation shows how the correction term controls the residual.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["math.display_followup_interpretation"]
    )
    violations = rule.check(document, context)
    assert violations == []


def test_math_display_followup_interpretation_rule_skips_bare_pronoun_followup(
    registry, language_pack, research_profile
) -> None:
    source = "We derive the bound:\n\n$$\na=b+c+d+e+f+g\n$$\n\nIt follows.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["math.display_followup_interpretation"]
    )
    violations = rule.check(document, context)
    assert violations == []


def test_math_bare_pronoun_after_display_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "We derive the bound:\n\n$$\na=b+c+d+e+f+g\n$$\n\nIt follows.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.bare_pronoun_after_display"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.bare_pronoun_after_display"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["pronoun"] == "it"


def test_math_bare_pronoun_after_display_rule_accepts_named_object_followup(
    registry, language_pack, research_profile
) -> None:
    source = (
        "We derive the bound:\n\n$$\na=b+c+d+e+f+g\n$$\n\n"
        "This expression implies stability.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.bare_pronoun_after_display"])
    violations = rule.check(document, context)
    assert violations == []


def test_math_display_math_rule_emits_on_punctuation_before_linebreak(
    registry, language_pack, research_profile
) -> None:
    source = (
        "We compute the decomposition:\n\n$$\n\\begin{aligned}\n"
        "a &= b, \\\\\n"
        "c &= d\n"
        "\\end{aligned}\n$$\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.display_math"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.display_math"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["check"] == "punctuation_before_linebreak"


def test_math_display_math_rule_allows_internal_nonterminal_punctuation(
    registry, language_pack, research_profile
) -> None:
    source = "We define the map:\n\n$$\nf(a,b)=a+b\n$$\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.display_math"])
    violations = rule.check(document, context)
    assert violations == []


def test_math_consecutive_display_blocks_without_bridge_rule_passes_with_motivation(
    registry, language_pack, research_profile
) -> None:
    source = (
        "We introduce two identities:\n\n$$\na=b\n$$\n\n"
        "$$\nc=d\n$$\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["math.consecutive_display_blocks_without_bridge"]
    )
    violations = rule.check(document, context)
    assert violations == []


def test_discourse_semicolon_connector_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "The bound is stable; the estimate remains tight.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["discourse.semicolon_connector"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "discourse.semicolon_connector"


def test_paragraph_inline_enumeration_overload_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = (
        "We consider (i) the linear regime, (ii) the nonlinear regime, and "
        "(iii) the stochastic regime.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["paragraph.inline_enumeration_overload"]
    )
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.inline_enumeration_overload"


def test_paragraph_inline_case_split_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "When g < 1, the series converges; when g >= 1, it diverges.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.inline_case_split"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.inline_case_split"


def test_audience_qualitative_claim_without_quant_support_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "The method is robust across settings.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["audience.qualitative_claim_without_quant_support"]
    )
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "audience.qualitative_claim_without_quant_support"
