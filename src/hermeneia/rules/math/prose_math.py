"""Prose paraphrase checks for mathematical relations."""

from __future__ import annotations

import re

from hermeneia.document.model import Span
from hermeneia.rules.base import (
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    SourcePatternRule,
    Tractability,
    Violation,
)
from hermeneia.rules.common import line_text_outside_excluded

PROSE_MATH_RE = re.compile(
    r"\b(?:times|multiplied by|of order|converges to one|given by)\b",
    re.IGNORECASE,
)


class ProseMathRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.prose_math",
        label="Avoid prose paraphrases for explicit mathematical relations",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("phrase",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = PROSE_MATH_RE.search(probe)
            if match is None:
                continue
            phrase = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Phrase '{phrase}' paraphrases a mathematical relation; use explicit math notation.",
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"phrase": phrase.lower()}),
                    rewrite_tactics=(
                        "Render the relation in math notation (for example with '=', multiplication symbols, or asymptotic notation).",
                    ),
                )
            )
        return violations


def _match_span(line, start: int, end: int) -> Span:
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    registry.add(ProseMathRule)

