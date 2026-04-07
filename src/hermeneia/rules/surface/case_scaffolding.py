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

CASE_SCAFFOLD_RE = re.compile(
    r"\bthe\s+(?:\w+\s+){0,3}case\b",
    re.IGNORECASE,
)


class CaseScaffoldingRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.case_scaffolding",
        label="Avoid noun-phrase case scaffolding",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
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
            match = CASE_SCAFFOLD_RE.search(probe)
            if match is None:
                continue
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
                        "Use a direct relation (for/in/when ...) instead of abstract 'the ... case' scaffolding.",
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
    registry.add(CaseScaffoldingRule)

