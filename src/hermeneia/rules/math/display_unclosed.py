"""Unclosed display-math delimiter checks."""

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


class DisplayUnclosedRule(SourcePatternRule):
    """Displayunclosedrule."""

    metadata = RuleMetadata(
        rule_id="math.display_unclosed",
        label="Display math delimiters must be properly closed",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("opening_line",),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc, ctx
        violations: list[Violation] = []
        open_line = None
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue
            delimiter_count = len(DISPLAY_DELIMITER_RE.findall(line.text))
            if delimiter_count % 2 == 1:
                if open_line is None:
                    open_line = line
                else:
                    open_line = None
        if open_line is not None:
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="Display math block starts with '$$' but is never closed.",
                    span=span_from_lines(open_line),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"opening_line": open_line.span.start_line}
                    ),
                    rewrite_tactics=(
                        "Add a closing '$$' delimiter for the opened display equation.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    """Register."""
    registry.add(DisplayUnclosedRule)
