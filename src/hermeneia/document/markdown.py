"""Markdown-it-backed parser into the Hermeneia document IR."""

from __future__ import annotations

from dataclasses import dataclass
from itertools import count
import re
from markdown_it import MarkdownIt
from markdown_it.token import Token as MarkdownToken

from hermeneia.document.indexes import DocumentIndexes, build_document_indexes
from hermeneia.document.model import (
    Block,
    BlockKind,
    Document,
    InlineKind,
    InlineNode,
    Sentence,
    Span,
)
from hermeneia.document.parser import DocumentParser, ParseRequest
from hermeneia.document.projection import ProjectionSettings, build_projection
from hermeneia.document.source_view import build_source_lines
from hermeneia.language.base import LanguagePack

INLINE_MATH_RE = re.compile(r"(?<!\\)\$(?!\$)(.+?)(?<!\\)\$")
FOOTNOTE_RE = re.compile(r"^\s*\[\^([^\]]+)\]:\s*")
ADMONITION_RE = re.compile(r"^\s*\[!([A-Z]+)\]\s*$")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z(])")


@dataclass(frozen=True)
class VisibleBuffer:
    text: str
    source_offsets: tuple[int | None, ...]
    special_spans: tuple["InlineSpan", ...]


@dataclass(frozen=True)
class InlineSpan:
    kind: InlineKind
    start: int
    end: int
    span: Span
    text: str


