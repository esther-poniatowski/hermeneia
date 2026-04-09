"""Hard check for bare pronoun openings after display equations."""

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

LEADING_PRONOUN_RE = re.compile(r"^\s*(it|this|they|these)\b", re.IGNORECASE)
FIRST_WORD_RE = re.compile(r"^[A-Za-z]+")
PREDICATE_STARTERS = frozenset(
    {
        "is",
        "are",
        "was",
        "were",
        "be",
        "being",
        "been",
        "can",
        "could",
        "may",
        "might",
        "must",
        "should",
        "would",
        "will",
        "do",
        "does",
        "did",
        "has",
        "have",
        "had",
        "follows",
        "follow",
        "gives",
        "give",
        "shows",
        "show",
        "implies",
        "imply",
        "yields",
        "yield",
        "means",
        "mean",
        "holds",
        "hold",
        "states",
        "state",
        "demonstrates",
        "demonstrate",
        "proves",
        "prove",
        "indicates",
        "indicate",
        "suggests",
        "suggest",
    }
)


class BarePronounAfterDisplayRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="math.bare_pronoun_after_display",
        label="Avoid bare pronoun openings after display equations",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pronoun", "signal"),
    )

    def check(self, doc, ctx):
        interpretive_nouns = frozenset(
            noun.lower() for noun in ctx.language_pack.lexicons.display_interpretive_nouns
        )
        flat_blocks = list(doc.iter_blocks())
        violations: list[Violation] = []
        for index, block in enumerate(flat_blocks):
            if block.kind != BlockKind.DISPLAY_MATH:
                continue
            followup_sentence = _next_followup_sentence(flat_blocks, index)
            if followup_sentence is None:
                continue
            signal = _bare_pronoun_signal(
                followup_sentence,
                interpretive_nouns=interpretive_nouns,
            )
            if signal is None:
                continue
            pronoun = _leading_pronoun(followup_sentence.projection.text)
            if pronoun is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Sentence after display math opens with a bare pronoun; "
                        "name the object (equation, bound, ratio, expression) explicitly."
                    ),
                    span=followup_sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"pronoun": pronoun, "signal": signal}),
                    confidence=0.95 if pronoun in {"it", "they"} else 0.9,
                    rewrite_tactics=(
                        "Replace the pronoun opener with a noun phrase that names what the equation does.",
                    ),
                )
            )
        return violations


def _next_followup_sentence(blocks, display_index: int):
    for index in range(display_index + 1, len(blocks)):
        block = blocks[index]
        if block.kind in {BlockKind.PARAGRAPH, BlockKind.BLOCK_QUOTE, BlockKind.LIST_ITEM}:
            return block.sentences[0] if block.sentences else None
        if block.kind in {BlockKind.HEADING, BlockKind.DISPLAY_MATH, BlockKind.CODE_BLOCK}:
            return None
    return None


def _bare_pronoun_signal(sentence, *, interpretive_nouns: frozenset[str]) -> str | None:
    if sentence.tokens:
        return _token_signal(sentence.tokens, interpretive_nouns=interpretive_nouns)
    return _text_signal(sentence.projection.text, interpretive_nouns=interpretive_nouns)


def _token_signal(tokens, *, interpretive_nouns: frozenset[str]) -> str | None:
    first = _token_word(tokens[0])
    if first not in {"it", "this", "they", "these"}:
        return None
    if first in {"it", "they"}:
        return "bare_pronoun_subject"
    if len(tokens) == 1:
        return "demonstrative_without_head"
    second = tokens[1]
    second_word = _token_word(second)
    second_pos = (second.pos or "").upper()
    if second_pos in {"AUX", "VERB"} or second_word in PREDICATE_STARTERS:
        return "demonstrative_followed_by_predicate"
    if second_pos in {"NOUN", "PROPN"} or second_word in interpretive_nouns:
        return None
    if second_pos in {"ADJ", "NUM"} and len(tokens) >= 3:
        third = tokens[2]
        third_word = _token_word(third)
        third_pos = (third.pos or "").upper()
        if third_pos in {"NOUN", "PROPN"} or third_word in interpretive_nouns:
            return None
    if second_pos in {"DET", "PRON", "ADP", "ADV", "CCONJ", "SCONJ", "PART"}:
        return "demonstrative_without_head"
    return None


def _text_signal(text: str, *, interpretive_nouns: frozenset[str]) -> str | None:
    pronoun = _leading_pronoun(text)
    if pronoun is None:
        return None
    if pronoun in {"it", "they"}:
        return "bare_pronoun_subject"
    matched = LEADING_PRONOUN_RE.match(text)
    if matched is None:
        return None
    remainder = text[matched.end() :].lstrip()
    if not remainder:
        return "demonstrative_without_head"
    first_word_match = FIRST_WORD_RE.match(remainder)
    if first_word_match is None:
        return "demonstrative_without_head"
    next_word = first_word_match.group(0).lower()
    if next_word in interpretive_nouns:
        return None
    if next_word in PREDICATE_STARTERS:
        return "demonstrative_followed_by_predicate"
    return None


def _leading_pronoun(text: str) -> str | None:
    match = LEADING_PRONOUN_RE.match(text)
    if match is None:
        return None
    return match.group(1).lower()


def _token_word(token) -> str:
    return (token.text or token.lemma or "").lower()


def register(registry) -> None:
    registry.add(BarePronounAfterDisplayRule)
