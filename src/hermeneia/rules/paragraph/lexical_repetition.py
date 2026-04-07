"""Paragraph-level lexical repetition diagnostics."""

from __future__ import annotations

from collections import Counter

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

STOPWORDS = frozenset(
    {
        "the",
        "a",
        "an",
        "and",
        "or",
        "of",
        "to",
        "in",
        "for",
        "on",
        "with",
        "by",
        "is",
        "are",
    }
)


class LexicalRepetitionRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="paragraph.lexical_repetition",
        label="Paragraph repeats the same lexical core excessively",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        default_options={"max_top_lemma_share": 0.3},
        evidence_fields=("top_lemma", "top_lemma_share", "token_count"),
    )

    def check(self, doc, ctx):
        max_share = self.settings.float_option("max_top_lemma_share", 0.3)
        violations: list[Violation] = []
        for block in iter_blocks(doc, {BlockKind.PARAGRAPH}):
            lemmas = _block_lemmas(block)
            if len(lemmas) < 8:
                continue
            counts = Counter(lemmas)
            lemma, count = counts.most_common(1)[0]
            share = count / len(lemmas)
            if share <= max_share:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=f"Paragraph repeats '{lemma}' in {share:.1%} of lexical tokens.",
                    span=block.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "top_lemma": lemma,
                            "top_lemma_share": round(share, 3),
                            "token_count": len(lemmas),
                        },
                        threshold=max_share,
                    ),
                    confidence=0.61,
                    rewrite_tactics=(
                        "Condense repeated phrasing and vary lexical realizations where meaning is unchanged.",
                    ),
                )
            )
        return violations


def _block_lemmas(block) -> list[str]:
    lemmas: list[str] = []
    for sentence in block.sentences:
        if sentence.tokens:
            lemmas.extend(
                token.lemma.lower()
                for token in sentence.tokens
                if token.lemma.isalpha() and token.lemma.lower() not in STOPWORDS
            )
        else:
            lemmas.extend(
                word.lower()
                for word in sentence.projection.text.split()
                if word.isalpha() and word.lower() not in STOPWORDS
            )
    return lemmas


def register(registry) -> None:
    registry.add(LexicalRepetitionRule)

