"""Generic/procedural link-text checks."""

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

MARKDOWN_LINK_RE = re.compile(
    r"(?<!\!)\[(?P<link_text>[^\]\n]+)\]\((?P<link_target>[^)\n]*)\)"
)
COMMA_SEPARATOR = ", "


class _GenericLinkTextOptions:
    """Genericlinktextoptions."""

    def __init__(
        self,
        *,
        reference_labels: tuple[str, ...] | None = None,
        procedural_terms: tuple[str, ...] | None = None,
    ) -> None:
        """Init."""
        self.reference_labels = reference_labels
        self.procedural_terms = procedural_terms

    @classmethod
    def model_validate(cls, raw: object) -> "_GenericLinkTextOptions":
        """Model validate."""
        if not isinstance(raw, Mapping):
            raise ValueError("options must be a mapping")
        allowed = frozenset({"reference_labels", "procedural_terms"})
        unknown = sorted(key for key in raw if key not in allowed)
        if unknown:
            raise ValueError(f"unknown option keys: {COMMA_SEPARATOR.join(unknown)}")
        return cls(
            reference_labels=_as_string_tuple(
                raw.get("reference_labels"), "reference_labels"
            ),
            procedural_terms=_as_string_tuple(
                raw.get("procedural_terms"), "procedural_terms"
            ),
        )

    def model_dump(self) -> dict[str, object]:
        """Model dump."""
        dumped: dict[str, object] = {}
        if self.reference_labels is not None:
            dumped["reference_labels"] = self.reference_labels
        if self.procedural_terms is not None:
            dumped["procedural_terms"] = self.procedural_terms
        return dumped


class GenericLinkTextRule(SourcePatternRule):
    """Genericlinktextrule."""

    options_model = _GenericLinkTextOptions

    metadata = RuleMetadata(
        rule_id="reference.generic_link_text",
        label="Avoid generic or procedural markdown link text",
        layer=Layer.SURFACE_STYLE,
        tractability=Tractability.CLASS_A,
        kind=RuleKind.HARD_CONSTRAINT,
        default_severity=Severity.ERROR,
        supported_languages=frozenset({"en"}),
        evidence_fields=("link_text", "signal", "matched"),
    )

    def check_source(self, lines, doc, ctx):
        """Check source."""
        _ = doc
        silenced = {pattern.lower() for pattern in self.settings.silenced_patterns}
        configured_labels = _as_string_tuple(
            self.settings.options.get("reference_labels"),
            "reference_labels",
        )
        configured_terms = _as_string_tuple(
            self.settings.options.get("procedural_terms"),
            "procedural_terms",
        )
        reference_labels = (
            configured_labels
            if configured_labels is not None
            else tuple(ctx.language_pack.lexicons.generic_link_reference_labels)
        )
        procedural_terms = (
            configured_terms
            if configured_terms is not None
            else tuple(ctx.language_pack.lexicons.procedural_link_terms)
        )
        procedural_terms = procedural_terms + self.settings.extra_patterns
        reference_labels = tuple(
            label for label in reference_labels if label.strip().lower() not in silenced
        )
        procedural_terms = tuple(
            term for term in procedural_terms if term.strip().lower() not in silenced
        )
        citation_pattern = _compile_generic_link_text_pattern(reference_labels)
        procedural_pattern = _compile_procedural_link_pattern(procedural_terms)
        violations: list[Violation] = []
        for line in lines:
            if any(kind.value == "code_block" for kind in line.container_kinds):
                continue
            probe = line_text_outside_excluded(line)
            for match in MARKDOWN_LINK_RE.finditer(probe):
                link_text = match.group("link_text").strip()
                signal, matched = _classify_link_text(
                    link_text=link_text,
                    citation_pattern=citation_pattern,
                    procedural_pattern=procedural_pattern,
                )
                if signal is None:
                    continue
                violations.append(
                    Violation(
                        rule_id=self.rule_id,
                        message=(
                            "Link text must name a result, object, or property, not a container "
                            "or procedural placeholder."
                        ),
                        span=_match_span(
                            line,
                            match.start("link_text"),
                            match.end("link_text"),
                        ),
                        severity=self.settings.severity,
                        layer=self.metadata.layer,
                        evidence=RuleEvidence(
                            features={
                                "link_text": link_text,
                                "signal": signal,
                                "matched": matched,
                            }
                        ),
                        confidence=0.92 if signal == "procedural_term" else 0.88,
                        rewrite_tactics=(
                            "Rewrite the link text to name the actual result or mathematical object.",
                        ),
                    )
                )
        return violations


def _compile_generic_link_text_pattern(labels: tuple[str, ...]) -> re.Pattern[str]:
    """Compile generic link text pattern."""
    normalized_labels = normalize_phrases(labels)
    if not normalized_labels:
        return re.compile(r"(?!x)x")
    label_body = "|".join(re.escape(label) for label in normalized_labels)
    return re.compile(
        rf"^\s*(?P<label>{label_body})(?:\s*(?:\([^)]+\)|\d+[A-Za-z]?|[IVXLCDM]+))?\s*$",
        re.IGNORECASE,
    )


def _compile_procedural_link_pattern(terms: tuple[str, ...]) -> re.Pattern[str]:
    """Compile procedural link pattern."""
    normalized_terms = normalize_phrases(terms)
    if not normalized_terms:
        return re.compile(r"(?!x)x")
    body = "|".join(re.escape(term) for term in normalized_terms)
    return re.compile(rf"\b(?P<term>{body})\b", re.IGNORECASE)


def _classify_link_text(
    *,
    link_text: str,
    citation_pattern: re.Pattern[str],
    procedural_pattern: re.Pattern[str],
) -> tuple[str | None, str | None]:
    """Classify link text."""
    citation_match = citation_pattern.fullmatch(link_text)
    if citation_match is not None:
        label = citation_match.group("label")
        return "citation_label", label.lower()
    procedural_match = procedural_pattern.search(link_text)
    if procedural_match is not None:
        term = procedural_match.group("term")
        return "procedural_term", term.lower()
    return None, None


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
    registry.add(GenericLinkTextRule)
