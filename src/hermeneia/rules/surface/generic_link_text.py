"""Generic link-text checks."""

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

GENERIC_LINK_TEXT_RE = re.compile(
    r"\[(?:Lemma|Result|Proposition|Theorem|Corollary)\s*\([^\]]+\)\]\([^)]*\)",
    re.IGNORECASE,
)


class GenericLinkTextRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.generic_link_text",
        label="Avoid generic citation-like markdown link text",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("link_text",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = GENERIC_LINK_TEXT_RE.search(probe)
            if match is None:
                continue
            link_text = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Generic link text hides the reference role; use descriptive anchor text "
                        "that states what the reader should take from the reference."
                    ),
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"link_text": link_text}),
                    rewrite_tactics=(
                        "Replace label-only link text with a descriptive, claim-relevant phrase.",
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
    registry.add(GenericLinkTextRule)

