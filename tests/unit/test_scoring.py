from __future__ import annotations

import pytest

from hermeneia.document.model import Span
from hermeneia.rules.base import Layer, Severity, Violation
from hermeneia.scoring.scorer import HierarchicalScorer


def test_hierarchical_scorer_applies_rule_weights_by_layer() -> None:
    span = Span(0, 5, 1, 1, 1, 6)
    scorecard = HierarchicalScorer().score(
        [
            Violation(
                "vocabulary.contraction", "x", span, Severity.WARNING, Layer.SURFACE_STYLE
            ),
            Violation(
                "math.display_math", "y", span, Severity.ERROR, Layer.SURFACE_STYLE
            ),
            Violation(
                "paragraph.topic_sentence",
                "z",
                span,
                Severity.INFO,
                Layer.PARAGRAPH_RHETORIC,
            ),
        ],
        rule_weights={
            "vocabulary.contraction": 1.0,
            "math.display_math": 0.25,
            "paragraph.topic_sentence": 2.0,
        },
    )
    surface = next(
        layer for layer in scorecard.layer_scores if layer.layer == Layer.SURFACE_STYLE
    )
    paragraph = next(
        layer
        for layer in scorecard.layer_scores
        if layer.layer == Layer.PARAGRAPH_RHETORIC
    )
    assert surface.violation_count == 2
    assert surface.weighted_penalty == 1.5
    assert paragraph.weighted_penalty == 1.0
    assert scorecard.global_score == 87.5


def test_hierarchical_scorer_rejects_missing_rule_weight() -> None:
    span = Span(0, 5, 1, 1, 1, 6)
    with pytest.raises(
        ValueError, match="Missing rule weight for rule id 'vocabulary.contraction'"
    ):
        HierarchicalScorer().score(
            [
                Violation(
                    "vocabulary.contraction",
                    "x",
                    span,
                    Severity.WARNING,
                    Layer.SURFACE_STYLE,
                )
            ],
            rule_weights={},
        )


def test_hierarchical_scorer_rejects_negative_rule_weight() -> None:
    span = Span(0, 5, 1, 1, 1, 6)
    with pytest.raises(
        ValueError,
        match="Rule weight for rule id 'vocabulary.contraction' must be non-negative",
    ):
        HierarchicalScorer().score(
            [
                Violation(
                    "vocabulary.contraction",
                    "x",
                    span,
                    Severity.WARNING,
                    Layer.SURFACE_STYLE,
                )
            ],
            rule_weights={"vocabulary.contraction": -1.0},
        )
