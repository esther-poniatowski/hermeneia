<a id="scoring"></a>

# Scoring

Hierarchical scoring of rule violations.

<a id="module-hermeneia.scoring.scorer"></a>

<a id="scorer"></a>

## Scorer

Hierarchical scoring over violation sets.

<a id="hermeneia.scoring.scorer.LayerScore"></a>

### *class* hermeneia.scoring.scorer.LayerScore(layer, violation_count, weighted_penalty, score)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Layerscore.

<a id="hermeneia.scoring.scorer.LayerScore.layer"></a>

#### layer *: [Layer](rules-base.md#hermeneia.rules.base.Layer)*

<a id="hermeneia.scoring.scorer.LayerScore.violation_count"></a>

#### violation_count *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.scoring.scorer.LayerScore.weighted_penalty"></a>

#### weighted_penalty *: [float](https://docs.python.org/3/library/functions.html#float)*

<a id="hermeneia.scoring.scorer.LayerScore.score"></a>

#### score *: [float](https://docs.python.org/3/library/functions.html#float)*

<a id="hermeneia.scoring.scorer.Scorecard"></a>

### *class* hermeneia.scoring.scorer.Scorecard(layer_scores, global_score)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Scorecard.

<a id="hermeneia.scoring.scorer.Scorecard.layer_scores"></a>

#### layer_scores *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[LayerScore](#hermeneia.scoring.scorer.LayerScore), ...]*

<a id="hermeneia.scoring.scorer.Scorecard.global_score"></a>

#### global_score *: [float](https://docs.python.org/3/library/functions.html#float)*

<a id="hermeneia.scoring.scorer.HierarchicalScorer"></a>

### *class* hermeneia.scoring.scorer.HierarchicalScorer

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Score a violation list by layer with deterministic weights.

<a id="hermeneia.scoring.scorer.HierarchicalScorer.score"></a>

#### score(violations, rule_weights)

Score.

* **Parameters:**
  * **violations** (*Sequence* *[*[*Violation*](rules-base.md#hermeneia.rules.base.Violation) *]*) – Input value for `violations`.
  * **rule_weights** (*Mapping* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*) – Input value for `rule_weights`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Scorecard](#hermeneia.scoring.scorer.Scorecard)
