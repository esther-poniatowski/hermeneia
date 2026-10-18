"""Rule reporting a restrictive relative clause written without its relativizer."""

from __future__ import annotations

from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import (
    clause_metadata,
    finding,
    prose_sentences,
    relative_clauses,
    token_span,
)


class MissingRelativePronounRule(AnnotatedRule):
    """Report a noun followed directly by the subject of its relative clause.

    In "the tests an answer must pass", a reader first parses "an answer" as a new constituent, and
    backtracks when the relative verb arrives.
    """

    metadata = clause_metadata(
        "syntax.missing_relative_pronoun", "Restrictive relative clause needs its pronoun"
    )

    def check(self, doc, ctx):
        """Report each relative clause with a subject and no relativizer.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per clause omitting its relativizer.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            tokens = sentence.tokens
            for clause in relative_clauses(tokens):
                if clause.relativizer is not None or clause.subject is None:
                    continue
                violations.append(
                    finding(
                        self,
                        token_span(tokens, clause.head, clause.verb),
                        "Insert 'that' after the noun: the relative clause omits its pronoun.",
                        "missing_relativizer",
                        "Write the pronoun, then reduce the clause to a participle where the sense allows.",
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
    registry.add(MissingRelativePronounRule)
