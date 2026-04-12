"""Inline-enumeration overload checks."""

from __future__ import annotations

import re

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
from hermeneia.rules.common import iter_sentences, sentence_word_count

ENUM_LABEL_RE = re.compile(
    r"(?:\(\s*(?:[ivx]+|\d+)\s*\)|\b(?:first|second|third|fourth)\b)",
    re.IGNORECASE,
)
FALLBACK_VERB_RE = re.compile(
    r"\b(?:is|are|was|were|be|been|being|has|have|had|\w+ed|\w+ing)\b"
)


class InlineEnumerationOverloadRule(HeuristicSemanticRule):
    """Inlineenumerationoverloadrule."""

    metadata = RuleMetadata(
        rule_id="paragraph.inline_enumeration_overload",
        label="Dense inline enumerations should be converted to lists",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"max_inline_commas": 2, "min_words_for_clause_mode": 28},
        evidence_fields=("issue", "comma_count", "label_count"),
    )

    def check(self, doc, ctx):
        """Check."""
        _ = ctx
        max_inline_commas = self.settings.int_option("max_inline_commas", 2)
        min_words = self.settings.int_option("min_words_for_clause_mode", 28)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            text = sentence.source_text
            label_count = len(ENUM_LABEL_RE.findall(text))
            comma_count = text.count(",")
            if label_count >= 2:
                issue = "multi_label_inline_enumeration"
            else:
                if comma_count <= max_inline_commas:
                    continue
                if sentence_word_count(sentence) < min_words:
                    continue
                verb_count = _verb_count(sentence)
                if verb_count < 3:
                    continue
                issue = "comma_clause_overload"
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Sentence packs a dense inline enumeration; use a lead-in sentence "
                        "and bullet list."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "issue": issue,
                            "comma_count": comma_count,
                            "label_count": label_count,
                        },
                        score=float(comma_count),
                        threshold=float(max_inline_commas),
                    ),
                    confidence=0.67,
                    rationale=(
                        "Enumeration-overload checks use punctuation and shallow clause cues, "
                        "not full syntactic decomposition."
                    ),
                    rewrite_tactics=(
                        "Split the items into bullets under one lead-in sentence that states the organizing principle.",
                    ),
                )
            )
        return violations


def _verb_count(sentence) -> int:
    """Verb count."""
    if sentence.tokens:
        return sum(1 for token in sentence.tokens if token.pos in {"VERB", "AUX"})
    return len(FALLBACK_VERB_RE.findall(sentence.projection.text))


def register(registry) -> None:
    """Register."""
    registry.add(InlineEnumerationOverloadRule)
