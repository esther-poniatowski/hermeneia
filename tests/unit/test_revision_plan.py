from __future__ import annotations

from hermeneia.document.model import Span
from hermeneia.rules.base import Layer, Severity, Violation
from hermeneia.suggest.planner import RevisionPlanner


def test_revision_plan_orders_by_logical_phase_before_local_rewrites() -> None:
    span = Span(0, 1, 1, 1, 1, 2)
    plan = RevisionPlanner().build(
        [
            Violation(
                "surface.contraction",
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
                "discourse.subject_verb_distance",
                "discourse",
                span,
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
            Violation(
                "audience.definition_before_use",
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
        "discourse.subject_verb_distance",
        "audience.definition_before_use",
        "surface.contraction",
    )


def test_revision_plan_uses_position_and_rule_id_for_stable_ties() -> None:
    plan = RevisionPlanner().build(
        [
            Violation(
                "discourse.b",
                "late",
                Span(30, 35, 3, 1, 3, 6),
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
            Violation(
                "discourse.c",
                "same-span-c",
                Span(10, 15, 1, 1, 1, 6),
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
            Violation(
                "discourse.a",
                "same-span-a",
                Span(10, 15, 1, 1, 1, 6),
                Severity.WARNING,
                Layer.LOCAL_DISCOURSE,
            ),
        ]
    )
    assert tuple(operation.rule_id for operation in plan.operations) == (
        "discourse.a",
        "discourse.c",
        "discourse.b",
    )
