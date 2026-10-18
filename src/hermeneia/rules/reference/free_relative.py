"""Rule reporting a clause or a pronoun standing where a sentence must name its object."""

from __future__ import annotations

import re

from hermeneia.rules.base import AnnotatedRule
from hermeneia.rules.clauses import clause_metadata, finding, in_inline_code, lemma, prose_sentences

#: Words heading a free relative.
FREE_RELATIVE_WORDS = frozenset({"what", "whatever", "whichever"})
#: Verbs of asking or knowing, whose indirect question names no object by design.
QUESTION_VERBS = frozenset(
    {
        "ask",
        "check",
        "decide",
        "determine",
        "examine",
        "explain",
        "find",
        "know",
        "learn",
        "record",
        "report",
        "see",
        "show",
        "specify",
        "state",
        "tell",
        "test",
        "understand",
        "verify",
        "wonder",
    }
)
#: "the one" or "the ones" in place of a noun, except in "on the one hand".
THE_ONE_RE = re.compile(r"\bthe\s+ones?\b(?!\s+hand\b)(?!-)", re.IGNORECASE)


class FreeRelativeRule(AnnotatedRule):
    """Report a free relative or the pronoun "the one" standing for an unnamed object.

    "What a candidate proposes is a system" names the object by its role in a clause, so
    the reader parses the clause before learning what the sentence is about. An indirect question
    completing a verb of asking or knowing ("records what changed") is admitted.
    """

    metadata = clause_metadata(
        "reference.free_relative", "Name the object instead of a free relative"
    )

    def check(self, doc, ctx):
        """Report free relatives outside questions, and each "the one" standing for a noun.

        Parameters
        ----------
        doc : Document
            Document instance to inspect.
        ctx : RuleContext
            Rule evaluation context.

        Returns
        -------
        list[Violation]
            One violation per free relative or pronoun.
        """
        _ = ctx
        violations = []
        for _block, _position, sentence in prose_sentences(doc):
            tokens = sentence.tokens
            if sentence.projection.text.rstrip().endswith("?"):
                continue
            for index, token in enumerate(tokens):
                if lemma(token) not in FREE_RELATIVE_WORDS or in_inline_code(sentence, token):
                    continue
                if _completes_question_verb(tokens, index):
                    continue
                violations.append(
                    finding(
                        self,
                        token.source_span,
                        f"Free relative '{token.text}': name the object with a noun and give it a direct predicate.",
                        "free_relative",
                        "Ask which noun the clause stands for, and write that noun.",
                    )
                )
            for match in THE_ONE_RE.finditer(sentence.projection.text):
                one = next((t for t in tokens if t.projection_start >= match.start() + 4), None)
                if one is None or in_inline_code(sentence, one):
                    continue
                violations.append(
                    finding(
                        self,
                        one.source_span,
                        "'the one' stands for a noun: write the noun.",
                        "the_one",
                        "Name the object that the pronoun replaces.",
                    )
                )
        return violations


def _completes_question_verb(tokens, index: int) -> bool:
    """Whether the clause headed by a wh-word completes a verb of asking or knowing."""
    clause_verb = tokens[index].head_idx
    if clause_verb is None:
        return False
    governor = tokens[clause_verb].head_idx
    if tokens[clause_verb].dep not in {"ccomp", "xcomp", "dobj"} or governor is None:
        return False
    return lemma(tokens[governor]) in QUESTION_VERBS


def register(registry) -> None:
    """Register.

    Parameters
    ----------
    registry : object
        Rule registry used to resolve implementations.
    """
    registry.add(FreeRelativeRule)
