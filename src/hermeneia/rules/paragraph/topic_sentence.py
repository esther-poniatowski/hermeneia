"""Topic-sentence heuristics."""

from __future__ import annotations

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
from hermeneia.rules.patterns import compile_leading_phrase_regex


class TopicSentenceRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.topic_sentence",
        label="Paragraph lacks a strong topic sentence",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"minimum_score": 0.45},
        evidence_fields=("first_score", "second_score", "sentence_count"),
    )

    def check(self, doc, ctx):
        threshold = self.settings.float_option("minimum_score", 0.45)
        transitional_openers = tuple(ctx.language_pack.lexicons.topic_sentence_openers)
        opener_pattern = compile_leading_phrase_regex(transitional_openers)
        violations: list[Violation] = []
        for block in iter_blocks(doc, {BlockKind.PARAGRAPH}):
            if len(block.sentences) < 2:
                continue
            first, second = block.sentences[0], block.sentences[1]
            first_score = self._score_candidate(
                first, block, ctx, position_bonus=0.35, opener_pattern=opener_pattern
            )
            second_score = self._score_candidate(
                second, block, ctx, position_bonus=0.30, opener_pattern=opener_pattern
            )
            best_score = max(first_score, second_score)
            if best_score >= threshold:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message="The paragraph’s opening sentences do not establish a strong topic frame for what follows.",
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "first_score": round(first_score, 3),
                            "second_score": round(second_score, 3),
                            "sentence_count": len(block.sentences),
                        },
                        score=round(best_score, 3),
                        threshold=threshold,
                    ),
                    confidence=0.65,
                    rationale="Topic-sentence detection is a bounded heuristic combining early position and lexical centrality.",
                    rewrite_tactics=(
                        "Open the paragraph with the paragraph’s governing claim, object, or question before elaboration or examples.",
                    ),
                )
            )
        return violations

    def _score_candidate(
        self,
        sentence,
        block,
        ctx,
        position_bonus: float,
        opener_pattern,
    ) -> float:
        if opener_pattern.search(sentence.source_text):
            position_bonus -= 0.15
        others = [other for other in block.sentences if other.id != sentence.id]
        overlap = (
            0.0
            if not others
            else sum(ctx.features.sentence_overlap(sentence.id, other.id) for other in others)
            / len(others)
        )
        return max(0.0, min(1.0, position_bonus + overlap))


def register(registry) -> None:
    registry.add(TopicSentenceRule)
