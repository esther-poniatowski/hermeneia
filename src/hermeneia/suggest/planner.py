"""Revision planning from violations."""

from __future__ import annotations

from hermeneia.report.revision_plan import RevisionOperation, RevisionPlan
from hermeneia.rules.base import Layer, Severity, SuggestionMode, Violation
from hermeneia.suggest.template import (
    RewriteCandidate,
    no_deterministic_rewrite_available,
    rewrite_for_contraction,
    rewrite_for_nominalization,
    rewrite_for_passive_voice,
    rewrite_for_proof_marker,
    tactic_only,
)


class RevisionPlanner:
    def __init__(self, default_mode: SuggestionMode = SuggestionMode.TACTIC_ONLY) -> None:
        self._default_mode = default_mode

    def build(self, violations: list[Violation]) -> RevisionPlan:
        operations = [self._operation_for(violation) for violation in violations]
        ordered = tuple(
            sorted(
                operations,
                key=lambda op: (
                    _layer_rank(op.layer),
                    -_severity_rank(op.severity),
                    op.span.start,
                    op.span.end,
                    op.rule_id,
                ),
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
        if violation.rule_id == "vocabulary.contraction":
            contraction = _evidence_str(violation, "contraction")
            return rewrite_for_contraction(contraction)
        if violation.rule_id == "math.proof_marker":
            return rewrite_for_proof_marker()
        if violation.rule_id == "syntax.passive_voice":
            candidate = rewrite_for_passive_voice(
                actor=_evidence_str(violation, "actor"),
                participle=_evidence_str(violation, "participle"),
            )
            if candidate is not None:
                return candidate
        if violation.rule_id == "vocabulary.nominalization":
            candidate = rewrite_for_nominalization(
                nominalization=_evidence_str(violation, "nominalization"),
                support_verb=_evidence_str(violation, "support_verb"),
            )
            if candidate is not None:
                return candidate
        if violation.rewrite_tactics:
            return tactic_only(violation.rewrite_tactics[0])
        if self._default_mode == SuggestionMode.NONE:
            return tactic_only("No suggestion configured for this violation.")
        if self._default_mode == SuggestionMode.TEMPLATE:
            return no_deterministic_rewrite_available()
        return no_deterministic_rewrite_available()


def _severity_rank(severity) -> int:
    return {
        Severity.ERROR: 3,
        Severity.WARNING: 2,
        Severity.INFO: 1,
    }[severity]


def _layer_rank(layer: Layer) -> int:
    return {
        Layer.DOCUMENT_STRUCTURE: 0,
        Layer.PARAGRAPH_RHETORIC: 1,
        Layer.LOCAL_DISCOURSE: 2,
        Layer.AUDIENCE_FIT: 3,
        Layer.SURFACE_STYLE: 4,
    }[layer]


def _evidence_str(violation: Violation, field: str) -> str | None:
    if violation.evidence is None:
        return None
    raw = violation.evidence.features.get(field)
    if isinstance(raw, str):
        return raw
    return None
