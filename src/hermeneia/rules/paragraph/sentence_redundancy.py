"""Adjacent-sentence redundancy heuristics."""

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
from hermeneia.rules.common import sentence_has_marker


class SentenceRedundancyRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.sentence_redundancy",
        label="Adjacent sentences appear redundant",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"min_overlap": 0.78},
        evidence_fields=("overlap", "left_sentence_id", "right_sentence_id"),
    )

    def check(self, doc, ctx):
        min_overlap = self.settings.float_option("min_overlap", 0.78)
        violations: list[Violation] = []
        sentence_refs = doc.indexes.sentences
        support_by_sentence = {
            signal.sentence_id: signal.kind
            for signal in doc.indexes.support_signals
            if signal.sentence_id is not None
        }
        strong_claim_markers = tuple(
            marker.lower() for marker in ctx.language_pack.lexicons.strong_claim_markers
        )
        for index in range(len(sentence_refs) - 1):
            left_ref = sentence_refs[index]
            right_ref = sentence_refs[index + 1]
            if left_ref.block_id != right_ref.block_id:
                continue
            overlap = ctx.features.sentence_overlap(left_ref.id, right_ref.id)
            if overlap < min_overlap:
                continue
            right_sentence = doc.sentence_by_id(right_ref.id)
            if right_sentence is None:
                continue
            if _introduces_citation_or_claim(
                right_sentence,
                support_by_sentence.get(right_ref.id),
                strong_claim_markers,
            ):
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="Two adjacent sentences restate largely the same content.",
                    span=right_sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "overlap": round(overlap, 3),
                            "left_sentence_id": left_ref.id,
                            "right_sentence_id": right_ref.id,
                        },
                        score=overlap,
                        threshold=min_overlap,
                    ),
                    confidence=min(0.9, max(0.55, overlap)),
                    rationale="Sentence redundancy combines lexical overlap with bounded suppression signals.",
                    rewrite_tactics=(
                        "Merge the adjacent statements or keep only the sentence that carries new information.",
                    ),
                )
            )
        return violations


def _introduces_citation_or_claim(
    sentence,
    signal_kind: SupportSignalKind | None,
    strong_claim_markers: tuple[str, ...],
) -> bool:
    if signal_kind == SupportSignalKind.CITATION:
        return True
    return sentence_has_marker(sentence, strong_claim_markers)


def register(registry) -> None:
    registry.add(SentenceRedundancyRule)
