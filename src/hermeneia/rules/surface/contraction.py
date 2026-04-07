"""Contraction bans for formal technical prose."""

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
from hermeneia.rules.common import match_allowed

CONTRACTION_RE = re.compile(
    r"\b(?:"
    r"it's|that's|there's|here's|let's|"
    r"can't|won't|don't|doesn't|didn't|isn't|aren't|wasn't|weren't|"
    r"haven't|hasn't|hadn't|wouldn't|shouldn't|couldn't|"
    r"i'm|i've|i'll|"
    r"you're|you've|you'll|"
    r"we're|we've|we'll|"
    r"they're|they've|they'll"
    r")\b",
    re.IGNORECASE,
)


class ContractionRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.contraction",
        label="Avoid contractions in formal technical prose",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("contraction",),
    )

    def check_source(self, lines, doc, ctx):
        violations: list[Violation] = []
        for line in lines:
            if "code_block" in {kind.value for kind in line.container_kinds}:
                continue
            match = match_allowed(line, CONTRACTION_RE)
            if match is None:
                continue
            span = _match_span(line, match.start(), match.end())
            contraction = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Expand the contraction '{contraction}' in formal prose.",
                    span=span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"contraction": contraction.lower()}),
                    rewrite_tactics=("Expand the contraction to its full form.",),
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
    registry.add(ContractionRule)
