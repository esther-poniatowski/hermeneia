"""Abstract-framing checks for direct technical phrasing."""

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

ABSTRACT_FRAMING_RE = re.compile(
    r"\b(?:the\s+fact\s+that|the\s+question\s+of|the\s+issue\s+of|in\s+terms\s+of|is\s+given\s+by)\b",
    re.IGNORECASE,
)


class AbstractFramingRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.abstract_framing",
        label="Avoid abstract framing before the operative statement",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("phrase",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            match = ABSTRACT_FRAMING_RE.search(probe)
            if match is None:
                continue
            phrase = match.group(0)
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Replace abstract framing '{phrase}' with a direct statement "
                        "of the mechanism, relation, or claim."
                    ),
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"phrase": phrase.lower()}),
                    rewrite_tactics=(
                        "State what acts on what, or what follows from what, without meta-framing.",
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
    registry.add(AbstractFramingRule)
