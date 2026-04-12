"""Shared helper logic for built-in rules."""

from __future__ import annotations

import re
from typing import Iterable, Sequence

from hermeneia.document.model import (
    Block,
    BlockKind,
    Document,
    Sentence,
    SourceLine,
    Span,
)

WORD_RE = re.compile(r"\b\w+\b")


def iter_sentences(doc: Document) -> Iterable[Sentence]:
    """Iter sentences."""
    for block in doc.iter_blocks():
        yield from block.sentences


def iter_blocks(doc: Document, kinds: set[BlockKind] | None = None) -> Iterable[Block]:
    """Iter blocks."""
    for block in doc.iter_blocks():
        if kinds is None or block.kind in kinds:
            yield block


def sentence_word_count(sentence: Sentence) -> int:
    """Sentence word count."""
    return len(WORD_RE.findall(sentence.projection.text))


def sentence_lemmas(sentence: Sentence) -> set[str]:
    """Sentence lemmas."""
    if sentence.tokens:
        lemmas = {
            token.lemma.lower()
            for token in sentence.tokens
            if token.lemma and token.lemma.isalpha()
        }
        if lemmas:
            return lemmas
    return {
        match.group(0).lower() for match in WORD_RE.finditer(sentence.projection.text)
    }


def matched_sentence_markers(
    sentence: Sentence,
    markers: Iterable[str],
) -> tuple[str, ...]:
    """Matched sentence markers."""
    normalized: list[str] = []
    seen: set[str] = set()
    for marker in markers:
        value = marker.strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    if not normalized:
        return ()
    lower_text = sentence.projection.text.lower()
    lemmas = sentence_lemmas(sentence)
    matches: list[str] = []
    seen_matches: set[str] = set()
    for marker in normalized:
        if " " in marker and marker in lower_text:
            if marker not in seen_matches:
                seen_matches.add(marker)
                matches.append(marker)
            continue
        if marker in lemmas and sentence.tokens:
            token_match = next(
                (
                    token.text.lower()
                    for token in sentence.tokens
                    if token.lemma and token.lemma.lower() == marker and token.text
                ),
                marker,
            )
            if token_match not in seen_matches:
                seen_matches.add(token_match)
                matches.append(token_match)
            continue
        if re.search(rf"\b{re.escape(marker)}\b", lower_text):
            if marker not in seen_matches:
                seen_matches.add(marker)
                matches.append(marker)
    return tuple(matches)


def sentence_has_marker(sentence: Sentence, markers: Iterable[str]) -> bool:
    """Sentence has marker."""
    return bool(matched_sentence_markers(sentence, markers))


def text_has_marker(text: str, markers: Iterable[str]) -> bool:
    """Text has marker."""
    normalized = text.lower()
    for marker in markers:
        value = marker.strip().lower()
        if not value:
            continue
        if " " in value:
            if value in normalized:
                return True
            continue
        if re.search(rf"\b{re.escape(value)}\b", normalized):
            return True
    return False


def line_text_outside_excluded(line: SourceLine) -> str:
    """Line text outside excluded."""
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
    """Match allowed."""
    return pattern.search(line_text_outside_excluded(line))


def block_text(block: Block) -> str:
    """Block text."""
    return " ".join(sentence.projection.text for sentence in block.sentences)


def previous_prose_block(blocks: Sequence[Block], before_index: int) -> Block | None:
    """Previous prose block."""
    prose_kinds = {BlockKind.PARAGRAPH, BlockKind.BLOCK_QUOTE, BlockKind.LIST_ITEM}
    for offset in range(before_index - 1, -1, -1):
        candidate = blocks[offset]
        if candidate.kind in prose_kinds:
            return candidate
        if candidate.kind == BlockKind.HEADING:
            return None
    return None


def upstream_limits(sentence: Sentence) -> tuple[str, ...]:
    """Upstream limits."""
    return tuple(
        sorted(
            flag for flag in sentence.annotation_flags if flag != "table_cell_context"
        )
    )


def span_from_lines(start_line: SourceLine, end_line: SourceLine | None = None) -> Span:
    """Span from lines."""
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
