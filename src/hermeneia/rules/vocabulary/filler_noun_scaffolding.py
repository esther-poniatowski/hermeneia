"""Detect filler nouns that weaken technical precision."""

from __future__ import annotations

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
from hermeneia.rules.common import match_allowed
from hermeneia.rules.patterns import compile_inline_phrase_regex, normalize_phrases

COMMA_SEPARATOR = ", "


class _FillerNounScaffoldingOptions:
    """Fillernounscaffoldingoptions."""

    def __init__(self, *, filler_terms: tuple[str, ...] | None = None) -> None:
        """Initialize the instance."""
        self.filler_terms = filler_terms

    @classmethod
    def model_validate(cls, raw: object) -> "_FillerNounScaffoldingOptions":
        """Validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset({"filler_terms"})
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        return cls(filler_terms=_as_string_tuple(raw.get("filler_terms"), "filler_terms"))

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        if self.filler_terms is None:
            return {}
        return {"filler_terms": self.filler_terms}


class FillerNounScaffoldingRule(SourcePatternRule):
    """Fillernounscaffoldingrule."""

    options_model = _FillerNounScaffoldingOptions

    metadata = RuleMetadata(
        rule_id="vocabulary.filler_noun_scaffolding",
        label="Avoid filler nouns in technical claims",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("term",),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        configured = _as_string_tuple(self.settings.options.get("filler_terms"), "filler_terms")
        silenced = {value.lower() for value in self.settings.silenced_patterns}
        defaults = tuple(ctx.language_pack.lexicons.filler_noun_terms)
        filler_terms = _merged_terms(
            configured=configured,
            defaults=defaults,
            silenced=silenced,
            extras=self.settings.extra_patterns,
        )
        pattern = compile_inline_phrase_regex(filler_terms)
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value in {"code_block", "display_math"} for kind in line.container_kinds):
                continue
            match = match_allowed(line, pattern)
            if match is None:
                continue
            term = match.group(0).lower()
            violations.append(
                Violation(
                    rule_id=self.rule_id,
                    message=(
                        f"Replace filler noun '{term}' with the precise object, mechanism, or result."
                    ),
                    span=_match_span(line, match.start(), match.end()),
                    severity=self.settings.severity,
                    layer=self.metadata.layer,
                    evidence=RuleEvidence(features={"term": term}),
                    rewrite_tactics=(
                        "Name the specific mathematical object, operation, or relation.",
                    ),
                )
            )
        return violations


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
    registry.add(FillerNounScaffoldingRule)
