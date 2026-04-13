"""Inline source-annotation rendering for text reports."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.document.model import Span
from hermeneia.rules.base import Violation


@dataclass(frozen=True)
class AnnotatedLine:
    """Annotatedline."""

    line_number: int
    line_text: str
    marker_line: str


@dataclass(frozen=True)
class AnnotatedExcerpt:
    """Annotatedexcerpt."""

    lines: tuple[AnnotatedLine, ...]


def build_excerpt(source: str, span: Span) -> AnnotatedExcerpt:
    """Build excerpt.

    Parameters
    ----------
    source : str
        Source text to parse or analyze.
    span : Span
        Input value for ``span``.

    Returns
    -------
    AnnotatedExcerpt
        Resulting value produced by this call.
    """
    source_lines = source.splitlines()
    start_line = max(1, span.start_line)
    end_line = max(start_line, span.end_line)
    annotated: list[AnnotatedLine] = []

    for line_number in range(start_line, end_line + 1):
        line_index = line_number - 1
        line_text = source_lines[line_index] if line_index < len(source_lines) else ""
        marker = _build_line_marker(
            line_text=line_text,
            line_number=line_number,
            start_line=start_line,
            end_line=end_line,
            start_column=span.start_column,
            end_column=span.end_column,
        )
        annotated.append(
            AnnotatedLine(
                line_number=line_number,
                line_text=line_text,
                marker_line=marker,
            )
        )
    return AnnotatedExcerpt(lines=tuple(annotated))


def annotate_violations(
    source: str, violations: tuple[Violation, ...]
) -> tuple[AnnotatedExcerpt, ...]:
    """Annotate violations.

    Parameters
    ----------
    source : str
        Source text to parse or analyze.
    violations : tuple[Violation, ...]
        Input value for ``violations``.

    Returns
    -------
    tuple[AnnotatedExcerpt, ...]
        Resulting value produced by this call.
    """
    return tuple(build_excerpt(source, violation.span) for violation in violations)


def _build_line_marker(
    line_text: str,
    line_number: int,
    start_line: int,
    end_line: int,
    start_column: int,
    end_column: int,
) -> str:
    """Build line marker."""
    line_length = len(line_text)
    if line_number == start_line:
        marker_start = _clamp_column(start_column, line_length)
    else:
        marker_start = 1

    if line_number == end_line:
        marker_end = _clamp_column(end_column, line_length)
    else:
        marker_end = line_length + 1

    marker_end = max(marker_end, marker_start)
    width = max(1, marker_end - marker_start)
    return " " * (marker_start - 1) + "^" * width


def _clamp_column(column: int, line_length: int) -> int:
    """Clamp column."""
    return min(max(1, column), line_length + 1)
