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
    """Diagnosticreport."""

    path: Path | None
    violations: tuple[Violation, ...]
    scorecard: Scorecard | None
    revision_plan: RevisionPlan
    scoring_output: frozenset[str] = frozenset(
        {"layer_scores", "global_score", "violation_list"}
    )

    def to_dict(self) -> dict[str, object]:
        """To dict.

        Returns
        -------
        dict[str, object]
            Resulting value produced by this call.
        """
        payload: dict[str, object] = {
            "path": str(self.path) if self.path is not None else None,
            "revision_plan": asdict(self.revision_plan),
        }
        if "violation_list" in self.scoring_output:
            payload["violations"] = [asdict(violation) for violation in self.violations]
        if self.scorecard is not None:
            score_payload: dict[str, object] = {}
            raw = asdict(self.scorecard)
            if "layer_scores" in self.scoring_output:
                score_payload["layer_scores"] = raw["layer_scores"]
            if "global_score" in self.scoring_output:
                score_payload["global_score"] = raw["global_score"]
            if score_payload:
                payload["scorecard"] = score_payload
        return payload

    def to_json(self) -> str:
        """To json.

        Returns
        -------
        str
            Resulting value produced by this call.
        """
        return json.dumps(self.to_dict(), indent=2, sort_keys=True)
