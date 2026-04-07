from __future__ import annotations

from pathlib import Path

from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import BlockKind, MaskedSegmentKind
from hermeneia.document.parser import ParseRequest


def test_markdown_parser_builds_blocks_and_sentence_ids(language_pack) -> None:
    source = """# Intro

Paragraph with $x$.

- item fragment

$$
a=b
$$
"""
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    flat_blocks = [(block.id, block.kind) for block in document.iter_blocks()]
    assert ("b000", BlockKind.HEADING) in flat_blocks
    assert any(kind == BlockKind.LIST for _, kind in flat_blocks)
    assert any(kind == BlockKind.LIST_ITEM for _, kind in flat_blocks)
    assert any(kind == BlockKind.DISPLAY_MATH for _, kind in flat_blocks)
    sentence_ids = [
        sentence.id for block in document.iter_blocks() for sentence in block.sentences
    ]
    assert sentence_ids[:3] == ["s000", "s001", "s002"]
    paragraph_sentence = next(
        sentence
        for block in document.iter_blocks()
        for sentence in block.sentences
        if "$x$" in sentence.source_text
    )
    assert paragraph_sentence.projection.text == "Paragraph with MATHSYM."
    list_sentence = next(
        sentence
        for block in document.iter_blocks()
        for sentence in block.sentences
        if "item fragment" in sentence.source_text
    )
    assert "list_item_fragment" in list_sentence.annotation_flags


def test_markdown_parser_builds_source_line_contexts(language_pack) -> None:
    source = """- item

$$
a=b,
$$
"""
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    list_line = document.source_lines[0]
    assert any(kind.value == "list_item" for kind in list_line.container_kinds)
    display_line = document.source_lines[2]
    assert any(kind.value == "display_math" for kind in display_line.container_kinds)


def test_markdown_parser_emits_link_target_masked_segments(language_pack) -> None:
    source = "See [the docs](https://example.org/reference) now.\n"
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=Path("demo.md"))
    )
    sentence = next(
        sentence
        for block in document.iter_blocks()
        for sentence in block.sentences
        if "the docs" in sentence.source_text
    )
    assert sentence.projection.text == "See the docs now."
    assert any(
        segment.kind == MaskedSegmentKind.LINK_TARGET
        for segment in sentence.projection.masked_segments
    )
