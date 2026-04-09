"""Detect vague procedural nominalizations with missing argument structure."""

from __future__ import annotations

import re

from hermeneia.document.model import Span
from hermeneia.rules.base import (
    Layer,
    RuleEvidence,
    RuleKind,
    RuleMetadata,
    Severity,
    SourcePatternRule,
    Tractability,
    Violation,
)
from hermeneia.rules.common import line_text_outside_excluded

DETERMINER_RE = r"(?:the|this|that)"
STOP_CHARS = {".", ";", ":", "!", "?"}


class VagueProceduralNominalizationRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.vague_procedural_nominalization",
        label="Procedural nominalization should name its arguments",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("term", "signal"),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc
        terms = tuple(ctx.language_pack.lexicons.procedural_nominalization_terms)
        argument_markers = frozenset(
            marker.lower() for marker in ctx.language_pack.lexicons.procedural_argument_markers
        )
        term_pattern = _compile_term_pattern(terms)
        if term_pattern is None:
            return []
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for match in term_pattern.finditer(probe):
                tail = probe[match.end() :]
                if _has_argument_specification(tail, argument_markers):
                    continue
                term = match.group("term").lower()
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            f"'{match.group(0)}' is underspecified; name its arguments explicitly "
                            "(for example, between X and Y, of A, with B)."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={"term": term, "signal": "missing_arguments"}
                        ),
                        rewrite_tactics=(
                            "Replace the noun phrase with a verb phrase or attach explicit arguments.",
                        ),
                    )
                )
        return violations


def _compile_term_pattern(terms: tuple[str, ...]) -> re.Pattern[str] | None:
    normalized = tuple(sorted({term.strip().lower() for term in terms if term.strip()}))
    if not normalized:
        return None
    body = "|".join(re.escape(term) for term in normalized)
    return re.compile(
        rf"\b{DETERMINER_RE}\s+(?P<term>{body})(?:s)?\b",
        re.IGNORECASE,
    )


def _has_argument_specification(tail: str, markers: frozenset[str]) -> bool:
    window_chars: list[str] = []
    for char in tail:
        if char in STOP_CHARS:
            break
        window_chars.append(char)
        if len(window_chars) >= 80:
            break
    window = "".join(window_chars).lower()
    words = re.findall(r"\b[a-z]+\b", window)
    return any(word in markers for word in words)


def _match_span(line, start: int, end: int) -> Span:
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    registry.add(VagueProceduralNominalizationRule)
