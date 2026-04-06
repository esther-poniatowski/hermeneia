"""Projection building and offset reconciliation for prose annotation."""

from __future__ import annotations

from dataclasses import dataclass
import re

from hermeneia.document.model import InlineKind, InlineNode, MaskedSegment, Span, TextProjection

MATH_SYMBOL_RE = re.compile(r"^[A-Za-z][A-Za-z0-9']*$")
MATH_NUMERIC_RE = re.compile(
    r"^(?:[+-]?\d+(?:\.\d+)?|[A-Za-z]\s*[+\-*/^]\s*\d+|[A-Za-z0-9+\-*/^() ]{1,10})$"
)
WORD_RE = re.compile(r"\b\w+\b")


@dataclass(frozen=True)
class ProjectionSettings:
    heavy_math_masking_ratio: float = 0.4
    symbol_dense_threshold: int = 4
    fragment_token_threshold: int = 4
    code_dominant_ratio: float = 0.5


@dataclass(frozen=True)
class ProjectionResult:
    projection: TextProjection
    flags: frozenset[str]


def classify_math_placeholder(raw_text: str) -> str:
    """Return the placeholder that best approximates the masked math slot."""

    content = raw_text.strip()
    if content.startswith("$") and content.endswith("$"):
        content = content[1:-1].strip()
    if MATH_SYMBOL_RE.fullmatch(content):
        return "MATHSYM"
    if MATH_NUMERIC_RE.fullmatch(content):
        return "MATHNUM"
    return "MATHEXPR"


def build_projection(
    text: str,
    source_offsets: tuple[int | None, ...],
    inline_nodes: list[InlineNode],
    settings: ProjectionSettings,
) -> ProjectionResult:
    """Build a normalized projection and populate reliability flags."""

    if len(text) != len(source_offsets):
        raise ValueError("Projection text and source-offset map must have the same length")

    masked_segments: list[MaskedSegment] = []
    normalized_chars: list[str] = []
    normalized_to_source: list[int | None] = []
    cursor = 0
    ordered_nodes = sorted(inline_nodes, key=lambda node: node.span.start)

    def append_literal(segment: str, offsets: tuple[int | None, ...]) -> None:
        normalized_chars.extend(segment)
        normalized_to_source.extend(offsets)

    math_masked_chars = 0
    code_masked_chars = 0
    math_segment_count = 0

    for node in ordered_nodes:
        node_start = _relative_start(node.span.start, source_offsets)
        node_end = _relative_end(node.span.end, source_offsets)
        if node_start is None or node_end is None or node_end <= node_start:
            continue
        if node_start > cursor:
            append_literal(text[cursor:node_start], source_offsets[cursor:node_start])

        if node.kind == InlineKind.TEXT:
            append_literal(text[node_start:node_end], source_offsets[node_start:node_end])
        else:
            placeholder = (
                "CODEID"
                if node.kind == InlineKind.INLINE_CODE
                else classify_math_placeholder(node.text)
            )
            if (
                normalized_chars
                and not normalized_chars[-1].isspace()
                and normalized_chars[-1] not in "([{"
            ):
                normalized_chars.append(" ")
                normalized_to_source.append(source_offsets[node_start])
            normalized_chars.extend(placeholder)
            normalized_to_source.extend([source_offsets[node_start]] * len(placeholder))
            next_char = text[node_end : node_end + 1]
            if next_char and not next_char.isspace() and next_char not in ".,;:!?)]}":
                normalized_chars.append(" ")
                normalized_to_source.append(source_offsets[node_end - 1])
            masked_segments.append(
                MaskedSegment(
                    kind="inline_code" if node.kind == InlineKind.INLINE_CODE else "inline_math",
                    source_span=node.span,
                    placeholder=placeholder,
                )
            )
            if node.kind == InlineKind.INLINE_CODE:
                code_masked_chars += node_end - node_start
            else:
                math_masked_chars += node_end - node_start
                math_segment_count += 1
        cursor = node_end

    if cursor < len(text):
        append_literal(text[cursor:], source_offsets[cursor:])

    projection_text = _normalize_whitespace("".join(normalized_chars))
    normalized_map = _normalize_map(
        tuple(normalized_to_source), "".join(normalized_chars), projection_text
    )

    flags: set[str] = set()
    total_chars = max(1, len(text))
    if math_masked_chars / total_chars > settings.heavy_math_masking_ratio:
        flags.add("heavy_math_masking")
    if math_segment_count >= settings.symbol_dense_threshold:
        flags.add("symbol_dense_sentence")
    if code_masked_chars / total_chars > settings.code_dominant_ratio:
        flags.add("code_dominant")
    if len(WORD_RE.findall(projection_text)) < settings.fragment_token_threshold:
        flags.add("fragment_sentence")

    return ProjectionResult(
        projection=TextProjection(
            text=projection_text,
            normalized_to_source=normalized_map,
            masked_segments=tuple(masked_segments),
        ),
        flags=frozenset(flags),
    )


def _relative_start(source_start: int, offsets: tuple[int | None, ...]) -> int | None:
    for index, offset in enumerate(offsets):
        if offset == source_start:
            return index
    return None


def _relative_end(source_end: int, offsets: tuple[int | None, ...]) -> int | None:
    for index in range(len(offsets) - 1, -1, -1):
        offset = offsets[index]
        if offset is not None and offset < source_end:
            return index + 1
    return None


def _normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _normalize_map(
    raw_map: tuple[int | None, ...],
    raw_text: str,
    normalized_text: str,
) -> tuple[int | None, ...]:
    if raw_text == normalized_text:
        return raw_map
    result: list[int | None] = []
    raw_index = 0
    for char in normalized_text:
        while raw_index < len(raw_text) and raw_text[raw_index].isspace() and char != " ":
            raw_index += 1
        if raw_index < len(raw_text):
            result.append(raw_map[raw_index])
            raw_index += 1
        else:
            result.append(None)
    return tuple(result)
