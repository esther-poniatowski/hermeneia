"""Shared helper logic for built-in rules."""

from __future__ import annotations

import re
from typing import Iterable

from hermeneia.document.model import Block, BlockKind, Document, Sentence, SourceLine, Span

WORD_RE = re.compile(r"\b\w+\b")


def iter_sentences(doc: Document) -> Iterable[Sentence]:
    for block in doc.iter_blocks():
        yield from block.sentences


def iter_blocks(doc: Document, kinds: set[BlockKind] | None = None) -> Iterable[Block]:
    for block in doc.iter_blocks():
        if kinds is None or block.kind in kinds:
            yield block


def sentence_word_count(sentence: Sentence) -> int:
    return len(WORD_RE.findall(sentence.projection.text))


def line_text_outside_excluded(line: SourceLine) -> str:
    if not line.excluded_spans:
        return line.text
    chars = list(line.text)
    line_start = line.span.start
    for span in line.excluded_spans:
        start = max(0, span.start - line_start)
        end = min(len(chars), span.end - line_start)
        for index in range(start, end):
            chars[index] = " "
    return "".join(chars)


def match_allowed(
    line: SourceLine,
    pattern: re.Pattern[str],
) -> re.Match[str] | None:
    return pattern.search(line_text_outside_excluded(line))


def block_text(block: Block) -> str:
    return " ".join(sentence.projection.text for sentence in block.sentences)


def upstream_limits(sentence: Sentence) -> tuple[str, ...]:
    return tuple(sorted(flag for flag in sentence.annotation_flags if flag != "table_cell_context"))


def span_from_lines(start_line: SourceLine, end_line: SourceLine | None = None) -> Span:
    if end_line is None:
        end_line = start_line
    return Span(
        start=start_line.span.start,
        end=end_line.span.end,
        start_line=start_line.span.start_line,
        start_column=start_line.span.start_column,
        end_line=end_line.span.end_line,
        end_column=end_line.span.end_column,
    )
