<a id="report"></a>

# Report

Diagnostic emission, annotations, and revision-plan composition.

<a id="module-hermeneia.report.annotations"></a>

<a id="annotations"></a>

## Annotations

Inline source-annotation rendering for text reports.

<a id="hermeneia.report.annotations.AnnotatedLine"></a>

### *class* hermeneia.report.annotations.AnnotatedLine(line_number, line_text, marker_line)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Annotatedline.

<a id="hermeneia.report.annotations.AnnotatedLine.line_number"></a>

#### line_number *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.report.annotations.AnnotatedLine.line_text"></a>

#### line_text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.report.annotations.AnnotatedLine.marker_line"></a>

#### marker_line *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.report.annotations.AnnotatedExcerpt"></a>

### *class* hermeneia.report.annotations.AnnotatedExcerpt(lines)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Annotatedexcerpt.

<a id="hermeneia.report.annotations.AnnotatedExcerpt.lines"></a>

#### lines *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[AnnotatedLine](#hermeneia.report.annotations.AnnotatedLine), ...]*

<a id="hermeneia.report.annotations.build_excerpt"></a>

### hermeneia.report.annotations.build_excerpt(source, span)

Build excerpt.

* **Parameters:**
  * **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Source text to parse or analyze.
  * **span** ([*Span*](document.md#hermeneia.document.model.Span)) – Input value for `span`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [AnnotatedExcerpt](#hermeneia.report.annotations.AnnotatedExcerpt)

<a id="hermeneia.report.annotations.annotate_violations"></a>

### hermeneia.report.annotations.annotate_violations(source, violations)

Annotate violations.

* **Parameters:**
  * **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Source text to parse or analyze.
  * **violations** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*Violation*](rules-base.md#hermeneia.rules.base.Violation) *,*  *...* *]*) – Input value for `violations`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[AnnotatedExcerpt](#hermeneia.report.annotations.AnnotatedExcerpt), …]

<a id="module-hermeneia.report.diagnostic"></a>

<a id="diagnostic"></a>

## Diagnostic

Diagnostic report DTOs and serialization helpers.

<a id="hermeneia.report.diagnostic.DiagnosticReport"></a>

### *class* hermeneia.report.diagnostic.DiagnosticReport(path, violations, scorecard, revision_plan, scoring_output=frozenset({'global_score', 'layer_scores', 'violation_list'}))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Diagnosticreport.

<a id="hermeneia.report.diagnostic.DiagnosticReport.path"></a>

#### path *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.report.diagnostic.DiagnosticReport.violations"></a>

#### violations *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[Violation](rules-base.md#hermeneia.rules.base.Violation), ...]*

<a id="hermeneia.report.diagnostic.DiagnosticReport.scorecard"></a>

#### scorecard *: [Scorecard](scoring.md#hermeneia.scoring.scorer.Scorecard) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.report.diagnostic.DiagnosticReport.revision_plan"></a>

#### revision_plan *: [RevisionPlan](#hermeneia.report.revision_plan.RevisionPlan)*

<a id="hermeneia.report.diagnostic.DiagnosticReport.scoring_output"></a>

#### scoring_output *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'global_score', 'layer_scores', 'violation_list'})*

<a id="hermeneia.report.diagnostic.DiagnosticReport.to_dict"></a>

#### to_dict()

To dict.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]

<a id="hermeneia.report.diagnostic.DiagnosticReport.to_json"></a>

#### to_json()

To json.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="module-hermeneia.report.revision_plan"></a>

<a id="revision-plan"></a>

## Revision plan

Revision-plan report types.

<a id="hermeneia.report.revision_plan.RevisionOperation"></a>

### *class* hermeneia.report.revision_plan.RevisionOperation(layer, rule_id, severity, span, tactic, candidate_rewrite=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Revisionoperation.

<a id="hermeneia.report.revision_plan.RevisionOperation.layer"></a>

#### layer *: [Layer](rules-base.md#hermeneia.rules.base.Layer)*

<a id="hermeneia.report.revision_plan.RevisionOperation.rule_id"></a>

#### rule_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.report.revision_plan.RevisionOperation.severity"></a>

#### severity *: [Severity](rules-base.md#hermeneia.rules.base.Severity)*

<a id="hermeneia.report.revision_plan.RevisionOperation.span"></a>

#### span *: [Span](document.md#hermeneia.document.model.Span)*

<a id="hermeneia.report.revision_plan.RevisionOperation.tactic"></a>

#### tactic *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.report.revision_plan.RevisionOperation.candidate_rewrite"></a>

#### candidate_rewrite *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.report.revision_plan.RevisionPlan"></a>

### *class* hermeneia.report.revision_plan.RevisionPlan(operations)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Revisionplan.

<a id="hermeneia.report.revision_plan.RevisionPlan.operations"></a>

#### operations *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[RevisionOperation](#hermeneia.report.revision_plan.RevisionOperation), ...]*
