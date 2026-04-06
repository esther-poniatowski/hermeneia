"""Inline source-annotation rendering for text reports."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.document.model import Span
from hermeneia.rules.base import Violation


@dataclass(frozen=True)
class AnnotatedExcerpt:
    line_number: int
    line_text: str
    marker_line: str


def build_excerpt(source: str, span: Span) -> AnnotatedExcerpt:
    lines = source.splitlines()
    line_index = max(0, span.start_line - 1)
    line_text = lines[line_index] if line_index < len(lines) else ""
    start_column = max(1, span.start_column)
    width = max(1, span.end_column - span.start_column)
    marker = " " * (start_column - 1) + "^" * width
    return AnnotatedExcerpt(line_number=span.start_line, line_text=line_text, marker_line=marker)


def annotate_violations(
    source: str, violations: tuple[Violation, ...]
) -> tuple[AnnotatedExcerpt, ...]:
    return tuple(build_excerpt(source, violation.span) for violation in violations)