class MarkdownDocumentParser(DocumentParser):
    """Parse markdown into the shared block/inline document IR."""

    def __init__(self, language_pack: LanguagePack) -> None:
        self._language_pack = language_pack
        self._projection_settings = ProjectionSettings(
            heavy_math_masking_ratio=language_pack.preprocessing.heavy_math_masking_ratio,
            symbol_dense_threshold=language_pack.preprocessing.symbol_dense_threshold,
            fragment_token_threshold=language_pack.preprocessing.fragment_token_threshold,
            code_dominant_ratio=language_pack.preprocessing.code_dominant_ratio,
        )
        self._markdown = MarkdownIt("commonmark").enable("table")

    def parse(self, request: ParseRequest) -> Document:
        source = request.source
        line_starts = _line_starts(source)
        tokens = self._markdown.parse(source)
        block_counter = count()
        sentence_counter = count()
        cursor = 0
        roots: list[Block] = []
        stack: list[Block] = []

        while cursor < len(tokens):
            token = tokens[cursor]
            if token.type in {
                "bullet_list_open",
                "ordered_list_open",
                "blockquote_open",
                "table_open",
                "tr_open",
            }:
                block_kind, metadata = _container_kind(token)
                block = Block(
                    id=_block_id(block_counter),
                    kind=block_kind,
                    span=_token_span(token, source, line_starts),
                    metadata=metadata,
                )
                _append_block(roots, stack, block)
                stack.append(block)
                cursor += 1
                continue
            if token.type in {
                "bullet_list_close",
                "ordered_list_close",
                "blockquote_close",
                "table_close",
                "tr_close",
            }:
                if stack:
                    stack.pop()
                cursor += 1
                continue
            if token.type == "list_item_open":
                block = Block(
                    id=_block_id(block_counter),
                    kind=BlockKind.LIST_ITEM,
                    span=_token_span(token, source, line_starts),
                )
                _append_block(roots, stack, block)
                stack.append(block)
                cursor += 1
                continue
            if token.type == "list_item_close":
                if stack:
                    stack.pop()
                cursor += 1
                continue
            if token.type in {"thead_open", "tbody_open"}:
                cursor += 1
                continue
            if token.type in {"thead_close", "tbody_close"}:
                cursor += 1
                continue
            if token.type in {"th_open", "td_open"}:
                block = self._build_table_cell(
                    token=tokens[cursor],
                    inline_token=tokens[cursor + 1],
                    _close_token=tokens[cursor + 2],
                    source=source,
                    line_starts=line_starts,
                    block_counter=block_counter,
                    sentence_counter=sentence_counter,
                )
                _append_block(roots, stack, block)
                cursor += 3
                continue
            if token.type == "heading_open":
                block = self._build_leaf_block(
                    kind=BlockKind.HEADING,
                    open_token=tokens[cursor],
                    inline_token=tokens[cursor + 1],
                    _close_token=tokens[cursor + 2],
                    source=source,
                    line_starts=line_starts,
                    block_counter=block_counter,
                    sentence_counter=sentence_counter,
                    metadata={"level": int(token.tag[1])},
                    container_kinds=tuple(parent.kind for parent in stack),
                )
                _append_block(roots, stack, block)
                cursor += 3
                continue
            if token.type == "paragraph_open":
                block = self._build_leaf_block(
                    kind=BlockKind.PARAGRAPH,
                    open_token=tokens[cursor],
                    inline_token=tokens[cursor + 1],
                    _close_token=tokens[cursor + 2],
                    source=source,
                    line_starts=line_starts,
                    block_counter=block_counter,
                    sentence_counter=sentence_counter,
                    container_kinds=tuple(parent.kind for parent in stack),
                )
                self._normalize_container(block, stack)
                _append_block(roots, stack, block)
                cursor += 3
                continue
            if token.type == "fence":
                block = Block(
                    id=_block_id(block_counter),
                    kind=BlockKind.CODE_BLOCK,
                    span=_token_span(token, source, line_starts),
                    metadata={"info": token.info, "content": token.content},
                )
                _append_block(roots, stack, block)
                cursor += 1
                continue
            cursor += 1

        document = Document(
            blocks=roots,
            source_lines=[],
            indexes=DocumentIndexes(
                sections=[],
                sentences=(),
                math_block_ids=(),
                code_block_ids=(),
                term_first_use={},
                symbol_first_use={},
                support_signals=[],
            ),
            source=source,
            path=request.path,
        )
        document.indexes = build_document_indexes(
            document,
            self._language_pack.lexicons.contrast_markers,
            self._language_pack.lexicons.definitional_markers,
        )
        document.source_lines = build_source_lines(source, roots)
        return document

    def _build_leaf_block(
        self,
        kind: BlockKind,
        open_token: MarkdownToken,
        inline_token: MarkdownToken,
        _close_token: MarkdownToken,
        source: str,
        line_starts: list[int],
        block_counter: count[int],
        sentence_counter: count[int],
        metadata: dict[str, object] | None = None,
        container_kinds: tuple[BlockKind, ...] = (),
    ) -> Block:
        block_span = _token_span(open_token, source, line_starts)
        raw_segment = source[block_span.start : block_span.end]
        buffer = _visible_buffer(
            raw_segment, block_span.start, inline_token, source, line_starts
        )
        block_metadata = dict(metadata or {})
        block_kind = kind

        raw_stripped = raw_segment.strip()
        if kind == BlockKind.PARAGRAPH and _is_display_math(raw_stripped):
            block_kind = BlockKind.DISPLAY_MATH
            block_metadata["content"] = raw_stripped
        elif kind == BlockKind.PARAGRAPH:
            footnote_match = FOOTNOTE_RE.match(buffer.text)
            if footnote_match is not None:
                block_kind = BlockKind.FOOTNOTE
                buffer = _strip_prefix(buffer, footnote_match.end())
                block_metadata["label"] = footnote_match.group(1)

        sentences = (
            []
            if block_kind == BlockKind.DISPLAY_MATH
            else _build_sentences(
                block_kind,
                buffer,
                line_starts,
                sentence_counter,
                self._projection_settings,
                container_kinds=container_kinds,
            )
        )
        inline_nodes = _inline_nodes_from_buffer(buffer, line_starts)
        return Block(
            id=_block_id(block_counter),
            kind=block_kind,
            span=block_span,
            children=[],
            sentences=sentences,
            inline_nodes=inline_nodes,
            metadata=block_metadata,
        )

    def _build_table_cell(
        self,
        token: MarkdownToken,
        inline_token: MarkdownToken,
        _close_token: MarkdownToken,
        source: str,
        line_starts: list[int],
        block_counter: count[int],
        sentence_counter: count[int],
    ) -> Block:
        row_map = inline_token.map or token.map
        line_index = (row_map or [0, 1])[0]
        row_text = source.splitlines(keepends=True)[line_index]
        content = inline_token.content
        start_column = row_text.find(content)
        start_offset = line_starts[line_index] + max(0, start_column)
        buffer = VisibleBuffer(
            text=content,
            source_offsets=tuple(start_offset + index for index in range(len(content))),
            special_spans=(),
        )
        sentences = _build_sentences(
            BlockKind.TABLE_CELL,
            buffer,
            line_starts,
            sentence_counter,
            self._projection_settings,
        )
        inline_nodes = _inline_nodes_from_buffer(buffer, line_starts)
        return Block(
            id=_block_id(block_counter),
            kind=BlockKind.TABLE_CELL,
            span=_token_span(inline_token, source, line_starts),
            sentences=sentences,
            inline_nodes=inline_nodes,
        )

    def _normalize_container(self, block: Block, stack: list[Block]) -> None:
        if not stack:
            return
        parent = stack[-1]
        if parent.kind == BlockKind.BLOCK_QUOTE and block.sentences:
            match = ADMONITION_RE.match(block.sentences[0].source_text.strip())
            if match is not None:
                parent.kind = BlockKind.ADMONITION
                block.sentences = (
                    block.sentences[1:] if len(block.sentences) > 1 else []
                )
                parent.metadata = {"label": match.group(1).lower()}


