<a id="rules-linkage"></a>

# Rules — linkage

Linkage-layer rules covering transitions, case scaffolding, stress position, and connectors.

<a id="module-hermeneia.rules.linkage.banned_transition"></a>

<a id="banned-transition"></a>

## Banned transition

Content-free transitional scaffolding.

<a id="hermeneia.rules.linkage.banned_transition.BannedTransitionRule"></a>

### *class* hermeneia.rules.linkage.banned_transition.BannedTransitionRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Bannedtransitionrule.

<a id="hermeneia.rules.linkage.banned_transition.BannedTransitionRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='linkage.banned_transition', label='Avoid content-free transition scaffolding', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('transition',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.linkage.banned_transition.BannedTransitionRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

* **Parameters:**
  * **lines** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Source lines involved in this computation.
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.linkage.banned_transition.register"></a>

### hermeneia.rules.linkage.banned_transition.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.linkage.case_scaffolding"></a>

<a id="case-scaffolding"></a>

## Case scaffolding

Case-scaffolding noun-phrase checks.

<a id="hermeneia.rules.linkage.case_scaffolding.CaseScaffoldingRule"></a>

### *class* hermeneia.rules.linkage.case_scaffolding.CaseScaffoldingRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Casescaffoldingrule.

<a id="hermeneia.rules.linkage.case_scaffolding.CaseScaffoldingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='linkage.case_scaffolding', label='Avoid noun-phrase case scaffolding', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.linkage.case_scaffolding.CaseScaffoldingRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

* **Parameters:**
  * **lines** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Source lines involved in this computation.
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.linkage.case_scaffolding.register"></a>

### hermeneia.rules.linkage.case_scaffolding.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.linkage.numbered_case"></a>

<a id="numbered-case"></a>

## Numbered case

Numbered case-split checks.

<a id="hermeneia.rules.linkage.numbered_case.NumberedCaseRule"></a>

### *class* hermeneia.rules.linkage.numbered_case.NumberedCaseRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Numberedcaserule.

<a id="hermeneia.rules.linkage.numbered_case.NumberedCaseRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='linkage.numbered_case', label='Prefer named cases over anonymous numbered case splits', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.linkage.numbered_case.NumberedCaseRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

* **Parameters:**
  * **lines** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Source lines involved in this computation.
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.linkage.numbered_case.register"></a>

### hermeneia.rules.linkage.numbered_case.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.linkage.semicolon_connector"></a>

<a id="semicolon-connector"></a>

## Semicolon connector

Semicolon connector articulation checks.

<a id="hermeneia.rules.linkage.semicolon_connector.SemicolonConnectorRule"></a>

### *class* hermeneia.rules.linkage.semicolon_connector.SemicolonConnectorRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Semicolonconnectorrule.

<a id="hermeneia.rules.linkage.semicolon_connector.SemicolonConnectorRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='linkage.semicolon_connector', label='Semicolon joins should include explicit connective framing', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'apply_block_kinds': ('paragraph',)}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'right_clause_preview'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.linkage.semicolon_connector.SemicolonConnectorRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.linkage.semicolon_connector.register"></a>

### hermeneia.rules.linkage.semicolon_connector.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.linkage.stress_position"></a>

<a id="stress-position"></a>

## Stress position

Sentence stress-position heuristics.

<a id="hermeneia.rules.linkage.stress_position.StressPositionRule"></a>

### *class* hermeneia.rules.linkage.stress_position.StressPositionRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Stresspositionrule.

<a id="hermeneia.rules.linkage.stress_position.StressPositionRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='linkage.stress_position', label='Sentence stress position appears weak', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset({'symbol_dense_sentence', 'heavy_math_masking'}), evidence_fields=('final_token',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.linkage.stress_position.StressPositionRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.linkage.stress_position.register"></a>

### hermeneia.rules.linkage.stress_position.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.linkage.transition_quality"></a>

<a id="transition-quality"></a>

## Transition quality

Discourse-transition articulation heuristics.

<a id="hermeneia.rules.linkage.transition_quality.TransitionQualityRule"></a>

### *class* hermeneia.rules.linkage.transition_quality.TransitionQualityRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Transitionqualityrule.

<a id="hermeneia.rules.linkage.transition_quality.TransitionQualityRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='linkage.transition_quality', label='Discourse transitions are weakly articulated', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'apply_block_kinds': ('paragraph',), 'min_overlap_without_connector': 0.18, 'max_shift_findings': 3, 'min_paragraph_sentences': 4, 'min_average_overlap_without_connectors': 0.35, 'detect_if_without_then': True, 'max_if_without_then_findings': 3, 'detect_implicit_contrast': True, 'max_implicit_contrast_findings': 3, 'min_overlap_for_implicit_contrast': 0.2}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.linkage.transition_quality.TransitionQualityRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.linkage.transition_quality.register"></a>

### hermeneia.rules.linkage.transition_quality.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
