"""Rule asking whether a sentence opening on an indefinite article keeps the topic of its paragraph."""

from __future__ import annotations

from hermeneia.rules.base import AnnotatedRule, Layer, Severity
from hermeneia.rules.clauses import (
    SUBJECTS,
    clause_metadata,
    finding,
    first_word,
    lemma,
    prose_sentences,
)


class IndefiniteOpeningRule(AnnotatedRule):
    """Report a sentence whose subject opens on "a" or "an", after the first sentence of its block.

    An indefinite subject presents an entity as new, so it is the usual surface form of a subject
    that drifts from the topic left open by the previous sentence. A finding is a question: the
    subject is correct wherever the paragraph genuinely introduces the entity there.
    """

    metadata = clause_metadata(
        "linkage.indefinite_opening",
        "Check that an indefinite subject keeps the topic",
        severity=Severity.INFO,
        layer=Layer.LOCAL_DISCOURSE,
    )

    def check(self, doc, ctx):
        """Report each non-initial sentence of a block opening on an indefinite subject.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One finding per indefinite opening.
        """
        _ = ctx
        violations = []
        for _block, position, sentence in prose_sentences(doc):
            if position == 0:
                continue
            tokens = sentence.tokens
            start = first_word(tokens)
            if start is None or lemma(tokens[start]) not in {"a", "an"}:
                continue
            noun = tokens[start].head_idx
            if noun is None or tokens[noun].dep not in SUBJECTS:
                continue
            violations.append(
                finding(
                    self,
                    tokens[start].source_span,
                    "Indefinite subject: check that it carries the topic left open by the previous sentence.",
                    "indefinite_subject",
                    "Name the topic left open by the previous sentence, and make it the subject.",
                    confidence=0.4,
                )
            )
        return violations


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(IndefiniteOpeningRule)
