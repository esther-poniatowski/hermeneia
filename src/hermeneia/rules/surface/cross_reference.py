"""Ambiguous cross-reference checks."""

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

AMBIGUOUS_REF_RE = re.compile(
    r"\b(?:as\s+)?(?:shown|discussed|noted)?\s*(?:above|below|earlier|later)\b",
    re.IGNORECASE,
)
EXPLICIT_TARGET_RE = re.compile(
    r"\b(?:section|appendix|figure|table|equation|theorem|lemma|proposition|corollary)\b",
    re.IGNORECASE,
)


class CrossReferenceRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.cross_reference",
        label="Cross-reference should target an explicit object",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("reference",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = AMBIGUOUS_REF_RE.search(probe)
            if match is None:
                continue
            if EXPLICIT_TARGET_RE.search(probe):
                continue
            reference = match.group(0).strip()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Reference '{reference}' is ambiguous; name the section, theorem, or equation explicitly.",
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"reference": reference.lower()}),
                    rewrite_tactics=(
                        "Replace positional references with explicit anchors (for example, Section 3 or Theorem 2).",
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
    registry.add(CrossReferenceRule)

