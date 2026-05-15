"""Enforce tail-parenthetical placement for inline citation tags."""

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
from hermeneia.rules.reference.citation_styles import (
    citation_union_pattern,
    resolve_citation_patterns,
)

COMMA_SEPARATOR = ", "


class _CitationTailParentheticalOptions:
    """Citationtailparentheticaloptions."""

    def __init__(
        self,
        *,
        citation_styles: tuple[str, ...] | None = None,
        citation_tag_pattern: str | None = None,
        citation_tag_patterns: tuple[str, ...] | None = None,
    ) -> None:
        """Initialize the instance."""
        self.citation_styles = citation_styles
        self.citation_tag_pattern = citation_tag_pattern
        self.citation_tag_patterns = citation_tag_patterns

    @classmethod
    def model_validate(cls, raw: object) -> "_CitationTailParentheticalOptions":
        """Validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset({"citation_styles", "citation_tag_pattern", "citation_tag_patterns"})
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        pattern = raw.get("citation_tag_pattern")
        if pattern is not None and not isinstance(pattern, str):
            raise ValueError("citation_tag_pattern must be a string")
        citation_styles = _as_string_tuple(raw.get("citation_styles"), "citation_styles")
        citation_tag_patterns = _as_string_tuple(
            raw.get("citation_tag_patterns"), "citation_tag_patterns"
        )
        resolve_citation_patterns(
            citation_styles=citation_styles,
            citation_tag_pattern=pattern,
            citation_tag_patterns=citation_tag_patterns,
        )
        return cls(
            citation_styles=citation_styles,
            citation_tag_pattern=pattern,
            citation_tag_patterns=citation_tag_patterns,
        )

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        dumped: dict[str, object] = {}
        if self.citation_styles is not None:
            dumped["citation_styles"] = self.citation_styles
        if self.citation_tag_pattern is not None:
            dumped["citation_tag_pattern"] = self.citation_tag_pattern
        if self.citation_tag_patterns is not None:
            dumped["citation_tag_patterns"] = self.citation_tag_patterns
        return dumped


class CitationTailParentheticalRule(SourcePatternRule):
    """Citationtailparentheticalrule."""

    options_model = _CitationTailParentheticalOptions

    metadata = RuleMetadata(
        rule_id="reference.citation_tail_parenthetical",
        label="Citations should appear as tail parentheticals",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        default_options={"citation_styles": ("key_year_bracket",)},
        evidence_fields=("citation", "issue"),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        _ = ctx
        citation_styles = _as_string_tuple(
            self.settings.options.get("citation_styles"),
            "citation_styles",
        )
        citation_tag_pattern_raw = self.settings.options.get("citation_tag_pattern")
        citation_tag_pattern = (
            str(citation_tag_pattern_raw).strip() if citation_tag_pattern_raw is not None else None
        )
        citation_tag_patterns = _as_string_tuple(
            self.settings.options.get("citation_tag_patterns"),
            "citation_tag_patterns",
        )
        citation_patterns = resolve_citation_patterns(
            citation_styles=citation_styles,
            citation_tag_pattern=citation_tag_pattern,
            citation_tag_patterns=citation_tag_patterns,
        )
        citation_pattern_union = citation_union_pattern(citation_patterns)
        citation_re = re.compile(citation_pattern_union, re.IGNORECASE)
        trailing_re = _compile_trailing_remainder(citation_pattern_union)

        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for match in citation_re.finditer(probe):
                if _is_tail_parenthetical(
                    text=probe,
                    citation_end=match.end(),
                    trailing_re=trailing_re,
                ):
                    continue
                citation = match.group(0).lower()
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Place citations at the end of the statement, not inside sentence scaffolding."
                        ),
                        span=_match_span(line, match.start(), match.end()),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "citation": citation,
                                "issue": "citation_not_tail_parenthetical",
                            }
                        ),
                        rewrite_tactics=(
                            "Move the citation tag to the end of the sentence or clause it supports.",
                        ),
                    )
                )
        return violations


def _compile_trailing_remainder(citation_tag_pattern: str) -> re.Pattern[str]:
    """Compile trailing remainder matcher for valid tail citation placement."""
    return re.compile(
        rf"^\s*(?:[,;:]\s*)?(?:{citation_tag_pattern}\s*)*[\])\"'”’]*\s*[.?!,:;]*\s*$",
        re.IGNORECASE,
    )


def _is_tail_parenthetical(
    *,
    text: str,
    citation_end: int,
    trailing_re: re.Pattern[str],
) -> bool:
    """Is tail parenthetical."""
    return trailing_re.match(text[citation_end:]) is not None


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
    registry.add(CitationTailParentheticalRule)


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
