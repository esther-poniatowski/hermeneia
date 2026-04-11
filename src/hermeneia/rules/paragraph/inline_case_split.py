"""Inline case-split checks."""

from __future__ import annotations

import re

from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_sentences

INLINE_CASE_SPLIT_RE = re.compile(
    r"\b(?:if|when)\b[^;]{0,220};\s*(?:if|when)\b",
    re.IGNORECASE,
)


class InlineCaseSplitRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.inline_case_split",
        label="Inline semicolon case splits should be rendered as lists",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pattern",),
    )

    def check(self, doc, ctx):
        _ = ctx
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            match = INLINE_CASE_SPLIT_RE.search(sentence.source_text)
            if match is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Distinct cases are packed inline; use a lead-in sentence and "
                        "bullet-case structure."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"pattern": match.group(0)}),
                    rewrite_tactics=(
                        "Convert semicolon-joined case clauses into explicit case bullets.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(InlineCaseSplitRule)
