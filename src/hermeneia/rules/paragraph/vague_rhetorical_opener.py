"""Vague rhetorical opener checks."""

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
from hermeneia.rules.common import iter_sentences

_LEADING_PUNCTUATION_RE = re.compile(r'^[\s"\'`([{]+')


class VagueRhetoricalOpenerRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.vague_rhetorical_opener",
        label="Avoid vague rhetorical openers that delay the claim",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("opener",),
        experimental=True,
    )

    def check(self, doc, ctx):
        patterns = _resolve_patterns(
            base=tuple(ctx.language_pack.lexicons.vague_rhetorical_openers),
            extra=self.settings.extra_patterns,
            silenced=self.settings.silenced_patterns,
        )
        if not patterns:
            return []
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            opener = _matched_opener(sentence.projection.text, patterns)
            if opener is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Sentence opens with vague rhetorical scaffolding ('{opener}'). "
                        "State the claim directly."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"opener": opener}),
                    confidence=0.84,
                    rationale=(
                        "The opener matches a deterministic phrase list that often delays "
                        "technical content without adding argument structure."
                    ),
                    rewrite_tactics=(
                        "Replace the opener with the concrete claim, operation, or result.",
                    ),
                )
            )
        return violations


def _resolve_patterns(
    base: tuple[str, ...],
    extra: tuple[str, ...],
    silenced: tuple[str, ...],
) -> tuple[str, ...]:
    silenced_set = {item.strip().lower() for item in silenced}
    combined = tuple(base) + tuple(extra)
    normalized: list[str] = []
    seen: set[str] = set()
    for item in combined:
        value = item.strip().lower()
        if not value or value in silenced_set or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return tuple(normalized)


def _matched_opener(text: str, patterns: tuple[str, ...]) -> str | None:
    probe = _LEADING_PUNCTUATION_RE.sub("", text).lower()
    for pattern in patterns:
        if probe.startswith(pattern) and _token_boundary_after_pattern(probe, pattern):
            return pattern
    return None


def _token_boundary_after_pattern(text: str, pattern: str) -> bool:
    end = len(pattern)
    if end >= len(text):
        return True
    next_char = text[end]
    return not next_char.isalpha()


def register(registry) -> None:
    registry.add(VagueRhetoricalOpenerRule)
