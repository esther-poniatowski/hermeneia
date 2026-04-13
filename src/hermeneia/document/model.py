"""Pure document-domain models for Hermeneia.

Classes
-------
Span
    Public API symbol.
MaskedSegmentKind
    Public API symbol.
MaskedSegment
    Public API symbol.
TextProjection
    Public API symbol.
Token
    Public API symbol.
BlockKind
    Public API symbol.
InlineKind
    Public API symbol.
InlineNode
    Public API symbol.
Sentence
    Public API symbol.
Block
    Public API symbol.
SourceLine
    Public API symbol.
Document
    Public API symbol.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable, Mapping

if TYPE_CHECKING:
    from hermeneia.document.indexes import DocumentIndexes


@dataclass(frozen=True)
class Span:
    """Absolute and line-local coordinates for a source region."""

    start: int
    end: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int

    def contains_offset(self, offset: int) -> bool:
        """Return whether the span contains the offset.

        Parameters
        ----------
        offset : int
            Input value for ``offset``.

        Returns
        -------
        bool
            Resulting value produced by this call.
        """
        return self.start <= offset < self.end

    def overlaps(self, other: "Span") -> bool:
        """Overlaps.

        Parameters
        ----------
        other : Span
            Input value for ``other``.

        Returns
        -------
        bool
            Resulting value produced by this call.
        """
        return self.start < other.end and other.start < self.end

    def line_tuple(self) -> tuple[int, int]:
        """Line tuple.

        Returns
        -------
        tuple[int, int]
            Resulting value produced by this call.
        """
        return self.start_line, self.end_line


class MaskedSegmentKind(StrEnum):
    """Kinds of segments masked during text projection."""

    INLINE_MATH = "inline_math"
    INLINE_CODE = "inline_code"
    LINK_TARGET = "link_target"


@dataclass(frozen=True)
class MaskedSegment:
    """A source segment replaced or suppressed during NLP projection."""

    kind: MaskedSegmentKind
    source_span: Span
    placeholder: str


@dataclass(frozen=True)
class TextProjection:
    """Text sent to the annotator plus a character map back to source offsets."""

    text: str
    normalized_to_source: tuple[int | None, ...]
    masked_segments: tuple[MaskedSegment, ...] = ()

    def source_offset_for(self, projection_offset: int) -> int | None:
        """Source offset for.

        Parameters
        ----------
        projection_offset : int
            Input value for ``projection_offset``.

        Returns
        -------
        int | None
            Resulting value produced by this call.
        """
        if projection_offset < 0 or projection_offset >= len(self.normalized_to_source):
            return None
        return self.normalized_to_source[projection_offset]


@dataclass
class Token:
    """Annotated token aligned to both source and projection offsets."""

    text: str
    lemma: str
    pos: str | None
    dep: str | None
    head_idx: int | None
    source_span: Span
    projection_start: int
    projection_end: int


class BlockKind(StrEnum):
    """Kinds of block-level nodes in the document IR."""

    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    LIST_ITEM = "list_item"
    BLOCK_QUOTE = "block_quote"
    TABLE = "table"
    TABLE_ROW = "table_row"
    TABLE_CELL = "table_cell"
    CODE_BLOCK = "code_block"
    DISPLAY_MATH = "display_math"
    FOOTNOTE = "footnote"
    ADMONITION = "admonition"


class InlineKind(StrEnum):
    """Kinds of inline nodes captured in the document IR."""

    TEXT = "text"
    INLINE_MATH = "inline_math"
    INLINE_CODE = "inline_code"
    LINK_TARGET = "link_target"


@dataclass
class InlineNode:
    """A source-aligned inline fragment embedded in a prose block."""

    kind: InlineKind
    text: str
    span: Span


@dataclass
class Sentence:
    """A sentence or sentence-fragment extracted from an annotatable block."""

    id: str
    source_text: str
    span: Span
    inline_nodes: list[InlineNode]
    projection: TextProjection
    tokens: list[Token] = field(default_factory=list)
    annotation_flags: frozenset[str] = frozenset()

    def token_text(self) -> str:
        """Token text.

        Returns
        -------
        str
            Resulting value produced by this call.
        """
        return " ".join(token.text for token in self.tokens)


@dataclass
class Block:
    """A block-level node in the canonical document IR."""

    id: str
    kind: BlockKind
    span: Span
    children: list["Block"] = field(default_factory=list)
    sentences: list[Sentence] = field(default_factory=list)
    inline_nodes: list[InlineNode] = field(default_factory=list)
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def iter_blocks(self) -> Iterable["Block"]:
        """Iter blocks.

        Yields
        ------
        Iterable[Block]
            Items yielded by this iterator.
        """
        yield self
        for child in self.children:
            yield from child.iter_blocks()


@dataclass(frozen=True)
class SourceLine:
    """A raw source line tagged with parser-derived structural context."""

    text: str
    span: Span
    block_id: str | None
    container_kinds: tuple[BlockKind, ...]
    excluded_spans: tuple[Span, ...] = ()


@dataclass
class Document:
    """Canonical source-of-truth document representation."""

    blocks: list[Block]
    source_lines: list[SourceLine]
    indexes: "DocumentIndexes"
    source: str
    path: Path | None = None

    def iter_blocks(self) -> Iterable[Block]:
        """Iter blocks.

        Yields
        ------
        Iterable[Block]
            Items yielded by this iterator.
        """
        for block in self.blocks:
            yield from block.iter_blocks()

    def block_by_id(self, block_id: str) -> Block | None:
        """Block by id.

        Parameters
        ----------
        block_id : str
            Input value for ``block_id``.

        Returns
        -------
        Block | None
            Resulting value produced by this call.
        """
        for block in self.iter_blocks():
            if block.id == block_id:
                return block
        return None

    def sentence_by_id(self, sentence_id: str) -> Sentence | None:
        """Sentence by id.

        Parameters
        ----------
        sentence_id : str
            Input value for ``sentence_id``.

        Returns
        -------
        Sentence | None
            Resulting value produced by this call.
        """
        for block in self.iter_blocks():
            for sentence in block.sentences:
                if sentence.id == sentence_id:
                    return sentence
        return None

    def prose_blocks(self) -> Iterable[Block]:
        """Prose blocks.

        Yields
        ------
        Iterable[Block]
            Items yielded by this iterator.
        """
        annotatable = {
            BlockKind.HEADING,
            BlockKind.PARAGRAPH,
            BlockKind.LIST_ITEM,
            BlockKind.TABLE_CELL,
            BlockKind.BLOCK_QUOTE,
            BlockKind.ADMONITION,
            BlockKind.FOOTNOTE,
        }
        for block in self.iter_blocks():
            if block.kind in annotatable:
                yield block
