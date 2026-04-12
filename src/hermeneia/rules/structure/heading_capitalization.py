"""Sibling-heading capitalization consistency checks."""

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

WORD_RE = re.compile(r"[A-Za-z]+")


class HeadingCapitalizationRule(HeuristicSemanticRule):
    """Headingcapitalizationrule."""

    metadata = RuleMetadata(
        rule_id="structure.heading_capitalization",
        label="Sibling headings should share capitalization convention",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("actual_style", "expected_style", "level"),
    )

    def check(self, doc, ctx):
        """Check."""
        _ = doc
        violations: list[Violation] = []
        for level in range(1, 7):
            for headings in ctx.features.sibling_heading_groups(level):
                if len(headings) < 2:
                    continue
                styles = {
                    heading.id: _style(
                        " ".join(
                            sentence.projection.text for sentence in heading.sentences
                        )
                    )
                    for heading in headings
                }
                expected = _majority(tuple(styles.values()))
                if expected is None:
                    continue
                for heading in headings:
                    actual = styles[heading.id]
                    if actual == expected:
                        continue
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "Heading capitalization style "
                                f"'{actual}' diverges from sibling style '{expected}'."
                            ),
                            span=heading.span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "actual_style": actual,
                                    "expected_style": expected,
                                    "level": level,
                                }
                            ),
                            confidence=0.8,
                            rewrite_tactics=(
                                "Normalize heading capitalization across siblings "
                                "at the same level.",
                            ),
                        )
                    )
        return violations


def _style(text: str) -> str:
    """Style."""
    words = WORD_RE.findall(text)
    if not words:
        return "empty"
    if all(word.isupper() for word in words):
        return "all_caps"
    if words[0][0].isupper() and all(word[0].islower() for word in words[1:]):
        return "sentence_case"
    if all(word[0].isupper() for word in words if len(word) > 3):
        return "title_like"
    return "mixed"


def _majority(values: tuple[str, ...]) -> str | None:
    """Majority."""
    if len(values) == 2 and values[0] != values[1]:
        return values[0]
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return None
    winner, count = max(counts.items(), key=lambda item: item[1])
    return winner if count > 1 else None


def register(registry) -> None:
    """Register."""
    registry.add(HeadingCapitalizationRule)
