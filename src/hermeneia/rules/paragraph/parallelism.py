"""List-item parallelism checks."""

from __future__ import annotations

import re

from hermeneia.document.model import BlockKind
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
from hermeneia.rules.common import iter_blocks

WORD_RE = re.compile(r"[A-Za-z]+")


class ParagraphParallelismRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="paragraph.parallelism",
        label="List items should be frame-parallel",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("actual_frame", "expected_frame", "list_size"),
    )

    def check(self, doc, ctx):
        _ = ctx
        violations: list[Violation] = []
        for list_block in iter_blocks(doc, {BlockKind.LIST}):
            items = [child for child in list_block.children if child.kind == BlockKind.LIST_ITEM]
            if len(items) < 3:
                continue
            frames = {item.id: _frame(item) for item in items}
            majority = _majority(tuple(frames.values()))
            if majority is None:
                continue
            for item in items:
                frame = frames[item.id]
                if frame == majority:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=f"List item frame '{frame}' diverges from dominant frame '{majority}'.",
                        span=item.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "actual_frame": frame,
                                "expected_frame": majority,
                                "list_size": len(items),
                            }
                        ),
                        confidence=0.62,
                        rationale="Parallelism is estimated from opening lexical frames in sibling list items.",
                        rewrite_tactics=(
                            "Align list-item openings to a shared grammatical frame.",
                        ),
                    )
                )
        return violations


def _frame(block) -> str:
    text = " ".join(sentence.projection.text for sentence in block.sentences).strip().lower()
    words = WORD_RE.findall(text)
    if not words:
        return "fragment"
    first = words[0]
    if first.endswith("ing"):
        return "gerund"
    if first in {"to"}:
        return "infinitive"
    if first in {"the", "a", "an"}:
        return "nominal"
    if first in {"if", "when", "while", "because"}:
        return "clausal"
    return "verbal_or_nominal"


def _majority(values: tuple[str, ...]) -> str | None:
    if not values:
        return None
    counts: dict[str, int] = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    winner, count = max(counts.items(), key=lambda pair: pair[1])
    if count < 2:
        return None
    return winner


def register(registry) -> None:
    registry.add(ParagraphParallelismRule)

