"""Imperative-opening bans for mathematical prose."""

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

IMPERATIVE_START_RE = re.compile(
    r"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?(Define|Assume|Write|Let|Denote|Set)\b"
)


class ImperativeOpeningRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.imperative_opening",
        label="Avoid imperative mathematical openings",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("verb",),
    )

    def check_source(self, lines, doc, ctx):
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = IMPERATIVE_START_RE.search(probe)
            if match is None:
                continue
            verb = match.group(1)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Avoid imperative opening '{verb} ...'; name the object or purpose declaratively.",
                    span=_match_span(line, match.start(1), match.end(1)),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"verb": verb}),
                    rewrite_tactics=(
                        "State the purpose first, then introduce the object or assumption declaratively.",
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
    registry.add(ImperativeOpeningRule)
