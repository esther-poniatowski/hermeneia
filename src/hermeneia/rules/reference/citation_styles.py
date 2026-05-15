"""Shared citation-style resolution helpers for reference rules."""

from __future__ import annotations

import re

COMMA_SEPARATOR = ", "
DEFAULT_CITATION_STYLES = ("key_year_bracket",)
CITATION_STYLE_PATTERNS: dict[str, str] = {
    "key_year_bracket": r"\[[a-z][a-z0-9_-]*\d{4}[a-z]?\]",
    "key_bracket": r"\[[a-z][a-z0-9:_-]+\]",
    "numeric_bracket": r"\[(?:\d{1,4}(?:\s*(?:,|-)\s*\d{1,4})*)\]",
    "author_year_parenthetical": (
        r"\((?:[A-Z][A-Za-z'`-]+(?:\s+(?:and|&)\s+[A-Z][A-Za-z'`-]+)?)"
        r"(?:\s+et\s+al\.)?,?\s*\d{4}[a-z]?\)"
    ),
    "pandoc_citekey": r"\[@[A-Za-z0-9:_-]+\]",
}


def resolve_citation_patterns(
    *,
    citation_styles: tuple[str, ...] | None,
    citation_tag_pattern: str | None,
    citation_tag_patterns: tuple[str, ...] | None,
    default_styles: tuple[str, ...] = DEFAULT_CITATION_STYLES,
) -> tuple[str, ...]:
    """Resolve citation regex patterns from style names and custom patterns."""
    resolved: list[str] = []
    normalized_styles = _normalize_styles(citation_styles)
    if normalized_styles is None:
        normalized_styles = default_styles
    for style in normalized_styles:
        try:
            resolved.append(CITATION_STYLE_PATTERNS[style])
        except KeyError as exc:
            expected = COMMA_SEPARATOR.join(sorted(CITATION_STYLE_PATTERNS))
            raise ValueError(
                f"unknown citation_styles value '{style}'. Expected one of: {expected}"
            ) from exc
    single_pattern = (citation_tag_pattern or "").strip()
    if single_pattern:
        resolved.append(single_pattern)
    for pattern in citation_tag_patterns or ():
        candidate = pattern.strip()
        if candidate:
            resolved.append(candidate)
    deduped = tuple(dict.fromkeys(resolved))
    if not deduped:
        raise ValueError(
            "citation rules require at least one citation pattern "
            "(set citation_styles or citation_tag_pattern(s))"
        )
    _validate_patterns(deduped)
    return deduped


def citation_union_pattern(citation_patterns: tuple[str, ...]) -> str:
    """Build a non-capturing citation union regex fragment."""
    return "|".join(f"(?:{pattern})" for pattern in citation_patterns)


def _normalize_styles(raw_styles: tuple[str, ...] | None) -> tuple[str, ...] | None:
    """Normalize style identifiers."""
    if raw_styles is None:
        return None
    normalized: list[str] = []
    for style in raw_styles:
        value = style.strip().lower()
        if value:
            normalized.append(value)
    return tuple(dict.fromkeys(normalized))


def _validate_patterns(patterns: tuple[str, ...]) -> None:
    """Validate citation regex patterns."""
    for pattern in patterns:
        try:
            re.compile(pattern)
        except re.error as exc:  # pragma: no cover - validation guard
            raise ValueError(f"invalid citation pattern '{pattern}': {exc}") from exc
