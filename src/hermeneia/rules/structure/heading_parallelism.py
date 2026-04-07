"""Sibling-heading frame consistency heuristics."""

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


class HeadingParallelismRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="structure.heading_parallelism",
        label="Sibling headings are not frame-parallel",
        layer=Layer.DOCUMENT_STRUCTURE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("actual_frame", "expected_frame", "level"),
    )

    def check(self, doc, ctx):
        violations: list[Violation] = []
        for level in range(1, 7):
            for headings in ctx.features.sibling_heading_groups(level):
                if len(headings) < 2:
                    continue
                frames = {
                    heading.id: _heading_frame(
                        " ".join(sentence.projection.text for sentence in heading.sentences)
                    )
                    for heading in headings
                }
                majority = _majority(tuple(frames.values()))
                if majority is None:
                    continue
                for heading in headings:
                    frame = frames[heading.id]
                    if frame == majority:
                        continue
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=f"Heading frame '{frame}' diverges from sibling pattern '{majority}'.",
                            span=heading.span,
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "actual_frame": frame,
                                    "expected_frame": majority,
                                    "level": level,
                                }
                            ),
                            confidence=0.65,
                            rationale="Heading parallelism compares sibling heading frames only within the same level.",
                            rewrite_tactics=(
                                "Normalize sibling headings to a common nominal, gerund, or clausal frame.",
                            ),
                        ),
                    )
        return violations


def _heading_frame(text: str) -> str:
    probe = text.strip().lower()
    if probe.endswith("?"):
        return "question"
    words = re.findall(r"[a-z]+", probe)
    if not words:
        return "fragment"
    if words[0].endswith("ing"):
        return "gerund"
    if words[0] in {"how", "why", "when"}:
        return "clausal"
    if any(word in {"is", "are", "does", "do"} for word in words[:3]):
        return "clausal"
    return "nominal"


def _majority(values: tuple[str, ...]) -> str | None:
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    if not counts:
        return None
    winner = max(counts.items(), key=lambda item: item[1])
    return winner[0]


def register(registry) -> None:
    registry.add(HeadingParallelismRule)
