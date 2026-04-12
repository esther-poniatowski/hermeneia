"""NLP annotation integration with explicit fallback semantics."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any, Iterable

import spacy

from hermeneia.document.model import Document, Sentence, Span, Token
from hermeneia.engine.runner import AnnotationResult
from hermeneia.rules.base import ResolvedProfile

WORD_RE = re.compile(r"\b\w+\b")


@dataclass(frozen=True)
class AnnotationBackendStatus:
    """Annotationbackendstatus."""

    backend: str
    diagnostics: tuple[str, ...] = ()


class SpaCyDocumentAnnotator:
    """Annotate sentences with spaCy when available, otherwise degrade explicitly."""

    def __init__(self, model_name: str | None) -> None:
        """Init."""
        self._model_name = model_name
        self._nlp: Any | None = None
        self._status = AnnotationBackendStatus(
            backend="regex_fallback", diagnostics=("spaCy model unavailable",)
        )

    def annotate(
        self, document: Document, profile: ResolvedProfile
    ) -> AnnotationResult:
        """Annotate."""
        _ = profile
        if self._try_load():
            self._annotate_with_spacy(document)
            return AnnotationResult(document=document, diagnostics=())
        self._annotate_fallback(document)
        return AnnotationResult(
            document=document,
            diagnostics=(
                f"spaCy model '{self._model_name}' is unavailable; parser-local rules may abstain",
            ),
        )

    def _try_load(self) -> bool:
        """Try load."""
        if self._nlp is not None:
            return True
        if not self._model_name:
            return False
        try:
            self._nlp = spacy.load(self._model_name)
        except OSError:
            return False
        self._status = AnnotationBackendStatus(backend="spacy")
        return True

    def _annotate_with_spacy(self, document: Document) -> None:
        """Annotate with spacy."""
        nlp = self._nlp
        if nlp is None:
            return
        for sentence in _iter_sentences(document):
            doc = nlp(sentence.projection.text)
            sentence.tokens = [
                Token(
                    text=token.text,
                    lemma=token.lemma_,
                    pos=token.pos_,
                    dep=token.dep_,
                    head_idx=None if token.head is token else token.head.i,
                    source_span=_token_span(
                        sentence, token.idx, token.idx + len(token.text)
                    ),
                    projection_start=token.idx,
                    projection_end=token.idx + len(token.text),
                )
                for token in doc
            ]

    def _annotate_fallback(self, document: Document) -> None:
        """Annotate fallback."""
        for sentence in _iter_sentences(document):
            tokens: list[Token] = []
            for match in WORD_RE.finditer(sentence.projection.text):
                span = _token_span(sentence, match.start(), match.end())
                tokens.append(
                    Token(
                        text=match.group(0),
                        lemma=match.group(0).lower(),
                        pos=None,
                        dep=None,
                        head_idx=None,
                        source_span=span,
                        projection_start=match.start(),
                        projection_end=match.end(),
                    )
                )
            sentence.tokens = tokens


def _iter_sentences(document: Document) -> Iterable[Sentence]:
    """Iter sentences."""
    for block in document.iter_blocks():
        yield from block.sentences


def _token_span(sentence: Sentence, start: int, end: int) -> Span:
    """Token span."""
    source_start = sentence.projection.source_offset_for(start)
    source_end = sentence.projection.source_offset_for(max(start, end - 1))
    if source_start is None:
        source_start = sentence.span.start
    if source_end is None:
        source_end = sentence.span.end - 1
    return sentence.span.__class__(
        start=source_start,
        end=source_end + 1,
        start_line=sentence.span.start_line,
        start_column=sentence.span.start_column,
        end_line=sentence.span.end_line,
        end_column=sentence.span.end_column,
    )
