"""Rule reporting a sentence adverbial placed inside its own clause."""

from __future__ import annotations

from hermeneia.rules.base import AnnotatedRule, Layer
from hermeneia.rules.clauses import (
    clause_metadata,
    finding,
    first_word,
    in_inline_code,
    lemma,
    prose_sentences,
)

#: Adverbials relating a sentence to the previous sentence, due at the front of the sentence.
SENTENCE_ADVERBIALS = frozenset(
    {"therefore", "moreover", "however", "thus", "hence", "consequently", "instead", "then"}
)
#: Words before "then" that make it a temporal adverb or the second half of a conditional.
THEN_COMPANIONS = frozenset(
    {"and", "but", "or", "since", "until", "by", "from", "only", "even", "just"}
)
#: Words opening a conditional or temporal clause: after one of them, "then" may introduce the consequence.
CONDITIONALS = frozenset({"if", "when", "once", "whenever"})
#: Punctuation after which an adverbial opens a clause of its own.
CLAUSE_BREAKS = frozenset({";", ":", "—", "("})


class AdverbialPositionRule(AnnotatedRule):
    """Report a sentence adverbial reached in the middle of its sentence.

    "A researcher writing a law therefore names …" relates two sentences, yet the relation arrives
    after the reader has parsed the clause carrying it. The adverbial belongs at the boundary:
    "Therefore, a researcher …".
    """

    metadata = clause_metadata(
        "linkage.adverbial_position",
        "Sentence adverbial belongs at the front of its sentence",
        layer=Layer.LOCAL_DISCOURSE,
    )

    def check(self, doc, ctx):
        """Report each sentence adverbial preceded by a word of its own clause.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per adverbial placed inside its clause.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            tokens = sentence.tokens
            start = first_word(tokens)
            for index, token in enumerate(tokens):
                word = token.text.lower()
                if word not in SENTENCE_ADVERBIALS or start is None or index <= start:
                    continue
                if tokens[index - 1].text in CLAUSE_BREAKS or in_inline_code(sentence, token):
                    continue
                if not _frames_clause(tokens, index):
                    continue
                violations.append(
                    finding(
                        self,
                        token.source_span,
                        f"Move '{token.text}' to the front of its sentence: it relates this sentence to the previous one.",
                        "adverbial_inside_clause",
                        f"Rewrite as '{token.text.capitalize()}, …' at the start of the sentence.",
                    )
                )
        return violations


def _frames_clause(tokens, index: int) -> bool:
    """Whether an adverbial relates its sentence to the previous sentence, rather than modifying a word."""
    word = tokens[index].text.lower()
    following = tokens[index + 1] if index + 1 < len(tokens) else None
    if word == "instead" and (
        following is None or not following.text[:1].isalpha() or following.text.lower() == "of"
    ):
        return False
    if word == "however" and following is not None and following.pos in {"ADJ", "ADV"}:
        return False
    if word == "then":
        if lemma(tokens[index - 1]) in THEN_COMPANIONS or tokens[index - 1].text == ",":
            return False
        if any(lemma(token) in CONDITIONALS for token in tokens[:index]):
            return False
    return True


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(AdverbialPositionRule)
