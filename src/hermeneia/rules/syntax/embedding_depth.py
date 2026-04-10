"""Detect sentences with high syntactic embedding depth."""

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
from hermeneia.rules.common import iter_sentences, sentence_word_count, upstream_limits
from hermeneia.rules.patterns import compile_inline_phrase_regex

EMBEDDING_PUNCT_RE = re.compile(r"[,;:()—-]")


class EmbeddingDepthRule(AnnotatedRule):
    metadata = RuleMetadata(
        rule_id="syntax.embedding_depth",
        label="Sentence embedding depth is likely to require multiple reads",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={
            "max_dependency_depth": 5,
            "max_embedding_markers": 4,
            "min_sentence_words": 14,
        },
        abstain_when_flags=frozenset({"heavy_math_masking", "symbol_dense_sentence"}),
        evidence_fields=("signal_source", "dependency_depth", "embedding_markers"),
    )

    def check(self, doc, ctx):
        max_dependency_depth = self.settings.int_option("max_dependency_depth", 5)
        max_embedding_markers = self.settings.int_option("max_embedding_markers", 4)
        min_sentence_words = self.settings.int_option("min_sentence_words", 14)
        subordinate_markers = tuple(ctx.language_pack.lexicons.subordinate_clause_markers)
        subordinate_pattern = compile_inline_phrase_regex(subordinate_markers)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            if self.should_abstain(sentence.annotation_flags):
                continue
            if sentence_word_count(sentence) < min_sentence_words:
                continue
            depth = _dependency_depth(sentence.tokens)
            markers = _embedding_markers(sentence.projection.text, subordinate_pattern)
            if depth <= max_dependency_depth and markers <= max_embedding_markers:
                continue
            source = "dependency" if depth > 0 else "regex"
            score = float(max(depth, markers))
            threshold = float(
                max(max_dependency_depth, max_embedding_markers)
            )
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Sentence carries deep embedding and may require multiple passes "
                        "to parse."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={
                            "signal_source": source,
                            "dependency_depth": depth,
                            "embedding_markers": markers,
                        },
                        score=score,
                        threshold=threshold,
                        upstream_limits=upstream_limits(sentence),
                    ),
                    confidence=0.78 if source == "dependency" else 0.64,
                    rationale=(
                        "Embedding-depth checks combine dependency-tree depth with punctuation "
                        "and subordinate-marker density."
                    ),
                    rewrite_tactics=(
                        "Split the sentence so each clause carries one primary action.",
                    ),
                )
            )
        return violations


def _dependency_depth(tokens) -> int:
    if not tokens or not any(token.dep for token in tokens):
        return 0
    memo: dict[int, int] = {}
    stack: set[int] = set()

    def depth(index: int) -> int:
        if index in memo:
            return memo[index]
        token = tokens[index]
        head = token.head_idx
        if (
            head is None
            or head < 0
            or head >= len(tokens)
            or head == index
            or index in stack
        ):
            memo[index] = 1
            return 1
        stack.add(index)
        value = 1 + depth(head)
        stack.remove(index)
        memo[index] = value
        return value

    return max(depth(index) for index in range(len(tokens)))


def _embedding_markers(text: str, subordinate_pattern: re.Pattern[str]) -> int:
    punct = len(EMBEDDING_PUNCT_RE.findall(text))
    subordinate = sum(1 for _ in subordinate_pattern.finditer(text))
    return punct + subordinate


def register(registry) -> None:
    registry.add(EmbeddingDepthRule)

