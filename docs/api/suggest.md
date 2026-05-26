<a id="suggest"></a>

# Suggest

Suggestion planning and template materialization.

<a id="module-hermeneia.suggest.planner"></a>

<a id="planner"></a>

## Planner

Revision planning from violations.

<a id="hermeneia.suggest.planner.RevisionPlanner"></a>

### *class* hermeneia.suggest.planner.RevisionPlanner(default_mode=SuggestionMode.TACTIC_ONLY)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Revisionplanner.

* **Parameters:**
  **default_mode** ([*SuggestionMode*](rules-base.md#hermeneia.rules.base.SuggestionMode)) – Input value for `default_mode`.

<a id="hermeneia.suggest.planner.RevisionPlanner.__init__"></a>

#### \_\_init_\_(default_mode=SuggestionMode.TACTIC_ONLY)

Initialize the instance.

<a id="hermeneia.suggest.planner.RevisionPlanner.build"></a>

#### build(violations)

Build.

* **Parameters:**
  **violations** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*Violation*](rules-base.md#hermeneia.rules.base.Violation) *]*) – Input value for `violations`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RevisionPlan](report.md#hermeneia.report.revision_plan.RevisionPlan)

<a id="module-hermeneia.suggest.template"></a>

<a id="template"></a>

## Template

Guarded candidate rewrites.

<a id="hermeneia.suggest.template.RewriteCandidate"></a>

### *class* hermeneia.suggest.template.RewriteCandidate(tactic, candidate_rewrite=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Rewritecandidate.

<a id="hermeneia.suggest.template.RewriteCandidate.tactic"></a>

#### tactic *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.suggest.template.RewriteCandidate.candidate_rewrite"></a>

#### candidate_rewrite *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.suggest.template.rewrite_for_contraction"></a>

### hermeneia.suggest.template.rewrite_for_contraction(contraction)

Rewrite for contraction.

* **Parameters:**
  **contraction** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `contraction`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RewriteCandidate](#hermeneia.suggest.template.RewriteCandidate)

<a id="hermeneia.suggest.template.rewrite_for_proof_marker"></a>

### hermeneia.suggest.template.rewrite_for_proof_marker()

Rewrite for proof marker.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RewriteCandidate](#hermeneia.suggest.template.RewriteCandidate)

<a id="hermeneia.suggest.template.rewrite_for_nominalization"></a>

### hermeneia.suggest.template.rewrite_for_nominalization(nominalization, support_verb)

Rewrite for nominalization.

* **Parameters:**
  * **nominalization** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `nominalization`.
  * **support_verb** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `support_verb`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RewriteCandidate](#hermeneia.suggest.template.RewriteCandidate) | None

<a id="hermeneia.suggest.template.rewrite_for_passive_voice"></a>

### hermeneia.suggest.template.rewrite_for_passive_voice(actor, participle)

Rewrite for passive voice.

* **Parameters:**
  * **actor** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `actor`.
  * **participle** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `participle`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RewriteCandidate](#hermeneia.suggest.template.RewriteCandidate) | None

<a id="hermeneia.suggest.template.tactic_only"></a>

### hermeneia.suggest.template.tactic_only(message)

Tactic only.

* **Parameters:**
  **message** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `message`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RewriteCandidate](#hermeneia.suggest.template.RewriteCandidate)

<a id="hermeneia.suggest.template.no_deterministic_rewrite_available"></a>

### hermeneia.suggest.template.no_deterministic_rewrite_available()

No deterministic rewrite available.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RewriteCandidate](#hermeneia.suggest.template.RewriteCandidate)
