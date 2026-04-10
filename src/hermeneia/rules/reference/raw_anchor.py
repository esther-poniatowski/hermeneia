"""Raw block-anchor token checks."""

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

ANCHOR_TOKEN_RE = re.compile(r"\^[a-z][a-z0-9]*-[a-z0-9-]+")


class RawAnchorRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="reference.raw_anchor",
        label="Avoid raw anchor tokens in running prose",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("anchor",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for match in ANCHOR_TOKEN_RE.finditer(probe):
                if not probe[match.end() :].strip():
                    continue
                anchor = match.group(0)
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Raw block anchor token appears in running text; reference it via "
                            "a markdown link instead."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(features={"anchor": anchor}),
                        rewrite_tactics=(
                            "Replace the raw '^anchor' token with descriptive linked text.",
                        ),
                    )
                )
                break
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
    registry.add(RawAnchorRule)

