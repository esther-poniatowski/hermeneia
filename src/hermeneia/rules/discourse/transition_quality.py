"""Discourse-transition articulation heuristics."""

from __future__ import annotations

from hermeneia.document.model import BlockKind
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_blocks
from hermeneia.rules.patterns import (
    compile_leading_phrase_regex,
    compile_prefixed_term_regex,
)


class TransitionQualityRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="discourse.transition_quality",
        label="Discourse transitions are weakly articulated",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_overlap_without_connector": 0.18,
            "max_shift_findings": 3,
            "min_paragraph_sentences": 4,
            "min_average_overlap_without_connectors": 0.35,
        },
        evidence_fields=("issue",),
    )

    def check(self, doc, ctx):
        min_overlap = self.settings.float_option("min_overlap_without_connector", 0.18)
        max_shift_findings = self.settings.int_option("max_shift_findings", 3)
        min_paragraph_sentences = self.settings.int_option("min_paragraph_sentences", 4)
        min_average_overlap = self.settings.float_option(
            "min_average_overlap_without_connectors", 0.35
        )
        connector_pattern = compile_leading_phrase_regex(
            tuple(ctx.language_pack.lexicons.transition_connectors)
        )
        reference_pattern = compile_prefixed_term_regex(
            ("this", "these", "that", "such"),
            tuple(ctx.language_pack.lexicons.transition_reference_heads),
            anchored=True,
        )
        violations: list[Violation] = []
        for block in iter_blocks(doc, {BlockKind.PARAGRAPH, BlockKind.BLOCK_QUOTE, BlockKind.LIST_ITEM}):
            if len(block.sentences) < 2:
                continue
            connector_count = 0
            overlaps: list[float] = []
            shift_findings = 0
            for index in range(1, len(block.sentences)):
                previous = block.sentences[index - 1]
                current = block.sentences[index]
                current_text = current.projection.text
                if _starts_with_connector(current_text, connector_pattern):
                    connector_count += 1
                    continue
                overlap = ctx.features.sentence_overlap(previous.id, current.id)
                overlaps.append(overlap)
                if overlap >= min_overlap or _starts_with_linking_reference(
                    current_text, reference_pattern
                ):
                    continue
                if shift_findings >= max_shift_findings:
                    continue
                shift_findings += 1
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Adjacent sentences shift discourse without an explicit transition "
                            "or reference anchor."
                        ),
                        span=current.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "issue": "unmarked_shift",
                                "overlap": round(overlap, 3),
                                "previous_sentence_id": previous.id,
                                "current_sentence_id": current.id,
                            },
                            score=round(overlap, 3),
                            threshold=min_overlap,
                        ),
                        confidence=max(0.55, min(0.86, 0.9 - overlap)),
                        rationale=(
                            "Transition articulation checks adjacent-sentence continuity with "
                            "bounded overlap and explicit opener signals."
                        ),
                        rewrite_tactics=(
                            "Add a connector or a concrete reference link that states how this "
                            "sentence follows from the previous one.",
                        ),
                    )
                )
            if len(block.sentences) < min_paragraph_sentences:
                continue
            if connector_count > 0:
                continue
            if not overlaps:
                continue
            average_overlap = sum(overlaps) / len(overlaps)
            if average_overlap >= min_average_overlap:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "The paragraph chains multiple sentences without explicit transition "
                        "markers while local continuity remains weak."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": "connector_underuse",
                            "connector_count": connector_count,
                            "sentence_count": len(block.sentences),
                            "average_overlap": round(average_overlap, 3),
                        },
                        score=round(average_overlap, 3),
                        threshold=min_average_overlap,
                    ),
                    confidence=0.62,
                    rationale=(
                        "Paragraph-level articulation checks require explicit connective framing "
                        "when consecutive sentence overlap stays low."
                    ),
                    rewrite_tactics=(
                        "Introduce transition markers at key sentence boundaries to make the "
                        "argument steps explicit.",
                    ),
                )
            )
        return violations


def _starts_with_connector(text: str, connector_pattern) -> bool:
    return connector_pattern.search(text) is not None


def _starts_with_linking_reference(text: str, reference_pattern) -> bool:
    return reference_pattern.search(text) is not None


def register(registry) -> None:
    registry.add(TransitionQualityRule)
