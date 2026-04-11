from __future__ import annotations

from hermeneia.document.model import Span
from hermeneia.rules.base import Layer, RuleEvidence, Severity, Violation
from hermeneia.suggest.planner import RevisionPlanner


def test_revision_plan_orders_by_logical_phase_before_local_rewrites() -> None:
    span = Span(0, 1, 1, 1, 1, 2)
    plan = RevisionPlanner().build(
        [
            Violation(
                "vocabulary.contraction",
                "surface",
                span,
                Severity.ERROR,
                Layer.SURFACE_STYLE,
            ),
            Violation(
                "structure.heading_parallelism",
                "structure",
                span,
                Severity.INFO,
                Layer.DOCUMENT_STRUCTURE,
            ),
            Violation(
                "paragraph.topic_sentence",
                "paragraph-warning",
                span,
                Severity.WARNING,
                Layer.PARAGRAPH_RHETORIC,
            ),
            Violation(
                "paragraph.mixed_topic",
                "paragraph-error",
                span,
                Severity.ERROR,
                Layer.PARAGRAPH_RHETORIC,
            ),
            Violation(
                "syntax.subject_verb_distance",
                "discourse",
                span,
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
            Violation(
                "terminology.definition_before_use",
                "audience",
                span,
                Severity.ERROR,
                Layer.AUDIENCE_FIT,
            ),
        ]
    )
    assert tuple(operation.rule_id for operation in plan.operations) == (
        "structure.heading_parallelism",
        "paragraph.mixed_topic",
        "paragraph.topic_sentence",
        "syntax.subject_verb_distance",
        "terminology.definition_before_use",
        "vocabulary.contraction",
    )


def test_revision_plan_uses_position_and_rule_id_for_stable_ties() -> None:
    plan = RevisionPlanner().build(
        [
            Violation(
                "sentence.b",
                "late",
                Span(30, 35, 3, 1, 3, 6),
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
            Violation(
                "sentence.c",
                "same-span-c",
                Span(10, 15, 1, 1, 1, 6),
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
            Violation(
                "sentence.a",
                "same-span-a",
                Span(10, 15, 1, 1, 1, 6),
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
        ]
    )
    assert tuple(operation.rule_id for operation in plan.operations) == (
        "sentence.a",
        "sentence.c",
        "sentence.b",
    )


def test_revision_plan_contraction_emits_guarded_template_candidate() -> None:
    span = Span(0, 4, 1, 1, 1, 5)
    plan = RevisionPlanner().build(
        [
            Violation(
                "vocabulary.contraction",
                "Expand contraction",
                span,
                Severity.WARNING,
                Layer.SURFACE_STYLE,
                evidence=RuleEvidence(features={"contraction": "it's"}),
            )
        ]
    )
    op = plan.operations[0]
    assert op.tactic == "Expand 'it's' to its full form."
    assert op.candidate_rewrite == "it is"


def test_revision_plan_nominalization_template_requires_stable_mapping() -> None:
    span = Span(0, 5, 1, 1, 1, 6)
    plan = RevisionPlanner().build(
        [
            Violation(
                "vocabulary.nominalization",
                "nominalization",
                span,
                Severity.WARNING,
                Layer.SURFACE_STYLE,
                evidence=RuleEvidence(
                    features={"nominalization": "construction", "support_verb": "is"}
                ),
                rewrite_tactics=("Prefer a direct verb construction.",),
            ),
            Violation(
                "vocabulary.nominalization",
                "nominalization",
                span,
                Severity.WARNING,
                Layer.SURFACE_STYLE,
                evidence=RuleEvidence(
                    features={"nominalization": "compactness", "support_verb": "is"}
                ),
                rewrite_tactics=("Prefer a direct verb construction.",),
            ),
        ]
    )
    first, second = plan.operations
    assert first.candidate_rewrite == "construct"
    assert second.candidate_rewrite is None
    assert second.tactic == "Prefer a direct verb construction."


def test_revision_plan_falls_back_to_explicit_manual_tactic_when_absent() -> None:
    span = Span(10, 12, 1, 11, 1, 13)
    plan = RevisionPlanner().build(
        [
            Violation(
                "unknown.rule",
                "diagnostic message",
                span,
                Severity.INFO,
                Layer.LOCAL_DISCOURSE,
            )
        ]
    )
    op = plan.operations[0]
    assert op.candidate_rewrite is None
    assert op.tactic.startswith("No deterministic rewrite candidate is available")


def test_revision_plan_passive_voice_template_requires_identifiable_actor() -> None:
    span = Span(0, 8, 1, 1, 1, 9)
    plan = RevisionPlanner().build(
        [
            Violation(
                "syntax.passive_voice",
                "passive voice",
                span,
                Severity.WARNING,
                Layer.SURFACE_STYLE,
                evidence=RuleEvidence(features={"participle": "derived"}),
                rewrite_tactics=("Rewrite the clause in active voice.",),
            ),
            Violation(
                "syntax.passive_voice",
                "passive voice",
                span,
                Severity.WARNING,
                Layer.SURFACE_STYLE,
                evidence=RuleEvidence(features={"actor": "the authors", "participle": "derived"}),
                rewrite_tactics=("Rewrite the clause in active voice.",),
            ),
        ]
    )
    without_actor, with_actor = plan.operations
    assert without_actor.candidate_rewrite is None
    assert without_actor.tactic == "Rewrite the clause in active voice."
    assert with_actor.tactic == (
        "Rewrite in active voice with 'the authors' as the grammatical subject."
    )
    assert with_actor.candidate_rewrite == "The authors derived ..."
