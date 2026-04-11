"""Detect rhetorical reformulations that restate the same proposition."""

from __future__ import annotations

from hermeneia.document.indexes import SupportSignalKind
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
from hermeneia.rules.patterns import compile_leading_phrase_regex


class ReformulationInflationRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.reformulation_inflation",
        label="Avoid rhetorical reformulation when it adds no new contribution",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"min_overlap": 0.62},
        evidence_fields=("marker", "overlap", "left_sentence_id", "right_sentence_id"),
    )

    def check(self, doc, ctx):
        min_overlap = self.settings.float_option("min_overlap", 0.62)
        marker_pattern = compile_leading_phrase_regex(
            tuple(ctx.language_pack.lexicons.reformulation_markers)
        )
        support_by_sentence = _support_signals_by_sentence(doc)
        violations: list[Violation] = []
        sentence_refs = doc.indexes.sentences
        for index in range(len(sentence_refs) - 1):
            left_ref = sentence_refs[index]
            right_ref = sentence_refs[index + 1]
            if left_ref.block_id != right_ref.block_id:
                continue
            right_sentence = doc.sentence_by_id(right_ref.id)
            if right_sentence is None:
                continue
            marker_match = marker_pattern.search(right_sentence.projection.text)
            if marker_match is None:
                continue
            overlap = ctx.features.sentence_overlap(left_ref.id, right_ref.id)
            if overlap < min_overlap:
                continue
            if support_by_sentence.get(right_ref.id, frozenset()) & {
                SupportSignalKind.CITATION,
                SupportSignalKind.THEOREM_REF,
                SupportSignalKind.PROOF_REF,
                SupportSignalKind.QUANTITATIVE_RESULT,
                SupportSignalKind.DISPLAYED_EQUATION,
            }:
                continue
            marker = marker_match.group(0).strip().lower()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Reformulation marker introduces a near-restatement with minimal new "
                        "information."
                    ),
                    span=right_sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "marker": marker,
                            "overlap": round(overlap, 3),
                            "left_sentence_id": left_ref.id,
                            "right_sentence_id": right_ref.id,
                        },
                        score=round(overlap, 3),
                        threshold=min_overlap,
                    ),
                    confidence=max(0.62, min(0.9, overlap)),
                    rationale=(
                        "The rule combines explicit reformulation markers with high adjacent "
                        "sentence overlap and support-signal gating."
                    ),
                    rewrite_tactics=(
                        "Keep one formulation and spend the next sentence on new evidence, scope, or consequence.",
                    ),
                )
            )
        return violations


def _support_signals_by_sentence(doc) -> dict[str, frozenset[SupportSignalKind]]:
    signals: dict[str, set[SupportSignalKind]] = {}
    for signal in doc.indexes.support_signals:
        if signal.sentence_id is None:
            continue
        signals.setdefault(signal.sentence_id, set()).add(signal.kind)
    return {sentence_id: frozenset(signal_kinds) for sentence_id, signal_kinds in signals.items()}


def register(registry) -> None:
    registry.add(ReformulationInflationRule)
