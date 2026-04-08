"""Paragraph-level lexical repetition as a redundancy proxy."""

from __future__ import annotations

from hermeneia.document.indexes import SupportSignalKind
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


class LexicalRepetitionRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.lexical_repetition",
        label="Paragraph repeats equivalent claims with limited new contribution",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_nonadjacent_overlap": 0.7,
            "min_redundant_pairs": 1,
            "min_sentence_count": 3,
        },
        evidence_fields=("redundant_pairs", "max_overlap", "sentence_count"),
    )

    def check(self, doc, ctx):
        min_overlap = self.settings.float_option("min_nonadjacent_overlap", 0.7)
        min_redundant_pairs = self.settings.int_option("min_redundant_pairs", 1)
        min_sentence_count = self.settings.int_option("min_sentence_count", 3)
        strong_claim_markers = tuple(
            marker.lower() for marker in ctx.language_pack.lexicons.strong_claim_markers
        )
        support_by_sentence = _support_signals_by_sentence(doc)

        violations: list[Violation] = []
        for block in iter_blocks(doc, {BlockKind.PARAGRAPH}):
            if len(block.sentences) < min_sentence_count:
                continue
            redundant_pairs: list[tuple[str, str, float]] = []
            max_overlap = 0.0
            sentences = block.sentences
            for left_index in range(len(sentences)):
                left = sentences[left_index]
                for right_index in range(left_index + 2, len(sentences)):
                    right = sentences[right_index]
                    overlap = ctx.features.sentence_overlap(left.id, right.id)
                    if overlap < min_overlap:
                        continue
                    if _introduces_new_support(
                        right_sentence_text=right.projection.text.lower(),
                        right_sentence_signals=support_by_sentence.get(right.id, frozenset()),
                        strong_claim_markers=strong_claim_markers,
                    ):
                        continue
                    redundant_pairs.append((left.id, right.id, overlap))
                    if overlap > max_overlap:
                        max_overlap = overlap
            if len(redundant_pairs) < min_redundant_pairs:
                continue
            top_pairs = sorted(redundant_pairs, key=lambda item: (-item[2], item[0], item[1]))[:3]
            pair_payload = tuple(
                {
                    "left_sentence_id": left_id,
                    "right_sentence_id": right_id,
                    "overlap": round(overlap, 3),
                }
                for left_id, right_id, overlap in top_pairs
            )
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "The paragraph restates the same core proposition across multiple "
                        "sentences without clear new contribution."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "redundant_pairs": pair_payload,
                            "max_overlap": round(max_overlap, 3),
                            "sentence_count": len(sentences),
                        },
                        score=round(max_overlap, 3),
                        threshold=min_overlap,
                    ),
                    confidence=max(0.58, min(0.9, max_overlap)),
                    rationale=(
                        "The rule flags non-adjacent sentence pairs with high lexical overlap "
                        "when no strong support signal indicates genuine argumentative progress."
                    ),
                    rewrite_tactics=(
                        "Merge restatements so each sentence contributes a distinct claim, "
                        "evidence step, or consequence.",
                    ),
                )
            )
        return violations


def _support_signals_by_sentence(doc) -> dict[str, frozenset[SupportSignalKind]]:
    signals: dict[str, set[SupportSignalKind]] = {}
    for signal in doc.indexes.support_signals:
        if signal.sentence_id is None:
            continue
        bucket = signals.setdefault(signal.sentence_id, set())
        bucket.add(signal.kind)
    return {sentence_id: frozenset(kinds) for sentence_id, kinds in signals.items()}


def _introduces_new_support(
    right_sentence_text: str,
    right_sentence_signals: frozenset[SupportSignalKind],
    strong_claim_markers: tuple[str, ...],
) -> bool:
    if right_sentence_signals & {
        SupportSignalKind.CITATION,
        SupportSignalKind.THEOREM_REF,
        SupportSignalKind.PROOF_REF,
        SupportSignalKind.DISPLAYED_EQUATION,
        SupportSignalKind.QUANTITATIVE_RESULT,
    }:
        return True
    return any(marker in right_sentence_text for marker in strong_claim_markers)


def register(registry) -> None:
    registry.add(LexicalRepetitionRule)
