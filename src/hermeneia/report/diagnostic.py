"""Diagnostic report DTOs and serialization helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
from pathlib import Path

from hermeneia.report.revision_plan import RevisionPlan
from hermeneia.scoring.scorer import Scorecard
from hermeneia.rules.base import Violation


@dataclass(frozen=True)
class DiagnosticReport:
    path: Path | None
    violations: tuple[Violation, ...]
    scorecard: Scorecard
    revision_plan: RevisionPlan

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["path"] = str(self.path) if self.path is not None else None
        return payload

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)
