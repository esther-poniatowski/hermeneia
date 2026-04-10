from __future__ import annotations

import sys

from hermeneia.rules.loader import load_external_rules
from hermeneia.rules.base import (
    Layer,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    SourcePatternRule,
)


def test_load_builtin_rules_registers_expected_ids(registry) -> None:
    assert len(registry.rule_ids()) == 76
    assert all(
        not rule_id.startswith(("surface.", "discourse.", "audience.", "sentence."))
        for rule_id in registry.rule_ids()
    )
    assert "vocabulary.contraction" in registry.rule_ids()
    assert "syntax.passive_voice" in registry.rule_ids()
    assert "vocabulary.prep_chain" in registry.rule_ids()
    assert "vocabulary.abstract_framing" in registry.rule_ids()
    assert "vocabulary.abstract_compound_modifier" in registry.rule_ids()
    assert "vocabulary.vague_procedural_nominalization" in registry.rule_ids()
    assert "vocabulary.concrete_subject" in registry.rule_ids()
    assert "vocabulary.assumption_hypothesis_framing" in registry.rule_ids()
    assert "reference.personal_pronoun" in registry.rule_ids()
    assert "reference.generic_one" in registry.rule_ids()
    assert "reference.bare_pronoun_opening" in registry.rule_ids()
    assert "vocabulary.verbose_preamble" in registry.rule_ids()
    assert "vocabulary.redundant_leadin" in registry.rule_ids()
    assert "syntax.long_inline_enumeration" in registry.rule_ids()
    assert "vocabulary.stacked_nominalization_chain" in registry.rule_ids()
    assert "vocabulary.indefinite_reference" in registry.rule_ids()
    assert "vocabulary.double_negative" in registry.rule_ids()
    assert "vocabulary.boilerplate_opener" in registry.rule_ids()
    assert "math.display_math" in registry.rule_ids()
    assert "math.display_ambiguous" in registry.rule_ids()
    assert "math.display_unclosed" in registry.rule_ids()
    assert "math.inline_math" in registry.rule_ids()
    assert "math.shorthand" in registry.rule_ids()
    assert "math.assumption_motivation_order" in registry.rule_ids()
    assert "math.proof_placement_context" in registry.rule_ids()
    assert "math.display_followup_interpretation" in registry.rule_ids()
    assert "math.consecutive_display_blocks_without_bridge" in registry.rule_ids()
    assert "math.proof_marker" in registry.rule_ids()
    assert "paragraph.topic_sentence" in registry.rule_ids()
    assert "paragraph.paragraph_redundancy" in registry.rule_ids()
    assert "paragraph.inline_enumeration_overload" in registry.rule_ids()
    assert "paragraph.inline_case_split" in registry.rule_ids()
    assert "paragraph.double_framing" in registry.rule_ids()
    assert "paragraph.concept_reference_drift" in registry.rule_ids()
    assert "paragraph.reformulation_inflation" in registry.rule_ids()
    assert "linkage.transition_quality" in registry.rule_ids()
    assert "linkage.semicolon_connector" in registry.rule_ids()
    assert "syntax.embedding_depth" in registry.rule_ids()
    assert "linkage.numbered_case" in registry.rule_ids()
    assert "reference.heading_link" in registry.rule_ids()
    assert "reference.see_link" in registry.rule_ids()
    assert "reference.raw_anchor" in registry.rule_ids()
    assert "reference.generic_link_text" in registry.rule_ids()
    assert "structure.heading_capitalization" in registry.rule_ids()
    assert "structure.heading_level_skip" in registry.rule_ids()
    assert "structure.section_opener_block_kind" in registry.rule_ids()
    assert "structure.opening_sentence_presence" in registry.rule_ids()
    assert "structure.opening_message_focus" in registry.rule_ids()
    assert "structure.section_order_sequence" in registry.rule_ids()
    assert "structure.orphan_section" in registry.rule_ids()
    assert "structure.prose_outside_heading" in registry.rule_ids()
    assert "terminology.definition_before_use" in registry.rule_ids()
    assert "terminology.jargon_density" in registry.rule_ids()
    assert "evidence.qualitative_claim_without_quant_support" in registry.rule_ids()
    assert "evidence.imprecise_quantifier_without_citation" in registry.rule_ids()


def test_load_external_rules_uses_same_register_protocol(tmp_path, registry) -> None:
    module_path = tmp_path / "custom_rule_module.py"
    module_path.write_text(
        "\n".join(
            [
                "from hermeneia.rules.base import Layer, RuleKind, RuleMetadata, Severity, Tractability, SourcePatternRule",
                "class DemoRule(SourcePatternRule):",
                "    metadata = RuleMetadata(",
                "        rule_id='demo.rule',",
                "        label='demo',",
                "        layer=Layer.SURFACE_STYLE,",
                "        tractability=Tractability.CLASS_A,",
                "        kind=RuleKind.SOFT_HEURISTIC,",
                "        default_severity=Severity.INFO,",
                "        supported_languages=frozenset({'en'}),",
                "    )",
                "    def check_source(self, lines, doc, ctx):",
                "        return []",
                "def register(registry):",
                "    registry.add(DemoRule)",
            ]
        ),
        encoding="utf-8",
    )
    sys.path.insert(0, str(tmp_path))
    try:
        load_external_rules("custom_rule_module", registry)
    finally:
        sys.path.remove(str(tmp_path))
    assert "demo.rule" in registry.rule_ids()
