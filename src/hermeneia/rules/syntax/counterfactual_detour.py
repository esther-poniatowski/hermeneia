"""Rule reporting a fact established through the behavior of an unrealized alternative."""

from __future__ import annotations

import re

from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import clause_metadata, finding, in_inline_code, prose_sentences

#: Stacked modals and conditionals describing an alternative that did not happen.
COUNTERFACTUAL_RE = re.compile(
    r"\bwould\s+(?:have|require)\b|\bhad\s+(?:\w+\s+){1,3}been\b", re.IGNORECASE
)


class CounterfactualDetourRule(AnnotatedRule):
    """Report a counterfactual construction outside a question.

    "A parallel vocabulary would have had to draw its own distinctions" describes the behavior of an
    unrealized alternative, and leaves the reader to recover the actual fact. When the
    counterfactual is itself the content, as in a what-if analysis or a proof by contradiction, the
    reader of the finding admits it.
    """

    metadata = clause_metadata(
        "syntax.counterfactual_detour", "State the fact, not an unrealized alternative"
    )

    def check(self, doc, ctx):
        """Report each counterfactual construction of a declarative sentence.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per counterfactual construction.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            text = sentence.projection.text
            if text.rstrip().endswith("?"):
                continue
            for match in COUNTERFACTUAL_RE.finditer(text):
                token = next(
                    (t for t in sentence.tokens if t.projection_start >= match.start()), None
                )
                if token is None or in_inline_code(sentence, token):
                    continue
                violations.append(
                    finding(
                        self,
                        token.source_span,
                        f"Counterfactual '{match.group(0)}': state the actual fact that the detour implies.",
                        "counterfactual",
                        "Delete the hypothetical, then state what the sentence claims about the actual object.",
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
    registry.add(CounterfactualDetourRule)
