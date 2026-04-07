from __future__ import annotations

from hermeneia.document.model import Span
from hermeneia.report.annotations import build_excerpt


def test_build_excerpt_single_line_marker() -> None:
    source = "alpha beta gamma\n"
    span = Span(
        start=6,
        end=10,
        start_line=1,
        start_column=7,
        end_line=1,
        end_column=11,
    )
    excerpt = build_excerpt(source, span)
    assert len(excerpt.lines) == 1
    row = excerpt.lines[0]
    assert row.line_number == 1
    assert row.line_text == "alpha beta gamma"
    assert row.marker_line == "      ^^^^"


def test_build_excerpt_multi_line_marker_preserves_each_line_segment() -> None:
    source = "first line\nsecond line\nthird line\n"
    span = Span(
        start=6,
        end=26,
        start_line=1,
        start_column=7,
        end_line=3,
        end_column=6,
    )
    excerpt = build_excerpt(source, span)
    assert [row.line_number for row in excerpt.lines] == [1, 2, 3]
    assert excerpt.lines[0].line_text == "first line"
    assert excerpt.lines[0].marker_line == "      ^^^^"
    assert excerpt.lines[1].line_text == "second line"
    assert excerpt.lines[1].marker_line == "^^^^^^^^^^^"
    assert excerpt.lines[2].line_text == "third line"
    assert excerpt.lines[2].marker_line == "^^^^^"
