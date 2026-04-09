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


def test_stress_position_rule_emits_on_weak_terminal_token(
    registry, language_pack, research_profile
) -> None:
    source = "The residual bound is this.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["discourse.stress_position"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "discourse.stress_position"


def test_subordinate_clause_rule_emits_on_clause_stacking(
    registry, language_pack, research_profile
) -> None:
    source = (
        "Although the estimator is stable because the data are bounded, "
        "while the update remains small, the residual converges.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["discourse.subordinate_clause"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "discourse.subordinate_clause"


def test_embedding_depth_rule_emits_on_highly_embedded_sentence(
    registry, language_pack, research_profile
) -> None:
    source = (
        "Although the estimator, which we introduced when the benchmark that the paper "
        "defines was released, improves accuracy, the variance remains unstable.\n"
    )
    document = _annotate(language_pack, research_profile, _parse(language_pack, source))
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["discourse.embedding_depth"])
    violations = rule.check(document, context)
    assert len(violations) >= 1
    assert violations[0].rule_id == "discourse.embedding_depth"


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


def test_surface_vague_phrasing_rule_emits(registry, language_pack, research_profile) -> None:
    source = "The update affects convergence in many ways.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.vague_phrasing"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.vague_phrasing"


def test_surface_noun_cluster_rule_emits(registry, language_pack, research_profile) -> None:
    source = "High-order sparse tensor factorization pipeline design improves robustness.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.noun_cluster"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.noun_cluster"


def test_surface_cross_reference_rule_emits(registry, language_pack, research_profile) -> None:
    source = "As discussed above, the estimate remains stable.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.cross_reference"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.cross_reference"


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


def test_surface_double_negative_rule_emits(registry, language_pack, research_profile) -> None:
    source = "The estimate is not without error.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.double_negative"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.double_negative"


def test_surface_boilerplate_opener_rule_emits(registry, language_pack, research_profile) -> None:
    source = "Recently, there has been an increasing interest in this model.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.boilerplate_opener"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.boilerplate_opener"


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


def test_math_bare_symbol_rule_emits(registry, language_pack, research_profile) -> None:
    source = "We study a function on $\\Theta$ under perturbations.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["math.bare_symbol"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "math.bare_symbol"


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


def test_structure_section_opener_block_kind_rule_emits_on_list_opening(
    registry, language_pack, research_profile
) -> None:
    source = "# Setup\n\n- item\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.section_opener_block_kind"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.section_opener_block_kind"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["first_block_kind"] == "list"


def test_structure_section_opener_block_kind_rule_respects_heading_level_scope(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {
            "profile": {"name": "research"},
            "rules": {
                "overrides": {
                    "structure.section_opener_block_kind": {
                        "options": {"apply_heading_levels": [2]},
                    }
                }
            },
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    source = "# Top\n\n- top item\n\n## Details\n\n- detail item\n"
    document = _parse(language_pack, source)
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(profile.rules["structure.section_opener_block_kind"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.section_opener_block_kind"
    assert violations[0].span.start_line == 7


def test_structure_section_opener_block_kind_rule_respects_block_kind_filter(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {
            "profile": {"name": "research"},
            "rules": {
                "overrides": {
                    "structure.section_opener_block_kind": {
                        "options": {"blocked_block_kinds": ["display_math", "code_block"]},
                    }
                }
            },
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    source = "# Setup\n\n- item\n"
    document = _parse(language_pack, source)
    context = RuleContext(profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(profile.rules["structure.section_opener_block_kind"])
    assert rule.check(document, context) == []


def test_structure_opening_sentence_presence_rule_respects_block_kind_filter(
    registry, language_pack
) -> None:
    config = parse_project_config(
        {
            "profile": {"name": "research"},
            "rules": {
                "overrides": {
                    "structure.opening_sentence_presence": {
                        "options": {"forbidden_block_kinds": ["table"]},
                    }
                }
            },
        }
    )
    profile = ProfileResolver(registry).resolve(config, language_pack)
    list_opening = _parse(language_pack, "- item\n")
    list_context = RuleContext(
        profile, language_pack, FeatureStore(list_opening, list_opening.indexes)
    )
    rule = registry.instantiate(profile.rules["structure.opening_sentence_presence"])
    assert rule.check(list_opening, list_context) == []

    table_opening = _parse(language_pack, "| A |\n| - |\n| x |\n")
    table_context = RuleContext(
        profile, language_pack, FeatureStore(table_opening, table_opening.indexes)
    )
    violations = rule.check(table_opening, table_context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.opening_sentence_presence"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["first_structured_kind"] == "table"


def test_structure_section_balance_rule_emits(registry, language_pack, research_profile) -> None:
    source = (
        "# Long section\n\n"
        "This section introduces the central assumptions, then expands each premise with detailed "
        "motivations, examples, and implications for each stage of the argument progression.\n\n"
        "# Short section\n\n"
        "Brief note.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.section_balance"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.section_balance"


def test_structure_section_order_sequence_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = (
        "# Installation\n\n"
        "Run the setup command.\n\n"
        "# Overview\n\n"
        "This page explains the purpose.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.section_order_sequence"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.section_order_sequence"


def test_structure_opening_message_focus_rule_emits_on_enumeration_dominance(
    registry, language_pack, research_profile
) -> None:
    source = (
        "Clear, concise, convincing, fluid, organized, interesting, and useful prose matters.\n\n"
        "# Setup\n\n"
        "Details.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.opening_message_focus"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.opening_message_focus"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["issue"] == "enumeration_dominant_opening"


def test_structure_orphan_section_rule_emits(registry, language_pack, research_profile) -> None:
    source = (
        "# Methods\n\n"
        "Short intro.\n\n"
        "## Algorithm\n\n"
        "The algorithm section contains details.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["structure.orphan_section"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "structure.orphan_section"


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


def test_surface_bare_pronoun_opening_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "It follows that the estimate converges.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.bare_pronoun_opening"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "surface.bare_pronoun_opening"
    assert violations[0].evidence is not None
    assert violations[0].evidence.features["pronoun"] == "it"


def test_surface_bare_pronoun_opening_rule_accepts_named_subject(
    registry, language_pack, research_profile
) -> None:
    source = "This expression implies stability.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["surface.bare_pronoun_opening"])
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


def test_paragraph_parallelism_rule_emits(registry, language_pack, research_profile) -> None:
    source = (
        "- Computing the residual map.\n"
        "- Bounding the correction term.\n"
        "- The final convergence statement.\n"
    )
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(research_profile.rules["paragraph.parallelism"])
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "paragraph.parallelism"


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


def test_audience_imprecise_quantifier_without_citation_rule_emits(
    registry, language_pack, research_profile
) -> None:
    source = "Several methods improve the estimate, while others fail near the boundary.\n"
    document = _parse(language_pack, source)
    context = RuleContext(research_profile, language_pack, FeatureStore(document, document.indexes))
    rule = registry.instantiate(
        research_profile.rules["audience.imprecise_quantifier_without_citation"]
    )
    violations = rule.check(document, context)
    assert len(violations) == 1
    assert violations[0].rule_id == "audience.imprecise_quantifier_without_citation"
