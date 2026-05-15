"""Detect taxonomy-style explicit cardinality framing."""

from __future__ import annotations

import re
from typing import Mapping

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

COMMA_SEPARATOR = ", "


class _CardinalityFramingOptions:
    """Cardinalityframingoptions."""

    def __init__(
        self,
        *,
        target_terms: tuple[str, ...] | None = None,
        number_words: tuple[str, ...] | None = None,
    ) -> None:
        """Initialize the instance."""
        self.target_terms = target_terms
        self.number_words = number_words

    @classmethod
    def model_validate(cls, raw: object) -> "_CardinalityFramingOptions":
        """Validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset({"target_terms", "number_words"})
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        return cls(
            target_terms=_as_string_tuple(raw.get("target_terms"), "target_terms"),
            number_words=_as_string_tuple(raw.get("number_words"), "number_words"),
        )

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        dumped: dict[str, object] = {}
        if self.target_terms is not None:
            dumped["target_terms"] = self.target_terms
        if self.number_words is not None:
            dumped["number_words"] = self.number_words
        return dumped


class CardinalityFramingRule(SourcePatternRule):
    """Cardinalityframingrule."""

    options_model = _CardinalityFramingOptions

    metadata = RuleMetadata(
        rule_id="vocabulary.cardinality_framing",
        label="Avoid explicit cardinality labels in taxonomy framing",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.SOFT_HEURISTIC,
        default_severity=Severity.WARNING,
        supported_languages=frozenset({"en"}),
        evidence_fields=("number", "target"),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        silenced = {pattern.lower() for pattern in self.settings.silenced_patterns}
        target_terms = _merged_terms(
            configured=_as_string_tuple(
                self.settings.options.get("target_terms"),
                "target_terms",
            ),
            defaults=tuple(ctx.language_pack.lexicons.taxonomy_cardinality_targets),
            silenced=silenced,
            extras=self.settings.extra_patterns,
        )
        number_words = _merged_terms(
            configured=_as_string_tuple(
                self.settings.options.get("number_words"),
                "number_words",
            ),
            defaults=tuple(ctx.language_pack.lexicons.cardinality_number_words),
            silenced=silenced,
        )
        pattern = _compile_cardinality_pattern(target_terms, number_words)
        if pattern is None:
            return []
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for match in pattern.finditer(probe):
                if _preceded_by_at_least(probe, match.start()):
                    continue
                number = match.group("number").lower()
                target = match.group("target").lower()
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Avoid cardinality-first taxonomy labels when the count is not the substantive claim."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(features={"number": number, "target": target}),
                        rewrite_tactics=(
                            "Name the taxonomy directly "
                            "(for example, 'the challenge axes') "
                            "and reserve numbers for evidential claims.",
                        ),
                    )
                )
        return violations


def _compile_cardinality_pattern(
    target_terms: tuple[str, ...],
    number_words: tuple[str, ...],
) -> re.Pattern[str] | None:
    """Compile cardinality pattern."""
    if not target_terms:
        return None
    number_body = "|".join(re.escape(item) for item in number_words)
    if number_body:
        number_body = rf"(?:\d+|{number_body})"
    else:
        number_body = r"\d+"
    target_body = "|".join(re.escape(item) for item in target_terms)
    return re.compile(
        rf"\b(?P<number>{number_body})\s+(?P<target>{target_body})\b",
        re.IGNORECASE,
    )


def _preceded_by_at_least(text: str, start: int) -> bool:
    """Preceded by at least."""
    window = text[max(0, start - 16) : start].lower()
    return window.rstrip().endswith("at least")


def _merged_terms(
    *,
    configured: tuple[str, ...] | None,
    defaults: tuple[str, ...],
    silenced: set[str],
    extras: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Merge configured/default terms."""
    raw = configured if configured is not None else defaults
    normalized = normalize_phrases(tuple(raw) + tuple(extras))
    return tuple(value for value in normalized if value not in silenced)


def _as_string_tuple(raw: object, field: str) -> tuple[str, ...] | None:
    """As string tuple."""
    if raw is None:
        return None
    if isinstance(raw, str):
        return (raw,)
    if not isinstance(raw, (list, tuple)):
        raise ValueError(f"{field} must be a string or sequence of strings")
    if not all(isinstance(item, str) for item in raw):
        raise ValueError(f"{field} must be a string or sequence of strings")
    return tuple(raw)


def _match_span(line, start: int, end: int) -> Span:
    """Match span."""
    return Span(
        start=line.span.start + start,
        end=line.span.start + end,
        start_line=line.span.start_line,
        start_column=line.span.start_column + start,
        end_line=line.span.start_line,
        end_column=line.span.start_column + end,
    )


def register(registry) -> None:
    """Register."""
    registry.add(CardinalityFramingRule)
