<a id="rules-math"></a>

# Rules — math

Math-layer rules covering display blocks, inline math, proof discipline, and prose-math integration.

<a id="module-hermeneia.rules.math.assumption_motivation_order"></a>

<a id="assumption-motivation-order"></a>

## Assumption motivation order

Assumption-before-motivation ordering checks.

<a id="hermeneia.rules.math.assumption_motivation_order.AssumptionMotivationOrderRule"></a>

### *class* hermeneia.rules.math.assumption_motivation_order.AssumptionMotivationOrderRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Assumptionmotivationorderrule.

<a id="hermeneia.rules.math.assumption_motivation_order.AssumptionMotivationOrderRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.assumption_motivation_order', label='Assumptions should be introduced by purpose', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'lookback_sentences': 1}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('assumption_marker', 'has_prefix_purpose', 'previous_has_purpose'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.assumption_motivation_order.AssumptionMotivationOrderRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.math.assumption_motivation_order.register"></a>

### hermeneia.rules.math.assumption_motivation_order.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.bare_symbol"></a>

<a id="bare-symbol"></a>

## Bare symbol

Bare-symbol detection for math prose.

<a id="hermeneia.rules.math.bare_symbol.BareSymbolRule"></a>

### *class* hermeneia.rules.math.bare_symbol.BareSymbolRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Baresymbolrule.

<a id="hermeneia.rules.math.bare_symbol.BareSymbolRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.bare_symbol', label='Symbols in qualifier or prepositional position must carry object names', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('matched_text',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.bare_symbol.BareSymbolRule.check_source"></a>

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

<a id="hermeneia.rules.math.bare_symbol.register"></a>

### hermeneia.rules.math.bare_symbol.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.consecutive_display_blocks_without_bridge"></a>

<a id="consecutive-display-blocks-without-bridge"></a>

## Consecutive display blocks without bridge

Consecutive display-block bridge checks.

<a id="hermeneia.rules.math.consecutive_display_blocks_without_bridge.ConsecutiveDisplayBlocksWithoutBridgeRule"></a>

### *class* hermeneia.rules.math.consecutive_display_blocks_without_bridge.ConsecutiveDisplayBlocksWithoutBridgeRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Consecutivedisplayblockswithoutbridgerule.

<a id="hermeneia.rules.math.consecutive_display_blocks_without_bridge.ConsecutiveDisplayBlocksWithoutBridgeRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.consecutive_display_blocks_without_bridge', label='Consecutive display equations need a motivational bridge', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_chain_length': 2}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('chain_length', 'has_preceding_motivation'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.consecutive_display_blocks_without_bridge.ConsecutiveDisplayBlocksWithoutBridgeRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.math.consecutive_display_blocks_without_bridge.register"></a>

### hermeneia.rules.math.consecutive_display_blocks_without_bridge.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.display_ambiguous"></a>

<a id="display-ambiguous"></a>

## Display ambiguous

Ambiguous display-math delimiter checks.

<a id="hermeneia.rules.math.display_ambiguous.DisplayAmbiguousRule"></a>

### *class* hermeneia.rules.math.display_ambiguous.DisplayAmbiguousRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Displayambiguousrule.

<a id="hermeneia.rules.math.display_ambiguous.DisplayAmbiguousRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.display_ambiguous', label='Avoid ambiguous multiple display delimiters on one line', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('delimiter_count',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.display_ambiguous.DisplayAmbiguousRule.check_source"></a>

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

<a id="hermeneia.rules.math.display_ambiguous.register"></a>

### hermeneia.rules.math.display_ambiguous.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.display_followup_interpretation"></a>

<a id="display-follow-up-interpretation"></a>

## Display follow-up interpretation

Post-display interpretation checks.

<a id="hermeneia.rules.math.display_followup_interpretation.DisplayFollowupInterpretationRule"></a>

### *class* hermeneia.rules.math.display_followup_interpretation.DisplayFollowupInterpretationRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Displayfollowupinterpretationrule.

<a id="hermeneia.rules.math.display_followup_interpretation.DisplayFollowupInterpretationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.display_followup_interpretation', label='Display formulas should be followed by interpretive prose', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_display_chars': 12}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.display_followup_interpretation.DisplayFollowupInterpretationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.math.display_followup_interpretation.register"></a>

### hermeneia.rules.math.display_followup_interpretation.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.display_math"></a>

<a id="display-math"></a>

## Display math

Display-math structure and lead-in checks.

<a id="hermeneia.rules.math.display_math.DisplayMathRule"></a>

### *class* hermeneia.rules.math.display_math.DisplayMathRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Displaymathrule.

<a id="hermeneia.rules.math.display_math.DisplayMathRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.display_math', label='Display math must have a meaningful lead-in and no line-break punctuation', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'require_leadin': True, 'require_leadin_colon': True}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('check',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.display_math.DisplayMathRule.check_source"></a>

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

