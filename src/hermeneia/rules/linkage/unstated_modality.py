"""Rule asking whether a consequence states its modality."""

from __future__ import annotations

from hermeneia.rules.base import AnnotatedRule, Layer, Severity
from hermeneia.rules.clauses import (
    MODALS,
    children,
    clause_metadata,
    finding,
    first_word,
    lemma,
    prose_sentences,
    root,
)

#: Adverbials announcing a consequence.
CONSEQUENCE_MARKERS = frozenset({"therefore", "so", "thus", "hence", "consequently"})


class UnstatedModalityRule(AnnotatedRule):
    """Report a consequence whose main verb carries no modal.

    "Therefore, a researcher names only the declared quantities" reads as a report of fact, although
    the sentence may state an obligation or a possibility. A finding is a question: a fact or a
    definition takes the indicative.
    """

    metadata = clause_metadata(
        "linkage.unstated_modality",
        "Check that a consequence states its modality",
        severity=Severity.INFO,
        layer=Layer.LOCAL_DISCOURSE,
    )

    def check(self, doc, ctx):
        """Report each sentence opening on a consequence marker whose main verb has no modal.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One finding per consequence in the indicative.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            tokens = sentence.tokens
            start = first_word(tokens)
            if start is None or tokens[start].text.lower() not in CONSEQUENCE_MARKERS:
                continue
            main = root(tokens)
            if main is None or any(lemma(tokens[i]) in MODALS for i in children(tokens, main)):
                continue
            violations.append(
                finding(
                    self,
                    tokens[main].source_span,
                    "Consequence in the indicative: write 'must' for a requirement or 'can' for a possibility, unless it states a fact.",
                    "consequence_without_modal",
                    "Ask whether the sentence reports, obliges or permits, and choose the modal accordingly.",
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
    registry.add(UnstatedModalityRule)
