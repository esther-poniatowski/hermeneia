"""Revision planning from violations."""

from __future__ import annotations

from hermeneia.report.revision_plan import RevisionOperation, RevisionPlan
from hermeneia.rules.base import Violation
from hermeneia.suggest.template import RewriteCandidate, rewrite_for_contraction, tactic_only


class RevisionPlanner:
    def build(self, violations: list[Violation]) -> RevisionPlan:
        operations = [self._operation_for(violation) for violation in violations]
        ordered = tuple(
            sorted(
                operations,
                key=lambda op: (op.layer.value, -_severity_rank(op.severity), op.span.start),
            )
        )
        return RevisionPlan(operations=ordered)

    def _operation_for(self, violation: Violation) -> RevisionOperation:
        candidate = self._candidate_for(violation)
        return RevisionOperation(
            layer=violation.layer,
            rule_id=violation.rule_id,
            severity=violation.severity,
            span=violation.span,
            tactic=candidate.tactic,
            candidate_rewrite=candidate.candidate_rewrite,
        )

    def _candidate_for(self, violation: Violation) -> RewriteCandidate:
        if violation.rule_id == "surface.contraction":
            return rewrite_for_contraction()
        return tactic_only(
            violation.rewrite_tactics[0] if violation.rewrite_tactics else violation.message
        )


def _severity_rank(severity) -> int:
    return {"error": 3, "warning": 2, "info": 1}[severity.value]