def _visible_buffer(
    raw_segment: str,
    segment_start: int,
    inline_token: MarkdownToken,
    _source: str,
    line_starts: list[int],
) -> VisibleBuffer:
    children = inline_token.children or []
    if not children:
        source_offsets = tuple(
            segment_start + index for index in range(len(inline_token.content))
        )
        return VisibleBuffer(
            text=inline_token.content, source_offsets=source_offsets, special_spans=()
        )

    output: list[str] = []
    offsets: list[int | None] = []
    special_spans: list[InlineSpan] = []
    cursor = 0
    pending_link_close = False

    for child in children:
        if child.type == "text":
            found = raw_segment.find(child.content, cursor)
            if found < 0:
                found = raw_segment.find(child.content)
            if found < 0:
                found = cursor
            for index, char in enumerate(child.content):
                output.append(char)
                offsets.append(segment_start + found + index)
            cursor = found + len(child.content)
            continue
        if child.type == "softbreak":
            newline = raw_segment.find("\n", cursor)
            output.append(" ")
            offsets.append(None if newline < 0 else segment_start + newline)
            cursor = newline + 1 if newline >= 0 else cursor
            continue
        if child.type == "hardbreak":
            output.append(" ")
            offsets.append(None)
            continue
        if child.type == "code_inline":
            markup = child.markup or "`"
            raw_text = f"{markup}{child.content}{markup}"
            found = raw_segment.find(raw_text, cursor)
            if found < 0:
                found = raw_segment.find(raw_text)
            if found < 0:
                found = cursor
            start = len(output)
            for index, char in enumerate(raw_text):
                output.append(char)
                offsets.append(segment_start + found + index)
            cursor = found + len(raw_text)
            special_spans.append(
                InlineSpan(
                    kind=InlineKind.INLINE_CODE,
                    start=start,
                    end=len(output),
                    span=_span_from_offsets(
                        segment_start + found,
                        segment_start + found + len(raw_text),
                        line_starts,
                    ),
                    text=raw_text,
                )
            )
            continue
        if child.type == "link_open":
            pending_link_close = True
            continue
        if child.type == "link_close" and pending_link_close:
            open_paren = raw_segment.find("(", cursor)
            closing = raw_segment.find(")", open_paren if open_paren >= 0 else cursor)
            if open_paren >= 0:
                if closing > open_paren:
                    target_start = segment_start + open_paren + 1
                    target_end = segment_start + closing
                    special_spans.append(
                        InlineSpan(
                            kind=InlineKind.LINK_TARGET,
                            start=len(output),
                            end=len(output),
                            span=_span_from_offsets(
                                target_start, target_end, line_starts
                            ),
                            text=raw_segment[open_paren + 1 : closing],
                        )
                    )
            cursor = closing + 1 if closing >= 0 else cursor
            pending_link_close = False
            continue

    buffer = VisibleBuffer(
        text="".join(output),
        source_offsets=tuple(offsets),
        special_spans=tuple(special_spans),
    )
    return _inject_math_spans(buffer, line_starts)


