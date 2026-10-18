"""Rule reporting a claim compressed into a chain of copulas."""

from __future__ import annotations

import re

from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import clause_metadata, finding, in_inline_code, prose_sentences

#: "X is a Y, and a Y is …": the second copula restarts on the predicate of the first.
COPULA_CHAIN_RE = re.compile(
    r"\bis\s+(?:a|an|the)\s+(?P<term>[a-z][\w-]*),?\s+and\s+(?:a|an|the|every)\s+(?P=term)\s+is\b",
    re.IGNORECASE,
)


class AphorismRule(AnnotatedRule):
    """Report a chain of copulas, the commonest construction of an aphorism.

    "A proposed answer is a model, and a model is a system" compresses an argument into a memorable
    form, and leaves the reader to reconstruct the claim that it stands for.
    """

    metadata = clause_metadata(
        "vocabulary.aphorism", "State the claim literally, not as an aphorism"
    )

    def check(self, doc, ctx):
        """Report each chain of copulas restarting on the predicate of the first one.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per chain.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            for match in COPULA_CHAIN_RE.finditer(sentence.projection.text):
                token = next(
                    (t for t in sentence.tokens if t.projection_start >= match.start()), None
                )
                if token is None or in_inline_code(sentence, token):
                    continue
                violations.append(
                    finding(
                        self,
                        token.source_span,
                        "Chain of copulas: state the claim literally, with the mechanism it stands for.",
                        "copula_chain",
                        "Replace the chain by the relation it compresses, stated once.",
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
    registry.add(AphorismRule)
