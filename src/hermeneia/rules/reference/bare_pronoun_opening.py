"""Hard rule for bare pronoun sentence openings in prose."""

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

PROSE_BLOCK_KINDS = {
    BlockKind.HEADING,
    BlockKind.PARAGRAPH,
    BlockKind.LIST_ITEM,
    BlockKind.BLOCK_QUOTE,
    BlockKind.TABLE_CELL,
    BlockKind.FOOTNOTE,
    BlockKind.ADMONITION,
}

FIRST_WORD_RE = re.compile(r"^[A-Za-z]+")


class BarePronounOpeningRule(AnnotatedRule):
    """Barepronounopeningrule."""

    metadata = RuleMetadata(
        rule_id="reference.bare_pronoun_opening",
        label="Avoid bare pronoun sentence openings",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pronoun", "signal"),
    )

    def check(self, doc, ctx):
        """Check."""
        openers = frozenset(
            word.lower() for word in ctx.language_pack.lexicons.bare_pronoun_openers
        )
        predicate_starters = frozenset(
            word.lower()
            for word in ctx.language_pack.lexicons.bare_pronoun_predicate_starters
        )
        explicit_heads = frozenset(
            word.lower()
            for word in (
                tuple(ctx.language_pack.lexicons.display_interpretive_nouns)
                + tuple(ctx.language_pack.lexicons.transition_reference_heads)
            )
        )
        violations: list[Violation] = []
        for block in doc.iter_blocks():
            if block.kind not in PROSE_BLOCK_KINDS:
                continue
            for sentence in block.sentences:
                signal = _bare_pronoun_signal(
                    sentence,
                    openers=openers,
                    predicate_starters=predicate_starters,
                    explicit_heads=explicit_heads,
                )
                if signal is None:
                    continue
                pronoun = _leading_pronoun(sentence.projection.text, openers)
                if pronoun is None:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Sentence opens with a bare pronoun; replace it with a descriptive "
                            "noun phrase."
                        ),
                        span=sentence.span,
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"pronoun": pronoun, "signal": signal},
                        ),
                        confidence=0.95 if pronoun in {"it", "they"} else 0.9,
                        rewrite_tactics=(
                            "Name the specific object, claim, equation, or constraint in the subject phrase.",
                        ),
                    )
                )
        return violations


def _bare_pronoun_signal(
    sentence,
    *,
    openers: frozenset[str],
    predicate_starters: frozenset[str],
    explicit_heads: frozenset[str],
) -> str | None:
    """Bare pronoun signal."""
    if sentence.tokens:
        return _token_signal(
            sentence.tokens,
            openers=openers,
            predicate_starters=predicate_starters,
            explicit_heads=explicit_heads,
        )
    return _text_signal(
        sentence.projection.text,
        openers=openers,
        predicate_starters=predicate_starters,
        explicit_heads=explicit_heads,
    )


def _token_signal(
    tokens,
    *,
    openers: frozenset[str],
    predicate_starters: frozenset[str],
    explicit_heads: frozenset[str],
) -> str | None:
    """Token signal."""
    first = _token_word(tokens[0])
    if first not in openers:
        return None
    if first in {"it", "they"}:
        return "bare_pronoun_subject"
    if len(tokens) == 1:
        return "demonstrative_without_head"
    second = tokens[1]
    second_word = _token_word(second)
    second_pos = (second.pos or "").upper()
    if second_pos in {"AUX", "VERB"} or second_word in predicate_starters:
        return "demonstrative_followed_by_predicate"
    if second_pos in {"NOUN", "PROPN"} or second_word in explicit_heads:
        return None
    if second_pos in {"ADJ", "NUM"} and len(tokens) >= 3:
        third = tokens[2]
        third_word = _token_word(third)
        third_pos = (third.pos or "").upper()
        if third_pos in {"NOUN", "PROPN"} or third_word in explicit_heads:
            return None
    if second_pos in {"DET", "PRON", "ADP", "ADV", "CCONJ", "SCONJ", "PART"}:
        return "demonstrative_without_head"
    return None


def _text_signal(
    text: str,
    *,
    openers: frozenset[str],
    predicate_starters: frozenset[str],
    explicit_heads: frozenset[str],
) -> str | None:
    """Text signal."""
    pronoun = _leading_pronoun(text, openers)
    if pronoun is None:
        return None
    if pronoun in {"it", "they"}:
        return "bare_pronoun_subject"
    remainder = text[len(text) - len(text.lstrip()) :]
    opener_match = FIRST_WORD_RE.search(remainder)
    if opener_match is None:
        return "demonstrative_without_head"
    remainder = remainder[opener_match.end() :].lstrip()
    if not remainder:
        return "demonstrative_without_head"
    next_word_match = FIRST_WORD_RE.match(remainder)
    if next_word_match is None:
        return "demonstrative_without_head"
    next_word = next_word_match.group(0).lower()
    if next_word in explicit_heads:
        return None
    if next_word in predicate_starters:
        return "demonstrative_followed_by_predicate"
    return None


def _leading_pronoun(text: str, openers: frozenset[str]) -> str | None:
    """Leading pronoun."""
    match = FIRST_WORD_RE.search(text)
    if match is None:
        return None
    word = match.group(0).lower()
    return word if word in openers else None


def _token_word(token) -> str:
    """Token word."""
    return (token.text or token.lemma or "").lower()


def register(registry) -> None:
    """Register."""
    registry.add(BarePronounOpeningRule)
