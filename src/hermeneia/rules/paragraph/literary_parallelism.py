"""Experimental literary-parallelism diagnostics."""

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

WORD_RE = re.compile(r"[A-Za-z]+")


class LiteraryParallelismRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.literary_parallelism",
        label="Repeated rhetorical openings may dominate technical exposition",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.DIAGNOSTIC_METRIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("opening", "run_length"),
        experimental=True,
    )

    def check(self, doc, ctx):
        _ = ctx
        sentences = list(iter_sentences(doc))
        violations: list[Violation] = []
        if len(sentences) < 3:
            return violations
        run_opening: str | None = None
        run_start = 0
        run_length = 0
        for index, sentence in enumerate(sentences):
            opening = _opening(sentence.projection.text)
            if opening is None:
                run_opening = None
                run_length = 0
                continue
            if opening == run_opening:
                run_length += 1
            else:
                run_opening = opening
                run_start = index
                run_length = 1
            if run_length < 3 or run_opening is None:
                continue
            target = sentences[index]
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Three or more adjacent sentences repeat the opening '{run_opening}'.",
                    span=target.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "opening": run_opening,
                            "run_length": run_length,
                            "run_start_sentence_id": sentences[run_start].id,
                        }
                    ),
                    confidence=0.52,
                    rationale="Literary parallelism detection is experimental and intentionally conservative.",
                    rewrite_tactics=(
                        "Vary sentence openings when technical progression benefits from explicit differentiation.",
                    ),
                )
            )
        return violations


def _opening(text: str) -> str | None:
    words = [word.lower() for word in WORD_RE.findall(text)]
    if len(words) < 3:
        return None
    return " ".join(words[:2])


def register(registry) -> None:
    registry.add(LiteraryParallelismRule)

