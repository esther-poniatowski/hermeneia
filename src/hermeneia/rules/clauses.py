"""Clause-level helpers shared by the rules reading the dependency tree of a sentence.

The annotator stores, for each token, the index of its head within the same sentence, so a sentence
holds a complete dependency tree. The helpers below locate relative clauses, their relativizers and
their subjects in that tree, for the rules governing relative clauses and subjects.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from hermeneia.document.model import Block, BlockKind, Document, InlineKind, Sentence, Span, Token
from hermeneia.rules.base import (
    BaseRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)

#: Words introducing a relative clause.
RELATIVIZERS = frozenset({"that", "which", "who", "whom", "whose"})
#: Dependency labels of a grammatical subject.
SUBJECTS = frozenset({"nsubj", "nsubjpass", "csubj", "csubjpass"})
#: Dependency labels of an object of a verb or a preposition.
OBJECTS = frozenset({"dobj", "pobj", "obj"})
#: Modal auxiliaries stating an obligation, an ability or a possibility.
MODALS = frozenset({"must", "should", "can", "could", "may", "might", "shall", "will", "would"})
#: Blocks holding prose, as opposed to code, mathematics or containers.
PROSE_BLOCKS = frozenset(
    {
        BlockKind.PARAGRAPH,
        BlockKind.LIST_ITEM,
        BlockKind.BLOCK_QUOTE,
        BlockKind.TABLE_CELL,
        BlockKind.FOOTNOTE,
        BlockKind.ADMONITION,
    }
)


@dataclass(frozen=True)
class RelativeClause:
    """A relative clause, located by token indices within its sentence.

    Parameters
    ----------
    head : int
        Noun modified by the clause.
    verb : int
        Verb heading the clause.
    relativizer : int | None
        Word introducing the clause, absent when the clause omits it.
    subject : int | None
        Subject of the clause other than its relativizer, present in an object relative.
    """

    head: int
    verb: int
    relativizer: int | None
    subject: int | None


def prose_sentences(doc: Document) -> Iterable[tuple[Block, int, Sentence]]:
    """Yield each prose sentence with its block and its position in that block."""
    for block in doc.iter_blocks():
        if block.kind not in PROSE_BLOCKS:
            continue
        for position, sentence in enumerate(block.sentences):
            if sentence.tokens:
                yield block, position, sentence


def in_inline_code(sentence: Sentence, token: Token) -> bool:
    """Whether a token lies inside an inline code span.

    A code span quotes material and states no claim. A paragraph masks its code spans as inline
    nodes, whereas a table cell keeps their backticks in its text, so a token preceded by an odd
    number of backticks lies inside a span.
    """
    if any(
        node.kind == InlineKind.INLINE_CODE and node.span.overlaps(token.source_span)
        for node in sentence.inline_nodes
    ):
        return True
    return sentence.projection.text[: token.projection_start].count("`") % 2 == 1


def children(tokens: list[Token], index: int) -> list[int]:
    """Return the indices of the tokens whose head is the token at ``index``."""
    return [
        position
        for position, token in enumerate(tokens)
        if token.head_idx == index and position != index
    ]


def root(tokens: list[Token]) -> int | None:
    """Return the index of the root of a sentence.

    The annotator may record the root as its own head instead of leaving its head empty, so both
    forms are read as the root.
    """
    return next(
        (
            i
            for i, token in enumerate(tokens)
            if token.dep == "ROOT" or token.head_idx is None or token.head_idx == i
        ),
        None,
    )


def first_word(tokens: list[Token]) -> int | None:
    """Return the index of the first alphabetic token of a sentence."""
    return next((i for i, token in enumerate(tokens) if token.text[:1].isalpha()), None)


def lemma(token: Token) -> str:
    """Return the lowercase lemma of a token, or its text when no lemma is known."""
    return (token.lemma or token.text).lower()


def relative_clauses(tokens: list[Token]) -> list[RelativeClause]:
    """Locate the relative clauses of a sentence.

    A clause is a verb labelled ``relcl`` whose head precedes it. Its relativizer is a relative
    word standing between the head and the verb, and its subject is a subject of the verb other than
    that relativizer.
    """
    clauses: list[RelativeClause] = []
    for verb, token in enumerate(tokens):
        if token.dep != "relcl" or token.head_idx is None or token.head_idx >= verb:
            continue
        head = token.head_idx
        between = range(head + 1, verb)
        relativizer = next(
            (
                i
                for i in between
                if lemma(tokens[i]) in RELATIVIZERS or tokens[i].text.lower() in RELATIVIZERS
            ),
            None,
        )
        subject = next(
            (
                i
                for i in children(tokens, verb)
                if tokens[i].dep in SUBJECTS and i != relativizer and head < i < verb
            ),
            None,
        )
        clauses.append(RelativeClause(head, verb, relativizer, subject))
    return clauses


def token_span(tokens: list[Token], start: int, end: int) -> Span:
    """Return the source span running from the token at ``start`` to the token at ``end``."""
    first, last = tokens[start].source_span, tokens[end].source_span
    return Span(
        start=first.start,
        end=last.end,
        start_line=first.start_line,
        start_column=first.start_column,
        end_line=last.end_line,
        end_column=last.end_column,
    )


def finding(
    rule: BaseRule,
    span: Span,
    message: str,
    check: str,
    tactic: str,
    confidence: float = 0.75,
) -> Violation:
    """Build a violation of a rule, with the check that fired and one rewrite tactic."""
    return Violation(
        rule_id=rule.rule_id,
        message=message,
        span=span,
        severity=rule.settings.severity,
        layer=rule.metadata.layer,
        evidence=RuleEvidence(features={"check": check}),
        confidence=confidence,
        rewrite_tactics=(tactic,),
    )


def clause_metadata(
    rule_id: str,
    label: str,
    severity: Severity = Severity.WARNING,
    layer: Layer = Layer.SURFACE_STYLE,
) -> RuleMetadata:
    """Return the metadata of a clause-level rule, a soft heuristic reading the dependency tree."""
    return RuleMetadata(
        rule_id=rule_id,
        label=label,
        layer=layer,
        tractability=Tractability.CLASS_B,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=severity,
        supported_languages=frozenset({"en"}),
        evidence_fields=("check",),
    )
