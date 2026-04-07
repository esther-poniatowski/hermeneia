"""First-person and generic pronoun checks for formal prose."""

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

PRONOUN_RE = re.compile(
    r"\b(?:I|we|our|ours|us|you|your|yours|one can|one may)\b",
    re.IGNORECASE,
)


class PronounRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.pronoun",
        label="Avoid first-person or generic-pronoun scaffolding",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pronoun",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = PRONOUN_RE.search(probe)
            if match is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="Prefer object-centered phrasing over first-person or generic-pronoun scaffolding.",
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"pronoun": match.group(0).lower()}),
                    confidence=0.7,
                    rewrite_tactics=(
                        "Name the operation, statement, or object directly instead of using a generic actor.",
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
    registry.add(PronounRule)

