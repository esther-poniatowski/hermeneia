"""Concept-reference drift within a paragraph."""

from __future__ import annotations

import re

from hermeneia.document.model import BlockKind
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
from hermeneia.rules.common import iter_blocks

LABEL_RE = re.compile(
    r"\b(?:the|this|that)\s+"
    r"(method|approach|framework|strategy|procedure|technique|model|pipeline|scheme|mechanism|argument|proof)\b",
    re.IGNORECASE,
)


class ConceptReferenceDriftRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.concept_reference_drift",
        label="Paragraph varies concept labels in ways that may obscure referential stability",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={
            "min_distinct_labels": 3,
            "min_sentence_count": 3,
            "min_average_overlap": 0.35,
        },
        evidence_fields=("labels", "sentence_ids", "average_overlap"),
    )

    def check(self, doc, ctx):
        min_distinct_labels = self.settings.int_option("min_distinct_labels", 3)
        min_sentence_count = self.settings.int_option("min_sentence_count", 3)
        min_average_overlap = self.settings.float_option("min_average_overlap", 0.35)
        violations: list[Violation] = []
        for block in iter_blocks(doc, {BlockKind.PARAGRAPH}):
            if len(block.sentences) < min_sentence_count:
                continue
            label_mentions: dict[str, set[str]] = {}
            for sentence in block.sentences:
                labels = {
                    match.group(1).lower()
                    for match in LABEL_RE.finditer(sentence.projection.text)
                }
                if labels:
                    label_mentions[sentence.id] = labels
            if len(label_mentions) < 2:
                continue
            distinct_labels = sorted({label for labels in label_mentions.values() for label in labels})
            if len(distinct_labels) < min_distinct_labels:
                continue

            sentence_ids = sorted(label_mentions)
            overlaps: list[float] = []
            for left_index, left_id in enumerate(sentence_ids):
                for right_id in sentence_ids[left_index + 1 :]:
                    overlaps.append(ctx.features.sentence_overlap(left_id, right_id))
            if not overlaps:
                continue
            average_overlap = sum(overlaps) / len(overlaps)
            if average_overlap < min_average_overlap:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "The paragraph alternates labels for likely the same concept, which "
                        "can weaken referential stability."
                    ),
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "labels": tuple(distinct_labels),
                            "sentence_ids": tuple(sentence_ids),
                            "average_overlap": round(average_overlap, 3),
                        },
                        score=round(average_overlap, 3),
                        threshold=min_average_overlap,
                    ),
                    confidence=max(0.58, min(0.86, average_overlap)),
                    rationale=(
                        "Concept-reference drift uses label churn plus sentence-overlap "
                        "corroboration to estimate when varied labels likely refer to the same "
                        "underlying concept."
                    ),
                    rewrite_tactics=(
                        "Choose one canonical label for the concept and keep alternatives for "
                        "genuinely distinct entities only.",
                    ),
                )
            )
        return violations


def register(registry) -> None:
    registry.add(ConceptReferenceDriftRule)