def _inject_math_spans(buffer: VisibleBuffer, line_starts: list[int]) -> VisibleBuffer:
    special_spans = list(buffer.special_spans)
    for match in INLINE_MATH_RE.finditer(buffer.text):
        if any(
            span.start <= match.start() < span.end
            for span in special_spans
            if span.kind == InlineKind.INLINE_CODE
        ):
            continue
        source_start = buffer.source_offsets[match.start()]
        source_end = buffer.source_offsets[match.end() - 1]
        if source_start is None or source_end is None:
            continue
        special_spans.append(
            InlineSpan(
                kind=InlineKind.INLINE_MATH,
                start=match.start(),
                end=match.end(),
                span=_span_from_offsets(source_start, source_end + 1, line_starts),
                text=match.group(0),
            )
        )
    special_spans.sort(key=lambda span: span.start)
    return VisibleBuffer(
        text=buffer.text,
        source_offsets=buffer.source_offsets,
        special_spans=tuple(special_spans),
    )


def _inline_nodes_from_buffer(
    buffer: VisibleBuffer, line_starts: list[int]
) -> list[InlineNode]:
    return _inline_nodes_for_range(buffer, 0, len(buffer.text), line_starts)


def _inline_nodes_for_range(
    buffer: VisibleBuffer,
    start: int,
    end: int,
    line_starts: list[int],
) -> list[InlineNode]:
    nodes: list[InlineNode] = []
    cursor = start
    for span in buffer.special_spans:
        if span.start == span.end:
            if span.start < start or span.start > end:
                continue
        elif span.end <= start or span.start >= end:
            continue
        if cursor < span.start:
            nodes.append(_text_node(buffer, cursor, span.start, line_starts))
        nodes.append(InlineNode(kind=span.kind, text=span.text, span=span.span))
        cursor = span.end
    if cursor < end:
        nodes.append(_text_node(buffer, cursor, end, line_starts))
    return [node for node in nodes if node.text]


def _text_node(
    buffer: VisibleBuffer, start: int, end: int, line_starts: list[int]
) -> InlineNode:
    source_start = next(
        (offset for offset in buffer.source_offsets[start:end] if offset is not None),
        None,
    )
    source_end = next(
        (
            offset
            for offset in reversed(buffer.source_offsets[start:end])
            if offset is not None
        ),
        None,
    )
    if source_start is None or source_end is None:
        span = Span(0, 0, 1, 1, 1, 1)
    else:
        span = _span_from_offsets(source_start, source_end + 1, line_starts)
    return InlineNode(kind=InlineKind.TEXT, text=buffer.text[start:end], span=span)


def _build_sentences(
    block_kind: BlockKind,
    buffer: VisibleBuffer,
    line_starts: list[int],
    sentence_counter: count[int],
    projection_settings: ProjectionSettings,
    container_kinds: tuple[BlockKind, ...] = (),
) -> list[Sentence]:
    segments = _segment_ranges(block_kind, buffer.text)
    sentences: list[Sentence] = []
    for start, end, extra_flags in segments:
        segment_text = buffer.text[start:end].strip()
        if not segment_text:
            continue
        trimmed_start = (
            start + len(buffer.text[start:end]) - len(buffer.text[start:end].lstrip())
        )
        trimmed_end = (
            end - len(buffer.text[start:end]) + len(buffer.text[start:end].rstrip())
        )
        source_start = next(
            (
                offset
                for offset in buffer.source_offsets[trimmed_start:trimmed_end]
                if offset is not None
            ),
            None,
        )
        source_end = next(
            (
                offset
                for offset in reversed(buffer.source_offsets[trimmed_start:trimmed_end])
                if offset is not None
            ),
            None,
        )
        if source_start is None or source_end is None:
            continue
        span = _span_from_offsets(source_start, source_end + 1, line_starts)
        inline_nodes = _inline_nodes_for_range(
            buffer, trimmed_start, trimmed_end, line_starts
        )
        projection_result = build_projection(
            text=buffer.text[trimmed_start:trimmed_end],
            source_offsets=buffer.source_offsets[trimmed_start:trimmed_end],
            inline_nodes=inline_nodes,
            settings=projection_settings,
        )
        flags = set(projection_result.flags)
        flags.update(extra_flags)
        if BlockKind.LIST_ITEM in container_kinds and "fragment_sentence" in flags:
            flags.add("list_item_fragment")
        if block_kind == BlockKind.TABLE_CELL:
            flags.add("table_cell_context")
        sentences.append(
            Sentence(
                id=_sentence_id(sentence_counter),
                source_text=buffer.text[trimmed_start:trimmed_end],
                span=span,
                inline_nodes=inline_nodes,
                projection=projection_result.projection,
                annotation_flags=frozenset(flags),
            )
        )
    return sentences


