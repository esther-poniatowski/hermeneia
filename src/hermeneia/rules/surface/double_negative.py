"""Detect double-negative constructions in prose sentences."""

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
from hermeneia.rules.patterns import normalize_phrases


class DoubleNegativeRule(SourcePatternRule):
    metadata = RuleMetadata(
        rule_id="surface.double_negative",
        label="Avoid double-negative scaffolding",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        default_options={"max_gap_tokens": 5},
        evidence_fields=("matched_text",),
    )

    def check_source(self, lines, doc, ctx):
        _ = doc
        max_gap_tokens = self.settings.int_option("max_gap_tokens", 5)
        pattern = _compile_double_negative_pattern(
            tuple(ctx.language_pack.lexicons.negative_markers),
            max_gap_tokens=max_gap_tokens,
        )
        if pattern is None:
            return []
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for match in pattern.finditer(probe):
                matched = match.group(0).strip()
                if _is_allowed_negative_pair(matched):
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Double-negative phrasing can obscure polarity; rewrite with one "
                            "explicit negation."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(features={"matched_text": matched.lower()}),
                        rewrite_tactics=(
                            "Rewrite with a single negative or a direct positive statement.",
                        ),
                    )
                )
        return violations


def _compile_double_negative_pattern(
    markers: tuple[str, ...],
    *,
    max_gap_tokens: int,
) -> re.Pattern[str] | None:
    normalized = normalize_phrases(markers)
    if len(normalized) < 2:
        return None
    body = "|".join(re.escape(marker) for marker in normalized)
    return re.compile(
        rf"\b(?:{body})\b(?:\W+\w+){{0,{max(0, max_gap_tokens)}}}\W+\b(?:{body})\b",
        re.IGNORECASE,
    )


def _is_allowed_negative_pair(matched: str) -> bool:
    lowered = matched.lower()
    if lowered.startswith("not only"):
        return True
    if "neither" in lowered and " nor " in lowered:
        return True
    return False


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
    registry.add(DoubleNegativeRule)

