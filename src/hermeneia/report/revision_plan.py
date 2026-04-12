"""Revision-plan report types."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.document.model import Span
from hermeneia.rules.base import Layer, Severity


@dataclass(frozen=True)
class RevisionOperation:
    """Revisionoperation."""

    layer: Layer
    rule_id: str
    severity: Severity
    span: Span
    tactic: str
    candidate_rewrite: str | None = None


@dataclass(frozen=True)
class RevisionPlan:
    """Revisionplan."""

    operations: tuple[RevisionOperation, ...]
