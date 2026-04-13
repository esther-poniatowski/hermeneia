"""Shared regex skeleton builders for rule matching.

Functions
---------
normalize_phrases
    Public API symbol.
compile_leading_phrase_regex
    Public API symbol.
compile_inline_phrase_regex
    Public API symbol.
compile_structured_leading_term_regex
    Public API symbol.
compile_prefixed_term_regex
    Public API symbol.
compile_hyphen_suffix_regex
    Public API symbol.
"""

from __future__ import annotations

from functools import lru_cache
import re
from typing import Iterable

_EMPTY_REGEX = re.compile(r"(?!x)x")


def normalize_phrases(phrases: Iterable[str]) -> tuple[str, ...]:
    """Normalize phrases.

    Parameters
    ----------
    phrases : Iterable[str]
        Input value for ``phrases``.

    Returns
    -------
    tuple[str, ...]
        Resulting value produced by this call.
    """
    normalized: list[str] = []
    seen: set[str] = set()
    for phrase in phrases:
        value = phrase.strip().lower()
        if not value or value in seen:
            continue
        seen.add(value)
        normalized.append(value)
    return tuple(normalized)


@lru_cache(maxsize=256)
def compile_leading_phrase_regex(phrases: tuple[str, ...]) -> re.Pattern[str]:
    """Compile leading phrase regex.

    Parameters
    ----------
    phrases : tuple[str, ...]
        Input value for ``phrases``.

    Returns
    -------
    re.Pattern[str]
        Resulting value produced by this call.
    """
    normalized = normalize_phrases(phrases)
    if not normalized:
        return _EMPTY_REGEX
    body = "|".join(re.escape(phrase) for phrase in normalized)
    return re.compile(rf"^\s*(?:{body})\b", re.IGNORECASE)


@lru_cache(maxsize=256)
def compile_inline_phrase_regex(phrases: tuple[str, ...]) -> re.Pattern[str]:
    """Compile inline phrase regex.

    Parameters
    ----------
    phrases : tuple[str, ...]
        Input value for ``phrases``.

    Returns
    -------
    re.Pattern[str]
        Resulting value produced by this call.
    """
    normalized = normalize_phrases(phrases)
    if not normalized:
        return _EMPTY_REGEX
    body = "|".join(re.escape(phrase) for phrase in normalized)
    return re.compile(rf"\b(?:{body})\b", re.IGNORECASE)


@lru_cache(maxsize=256)
def compile_structured_leading_term_regex(terms: tuple[str, ...]) -> re.Pattern[str]:
    """Compile structured leading term regex.

    Parameters
    ----------
    terms : tuple[str, ...]
        Input value for ``terms``.

    Returns
    -------
    re.Pattern[str]
        Resulting value produced by this call.
    """
    normalized = normalize_phrases(terms)
    if not normalized:
        return _EMPTY_REGEX
    body = "|".join(re.escape(term) for term in normalized)
    return re.compile(
        rf"^\s*(?:>\s*)*(?:(?:[-*+])\s+|\d+\.\s+)?(?P<term>{body})\b",
        re.IGNORECASE,
    )


@lru_cache(maxsize=256)
def compile_prefixed_term_regex(
    prefixes: tuple[str, ...],
    terms: tuple[str, ...],
    anchored: bool = False,
) -> re.Pattern[str]:
    """Compile prefixed term regex.

    Parameters
    ----------
    prefixes : tuple[str, ...]
        Input value for ``prefixes``.
    terms : tuple[str, ...]
        Input value for ``terms``.
    anchored : bool
        Input value for ``anchored``.

    Returns
    -------
    re.Pattern[str]
        Resulting value produced by this call.
    """
    normalized_prefixes = normalize_phrases(prefixes)
    normalized_terms = normalize_phrases(terms)
    if not normalized_prefixes or not normalized_terms:
        return _EMPTY_REGEX
    prefix_body = "|".join(re.escape(prefix) for prefix in normalized_prefixes)
    term_body = "|".join(re.escape(term) for term in normalized_terms)
    start = r"^\s*" if anchored else r"\b"
    return re.compile(
        rf"{start}(?:{prefix_body})\s+(?P<term>{term_body})\b",
        re.IGNORECASE,
    )


@lru_cache(maxsize=256)
def compile_hyphen_suffix_regex(suffixes: tuple[str, ...]) -> re.Pattern[str]:
    """Compile hyphen suffix regex.

    Parameters
    ----------
    suffixes : tuple[str, ...]
        Input value for ``suffixes``.

    Returns
    -------
    re.Pattern[str]
        Resulting value produced by this call.
    """
    normalized = normalize_phrases(suffixes)
    if not normalized:
        return _EMPTY_REGEX
    suffix_body = "|".join(re.escape(suffix) for suffix in normalized)
    return re.compile(
        rf"\b(?P<stem>[A-Za-z][A-Za-z0-9-]*)-(?P<suffix>{suffix_body})\b",
        re.IGNORECASE,
    )
