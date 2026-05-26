<a id="rules-evidence"></a>

# Rules — evidence

Evidence-layer rules covering claim calibration and quantifier discipline.

<a id="module-hermeneia.rules.evidence.claim_calibration"></a>

<a id="claim-calibration"></a>

## Claim calibration

Strong-claim calibration against nearby support signals.

<a id="hermeneia.rules.evidence.claim_calibration.ClaimCalibrationRule"></a>

### *class* hermeneia.rules.evidence.claim_calibration.ClaimCalibrationRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Claimcalibrationrule.

<a id="hermeneia.rules.evidence.claim_calibration.ClaimCalibrationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='evidence.claim_calibration', label='Strong claim lacks nearby evidence cues', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'lookback_sentences': 3}, profiles_active=frozenset(), abstain_when_flags=frozenset({'fragment_sentence', 'heavy_math_masking', 'symbol_dense_sentence'}), evidence_fields=('claim_markers', 'support_signals'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.evidence.claim_calibration.ClaimCalibrationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.evidence.claim_calibration.register"></a>

### hermeneia.rules.evidence.claim_calibration.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.evidence.imprecise_quantifier_without_citation"></a>

<a id="imprecise-quantifier-without-citation"></a>

## Imprecise quantifier without citation

Detect imprecise quantity references without citation support.

<a id="hermeneia.rules.evidence.imprecise_quantifier_without_citation.ImpreciseQuantifierWithoutCitationRule"></a>

### *class* hermeneia.rules.evidence.imprecise_quantifier_without_citation.ImpreciseQuantifierWithoutCitationRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Imprecisequantifierwithoutcitationrule.

<a id="hermeneia.rules.evidence.imprecise_quantifier_without_citation.ImpreciseQuantifierWithoutCitationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='evidence.imprecise_quantifier_without_citation', label='Imprecise quantifier references should carry citation support', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'lookback_sentences': 0}, profiles_active=frozenset(), abstain_when_flags=frozenset({'fragment_sentence', 'heavy_math_masking', 'symbol_dense_sentence'}), evidence_fields=('quantifiers', 'support_signals'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.evidence.imprecise_quantifier_without_citation.ImpreciseQuantifierWithoutCitationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.evidence.imprecise_quantifier_without_citation.register"></a>

### hermeneia.rules.evidence.imprecise_quantifier_without_citation.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.evidence.qualitative_claim_without_quant_support"></a>

<a id="qualitative-claim-without-quantitative-support"></a>

## Qualitative claim without quantitative support

Qualitative-claim support checks.

<a id="hermeneia.rules.evidence.qualitative_claim_without_quant_support.QualitativeClaimWithoutQuantSupportRule"></a>

### *class* hermeneia.rules.evidence.qualitative_claim_without_quant_support.QualitativeClaimWithoutQuantSupportRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Qualitativeclaimwithoutquantsupportrule.

<a id="hermeneia.rules.evidence.qualitative_claim_without_quant_support.QualitativeClaimWithoutQuantSupportRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='evidence.qualitative_claim_without_quant_support', label='Qualitative claim lacks nearby quantitative support', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'lookback_sentences': 2}, profiles_active=frozenset(), abstain_when_flags=frozenset({'fragment_sentence', 'heavy_math_masking', 'symbol_dense_sentence'}), evidence_fields=('claim_markers', 'support_signals'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.evidence.qualitative_claim_without_quant_support.QualitativeClaimWithoutQuantSupportRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.evidence.qualitative_claim_without_quant_support.register"></a>

### hermeneia.rules.evidence.qualitative_claim_without_quant_support.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
