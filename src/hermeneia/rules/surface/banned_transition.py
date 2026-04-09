"""Content-free transitional scaffolding."""

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


class BannedTransitionRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.banned_transition",
        label="Avoid content-free transition scaffolding",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("transition",),
    )

    def check_source(self, lines, doc, ctx):
        patterns = list(ctx.language_pack.lexicons.banned_transitions) + list(
            self.settings.extra_patterns
        )
        silenced = {pattern.lower() for pattern in self.settings.silenced_patterns}
        if not patterns:
            return []
        combined = "|".join(
            re.escape(pattern) for pattern in patterns if pattern.lower() not in silenced
        )
        if not combined:
            return []
        regex = re.compile(
            rf"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?(?:{combined})\b", re.IGNORECASE
        )
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = regex.search(probe)
            if match is None:
                continue
            matched = match.group(0).strip()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Lead with a concrete mathematical or argumentative action instead of '{matched}'.",
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"transition": matched.lower()}),
                    rewrite_tactics=(
                        "Replace the transition with the operation, evidence, or claim being introduced.",
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
    registry.add(BannedTransitionRule)
