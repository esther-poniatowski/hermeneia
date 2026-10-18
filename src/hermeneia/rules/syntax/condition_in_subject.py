"""Rule reporting a condition packed into a restrictive relative clause inside the subject."""

from __future__ import annotations

from hermeneia.document.model import Token
from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import (
    SUBJECTS,
    children,
    clause_metadata,
    finding,
    lemma,
    prose_sentences,
    relative_clauses,
    root,
    token_span,
)

#: Determiners presenting the head noun as a case that may or may not occur.
INDEFINITE_DETERMINERS = frozenset({"a", "an", "any", "every", "no", "each"})


class ConditionInSubjectRule(AnnotatedRule):
    """Report an indefinite subject restricted by a relative clause, before the main verb.

    "A kind that no case can hold is listed" describes a case rather than a referent, yet no word
    of the sentence marks the subject as a case: the reader searches for an antecedent, finds none,
    and rereads. The rewrite states the condition as a clause, "When no case can hold a kind, …".
    """

    metadata = clause_metadata(
        "syntax.condition_in_subject", "Condition packed into a relative clause of the subject"
    )

    def check(self, doc, ctx):
        """Report each indefinite subject of a main verb when the subject carries a relative clause.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per conditional subject.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            tokens = sentence.tokens
            main = root(tokens)
            if main is None:
                continue
            for clause in relative_clauses(tokens):
                head = tokens[clause.head]
                if head.dep not in SUBJECTS or head.head_idx != main or clause.verb >= main:
                    continue
                if not _indefinite(tokens, clause.head):
                    continue
                violations.append(
                    finding(
                        self,
                        token_span(tokens, clause.head, clause.verb),
                        "The subject packs a condition: state it as a 'when' or 'if' clause, and the consequence as the main claim.",
                        "conditional_subject",
                        "Rewrite as 'When <condition>, <consequence>.'",
                    )
                )
        return violations


def _indefinite(tokens: list[Token], head: int) -> bool:
    """Whether a noun is indefinite: an indefinite determiner, or a bare plural."""
    determiners = [lemma(tokens[i]) for i in children(tokens, head) if tokens[i].dep == "det"]
    if determiners:
        return determiners[0] in INDEFINITE_DETERMINERS
    return tokens[head].text.lower().endswith("s") and tokens[head].pos == "NOUN"


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(ConditionInSubjectRule)