<a id="hermeneia.rules.math.display_math.register"></a>

### hermeneia.rules.math.display_math.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.display_unclosed"></a>

<a id="display-unclosed"></a>

## Display unclosed

Unclosed display-math delimiter checks.

<a id="hermeneia.rules.math.display_unclosed.DisplayUnclosedRule"></a>

### *class* hermeneia.rules.math.display_unclosed.DisplayUnclosedRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Displayunclosedrule.

<a id="hermeneia.rules.math.display_unclosed.DisplayUnclosedRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.display_unclosed', label='Display math delimiters must be properly closed', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('opening_line',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.display_unclosed.DisplayUnclosedRule.check_source"></a>

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

<a id="hermeneia.rules.math.display_unclosed.register"></a>

### hermeneia.rules.math.display_unclosed.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.imperative_opening"></a>

<a id="imperative-opening"></a>

## Imperative opening

Imperative-opening bans for mathematical prose.

<a id="hermeneia.rules.math.imperative_opening.ImperativeOpeningRule"></a>

### *class* hermeneia.rules.math.imperative_opening.ImperativeOpeningRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Imperativeopeningrule.

<a id="hermeneia.rules.math.imperative_opening.ImperativeOpeningRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.imperative_opening', label='Avoid imperative mathematical openings', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('verb',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.imperative_opening.ImperativeOpeningRule.check_source"></a>

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

<a id="hermeneia.rules.math.imperative_opening.register"></a>

### hermeneia.rules.math.imperative_opening.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.inline_math"></a>

<a id="inline-math"></a>

## Inline math

Equation-like inline-math checks.

<a id="hermeneia.rules.math.inline_math.InlineMathRule"></a>

### *class* hermeneia.rules.math.inline_math.InlineMathRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Inlinemathrule.

<a id="hermeneia.rules.math.inline_math.InlineMathRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.inline_math', label='Avoid equation-like inline math when display math is clearer', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_inline_length': 40}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('reason', 'expression'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.inline_math.InlineMathRule.check_source"></a>

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

<a id="hermeneia.rules.math.inline_math.register"></a>

### hermeneia.rules.math.inline_math.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.proof_marker"></a>

<a id="proof-marker"></a>

## Proof marker

Proof-marker placement checks.

<a id="hermeneia.rules.math.proof_marker.ProofMarkerRule"></a>

### *class* hermeneia.rules.math.proof_marker.ProofMarkerRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Proofmarkerrule.

<a id="hermeneia.rules.math.proof_marker.ProofMarkerRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.proof_marker', label='Proof end markers require explicit proof opener', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_lookback_lines': 12}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('end_marker', 'has_proof_opener'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.proof_marker.ProofMarkerRule.check_source"></a>

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

<a id="hermeneia.rules.math.proof_marker.register"></a>

### hermeneia.rules.math.proof_marker.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.proof_placement_context"></a>

<a id="proof-placement-context"></a>

## Proof placement context

Proof-placement context checks.

<a id="hermeneia.rules.math.proof_placement_context.ProofPlacementContextRule"></a>

### *class* hermeneia.rules.math.proof_placement_context.ProofPlacementContextRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Proofplacementcontextrule.

<a id="hermeneia.rules.math.proof_placement_context.ProofPlacementContextRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.proof_placement_context', label='Proof opener should follow interpretive context', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'previous_block_kind'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.proof_placement_context.ProofPlacementContextRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.math.proof_placement_context.register"></a>

### hermeneia.rules.math.proof_placement_context.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.prose_math"></a>

<a id="prose-math"></a>

## Prose math

Prose paraphrase checks for mathematical relations.

<a id="hermeneia.rules.math.prose_math.ProseMathRule"></a>

### *class* hermeneia.rules.math.prose_math.ProseMathRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Prosemathrule.

<a id="hermeneia.rules.math.prose_math.ProseMathRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.prose_math', label='Avoid prose paraphrases for explicit mathematical relations', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.prose_math.ProseMathRule.check_source"></a>

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

<a id="hermeneia.rules.math.prose_math.register"></a>

### hermeneia.rules.math.prose_math.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.math.shorthand"></a>

<a id="shorthand"></a>

## Shorthand

Math-shorthand introduction checks.

<a id="hermeneia.rules.math.shorthand.ShorthandRule"></a>

### *class* hermeneia.rules.math.shorthand.ShorthandRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Shorthandrule.

<a id="hermeneia.rules.math.shorthand.ShorthandRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='math.shorthand', label='Avoid unnecessary shorthand for input magnitude', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('pattern',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.math.shorthand.ShorthandRule.check_source"></a>

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

<a id="hermeneia.rules.math.shorthand.register"></a>

### hermeneia.rules.math.shorthand.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
