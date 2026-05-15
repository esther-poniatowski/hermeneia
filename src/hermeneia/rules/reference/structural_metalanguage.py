"""Detect structural-metalanguage scaffolding in running prose."""

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


class _StructuralMetalanguageOptions:
    """Structuralmetalanguageoptions."""

    def __init__(
        self,
        *,
        structural_terms: tuple[str, ...] | None = None,
        position_terms: tuple[str, ...] | None = None,
    ) -> None:
        """Initialize the instance."""
        self.structural_terms = structural_terms
        self.position_terms = position_terms

    @classmethod
    def model_validate(cls, raw: object) -> "_StructuralMetalanguageOptions":
        """Validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset({"structural_terms", "position_terms"})
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        return cls(
            structural_terms=_as_string_tuple(raw.get("structural_terms"), "structural_terms"),
            position_terms=_as_string_tuple(raw.get("position_terms"), "position_terms"),
        )

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        dumped: dict[str, object] = {}
        if self.structural_terms is not None:
            dumped["structural_terms"] = self.structural_terms
        if self.position_terms is not None:
            dumped["position_terms"] = self.position_terms
        return dumped


class StructuralMetalanguageRule(SourcePatternRule):
    """Structuralmetalanguagerule."""

    options_model = _StructuralMetalanguageOptions

    metadata = RuleMetadata(
        rule_id="reference.structural_metalanguage",
        label="Avoid structural metalanguage in prose claims",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("issue", "term"),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        configured_terms = _as_string_tuple(
            self.settings.options.get("structural_terms"),
            "structural_terms",
        )
        configured_positions = _as_string_tuple(
            self.settings.options.get("position_terms"),
            "position_terms",
        )
        silenced = {value.lower() for value in self.settings.silenced_patterns}
        structural_terms = _merged_terms(
            configured_terms,
            tuple(ctx.language_pack.lexicons.structural_metalanguage_terms),
            silenced,
            extras=self.settings.extra_patterns,
        )
        position_terms = _merged_terms(
            configured_positions,
            tuple(ctx.language_pack.lexicons.structural_metalanguage_positions),
            silenced,
        )
        if not structural_terms:
            return []
        patterns = _compile_patterns(structural_terms, position_terms)
        violations: list[Violation] = []
        seen_ranges: list[tuple[int, int]] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for issue, pattern in patterns:
                for match in pattern.finditer(probe):
                    span_key = (
                        line.span.start + match.start(),
                        line.span.start + match.end(),
                    )
                    if _overlaps_existing(span_key, seen_ranges):
                        continue
                    seen_ranges.append(span_key)
                    term = (match.groupdict().get("term") or "").lower()
                    violations.append(
                        Violation(
                            rule_id=self.rule_id,
                            message=(
                                "Replace structural metalanguage with a direct content label or concrete proposition."
                            ),
                            span=_match_span(line, match.start(), match.end()),
                            severity=self.settings.severity,
                            layer=self.metadata.layer,
                            evidence=RuleEvidence(
                                features={
                                    "issue": issue,
                                    "term": term,
                                }
                            ),
                            rewrite_tactics=(
                                "Name the actual mathematical content instead of referring to document containers.",
                            ),
                        )
                    )
        return violations


def _compile_patterns(
    structural_terms: tuple[str, ...],
    position_terms: tuple[str, ...],
) -> tuple[tuple[str, re.Pattern[str]], ...]:
    """Compile structural-metalanguage patterns."""
    term_body = "|".join(re.escape(value) for value in structural_terms)
    patterns: list[tuple[str, re.Pattern[str]]] = []
    if position_terms:
        position_body = "|".join(re.escape(value) for value in position_terms)
        patterns.append(
            (
                "structural_position_reference",
                re.compile(
                    rf"\b(?:the|this|that|these|those|previous|next|following|preceding)\s+"
                    rf"(?P<term>{term_body})\s+(?P<position>{position_body})\b",
                    re.IGNORECASE,
                ),
            )
        )
        patterns.append(
            (
                "positional_structural_reference",
                re.compile(
                    rf"\b(?P<term>{term_body})\s+(?P<position>{position_body})\b",
                    re.IGNORECASE,
                ),
            )
        )
    patterns.append(
        (
            "structural_of_scaffolding",
            re.compile(rf"\b(?:the\s+)?(?P<term>{term_body})\s+of\b", re.IGNORECASE),
        )
    )
    patterns.append(
        (
            "structural_on_scaffolding",
            re.compile(rf"\b(?:the\s+)?(?P<term>{term_body})\s+on\b", re.IGNORECASE),
        )
    )
    patterns.append(
        (
            "structural_file_reference",
            re.compile(rf"\b(?:the\s+)?(?P<term>{term_body})\s+file\b", re.IGNORECASE),
        )
    )
    return tuple(patterns)


def _overlaps_existing(
    candidate: tuple[int, int],
    existing: list[tuple[int, int]],
) -> bool:
    """Overlaps existing."""
    candidate_start, candidate_end = candidate
    for existing_start, existing_end in existing:
        if candidate_start < existing_end and existing_start < candidate_end:
            return True
    return False


def _merged_terms(
    configured: tuple[str, ...] | None,
    defaults: tuple[str, ...],
    silenced: set[str],
    extras: tuple[str, ...] = (),
) -> tuple[str, ...]:
    """Merge configured/default terms with silencing and extras."""
    terms = configured if configured is not None else defaults
    normalized = normalize_phrases(tuple(terms) + tuple(extras))
    return tuple(term for term in normalized if term not in silenced)


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
    registry.add(StructuralMetalanguageRule)
