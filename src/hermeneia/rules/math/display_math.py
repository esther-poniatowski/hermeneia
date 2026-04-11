"""Display-math structure and lead-in checks."""

from __future__ import annotations

import re

from hermeneia.document.model import BlockKind
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

CONTENT_FREE_LEADIN_RE = re.compile(
    r"^(?:therefore|hence|then|this gives|more explicitly|equivalently|rewriting)\s*:?\s*$",
    re.IGNORECASE,
)
TRAILING_PUNCTUATION_RE = re.compile(r"[.,;:!?]\s*$")
PUNCTUATION_BEFORE_LINEBREAK_RE = re.compile(r"[.,;:!?]\s*\\\\\s*$")


class DisplayMathRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="math.display_math",
        label="Display math must have a meaningful lead-in and no line-break punctuation",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        default_options={"require_leadin": True},
        evidence_fields=("check",),
    )

    def check_source(self, lines, doc, ctx):
        violations: list[Violation] = []
        require_leadin = bool(self.settings.options.get("require_leadin", True))
        source_lines = doc.source_lines
        for block in doc.iter_blocks():
            if block.kind != BlockKind.DISPLAY_MATH:
                continue
            block_lines = source_lines[block.span.start_line - 1 : block.span.end_line]
            inner_lines = [
                line.text.strip()
                for line in block_lines
                if line.text.strip() and line.text.strip() != "$$"
            ]
            punctuation_issue = _display_punctuation_issue(inner_lines)
            if punctuation_issue is not None:
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Move punctuation out of display math when it appears at line ends "
                            "or directly before LaTeX line breaks."
                        ),
                        span=block.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(features={"check": punctuation_issue}),
                        rewrite_tactics=(
                            "Move punctuation into the surrounding prose rather than leaving it inside the $$...$$ block.",
                        ),
                    )
                )
            if require_leadin:
                leadin = _previous_nonempty_line(
                    source_lines, block.span.start_line - 1
                )
                if leadin is None or CONTENT_FREE_LEADIN_RE.search(leadin.text.strip()):
                    span = block.span if leadin is None else leadin.span
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message="Display math should be introduced by a non-empty explanatory lead-in sentence.",
                            span=span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={"check": "missing_or_content_free_leadin"}
                            ),
                            rewrite_tactics=(
                                "Name the quantity, operation, or argumentative role before the display equation.",
                            ),
                        )
                    )
        return violations


def _previous_nonempty_line(lines, before_line_number: int):
    for index in range(before_line_number - 1, -1, -1):
        if lines[index].text.strip():
            return lines[index]
    return None


def _display_punctuation_issue(inner_lines: list[str]) -> str | None:
    for line in inner_lines:
        if PUNCTUATION_BEFORE_LINEBREAK_RE.search(line):
            return "punctuation_before_linebreak"
        if TRAILING_PUNCTUATION_RE.search(line):
            return "trailing_line_punctuation"
    return None


def register(registry) -> None:
    registry.add(DisplayMathRule)
