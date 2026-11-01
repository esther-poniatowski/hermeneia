from __future__ import annotations

import dataclasses
from pathlib import Path

import pytest

from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import BlockKind, Document, SourceKind, Span
from hermeneia.document.parser import ParseRequest
from hermeneia.report.sarif import (
    artifact_uri,
    digest,
    discriminator,
    logical_name,
    normalize,
    region,
    relative_path,
)
from hermeneia.rules.base import Layer, RuleEvidence, Severity, Violation

SOURCE = """# Heading

The first sentence states a claim. The second sentence  refines
it with a kind of detail.

```python
x = 1
```
"""


@pytest.fixture
def document(language_pack) -> Document:
    return MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=SOURCE, path=Path("demo.md"))
    )


def _sentences(document: Document):
    """Return the sentences of the paragraph; the heading holds a sentence of its own."""
    return [
        sentence
        for block in document.iter_blocks()
        for sentence in block.sentences
        if block.kind == BlockKind.PARAGRAPH
    ]


def _violation(span: Span, evidence: RuleEvidence | None = None) -> Violation:
    return Violation(
        rule_id="demo.rule",
        message="demo",
        span=span,
        severity=Severity.WARNING,
        layer=Layer.SURFACE_STYLE,
        evidence=evidence,
    )


def _span(document: Document, start: int, end: int) -> Span:
    return dataclasses.replace(document.blocks[0].span, start=start, end=end)


def test_normalize_collapses_whitespace_and_composes() -> None:
    assert normalize("  éte\n\t done ") == "éte done"
    assert digest("a  b") == digest("a b")
    assert digest("a b").startswith("sha256:") and len(digest("a b")) == 23


def test_a_sentence_violation_takes_the_sentence(document) -> None:
    second = _sentences(document)[1]
    assert discriminator(document, _violation(second.span)) == (
        "The second sentence refines it with a kind of detail."
    )


def test_a_partial_violation_takes_the_match_then_the_sentence(document) -> None:
    start = SOURCE.index("kind of")
    found = discriminator(document, _violation(_span(document, start, start + len("kind of"))))
    assert found == "[kind of] The second sentence refines it with a kind of detail."


def test_a_pair_violation_takes_the_digest_of_both_sentences(document) -> None:
    first, second = _sentences(document)[:2]
    evidence = RuleEvidence(features={"previous_sentence_id": first.id})
    found = discriminator(document, _violation(second.span, evidence))
    assert found == digest(
        "The first sentence states a claim. The second sentence refines it with a kind of detail."
    )


def test_a_span_outside_every_sentence_takes_a_digest(document) -> None:
    start = SOURCE.index("x = 1")
    found = discriminator(document, _violation(_span(document, start, start + 5)))
    assert found == digest("x = 1")


def test_an_empty_span_has_no_discriminator(document) -> None:
    assert discriminator(document, _violation(_span(document, 3, 3))) == ""


def test_the_region_of_a_structured_source_holds_lines_only(document) -> None:
    span = _sentences(document)[0].span
    assert region(document, span) == {
        "startLine": span.start_line,
        "endLine": span.end_line,
        "startColumn": span.start_column,
        "endColumn": span.end_column,
    }
    structured = dataclasses.replace(document, source_kind=SourceKind.YAML)
    assert set(region(structured, span)) == {"startLine", "endLine"}


def test_the_resource_escapes_and_the_uri_encodes(tmp_path) -> None:
    path = tmp_path / "notes" / "a#b%c d:e.md"
    assert relative_path(path, tmp_path) == "notes/a#b%c d:e.md"
    assert logical_name("notes/a#b%c d:e.md") == "path:notes/a%23b%25c d:e.md"
    assert artifact_uri("notes/a#b%c d:e.md") == "notes/a%23b%25c%20d%3Ae.md"
    with pytest.raises(ValueError, match="outside the root"):
        relative_path(tmp_path.parent / "elsewhere.md", tmp_path)
