"""Math-shorthand introduction checks."""

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
from hermeneia.rules.common import line_text_outside_excluded, span_from_lines

INPUT_MAG_SHORTHAND_RE = re.compile(r"\\rho\s*:?=\s*\\\|\\mathbf\{u\}\\\|")


class ShorthandRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.shorthand",
        label="Avoid unnecessary shorthand for input magnitude",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pattern",),
    )

    def check_source(self, lines, doc, ctx):
        _ = ctx
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue

            probe = line_text_outside_excluded(line)
            if INPUT_MAG_SHORTHAND_RE.search(probe):
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Avoid introducing shorthand for input magnitude unless it "
                            "materially improves clarity."
                        ),
                        span=span_from_lines(line),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"pattern": "\\rho := \\|\\mathbf{u}\\|"}
                        ),
                        rewrite_tactics=(
                            "Keep the original expression unless the shorthand is reused enough to justify a new symbol.",
                        ),
                    )
                )
                continue

            for span in line.excluded_spans:
                if span.start_line != span.end_line:
                    continue
                raw_fragment = doc.source[span.start : span.end]
                if not _is_inline_math_fragment(raw_fragment):
                    continue
                if INPUT_MAG_SHORTHAND_RE.search(raw_fragment) is None:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Avoid introducing shorthand for input magnitude unless it "
                            "materially improves clarity."
                        ),
                        span=span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"pattern": "\\rho := \\|\\mathbf{u}\\|"}
                        ),
                        rewrite_tactics=(
                            "Keep the original expression unless the shorthand is reused enough to justify a new symbol.",
                        ),
                    )
                )
                break
        return violations


def _is_inline_math_fragment(text: str) -> bool:
    return text.startswith("$") and text.endswith("$") and not text.startswith("$$")


def register(registry) -> None:
    registry.add(ShorthandRule)
