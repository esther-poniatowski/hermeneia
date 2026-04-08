"""Detect noun-before-assumption/hypothesis framing that obscures core claims."""

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

ASSUMPTION_FRAMING_RE = re.compile(
    r"\bthe\s+([A-Za-z][A-Za-z0-9-]{2,})\s+(assumption|hypothesis)\b",
    re.IGNORECASE,
)
IGNORED_MODIFIERS = frozenset(
    {"same", "above", "previous", "following", "main", "key", "central"}
)


class AssumptionHypothesisFramingRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.assumption_hypothesis_framing",
        label="Prefer 'assumption/hypothesis of ...' framing",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("modifier", "target"),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = ASSUMPTION_FRAMING_RE.search(probe)
            if match is None:
                continue
            modifier = match.group(1).lower()
            target = match.group(2).lower()
            if modifier in IGNORED_MODIFIERS:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Phrase '{match.group(0)}' hides the governing relation; "
                        f"prefer explicit '{target} of ...' framing."
                    ),
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"modifier": modifier, "target": target}
                    ),
                    confidence=0.74,
                    rewrite_tactics=(
                        "Rewrite to foreground the proposition explicitly, for example 'the assumption of ...'.",
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
    registry.add(AssumptionHypothesisFramingRule)
