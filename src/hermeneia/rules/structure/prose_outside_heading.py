"""Detect significant prose that appears before any heading."""

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
from hermeneia.rules.common import sentence_word_count

PROSE_KINDS = {
    BlockKind.PARAGRAPH,
    BlockKind.BLOCK_QUOTE,
    BlockKind.LIST_ITEM,
    BlockKind.TABLE_CELL,
    BlockKind.ADMONITION,
    BlockKind.FOOTNOTE,
}


class ProseOutsideHeadingRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="structure.prose_outside_heading",
        label="Significant prose should live under an explicit heading",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"min_words": 12},
        evidence_fields=("word_count",),
    )

    def check(self, doc, ctx):
        _ = ctx
        min_words = self.settings.int_option("min_words", 12)
        headings = [block for block in doc.iter_blocks() if block.kind == BlockKind.HEADING]
        if not headings:
            return []
        first_heading_start = min(heading.span.start for heading in headings)
        violations: list[Violation] = []
        for block in doc.iter_blocks():
            if block.kind not in PROSE_KINDS:
                continue
            if block.span.start >= first_heading_start:
                continue
            word_count = sum(sentence_word_count(sentence) for sentence in block.sentences)
            if word_count < min_words:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Significant prose appears before any heading; move it under an explicit section."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"word_count": word_count}),
                    confidence=0.75,
                    rewrite_tactics=(
                        "Introduce a heading and place the prose inside that section.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(ProseOutsideHeadingRule)
