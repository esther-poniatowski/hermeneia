"""Rule reporting a claim parked in a trailing ", which" clause."""

from __future__ import annotations

import re

from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import clause_metadata, finding, in_inline_code, prose_sentences

#: A non-restrictive relative clause, opened by a comma and "which".
TAIL_WHICH_RE = re.compile(r",\s+which\b", re.IGNORECASE)


class RelativeTailClaimRule(AnnotatedRule):
    """Report a non-restrictive ", which" clause.

    A claim placed in such a clause arrives after the reader has settled the meaning of the main
    clause, in the position reserved for incidental detail. A reader decides by deleting the clause:
    when the sentence loses its point, the clause carried the claim.
    """

    metadata = clause_metadata(
        "syntax.relative_tail_claim", "Claim parked in a trailing relative clause"
    )

    def check(self, doc, ctx):
        """Report each ", which" clause of a prose sentence.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per non-restrictive "which" clause.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            for match in TAIL_WHICH_RE.finditer(sentence.projection.text):
                which = next(
                    (t for t in sentence.tokens if t.projection_start > match.start()), None
                )
                if which is None or in_inline_code(sentence, which):
                    continue
                violations.append(
                    finding(
                        self,
                        which.source_span,
                        "Delete the ', which' clause: when the sentence loses its point, give the clause its own sentence.",
                        "tail_which",
                        "Promote the claim of the clause to a sentence with a named subject.",
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
    registry.add(RelativeTailClaimRule)
