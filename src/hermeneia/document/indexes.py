"""Document indexes and shared feature computations.

Classes
-------
SectionView
    Public API symbol.
SentenceRef
    Public API symbol.
SupportSignalKind
    Public API symbol.
SupportSignal
    Public API symbol.
DocumentIndexes
    Public API symbol.
EmbeddingBackend
    Public API symbol.
FeatureStore
    Public API symbol.

Functions
---------
build_document_indexes
    Public API symbol.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
import math
import re
from typing import Iterable, Protocol

from hermeneia.document.model import Block, BlockKind, Document, Sentence, Span

TERM_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9-]{2,}\b")
SYMBOL_RE = re.compile(r"^\$([A-Za-z][A-Za-z0-9']*)\$$")
CITATION_RE = re.compile(
    r"(?:\[[A-Z][^\]]+,\s*\d{4}\]|\\cite\{[^}]+\}|\[\d+(?:,\s*\d+)*\])"
)
THEOREM_RE = re.compile(r"\b(?:Theorem|Lemma|Proposition|Corollary)\s+\d+\b")
PROOF_RE = re.compile(r"\bProof\.\b")
QUANT_RE = re.compile(r"\b(?:Figure|Table)\s+\d+\b|\bp\s*[<>]=?\s*\d|\b\d+(?:\.\d+)?%")

REDUNDANCY_LOCAL_WINDOW = 4
REDUNDANCY_SECTION_WINDOW = 8
REDUNDANCY_TERM_NEIGHBOR_WINDOW = 5
REDUNDANCY_MAX_TERM_DF_RATIO = 0.35
REDUNDANCY_LEXICAL_FLOOR = 0.25


@dataclass(frozen=True)
class SectionView:
    """Sectionview."""

    heading_block_id: str | None
    level: int
    block_ids: tuple[str, ...]
    span: Span


@dataclass(frozen=True)
class SentenceRef:
    """Sentenceref."""

    id: str
    block_id: str
    ordinal: int
    span: Span


class SupportSignalKind(StrEnum):
    """Kinds of parser-derived support signals."""

    CITATION = "citation"
    THEOREM_REF = "theorem_ref"
    PROOF_REF = "proof_ref"
    DISPLAYED_EQUATION = "displayed_equation"
    QUANTITATIVE_RESULT = "quantitative_result"
    CONTRAST_MARKER = "contrast_marker"
    EXAMPLE_MARKER = "example_marker"
    DEFINITION_MARKER = "definition_marker"


@dataclass(frozen=True)
class SupportSignal:
    """Supportsignal."""

    kind: SupportSignalKind
    span: Span
    block_id: str
    sentence_id: str | None


@dataclass
class DocumentIndexes:
    """Precomputed indexes derived from a parsed document."""

    sections: list[SectionView]
    sentences: tuple[SentenceRef, ...]
    math_block_ids: tuple[str, ...]
    code_block_ids: tuple[str, ...]
    term_first_use: dict[str, Span]
    symbol_first_use: dict[str, Span]
    support_signals: list[SupportSignal]


class EmbeddingBackend(Protocol):
    """Protocol for embedding backend implementations."""

    def embed_text(self, text: str) -> tuple[float, ...]:
        """Embed text.

        Parameters
        ----------
        text : str
            Text content to process.

        Returns
        -------
        tuple[float, ...]
            Resulting value produced by this call.
        """


class FeatureStore:
    """Precomputed document-level features shared across rules.

    Parameters
    ----------
    doc : Document
        Document instance to inspect.
    indexes : DocumentIndexes
        Input value for ``indexes``.
    embedding_backend : EmbeddingBackend | None
        Input value for ``embedding_backend``.
    """

    def __init__(
        self,
        doc: Document,
        indexes: DocumentIndexes,
        embedding_backend: EmbeddingBackend | None = None,
    ) -> None:
        """Initialize the instance."""
        self._doc = doc
        self._indexes = indexes
        self._embedding_backend = embedding_backend
        self._sentence_embedding_cache: dict[str, tuple[float, ...]] = {}
        self._paragraph_embedding_cache: dict[str, tuple[float, ...]] = {}
        self._sentence_overlap_cache: dict[tuple[str, str], float] = {}
        self._paragraph_overlap_cache: dict[tuple[str, str], float] = {}
        self._redundancy_candidate_cache: dict[
            float, tuple[tuple[str, str, float], ...]
        ] = {}
        self._sentence_index = {ref.id: ref for ref in indexes.sentences}
        self._sentence_ordinals = {ref.id: ref.ordinal for ref in indexes.sentences}
        self._heading_parents = _heading_parent_map(indexes.sections)
        self._paragraph_blocks = tuple(
            block
            for block in self._doc.iter_blocks()
            if block.kind == BlockKind.PARAGRAPH
        )
        self._paragraph_ordinals = {
            block.id: ordinal for ordinal, block in enumerate(self._paragraph_blocks)
        }
        self._paragraph_terms = {
            block.id: _block_terms(block) for block in self._paragraph_blocks
        }
        self._block_sections = _block_section_map(indexes.sections)

    def term_first_use(self, term: str) -> Span | None:
        """Term first use.

        Parameters
        ----------
        term : str
            Input value for ``term``.

        Returns
        -------
        Span | None
            Resulting value produced by this call.
        """
        return self._indexes.term_first_use.get(term.lower())

    def symbol_first_use(self, symbol: str) -> Span | None:
        """Symbol first use.

        Parameters
        ----------
        symbol : str
            Input value for ``symbol``.

        Returns
        -------
        Span | None
            Resulting value produced by this call.
        """
        return self._indexes.symbol_first_use.get(symbol)

    def support_signals_in_window(
        self,
        anchor_sentence_id: str,
        max_sentences_back: int = 3,
    ) -> list[SupportSignal]:
        """Support signals in window.

        Parameters
        ----------
        anchor_sentence_id : str
            Input value for ``anchor_sentence_id``.
        max_sentences_back : int
            Input value for ``max_sentences_back``.

        Returns
        -------
        list[SupportSignal]
            Resulting value produced by this call.
        """
        anchor = self._sentence_ordinals.get(anchor_sentence_id)
        anchor_ref = self._sentence_index.get(anchor_sentence_id)
        if anchor is None or anchor_ref is None:
            return []
        results: list[SupportSignal] = []
        for signal in self._indexes.support_signals:
            if signal.sentence_id is not None:
                ordinal = self._sentence_ordinals.get(signal.sentence_id)
                if ordinal is None:
                    continue
                if 0 <= anchor - ordinal <= max_sentences_back:
                    results.append(signal)
                continue
            line_distance = anchor_ref.span.start_line - signal.span.end_line
            if (
                signal.span.start <= anchor_ref.span.end
                and 0 <= line_distance <= max_sentences_back * 4
            ):
                results.append(signal)
        return results

    def sentence_overlap(self, sent_a_id: str, sent_b_id: str) -> float:
        """Sentence overlap.

        Parameters
        ----------
        sent_a_id : str
            Input value for ``sent_a_id``.
        sent_b_id : str
            Input value for ``sent_b_id``.

        Returns
        -------
        float
            Resulting value produced by this call.
        """
        key = (
            (sent_a_id, sent_b_id) if sent_a_id <= sent_b_id else (sent_b_id, sent_a_id)
        )
        if key not in self._sentence_overlap_cache:
            sent_a = self._doc.sentence_by_id(sent_a_id)
            sent_b = self._doc.sentence_by_id(sent_b_id)
            self._sentence_overlap_cache[key] = _jaccard(
                _lemmas(sent_a), _lemmas(sent_b)
            )
        return self._sentence_overlap_cache[key]

    def paragraph_overlap(self, block_id_a: str, block_id_b: str) -> float:
        """Paragraph overlap.

        Parameters
        ----------
        block_id_a : str
            Input value for ``block_id_a``.
        block_id_b : str
            Input value for ``block_id_b``.

        Returns
        -------
        float
            Resulting value produced by this call.
        """
        key = (
            (block_id_a, block_id_b)
            if block_id_a <= block_id_b
            else (block_id_b, block_id_a)
        )
        if key not in self._paragraph_overlap_cache:
            block_a = self._doc.block_by_id(block_id_a)
            block_b = self._doc.block_by_id(block_id_b)
            terms_a = self._paragraph_terms.get(block_id_a, _block_terms(block_a))
            terms_b = self._paragraph_terms.get(block_id_b, _block_terms(block_b))
            self._paragraph_overlap_cache[key] = _jaccard(
                terms_a,
                terms_b,
            )
        return self._paragraph_overlap_cache[key]

    @property
    def embeddings_available(self) -> bool:
        """Embeddings available.

        Returns
        -------
        bool
            Resulting value produced by this call.
        """
        return self._embedding_backend is not None

    def sentence_embedding(self, sent_id: str) -> tuple[float, ...] | None:
        """Sentence embedding.

        Parameters
        ----------
        sent_id : str
            Input value for ``sent_id``.

        Returns
        -------
        tuple[float, ...] | None
            Resulting value produced by this call.
        """
        backend = self._embedding_backend
        if backend is None:
            return None
        if sent_id not in self._sentence_embedding_cache:
            sentence = self._doc.sentence_by_id(sent_id)
            if sentence is None:
                return None
            self._sentence_embedding_cache[sent_id] = backend.embed_text(
                sentence.projection.text
            )
        return self._sentence_embedding_cache[sent_id]

    def paragraph_embedding(self, block_id: str) -> tuple[float, ...] | None:
        """Paragraph embedding.

        Parameters
        ----------
        block_id : str
            Input value for ``block_id``.

        Returns
        -------
        tuple[float, ...] | None
            Resulting value produced by this call.
        """
        backend = self._embedding_backend
        if backend is None:
            return None
        if block_id not in self._paragraph_embedding_cache:
            block = self._doc.block_by_id(block_id)
            if block is None:
                return None
            self._paragraph_embedding_cache[block_id] = backend.embed_text(
                _block_text(block)
            )
        return self._paragraph_embedding_cache[block_id]

    def redundancy_candidates(
        self,
        similarity_threshold: float = 0.85,
    ) -> list[tuple[str, str, float]]:
        """Redundancy candidates.

        Parameters
        ----------
        similarity_threshold : float
            Input value for ``similarity_threshold``.

        Returns
        -------
        list[tuple[str, str, float]]
            Resulting value produced by this call.
        """
        cache_key = round(similarity_threshold, 6)
        cached = self._redundancy_candidate_cache.get(cache_key)
        if cached is not None:
            return list(cached)

        candidates: list[tuple[str, str, float]] = []
        for left_id, right_id in self._blocked_redundancy_pairs():
            lexical = self.paragraph_overlap(left_id, right_id)
            if lexical < REDUNDANCY_LEXICAL_FLOOR and not self.embeddings_available:
                continue
            similarity = lexical
            if self.embeddings_available:
                left_vector = self.paragraph_embedding(left_id)
                right_vector = self.paragraph_embedding(right_id)
                if left_vector is not None and right_vector is not None:
                    similarity = max(similarity, _cosine(left_vector, right_vector))
            if similarity >= similarity_threshold:
                candidates.append((left_id, right_id, similarity))
        candidates.sort(
            key=lambda row: (
                -row[2],
                self._paragraph_ordinals.get(row[0], -1),
                self._paragraph_ordinals.get(row[1], -1),
            )
        )
        frozen = tuple(candidates)
        self._redundancy_candidate_cache[cache_key] = frozen
        return list(frozen)

    def _blocked_redundancy_pairs(self) -> tuple[tuple[str, str], ...]:
        """Blocked redundancy pairs."""
        if len(self._paragraph_blocks) < 2:
            return ()
        ordinals = self._paragraph_ordinals
        pairs: set[tuple[str, str]] = set()

        for ordinal, block in enumerate(self._paragraph_blocks):
            upper = min(
                len(self._paragraph_blocks), ordinal + 1 + REDUNDANCY_LOCAL_WINDOW
            )
            for candidate_ordinal in range(ordinal + 1, upper):
                candidate = self._paragraph_blocks[candidate_ordinal]
                pairs.add((block.id, candidate.id))

        by_section: dict[str | None, list[str]] = {}
        for block in self._paragraph_blocks:
            section_id = self._block_sections.get(block.id)
            by_section.setdefault(section_id, []).append(block.id)
        for section_block_ids in by_section.values():
            for index, left_id in enumerate(section_block_ids):
                upper = min(
                    len(section_block_ids), index + 1 + REDUNDANCY_SECTION_WINDOW
                )
                for right_id in section_block_ids[index + 1 : upper]:
                    pairs.add(_ordered_paragraph_pair(left_id, right_id, ordinals))

        max_df = max(3, int(len(self._paragraph_blocks) * REDUNDANCY_MAX_TERM_DF_RATIO))
        term_postings: dict[str, list[str]] = {}
        for block in self._paragraph_blocks:
            for term in self._paragraph_terms.get(block.id, set()):
                term_postings.setdefault(term, []).append(block.id)
        for posting in term_postings.values():
            if len(posting) < 2 or len(posting) > max_df:
                continue
            ordered_posting = sorted(posting, key=lambda block_id: ordinals[block_id])
            for index, left_id in enumerate(ordered_posting):
                upper = min(
                    len(ordered_posting), index + 1 + REDUNDANCY_TERM_NEIGHBOR_WINDOW
                )
                for right_id in ordered_posting[index + 1 : upper]:
                    pairs.add(_ordered_paragraph_pair(left_id, right_id, ordinals))

        return tuple(
            sorted(pairs, key=lambda pair: (ordinals[pair[0]], ordinals[pair[1]]))
        )

    @property
    def sections(self) -> list[SectionView]:
        """Sections.

        Returns
        -------
        list[SectionView]
            Resulting value produced by this call.
        """
        return self._indexes.sections

    def sibling_headings(self, level: int) -> list[Block]:
        """Return sibling headings.

        Parameters
        ----------
        level : int
            Input value for ``level``.

        Returns
        -------
        list[Block]
            Resulting value produced by this call.
        """
        return [
            heading for group in self.sibling_heading_groups(level) for heading in group
        ]

    def sibling_heading_groups(self, level: int) -> tuple[tuple[Block, ...], ...]:
        """Return sibling heading groups.

        Parameters
        ----------
        level : int
            Input value for ``level``.

        Returns
        -------
        tuple[tuple[Block, ...], ...]
            Resulting value produced by this call.
        """
        grouped: dict[str | None, list[Block]] = {}
        for block in self._doc.iter_blocks():
            if block.kind != BlockKind.HEADING:
                continue
            if int(block.metadata.get("level", 0)) != level:
                continue
            parent_id = self._heading_parents.get(block.id)
            grouped.setdefault(parent_id, []).append(block)
        groups = [
            tuple(sorted(group, key=lambda heading: heading.span.start))
            for group in grouped.values()
            if len(group) >= 2
        ]
        return tuple(sorted(groups, key=lambda group: group[0].span.start))


def build_document_indexes(
    doc: Document,
    contrast_markers: Iterable[str],
    definitional_markers: Iterable[str],
) -> DocumentIndexes:
    """Compute canonical derived indexes for a parsed document.

    Parameters
    ----------
    doc : Document
        Document instance to inspect.
    contrast_markers : Iterable[str]
        Input value for ``contrast_markers``.
    definitional_markers : Iterable[str]
        Input value for ``definitional_markers``.

    Returns
    -------
    DocumentIndexes
        Resulting value produced by this call.
    """

    sentence_refs: list[SentenceRef] = []
    math_block_ids: list[str] = []
    code_block_ids: list[str] = []
    term_first_use: dict[str, Span] = {}
    symbol_first_use: dict[str, Span] = {}
    support_signals: list[SupportSignal] = []

    ordinal = 0
    for block in doc.iter_blocks():
        if block.kind == BlockKind.DISPLAY_MATH:
            math_block_ids.append(block.id)
            support_signals.append(
                SupportSignal(
                    kind=SupportSignalKind.DISPLAYED_EQUATION,
                    span=block.span,
                    block_id=block.id,
                    sentence_id=None,
                )
            )
        if block.kind == BlockKind.CODE_BLOCK:
            code_block_ids.append(block.id)
        for sentence in block.sentences:
            sentence_refs.append(
                SentenceRef(
                    id=sentence.id,
                    block_id=block.id,
                    ordinal=ordinal,
                    span=sentence.span,
                )
            )
            ordinal += 1
            _record_first_uses(sentence, term_first_use, symbol_first_use)
            support_signals.extend(
                _detect_support_signals(
                    sentence,
                    block.id,
                    contrast_markers,
                    definitional_markers,
                )
            )

    support_signals.sort(key=lambda signal: signal.span.start)
    return DocumentIndexes(
        sections=_build_sections(doc),
        sentences=tuple(sentence_refs),
        math_block_ids=tuple(math_block_ids),
        code_block_ids=tuple(code_block_ids),
        term_first_use=term_first_use,
        symbol_first_use=symbol_first_use,
        support_signals=support_signals,
    )


def _build_sections(doc: Document) -> list[SectionView]:
    """Build sections."""
    headings = [block for block in doc.iter_blocks() if block.kind == BlockKind.HEADING]
    flat_blocks = list(doc.iter_blocks())
    if not headings:
        return [
            SectionView(
                heading_block_id=None,
                level=0,
                block_ids=tuple(block.id for block in flat_blocks),
                span=flat_blocks[0].span if flat_blocks else Span(0, 0, 1, 1, 1, 1),
            )
        ]

    sections: list[SectionView] = []
    for index, heading in enumerate(headings):
        level = int(heading.metadata.get("level", 1))
        start = flat_blocks.index(heading)
        end = len(flat_blocks)
        for candidate in headings[index + 1 :]:
            candidate_level = int(candidate.metadata.get("level", 1))
            if candidate_level <= level:
                end = flat_blocks.index(candidate)
                break
        block_ids = tuple(block.id for block in flat_blocks[start:end])
        last_span = flat_blocks[end - 1].span
        sections.append(
            SectionView(
                heading_block_id=heading.id,
                level=level,
                block_ids=block_ids,
                span=Span(
                    start=heading.span.start,
                    end=last_span.end,
                    start_line=heading.span.start_line,
                    start_column=heading.span.start_column,
                    end_line=last_span.end_line,
                    end_column=last_span.end_column,
                ),
            )
        )
    return sections


def _record_first_uses(
    sentence: Sentence,
    term_index: dict[str, Span],
    symbol_index: dict[str, Span],
) -> None:
    """Record first uses."""
    for match in TERM_RE.finditer(sentence.projection.text):
        term_index.setdefault(match.group(0).lower(), sentence.span)
    for node in sentence.inline_nodes:
        symbol_match = SYMBOL_RE.fullmatch(node.text.strip())
        if symbol_match is not None:
            symbol_index.setdefault(symbol_match.group(1), node.span)


def _detect_support_signals(
    sentence: Sentence,
    block_id: str,
    contrast_markers: Iterable[str],
    definitional_markers: Iterable[str],
) -> list[SupportSignal]:
    """Detect support signals."""
    text = sentence.source_text
    lower = text.lower()
    results: list[SupportSignal] = []
    if CITATION_RE.search(text):
        results.append(
            SupportSignal(
                SupportSignalKind.CITATION, sentence.span, block_id, sentence.id
            )
        )
    if THEOREM_RE.search(text):
        results.append(
            SupportSignal(
                SupportSignalKind.THEOREM_REF, sentence.span, block_id, sentence.id
            )
        )
    if PROOF_RE.search(text):
        results.append(
            SupportSignal(
                SupportSignalKind.PROOF_REF, sentence.span, block_id, sentence.id
            )
        )
    if QUANT_RE.search(text):
        results.append(
            SupportSignal(
                SupportSignalKind.QUANTITATIVE_RESULT,
                sentence.span,
                block_id,
                sentence.id,
            )
        )
    if any(marker in lower for marker in contrast_markers):
        results.append(
            SupportSignal(
                SupportSignalKind.CONTRAST_MARKER, sentence.span, block_id, sentence.id
            )
        )
    if lower.startswith("for example") or "example" in lower:
        results.append(
            SupportSignal(
                SupportSignalKind.EXAMPLE_MARKER, sentence.span, block_id, sentence.id
            )
        )
    if _contains_any_marker(lower, definitional_markers):
        results.append(
            SupportSignal(
                SupportSignalKind.DEFINITION_MARKER,
                sentence.span,
                block_id,
                sentence.id,
            )
        )
    return results


def _contains_any_marker(lowered_text: str, markers: Iterable[str]) -> bool:
    """Contains any marker."""
    for marker in markers:
        normalized = marker.strip().lower()
        if not normalized:
            continue
        if " " in normalized:
            if normalized in lowered_text:
                return True
            continue
        if re.search(rf"\b{re.escape(normalized)}\b", lowered_text):
            return True
    return False


def _lemmas(sentence: Sentence | None) -> set[str]:
    """Lemmas."""
    if sentence is None:
        return set()
    if sentence.tokens:
        return {
            token.lemma.lower() for token in sentence.tokens if token.lemma.isalpha()
        }
    return {
        match.group(0).lower() for match in TERM_RE.finditer(sentence.projection.text)
    }


def _block_terms(block: Block | None) -> set[str]:
    """Block terms."""
    if block is None:
        return set()
    terms: set[str] = set()
    for sentence in block.sentences:
        terms |= _lemmas(sentence)
    return terms


def _block_text(block: Block | None) -> str:
    """Block text."""
    if block is None:
        return ""
    return " ".join(sentence.projection.text for sentence in block.sentences)


def _jaccard(left: set[str], right: set[str]) -> float:
    """Jaccard."""
    union = left | right
    if not union:
        return 0.0
    return len(left & right) / len(union)


def _cosine(left: tuple[float, ...], right: tuple[float, ...]) -> float:
    """Cosine."""
    if not left or not right or len(left) != len(right):
        return 0.0
    numerator = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = math.sqrt(sum(value * value for value in left))
    right_norm = math.sqrt(sum(value * value for value in right))
    if not left_norm or not right_norm:
        return 0.0
    return numerator / (left_norm * right_norm)


def _heading_parent_map(sections: list[SectionView]) -> dict[str, str | None]:
    """Heading parent map."""
    parents: dict[str, str | None] = {}
    stack: list[SectionView] = []
    ordered_sections = sorted(
        (section for section in sections if section.heading_block_id is not None),
        key=lambda section: section.span.start,
    )
    for section in ordered_sections:
        while stack and section.level <= stack[-1].level:
            stack.pop()
        heading_id = section.heading_block_id
        if heading_id is None:
            continue
        parents[heading_id] = stack[-1].heading_block_id if stack else None
        stack.append(section)
    return parents


def _block_section_map(sections: list[SectionView]) -> dict[str, str | None]:
    """Block section map."""
    block_sections: dict[str, str | None] = {}
    for section in sorted(sections, key=lambda value: value.level):
        for block_id in section.block_ids:
            block_sections[block_id] = section.heading_block_id
    return block_sections


def _ordered_paragraph_pair(
    left_id: str,
    right_id: str,
    ordinals: dict[str, int],
) -> tuple[str, str]:
    """Ordered paragraph pair."""
    if ordinals[left_id] <= ordinals[right_id]:
        return left_id, right_id
    return right_id, left_id
