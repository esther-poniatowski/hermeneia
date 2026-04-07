"""Vague mechanism-phrasing checks."""

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

VAGUE_PHRASE_RE = re.compile(
    r"\b(?:in\s+(?:many|various)\s+ways?|in\s+ways\s+that|kind\s+of|sort\s+of|somehow)\b",
    re.IGNORECASE,
)


class VaguePhrasingRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.vague_phrasing",
        label="Avoid vague mechanism phrasing",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
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
            match = VAGUE_PHRASE_RE.search(probe)
            if match is None:
                continue
            phrase = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Replace vague phrase '{phrase}' with a specific mechanism or operation.",
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"phrase": phrase.lower()}),
                    rewrite_tactics=("State the concrete mechanism instead of a broad qualitative placeholder.",),
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
    registry.add(VaguePhrasingRule)

