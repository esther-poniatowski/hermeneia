"""Cross-paragraph redundancy candidate diagnostics."""

from __future__ import annotations

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


class ParagraphRedundancyRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.paragraph_redundancy",
        label="Paragraph pair appears redundant",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_similarity": 0.88,
            "min_lexical_overlap": 0.35,
            "max_findings": 5,
        },
        evidence_fields=("similarity", "lexical_overlap", "left_block_id", "right_block_id"),
    )

    def check(self, doc, ctx):
        min_similarity = self.settings.float_option("min_similarity", 0.88)
        min_lexical_overlap = self.settings.float_option("min_lexical_overlap", 0.35)
        max_findings = self.settings.int_option("max_findings", 5)
        violations: list[Violation] = []
        for left_id, right_id, similarity in ctx.features.redundancy_candidates(
            similarity_threshold=min_similarity
        ):
            overlap = ctx.features.paragraph_overlap(left_id, right_id)
            if overlap < min_lexical_overlap:
                continue
            right_block = doc.block_by_id(right_id)
            if right_block is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="This paragraph appears semantically redundant with an earlier paragraph.",
                    span=right_block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "similarity": round(similarity, 3),
                            "lexical_overlap": round(overlap, 3),
                            "left_block_id": left_id,
                            "right_block_id": right_id,
                        },
                        score=similarity,
                        threshold=min_similarity,
                    ),
                    confidence=min(0.9, max(0.6, similarity)),
                    rationale="Paragraph redundancy uses blocked candidate generation plus lexical corroboration.",
                    rewrite_tactics=(
                        "Consolidate repeated claims into one paragraph and keep only genuinely new argument steps.",
                    ),
                )
            )
            if len(violations) >= max_findings:
                break
        return violations


def register(registry) -> None:
    registry.add(ParagraphRedundancyRule)
