"""Detect long inline enumerations that should be converted to lists."""

from __future__ import annotations

import re

from hermeneia.rules.base import (
    AnnotatedRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_sentences

SEPARATOR_RE = re.compile(r"(?:,\s+|;\s+)")


class LongInlineEnumerationRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="syntax.long_inline_enumeration",
        label="Long inline enumerations should be split into list format",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_items": 4},
        evidence_fields=("item_count", "max_items"),
    )

    def check(self, doc, ctx):
        _ = ctx
        max_items = self.settings.int_option("max_items", 4)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            text = sentence.projection.text.strip()
            if not text:
                continue
            item_count = _estimated_item_count(text)
            if item_count <= max_items:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Inline enumeration has {item_count} items; move it to a lead-in "
                        "sentence plus bullet list."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"item_count": item_count, "max_items": max_items},
                        score=float(item_count),
                        threshold=float(max_items),
                    ),
                    rewrite_tactics=(
                        "Use one lead-in sentence followed by bullets instead of a long inlined series.",
                    ),
                )
            )
        return violations


def _estimated_item_count(text: str) -> int:
    separators = len(SEPARATOR_RE.findall(text))
    if not separators:
        return 1
    tail = text.rsplit(",", 1)[-1].lower()
    has_terminal_conjunction = " and " in tail or " or " in tail
    return separators + (1 if has_terminal_conjunction else 0) + 1


def register(registry) -> None:
    registry.add(LongInlineEnumerationRule)
