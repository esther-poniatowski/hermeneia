"""Source-view construction for SourcePatternRule consumers."""

from __future__ import annotations

from collections import defaultdict

from hermeneia.document.model import Block, Document, InlineKind, SourceLine, Span


def build_source_lines(source: str, blocks: list[Block]) -> list[SourceLine]:
    """Build line-oriented source views tagged with parser-derived context.

    Parameters
    ----------
    source : str
        Source text to parse or analyze.
    blocks : list[Block]
        Input value for ``blocks``.

    Returns
    -------
    list[SourceLine]
        Resulting value produced by this call.
    """

    lines = source.splitlines(keepends=True)
    line_starts: list[int] = []
    offset = 0
    for line in lines:
        line_starts.append(offset)
        offset += len(line)

    line_contexts: dict[int, list[Block]] = defaultdict(list)
    excluded_by_line: dict[int, list[Span]] = defaultdict(list)
    for block in blocks:
        for nested in block.iter_blocks():
            for line_index in range(nested.span.start_line - 1, nested.span.end_line):
                line_contexts[line_index].append(nested)
            for inline in nested.inline_nodes:
                if inline.kind in {
                    InlineKind.INLINE_CODE,
                    InlineKind.INLINE_MATH,
                    InlineKind.LINK_TARGET,
                }:
                    excluded_by_line[inline.span.start_line - 1].append(inline.span)

    source_lines: list[SourceLine] = []
    for index, raw_line in enumerate(lines):
        line_start = line_starts[index]
        line_end = line_start + len(raw_line)
        contexts = sorted(
            line_contexts.get(index, []),
            key=lambda block: (block.span.start, block.span.end),
        )
        block_id = contexts[-1].id if contexts else None
        container_kinds = tuple(block.kind for block in contexts)
        source_lines.append(
            SourceLine(
                text=raw_line.rstrip("\n"),
                span=Span(
                    start=line_start,
                    end=line_end,
                    start_line=index + 1,
                    start_column=1,
                    end_line=index + 1,
                    end_column=max(1, len(raw_line.rstrip("\n")) + 1),
                ),
                block_id=block_id,
                container_kinds=container_kinds,
                excluded_spans=tuple(excluded_by_line.get(index, ())),
            )
        )
    return source_lines


def rebind_source_view(doc: Document) -> Document:
    """Return the document with its source-line view rebuilt from current blocks.

    Parameters
    ----------
    doc : Document
        Document instance to inspect.

    Returns
    -------
    Document
        Resulting value produced by this call.
    """

    doc.source_lines = build_source_lines(doc.source, doc.blocks)
    return doc
