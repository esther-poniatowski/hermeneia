from __future__ import annotations

from importlib import metadata
import json
from pathlib import Path

import pytest

from hermeneia.document.annotator import SpaCyDocumentAnnotator
from hermeneia.document.markdown import MarkdownDocumentParser
from hermeneia.document.model import Document, Span
from hermeneia.document.parser import ParseRequest
from hermeneia.language.en import ENGLISH_SPACY_MODEL_VERSION

SNAPSHOT_ROOT = Path(__file__).resolve().parents[1] / "fixtures" / "annotation_snapshots"
MODEL_PACKAGE = "en-core-web-sm"


def test_en_spacy_model_package_version_is_pinned() -> None:
    try:
        installed = metadata.version(MODEL_PACKAGE)
    except metadata.PackageNotFoundError:
        pytest.fail(
            f"Required spaCy model package '{MODEL_PACKAGE}' is not installed in the test environment."
        )
    assert installed == ENGLISH_SPACY_MODEL_VERSION


@pytest.mark.parametrize(
    "fixture_name",
    ("inline_math_code_link", "math_heavy_masking"),
)
def test_spacy_annotation_matches_frozen_snapshot(
    fixture_name: str, language_pack, research_profile
) -> None:
    source_path = SNAPSHOT_ROOT / f"{fixture_name}.md"
    expected_path = SNAPSHOT_ROOT / f"{fixture_name}.snapshot.json"

    source = source_path.read_text(encoding="utf-8")
    document = MarkdownDocumentParser(language_pack).parse(
        ParseRequest(source=source, path=source_path)
    )
    annotation = SpaCyDocumentAnnotator(language_pack.parser_model).annotate(
        document, research_profile
    )
    assert annotation.diagnostics == ()

    snapshot = _serialize_document(annotation.document)
    expected = json.loads(expected_path.read_text(encoding="utf-8"))
    assert snapshot == expected


def _serialize_document(document: Document) -> dict[str, object]:
    sentence_rows: list[dict[str, object]] = []
    for block in document.iter_blocks():
        for sentence in block.sentences:
            sentence_rows.append(
                {
                    "block_id": block.id,
                    "block_kind": block.kind.value,
                    "sentence_id": sentence.id,
                    "source_text": sentence.source_text,
                    "sentence_span": _serialize_span(sentence.span),
                    "projection_text": sentence.projection.text,
                    "annotation_flags": sorted(sentence.annotation_flags),
                    "masked_segments": [
                        {
                            "kind": segment.kind.value,
                            "placeholder": segment.placeholder,
                            "source_span": _serialize_span(segment.source_span),
                        }
                        for segment in sentence.projection.masked_segments
                    ],
                    "tokens": [
                        {
                            "text": token.text,
                            "lemma": token.lemma,
                            "pos": token.pos,
                            "dep": token.dep,
                            "head_idx": token.head_idx,
                            "projection_start": token.projection_start,
                            "projection_end": token.projection_end,
                            "source_span": _serialize_span(token.source_span),
                        }
                        for token in sentence.tokens
                    ],
                }
            )
    return {"sentences": sentence_rows}


def _serialize_span(span: Span) -> dict[str, int]:
    return {
        "start": span.start,
        "end": span.end,
        "start_line": span.start_line,
        "start_column": span.start_column,
        "end_line": span.end_line,
        "end_column": span.end_column,
    }
