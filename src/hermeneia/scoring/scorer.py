"""Hierarchical scoring over violation sets."""

from __future__ import annotations

from dataclasses import dataclass

from hermeneia.rules.base import Layer, Severity, Violation

SEVERITY_WEIGHTS = {
    Severity.INFO: 0.5,
    Severity.WARNING: 1.0,
    Severity.ERROR: 2.0,
}


@dataclass(frozen=True)
class LayerScore:
    layer: Layer
    violation_count: int
    weighted_penalty: float
    score: float


@dataclass(frozen=True)
class Scorecard:
    layer_scores: tuple[LayerScore, ...]
    global_score: float


class HierarchicalScorer:
    """Score a violation list by layer with deterministic weights."""

    def score(self, violations: list[Violation]) -> Scorecard:
        per_layer: dict[Layer, list[Violation]] = {layer: [] for layer in Layer}
        for violation in violations:
            per_layer[violation.layer].append(violation)
        layer_scores = tuple(
            self._score_layer(layer, issues) for layer, issues in per_layer.items()
        )
        penalties = sum(score.weighted_penalty for score in layer_scores)
        global_score = max(0.0, 100.0 - penalties * 5.0)
        return Scorecard(layer_scores=layer_scores, global_score=round(global_score, 2))

    def _score_layer(self, layer: Layer, violations: list[Violation]) -> LayerScore:
        penalty = sum(SEVERITY_WEIGHTS[violation.severity] for violation in violations)
        score = max(0.0, 100.0 - penalty * 10.0)
        return LayerScore(
            layer=layer,
            violation_count=len(violations),
            weighted_penalty=round(penalty, 2),
            score=round(score, 2),
        )
