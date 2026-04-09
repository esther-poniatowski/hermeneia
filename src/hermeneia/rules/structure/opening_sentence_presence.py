"""Detect missing opening sentence before structured content."""

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

STRUCTURED_OPENING_KINDS = {
    BlockKind.LIST,
    BlockKind.TABLE,
    BlockKind.CODE_BLOCK,
    BlockKind.DISPLAY_MATH,
}
PROSE_KINDS = {
    BlockKind.PARAGRAPH,
    BlockKind.BLOCK_QUOTE,
    BlockKind.LIST_ITEM,
    BlockKind.TABLE_CELL,
    BlockKind.ADMONITION,
    BlockKind.FOOTNOTE,
}


class OpeningSentencePresenceRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="structure.opening_sentence_presence",
        label="Document should open with a purpose sentence before structured blocks",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"min_opening_words": 8},
        evidence_fields=("first_structured_kind",),
    )

    def check(self, doc, ctx):
        min_opening_words = self.settings.int_option("min_opening_words", 8)
        flat_blocks = list(doc.iter_blocks())
        if not flat_blocks:
            return []
        first_structured_index = _first_structured_index(flat_blocks)
        opening_sentence = _opening_sentence(
            flat_blocks,
            before_index=first_structured_index,
            min_words=min_opening_words,
        )
        if opening_sentence is not None:
            return []
        if first_structured_index is None:
            return []
        first_structured = flat_blocks[first_structured_index]
        return [
            Violation(
                rule_id=self.rule_id,
                message=(
                    "Document starts with structured content before an opening purpose sentence."
                ),
                span=first_structured.span,
                severity=self.settings.severity,
                layer=self.metadata.layer,
                evidence=RuleEvidence(
                    features={"first_structured_kind": first_structured.kind.value}
                ),
                confidence=0.7,
                rationale=(
                    "Opening-sentence checks use early block order and word-count thresholds."
                ),
                rewrite_tactics=(
                    "Add one opening sentence stating document purpose before lists, code, tables, or equations.",
                ),
            )
        ]


def _first_structured_index(blocks) -> int | None:
    for index, block in enumerate(blocks):
        if block.kind in STRUCTURED_OPENING_KINDS:
            return index
    return None


def _opening_sentence(blocks, *, before_index: int | None, min_words: int):
    limit = before_index if before_index is not None else len(blocks)
    for block in blocks[:limit]:
        if block.kind not in PROSE_KINDS:
            continue
        for sentence in block.sentences:
            if sentence_word_count(sentence) >= min_words:
                return sentence
    return None


def register(registry) -> None:
    registry.add(OpeningSentencePresenceRule)
