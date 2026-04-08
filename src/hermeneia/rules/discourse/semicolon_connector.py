"""Semicolon connector articulation checks."""

from __future__ import annotations

import re

from hermeneia.document.model import Span
from hermeneia.rules.base import (
    HeuristicSemanticRule,
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    Tractability,
    Violation,
)
from hermeneia.rules.common import iter_sentences
from hermeneia.rules.patterns import compile_leading_phrase_regex

CONDITIONAL_STARTERS = ("if", "when", "where", "for")


class SemicolonConnectorRule(HeuristicSemanticRule):
    metadata = RuleMetadata(
        rule_id="discourse.semicolon_connector",
        label="Semicolon joins should include explicit connective framing",
        layer=Layer.LOCAL_DISCOURSE,
        tractability=Tractability.CLASS_H,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("issue", "right_clause_preview"),
    )

    def check(self, doc, ctx):
        connectors = tuple(ctx.language_pack.lexicons.semicolon_connectors) + tuple(
            ctx.language_pack.lexicons.transition_connectors
        )
        connector_pattern = compile_leading_phrase_regex(connectors)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            text = sentence.source_text
            if ";" not in text:
                continue
            clauses = [clause.strip() for clause in text.split(";")]
            for index in range(1, len(clauses)):
                left = clauses[index - 1]
                right = clauses[index]
                if not left or not right:
                    continue
                if connector_pattern.search(right):
                    continue
                if _strict_parallel_pair(left, right):
                    continue
                semicolon_offset = _semicolon_offset(text, index)
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Semicolon joins independent clauses without an explicit logical "
                            "connector."
                        ),
                        span=_semicolon_span(sentence, semicolon_offset),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "issue": "missing_semicolon_connector",
                                "right_clause_preview": right[:80],
                            }
                        ),
                        confidence=0.76,
                        rationale=(
                            "Semicolon checks operate on clause-local cues and may abstain on "
                            "subtle rhetorical parallels."
                        ),
                        rewrite_tactics=(
                            "Insert a connector after the semicolon or split into separate sentences.",
                        ),
                    )
                )
                break
        return violations


def _strict_parallel_pair(left: str, right: str) -> bool:
    left_first = _first_token(left)
    right_first = _first_token(right)
    if left_first is None or right_first is None:
        return False
    if left_first == right_first and left_first in CONDITIONAL_STARTERS:
        return True
    left_lower = left.lower().lstrip()
    right_lower = right.lower().lstrip()
    return left_lower.startswith("if ") and right_lower.startswith("if ")


def _first_token(text: str) -> str | None:
    match = re.search(r"\b[A-Za-z]+\b", text.lower())
    if match is None:
        return None
    return match.group(0)


def _semicolon_offset(text: str, boundary_index: int) -> int:
    seen = 0
    for index, char in enumerate(text):
        if char != ";":
            continue
        seen += 1
        if seen == boundary_index:
            return index
    return max(0, text.find(";"))


def _semicolon_span(sentence, semicolon_offset: int) -> Span:
    return Span(
        start=sentence.span.start + semicolon_offset,
        end=sentence.span.start + semicolon_offset + 1,
        start_line=sentence.span.start_line,
        start_column=sentence.span.start_column + semicolon_offset,
        end_line=sentence.span.start_line,
        end_column=sentence.span.start_column + semicolon_offset + 1,
    )


def register(registry) -> None:
    registry.add(SemicolonConnectorRule)
