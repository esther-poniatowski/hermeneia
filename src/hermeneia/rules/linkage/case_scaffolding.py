"""Case-scaffolding noun-phrase checks."""

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

IN_THE_CASE_RE = re.compile(
    r"\b(?:in|under)\s+the\s+(?:[A-Za-z0-9-]+\s+){0,4}cases?\b",
    re.IGNORECASE,
)
THE_CASE_NP_RE = re.compile(
    r"\bthe\s+(?:[A-Za-z0-9-]+\s+){0,4}cases?\b",
    re.IGNORECASE,
)
CASE_OF_RE = re.compile(
    r"\bcases?\s+of\s+(?:[A-Za-z0-9-]+\s+){0,4}[A-Za-z0-9-]+\b",
    re.IGNORECASE,
)
THIS_CASE_RE = re.compile(
    r"\bthis\s+(?:[A-Za-z0-9-]+\s+){0,4}cases?\b",
    re.IGNORECASE,
)
CASE_PATTERNS: tuple[re.Pattern[str], ...] = (
    IN_THE_CASE_RE,
    THE_CASE_NP_RE,
    CASE_OF_RE,
    THIS_CASE_RE,
)


class CaseScaffoldingRule(SourcePatternRule):
    """Casescaffoldingrule."""

    metadata = RuleMetadata(
        rule_id="linkage.case_scaffolding",
        label="Avoid noun-phrase case scaffolding",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("phrase",),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc, ctx
        violations: list[Violation] = []
        seen_spans: list[tuple[int, int, int]] = []
        for line in lines:
            if any(
                kind.value in {"code_block", "display_math"}
                for kind in line.container_kinds
            ):
                continue
            probe = line_text_outside_excluded(line)
            for pattern in CASE_PATTERNS:
                for match in pattern.finditer(probe):
                    span_key = (line.span.start_line, match.start(), match.end())
                    if _is_span_covered(seen_spans, span_key):
                        continue
                    seen_spans.append(span_key)
                    phrase = match.group(0)
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=f"Rewrite '{phrase}' as a direct prepositional or clausal form.",
                            span=_match_span(line, match.start(), match.end()),
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(features={"phrase": phrase.lower()}),
                            rewrite_tactics=(
                                "Use a direct relation (for/in/when ...) instead of abstract "
                                "'the ... case' scaffolding.",
                            ),
                        )
                    )
        return violations


def _match_span(line, start: int, end: int) -> Span:
    """Match span."""
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def _is_span_covered(
    seen_spans: list[tuple[int, int, int]],
    candidate: tuple[int, int, int],
) -> bool:
    """Is span covered."""
    line, start, end = candidate
    for seen_line, seen_start, seen_end in seen_spans:
        if seen_line != line:
            continue
        if seen_start <= start and end <= seen_end:
            return True
    return False


def register(registry) -> None:
    """Register."""
    registry.add(CaseScaffoldingRule)
