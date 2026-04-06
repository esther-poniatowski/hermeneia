from __future__ import annotations

from hermeneia.document.model import Span
from hermeneia.rules.base import Layer, Severity, Violation
from hermeneia.scoring.scorer import HierarchicalScorer


def test_hierarchical_scorer_groups_by_layer() -> None:
    span = Span(0, 5, 1, 1, 1, 6)
    scorecard = HierarchicalScorer().score(
        [
            Violation("surface.contraction", "x", span, Severity.WARNING, Layer.SURFACE_STYLE),
            Violation("math.display_math", "y", span, Severity.ERROR, Layer.SURFACE_STYLE),
            Violation(
                "paragraph.topic_sentence", "z", span, Severity.INFO, Layer.PARAGRAPH_RHETORIC
            ),
        ]
    )
    surface = next(layer for layer in scorecard.layer_scores if layer.layer == Layer.SURFACE_STYLE)
    assert surface.violation_count == 2
    assert scorecard.global_score < 100.0