def _segment_ranges(
    block_kind: BlockKind, text: str
) -> list[tuple[int, int, set[str]]]:
    stripped = text.strip()
    if not stripped:
        return []
    if block_kind == BlockKind.HEADING:
        return [(0, len(text), set())]
    if block_kind in {BlockKind.LIST_ITEM, BlockKind.TABLE_CELL} and not re.search(
        r"[.!?]\s*$", stripped
    ):
        extra = {"list_item_fragment"} if block_kind == BlockKind.LIST_ITEM else set()
        return [(0, len(text), extra)]

    segments: list[tuple[int, int, set[str]]] = []
    cursor = 0
    for match in SENTENCE_SPLIT_RE.finditer(text):
        segments.append((cursor, match.start(), set()))
        cursor = match.end()
    segments.append((cursor, len(text), set()))
    return segments


def _append_block(roots: list[Block], stack: list[Block], block: Block) -> None:
    if stack:
        stack[-1].children.append(block)
    else:
        roots.append(block)


def _container_kind(token: MarkdownToken) -> tuple[BlockKind, dict[str, object]]:
    if token.type in {"bullet_list_open", "ordered_list_open"}:
        return BlockKind.LIST, {"ordered": token.type == "ordered_list_open"}
    if token.type == "blockquote_open":
        return BlockKind.BLOCK_QUOTE, {}
    if token.type == "table_open":
        return BlockKind.TABLE, {}
    if token.type == "tr_open":
        return BlockKind.TABLE_ROW, {}
    raise ValueError(f"Unsupported container token {token.type}")


def _is_display_math(text: str) -> bool:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return len(lines) >= 2 and lines[0] == "$$" and lines[-1] == "$$"


def _strip_prefix(buffer: VisibleBuffer, character_count: int) -> VisibleBuffer:
    return VisibleBuffer(
        text=buffer.text[character_count:],
        source_offsets=buffer.source_offsets[character_count:],
        special_spans=tuple(
            InlineSpan(
                kind=span.kind,
                start=span.start - character_count,
                end=span.end - character_count,
                span=span.span,
                text=span.text,
            )
            for span in buffer.special_spans
            if span.end > character_count
        ),
    )


def _block_id(counter: count[int]) -> str:
    return f"b{next(counter):03d}"


def _sentence_id(counter: count[int]) -> str:
    return f"s{next(counter):03d}"


def _token_span(token: MarkdownToken, source: str, line_starts: list[int]) -> Span:
    line_map = token.map or [0, 1]
    start_line = line_map[0]
    end_line = max(start_line + 1, line_map[1])
    start = line_starts[start_line]
    end = line_starts[end_line] if end_line < len(line_starts) else len(source)
    end_line_number = source.count("\n", 0, end) + 1 if source else 1
    end_column = (
        end
        - (
            line_starts[end_line_number - 1]
            if end_line_number - 1 < len(line_starts)
            else 0
        )
        + 1
    )
    return Span(
        start=start,
        end=end,
        start_line=start_line + 1,
        start_column=1,
        end_line=end_line_number,
        end_column=end_column,
    )


def _span_from_offsets(start: int, end: int, line_starts: list[int]) -> Span:
    start_line, start_column = _line_col(start, line_starts)
    end_line, end_column = _line_col(end, line_starts)
    return Span(
        start=start,
        end=end,
        start_line=start_line,
        start_column=start_column,
        end_line=end_line,
        end_column=end_column,
    )


def _line_col(offset: int, line_starts: list[int]) -> tuple[int, int]:
    line_index = 0
    for index, start in enumerate(line_starts):
        if start > offset:
            break
        line_index = index
    return line_index + 1, offset - line_starts[line_index] + 1


def _line_starts(source: str) -> list[int]:
    starts = [0]
    for index, char in enumerate(source):
        if char == "\n":
            starts.append(index + 1)
    return starts
