"""Sentence stress-position heuristics."""

from __future__ import annotations

import re

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
from hermeneia.rules.common import iter_sentences, upstream_limits

WORD_RE = re.compile(r"\b[A-Za-z][A-Za-z0-9-]*\b")


class StressPositionRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="linkage.stress_position",
        label="Sentence stress position appears weak",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("final_token",),
    )

    def check(self, doc, ctx):
        weak_final_words = ctx.language_pack.lexicons.weak_final_words
        if not weak_final_words:
            return []
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            final_token = _final_content_token(sentence)
            if final_token is None:
                continue
            if final_token.lower() not in weak_final_words:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Sentence ends on weak stress token '{final_token}'.",
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"final_token": final_token.lower()},
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.58,
                    rationale="Stress-position checks are heuristic and should be interpreted with local rhetorical context.",
                    rewrite_tactics=(
                        "Move the key new information to the end of the sentence.",
                    ),
                )
            )
        return violations


def _final_content_token(sentence) -> str | None:
    if sentence.tokens:
        for token in reversed(sentence.tokens):
            if token.pos == "PUNCT":
                continue
            cleaned = token.text.strip().strip(".,;:!?")
            if cleaned:
                return cleaned
        return None
    words = [match.group(0) for match in WORD_RE.finditer(sentence.projection.text)]
    return words[-1] if words else None


def register(registry) -> None:
    registry.add(StressPositionRule)
