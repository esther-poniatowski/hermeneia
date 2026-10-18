"""Rule reporting a noun phrase that carries an object relative clause."""

from __future__ import annotations

from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import (
    clause_metadata,
    finding,
    prose_sentences,
    relative_clauses,
    token_span,
)


class ObjectRelativeRule(AnnotatedRule):
    """Report a relative clause whose head noun fills its object slot.

    In "the specifications that each layer fixes", a new subject intervenes, so the reader holds two
    noun phrases and an unresolved dependency until the relative verb arrives. A clause omitting its
    relativizer is reported by ``syntax.missing_relative_pronoun`` instead.
    """

    metadata = clause_metadata(
        "syntax.object_relative", "Noun phrase carries an object relative clause"
    )

    def check(self, doc, ctx):
        """Report each relative clause holding a relativizer followed by a distinct subject.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per object relative.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            tokens = sentence.tokens
            for clause in relative_clauses(tokens):
                if clause.relativizer is None or clause.subject is None:
                    continue
                if tokens[clause.relativizer].text.lower() == "whose":
                    continue
                if clause.subject < clause.relativizer:
                    continue
                violations.append(
                    finding(
                        self,
                        token_span(tokens, clause.head, clause.verb),
                        "Object relative: the head noun is the object of the clause, and a new subject intervenes.",
                        "object_relative",
                        "Reduce the clause to a participle, turn the relation round, or promote it to a sentence.",
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
    registry.add(ObjectRelativeRule)
