"""Shared regex skeleton builders for rule matching."""

from __future__ import annotations

from functools import lru_cache
import re
from typing import Iterable

_EMPTY_REGEX = re.compile(r"(?!x)x")


def normalize_phrases(phrases: Iterable[str]) -> tuple[str, ...]:
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
    normalized = normalize_phrases(phrases)
    if not normalized:
        return _EMPTY_REGEX
    body = "|".join(re.escape(phrase) for phrase in normalized)
    return re.compile(rf"^\s*(?:{body})\b", re.IGNORECASE)


@lru_cache(maxsize=256)
def compile_inline_phrase_regex(phrases: tuple[str, ...]) -> re.Pattern[str]:
    normalized = normalize_phrases(phrases)
    if not normalized:
        return _EMPTY_REGEX
    body = "|".join(re.escape(phrase) for phrase in normalized)
    return re.compile(rf"\b(?:{body})\b", re.IGNORECASE)


@lru_cache(maxsize=256)
def compile_prefixed_term_regex(
    prefixes: tuple[str, ...],
    terms: tuple[str, ...],
    anchored: bool = False,
) -> re.Pattern[str]:
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
    normalized = normalize_phrases(suffixes)
    if not normalized:
        return _EMPTY_REGEX
    suffix_body = "|".join(re.escape(suffix) for suffix in normalized)
    return re.compile(
        rf"\b(?P<stem>[A-Za-z][A-Za-z0-9-]*)-(?P<suffix>{suffix_body})\b",
        re.IGNORECASE,
    )
