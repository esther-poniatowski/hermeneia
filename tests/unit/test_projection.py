from __future__ import annotations

from hermeneia.document.model import InlineKind, InlineNode, Span
from hermeneia.document.projection import ProjectionSettings, build_projection


def test_build_projection_preserves_offsets_and_placeholders() -> None:
    text = "Let $x$ be `foo`."
    offsets = tuple(range(len(text)))
    projection = build_projection(
        text=text,
        source_offsets=offsets,
        inline_nodes=[
            InlineNode(InlineKind.INLINE_MATH, "$x$", Span(4, 7, 1, 5, 1, 8)),
            InlineNode(InlineKind.INLINE_CODE, "`foo`", Span(11, 16, 1, 12, 1, 17)),
        ],
        settings=ProjectionSettings(),
    )
    assert projection.projection.text == "Let MATHSYM be CODEID."
    assert len(projection.projection.masked_segments) == 2
    assert projection.flags == frozenset()


def test_build_projection_sets_masking_flags() -> None:
    text = "$x$ $y$ $z$ $w$"
    offsets = tuple(range(len(text)))
    nodes = [
        InlineNode(InlineKind.INLINE_MATH, "$x$", Span(0, 3, 1, 1, 1, 4)),
        InlineNode(InlineKind.INLINE_MATH, "$y$", Span(4, 7, 1, 5, 1, 8)),
        InlineNode(InlineKind.INLINE_MATH, "$z$", Span(8, 11, 1, 9, 1, 12)),
        InlineNode(InlineKind.INLINE_MATH, "$w$", Span(12, 15, 1, 13, 1, 16)),
    ]
    projection = build_projection(
        text=text, source_offsets=offsets, inline_nodes=nodes, settings=ProjectionSettings()
    )
    assert "heavy_math_masking" in projection.flags
    assert "symbol_dense_sentence" in projection.flags
