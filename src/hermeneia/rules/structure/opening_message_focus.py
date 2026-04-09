"""Detect opening sentences where enumeration blurs the core message."""

from __future__ import annotations

import re

from hermeneia.document.model import BlockKind
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import matched_sentence_markers, sentence_word_count

ENUM_MARKER_RE = re.compile(r"\((?:[ivx]+|\d+|[a-z])\)", re.IGNORECASE)
COORD_CONJ_RE = re.compile(r"\b(?:and|or)\b", re.IGNORECASE)

OPENING_PROSE_KINDS = {
    BlockKind.PARAGRAPH,
    BlockKind.BLOCK_QUOTE,
    BlockKind.LIST_ITEM,
    BlockKind.ADMONITION,
    BlockKind.FOOTNOTE,
}


class OpeningMessageFocusRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="structure.opening_message_focus",
        label="Opening sentence should state one clear purpose before enumeration",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_enumeration_items": 4,
            "min_opening_words": 8,
        },
        evidence_fields=("issue", "enumeration_items", "purpose_markers"),
    )

    def check(self, doc, ctx):
        min_items = self.settings.int_option("min_enumeration_items", 4)
        min_words = self.settings.int_option("min_opening_words", 8)
        sentence = _first_opening_sentence(doc)
        if sentence is None:
            return []
        words = sentence_word_count(sentence)
        if words < min_words:
            return []
        purpose_markers = matched_sentence_markers(
            sentence,
            tuple(ctx.language_pack.lexicons.opening_purpose_markers),
        )
        enumeration_items = _estimate_enumeration_items(sentence.projection.text)
        if enumeration_items >= min_items and not purpose_markers:
            return [
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Opening sentence is dominated by enumeration and does not surface a "
                        "single core purpose."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": "enumeration_dominant_opening",
                            "enumeration_items": enumeration_items,
                            "purpose_markers": purpose_markers,
                        },
                        score=float(enumeration_items),
                        threshold=float(min_items),
                    ),
                    confidence=0.82,
                    rationale=(
                        "Opening-message focus prefers one explicit purpose statement before "
                        "multi-item enumerations."
                    ),
                    rewrite_tactics=(
                        "Start with one sentence that states the document purpose, then enumerate supporting dimensions afterward.",
                    ),
                )
            ]
        if purpose_markers:
            return []
        return [
            Violation(
                rule_id=self.rule_id,
                message=(
                    "Opening sentence does not expose a clear purpose verb; readers may need to "
                    "infer the document intent."
                ),
                span=sentence.span,
                severity=self.settings.severity,
                layer=self.metadata.layer,
                evidence=RuleEvidence(
                    features={
                        "issue": "missing_purpose_signal",
                        "enumeration_items": enumeration_items,
                        "purpose_markers": purpose_markers,
                    },
                ),
                confidence=0.58,
                rationale=(
                    "Purpose-signal checks are lexical and should be interpreted as non-blocking guidance."
                ),
                rewrite_tactics=(
                    "Rewrite the opening sentence with a direct purpose verb such as explains, defines, checks, or enforces.",
                ),
            )
        ]


def _first_opening_sentence(doc):
    for block in doc.iter_blocks():
        if block.kind not in OPENING_PROSE_KINDS:
            continue
        for sentence in block.sentences:
            return sentence
    return None


def _estimate_enumeration_items(text: str) -> int:
    stripped = text.strip()
    if not stripped:
        return 0
    inline_markers = len(ENUM_MARKER_RE.findall(stripped))
    semicolons = stripped.count(";")
    commas = stripped.count(",")
    comma_items = 0
    if commas >= 2 and COORD_CONJ_RE.search(stripped):
        comma_items = commas + 1
    semi_items = semicolons + 1 if semicolons >= 2 else 0
    return max(inline_markers, comma_items, semi_items)


def register(registry) -> None:
    registry.add(OpeningMessageFocusRule)

