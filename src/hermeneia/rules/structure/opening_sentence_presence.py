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
from hermeneia.rules.structure._option_parsing import (
    as_block_kind_name_tuple,
    mapping_with_allowed_keys,
    resolve_block_kinds,
)

DEFAULT_FORBIDDEN_BLOCK_KINDS = (
    BlockKind.LIST,
    BlockKind.TABLE,
    BlockKind.CODE_BLOCK,
    BlockKind.DISPLAY_MATH,
)
PROSE_KINDS = {
    BlockKind.PARAGRAPH,
    BlockKind.BLOCK_QUOTE,
    BlockKind.LIST_ITEM,
    BlockKind.TABLE_CELL,
    BlockKind.ADMONITION,
    BlockKind.FOOTNOTE,
}


class _OpeningSentencePresenceOptions:
    def __init__(
        self,
        *,
        min_opening_words: int | None = None,
        forbidden_block_kinds: tuple[str, ...] | None = None,
    ) -> None:
        self.min_opening_words = min_opening_words
        self.forbidden_block_kinds = forbidden_block_kinds

    @classmethod
    def model_validate(cls, raw: object) -> "_OpeningSentencePresenceOptions":
        mapping = mapping_with_allowed_keys(
            raw,
            allowed=frozenset({"min_opening_words", "forbidden_block_kinds"}),
            scope="opening_sentence_presence options",
        )
        min_opening_words = _parse_positive_int(
            mapping.get("min_opening_words"), field="min_opening_words"
        )
        forbidden_block_kinds = as_block_kind_name_tuple(
            mapping.get("forbidden_block_kinds"), field="forbidden_block_kinds"
        )
        return cls(
            min_opening_words=min_opening_words,
            forbidden_block_kinds=forbidden_block_kinds,
        )

    def model_dump(self) -> dict[str, object]:
        dumped: dict[str, object] = {}
        if self.min_opening_words is not None:
            dumped["min_opening_words"] = self.min_opening_words
        if self.forbidden_block_kinds is not None:
            dumped["forbidden_block_kinds"] = self.forbidden_block_kinds
        return dumped


class OpeningSentencePresenceRule(HeuristicSemanticRule):
    options_model = _OpeningSentencePresenceOptions

    metadata = RuleMetadata(
        rule_id="structure.opening_sentence_presence",
        label="Document should open with a purpose sentence before structured blocks",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_opening_words": 8,
            "forbidden_block_kinds": tuple(kind.value for kind in DEFAULT_FORBIDDEN_BLOCK_KINDS),
        },
        evidence_fields=("first_structured_kind",),
    )

    def check(self, doc, ctx):
        min_opening_words = self.settings.int_option("min_opening_words", 8)
        forbidden_block_kinds = resolve_block_kinds(
            self.settings.options.get("forbidden_block_kinds"),
            field="forbidden_block_kinds",
            default=DEFAULT_FORBIDDEN_BLOCK_KINDS,
        )
        if not forbidden_block_kinds:
            return []
        flat_blocks = list(doc.iter_blocks())
        if not flat_blocks:
            return []
        first_structured_index = _first_structured_index(
            flat_blocks, forbidden_block_kinds=forbidden_block_kinds
        )
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
                    "Add one opening sentence stating document purpose before configured structured blocks.",
                ),
            )
        ]


def _first_structured_index(
    blocks,
    *,
    forbidden_block_kinds: frozenset[BlockKind],
) -> int | None:
    for index, block in enumerate(blocks):
        if block.kind in forbidden_block_kinds:
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


def _parse_positive_int(raw: object, *, field: str) -> int | None:
    if raw is None:
        return None
    if isinstance(raw, bool) or not isinstance(raw, int):
        raise ValueError(f"{field} must be an integer")
    if raw < 1:
        raise ValueError(f"{field} must be >= 1")
    return raw


def register(registry) -> None:
    registry.add(OpeningSentencePresenceRule)
