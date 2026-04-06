"""Sentence-length diagnostics."""

from __future__ import annotations

from hermeneia.rules.base import (
    AnnotatedRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_sentences, sentence_word_count


class SentenceLengthRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="surface.sentence_length",
        label="Sentence exceeds the profile target length",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_words": 28},
    )

    def check(self, doc, ctx):
        violations: list[Violation] = []
        max_words = self.settings.int_option("max_words", 28)
        for sentence in iter_sentences(doc):
            count = sentence_word_count(sentence)
            if count <= max_words:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Sentence contains {count} words; the {ctx.profile.profile_name} profile target is {max_words}.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"word_count": count}, threshold=float(max_words)
                    ),
                    rewrite_tactics=(
                        "Split the sentence or move subordinate material to a following sentence.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(SentenceLengthRule)
