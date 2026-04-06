"""Guarded candidate rewrites."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RewriteCandidate:
    tactic: str
    candidate_rewrite: str | None = None


def rewrite_for_contraction() -> RewriteCandidate:
    return RewriteCandidate(tactic="Expand contractions in technical prose")


def tactic_only(message: str) -> RewriteCandidate:
    return RewriteCandidate(tactic=message)
