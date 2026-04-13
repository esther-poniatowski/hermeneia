"""Inline case-split checks."""

from __future__ import annotations

import re

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
from hermeneia.rules.patterns import normalize_phrases

EMPTY_MATCH_RE = re.compile(r"(?!x)x")


class InlineCaseSplitRule(HeuristicSemanticRule):
    """Inlinecasesplitrule."""

    metadata = RuleMetadata(
        rule_id="paragraph.inline_case_split",
        label="Inline semicolon case splits should be rendered as lists",
        layer=Layer.PARAGRAPH_RHETORIC,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.RHETORICAL_EXPECTATION,
        default_severity=Severity.INFO,
        supported_languages=frozenset({"en"}),
        evidence_fields=("pattern",),
    )

    def check(self, doc, ctx):
        """Check.

        Parameters
        ----------
        doc : object
            Document instance to inspect.
        ctx : object
            Rule evaluation context.

        Returns
        -------
        object
            Resulting value produced by this call.
        """
        condition_markers = normalize_phrases(
            tuple(ctx.language_pack.lexicons.inline_case_condition_markers)
        )
        fallback_markers = normalize_phrases(
            tuple(ctx.language_pack.lexicons.inline_case_fallback_markers)
        )
        patterns = _compile_inline_case_patterns(condition_markers, fallback_markers)
        violations: list[Violation] = []
        for sentence in iter_sentences(doc):
            issue, match = _first_match(sentence.source_text, patterns)
            if match is None or issue is None:
                continue
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        "Distinct cases are packed inline; use a lead-in sentence and "
                        "bullet-case structure."
                    ),
                    span=sentence.span,
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(
                        features={"pattern": match.group(0), "issue": issue}
                    ),
                    rewrite_tactics=(
                        "Convert semicolon-joined case clauses into explicit case bullets.",
                    ),
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
    registry.add(InlineCaseSplitRule)


def _compile_inline_case_patterns(
    condition_markers: tuple[str, ...], fallback_markers: tuple[str, ...]
) -> tuple[tuple[str, re.Pattern[str]], ...]:
    """Compile inline case patterns."""
    if not condition_markers:
        return ()
    condition_body = "|".join(re.escape(marker) for marker in condition_markers)
    semicolon_repeated_conditional = re.compile(
        rf"\b(?:{condition_body})\b[^;]{{0,240}};\s*(?:{condition_body})\b",
        re.IGNORECASE,
    )
    comma_repeated_conditional = re.compile(
        rf"\b(?:{condition_body})\b[^\n]{{0,240}},\s*(?:{condition_body})\b",
        re.IGNORECASE,
    )
    conditional_fallback = EMPTY_MATCH_RE
    if fallback_markers:
        fallback_body = "|".join(re.escape(marker) for marker in fallback_markers)
        conditional_fallback = re.compile(
            rf"\b(?:{condition_body})\b[^;]{{0,240}};\s*(?:{fallback_body})\b",
            re.IGNORECASE,
        )
    return (
        ("repeated_conditional_semicolon", semicolon_repeated_conditional),
        ("repeated_conditional_comma", comma_repeated_conditional),
        ("conditional_fallback_semicolon", conditional_fallback),
    )


def _first_match(
    sentence_text: str, patterns: tuple[tuple[str, re.Pattern[str]], ...]
) -> tuple[str | None, re.Match[str] | None]:
    """First match."""
    for issue, pattern in patterns:
        match = pattern.search(sentence_text)
        if match is not None:
            return issue, match
    return None, None
