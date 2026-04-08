"""Ambiguous display-math delimiter checks."""

from __future__ import annotations

import re

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
from hermeneia.rules.common import span_from_lines

DISPLAY_DELIMITER_RE = re.compile(r"(?<!\\)\$\$")


class DisplayAmbiguousRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.display_ambiguous",
        label="Avoid ambiguous multiple display delimiters on one line",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("delimiter_count",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc, ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue
            delimiter_count = len(DISPLAY_DELIMITER_RE.findall(line.text))
            if delimiter_count < 3:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Display math delimiters are ambiguous on this line; "
                        "split the expression into one explicit $$...$$ block."
                    ),
                    span=span_from_lines(line),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"delimiter_count": delimiter_count}),
                    rewrite_tactics=(
                        "Use one opening '$$' and one closing '$$' for each display equation.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(DisplayAmbiguousRule)
