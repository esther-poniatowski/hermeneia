<a id="rules-vocabulary"></a>

# Rules — vocabulary

Vocabulary-layer rules covering nominalization, vague phrasing, framing, and lexical economy.

<a id="module-hermeneia.rules.vocabulary.abstract_compound_modifier"></a>

<a id="abstract-compound-modifier"></a>

## Abstract compound modifier

Detect abstract compound modifiers that hide explicit relations.

<a id="hermeneia.rules.vocabulary.abstract_compound_modifier.AbstractCompoundModifierRule"></a>

### *class* hermeneia.rules.vocabulary.abstract_compound_modifier.AbstractCompoundModifierRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Abstractcompoundmodifierrule.

<a id="hermeneia.rules.vocabulary.abstract_compound_modifier.AbstractCompoundModifierRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.abstract_compound_modifier', label='Replace abstract compound modifiers with explicit relations', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'allow_lexicalized_exception': True, 'extra_lexicalized_adjectives': ()}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('compound', 'signal'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.abstract_compound_modifier.AbstractCompoundModifierRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.abstract_compound_modifier.register"></a>

### hermeneia.rules.vocabulary.abstract_compound_modifier.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.abstract_framing"></a>

<a id="abstract-framing"></a>

## Abstract framing

Abstract-framing checks for direct technical phrasing.

<a id="hermeneia.rules.vocabulary.abstract_framing.AbstractFramingRule"></a>

### *class* hermeneia.rules.vocabulary.abstract_framing.AbstractFramingRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Abstractframingrule.

<a id="hermeneia.rules.vocabulary.abstract_framing.AbstractFramingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.abstract_framing', label='Avoid abstract framing before the operative statement', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.abstract_framing.AbstractFramingRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.abstract_framing.register"></a>

### hermeneia.rules.vocabulary.abstract_framing.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.assumption_hypothesis_framing"></a>

<a id="assumption-hypothesis-framing"></a>

## Assumption-hypothesis framing

Detect noun-before-assumption/hypothesis framing that obscures core claims.

<a id="hermeneia.rules.vocabulary.assumption_hypothesis_framing.AssumptionHypothesisFramingRule"></a>

### *class* hermeneia.rules.vocabulary.assumption_hypothesis_framing.AssumptionHypothesisFramingRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Assumptionhypothesisframingrule.

<a id="hermeneia.rules.vocabulary.assumption_hypothesis_framing.AssumptionHypothesisFramingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.assumption_hypothesis_framing', label="Prefer 'assumption/hypothesis of ...' framing", layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('modifier', 'target'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.assumption_hypothesis_framing.AssumptionHypothesisFramingRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.assumption_hypothesis_framing.register"></a>

### hermeneia.rules.vocabulary.assumption_hypothesis_framing.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.boilerplate_opener"></a>

<a id="boilerplate-opener"></a>

## Boilerplate opener

Detect boilerplate sentence openers that delay the key claim.

<a id="hermeneia.rules.vocabulary.boilerplate_opener.BoilerplateOpenerRule"></a>

### *class* hermeneia.rules.vocabulary.boilerplate_opener.BoilerplateOpenerRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Boilerplateopenerrule.

<a id="hermeneia.rules.vocabulary.boilerplate_opener.BoilerplateOpenerRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.boilerplate_opener', label='Avoid boilerplate openers in declarative prose', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('opener',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.boilerplate_opener.BoilerplateOpenerRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.vocabulary.boilerplate_opener.register"></a>

### hermeneia.rules.vocabulary.boilerplate_opener.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.cardinality_framing"></a>

<a id="cardinality-framing"></a>

## Cardinality framing

Detect taxonomy-style explicit cardinality framing.

<a id="hermeneia.rules.vocabulary.cardinality_framing.CardinalityFramingRule"></a>

### *class* hermeneia.rules.vocabulary.cardinality_framing.CardinalityFramingRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Cardinalityframingrule.

<a id="hermeneia.rules.vocabulary.cardinality_framing.CardinalityFramingRule.options_model"></a>

#### options_model

alias of `_CardinalityFramingOptions`

<a id="hermeneia.rules.vocabulary.cardinality_framing.CardinalityFramingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.cardinality_framing', label='Avoid explicit cardinality labels in taxonomy framing', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('number', 'target'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.cardinality_framing.CardinalityFramingRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

<a id="hermeneia.rules.vocabulary.cardinality_framing.register"></a>

### hermeneia.rules.vocabulary.cardinality_framing.register(registry)

Register.

<a id="module-hermeneia.rules.vocabulary.concrete_subject"></a>

<a id="concrete-subject"></a>

## Concrete subject

Detect document/tool subjects used as the main actor.

<a id="hermeneia.rules.vocabulary.concrete_subject.ConcreteSubjectRule"></a>

### *class* hermeneia.rules.vocabulary.concrete_subject.ConcreteSubjectRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Concretesubjectrule.

<a id="hermeneia.rules.vocabulary.concrete_subject.ConcreteSubjectRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.concrete_subject', label='Use concrete technical subjects instead of document/tool subjects', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('subject', 'verb'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.concrete_subject.ConcreteSubjectRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.concrete_subject.register"></a>

### hermeneia.rules.vocabulary.concrete_subject.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.contraction"></a>

<a id="contraction"></a>

## Contraction

Contraction bans for formal technical prose.

<a id="hermeneia.rules.vocabulary.contraction.ContractionRule"></a>

### *class* hermeneia.rules.vocabulary.contraction.ContractionRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Contractionrule.

<a id="hermeneia.rules.vocabulary.contraction.ContractionRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.contraction', label='Avoid contractions in formal technical prose', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('contraction',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.contraction.ContractionRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.contraction.register"></a>

### hermeneia.rules.vocabulary.contraction.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.double_negative"></a>

<a id="double-negative"></a>

## Double negative

Detect double-negative constructions in prose sentences.

<a id="hermeneia.rules.vocabulary.double_negative.DoubleNegativeRule"></a>

### *class* hermeneia.rules.vocabulary.double_negative.DoubleNegativeRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Doublenegativerule.

<a id="hermeneia.rules.vocabulary.double_negative.DoubleNegativeRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.double_negative', label='Avoid double-negative scaffolding', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_gap_tokens': 5}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('matched_text',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.double_negative.DoubleNegativeRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.double_negative.register"></a>

### hermeneia.rules.vocabulary.double_negative.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.filler_noun_scaffolding"></a>

<a id="filler-noun-scaffolding"></a>

## Filler-noun scaffolding

Detect filler nouns that weaken technical precision.

<a id="hermeneia.rules.vocabulary.filler_noun_scaffolding.FillerNounScaffoldingRule"></a>

### *class* hermeneia.rules.vocabulary.filler_noun_scaffolding.FillerNounScaffoldingRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Fillernounscaffoldingrule.

<a id="hermeneia.rules.vocabulary.filler_noun_scaffolding.FillerNounScaffoldingRule.options_model"></a>

#### options_model

alias of `_FillerNounScaffoldingOptions`

<a id="hermeneia.rules.vocabulary.filler_noun_scaffolding.FillerNounScaffoldingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.filler_noun_scaffolding', label='Avoid filler nouns in technical claims', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('term',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.filler_noun_scaffolding.FillerNounScaffoldingRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

<a id="hermeneia.rules.vocabulary.filler_noun_scaffolding.register"></a>

### hermeneia.rules.vocabulary.filler_noun_scaffolding.register(registry)

Register.

<a id="module-hermeneia.rules.vocabulary.indefinite_reference"></a>

<a id="indefinite-reference"></a>

## Indefinite reference

Indefinite-pronoun/adverb checks.

<a id="hermeneia.rules.vocabulary.indefinite_reference.IndefiniteReferenceRule"></a>

### *class* hermeneia.rules.vocabulary.indefinite_reference.IndefiniteReferenceRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Indefinitereferencerule.

<a id="hermeneia.rules.vocabulary.indefinite_reference.IndefiniteReferenceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.indefinite_reference', label='Avoid broad indefinite references in technical claims', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('term',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.indefinite_reference.IndefiniteReferenceRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.indefinite_reference.register"></a>

### hermeneia.rules.vocabulary.indefinite_reference.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.nominalization"></a>

<a id="nominalization"></a>

## Nominalization

Nominalization diagnostics with hard-blocker process-noun signals.

<a id="hermeneia.rules.vocabulary.nominalization.NominalizationRule"></a>

### *class* hermeneia.rules.vocabulary.nominalization.NominalizationRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Nominalizationrule.

<a id="hermeneia.rules.vocabulary.nominalization.NominalizationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.nominalization', label='Nominalization obscures direct action', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'allow_adjective_position_exception': True, 'allow_lexicalized_noun_exception': True, 'extra_lexicalized_nouns': ()}, profiles_active=frozenset(), abstain_when_flags=frozenset({'symbol_dense_sentence', 'heavy_math_masking'}), evidence_fields=('nominalization', 'support_verb', 'signal_type'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.nominalization.NominalizationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.vocabulary.nominalization.register"></a>

### hermeneia.rules.vocabulary.nominalization.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.noun_cluster"></a>

<a id="noun-cluster"></a>

## Noun cluster

Noun-cluster density checks.

<a id="hermeneia.rules.vocabulary.noun_cluster.NounClusterRule"></a>

### *class* hermeneia.rules.vocabulary.noun_cluster.NounClusterRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Nounclusterrule.

<a id="hermeneia.rules.vocabulary.noun_cluster.NounClusterRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.noun_cluster', label='Sentence contains an overloaded noun cluster', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_cluster_tokens': 4}, profiles_active=frozenset(), abstain_when_flags=frozenset({'symbol_dense_sentence', 'heavy_math_masking'}), evidence_fields=('cluster_length', 'cluster'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.noun_cluster.NounClusterRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.vocabulary.noun_cluster.register"></a>

### hermeneia.rules.vocabulary.noun_cluster.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.prep_chain"></a>

<a id="preposition-chain"></a>

## Preposition chain

Prepositional-chain density diagnostics.

<a id="hermeneia.rules.vocabulary.prep_chain.PrepChainRule"></a>

### *class* hermeneia.rules.vocabulary.prep_chain.PrepChainRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Prepchainrule.

<a id="hermeneia.rules.vocabulary.prep_chain.PrepChainRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.prep_chain', label='Sentence has dense prepositional chaining', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_prepositions': 4}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('preposition_count', 'prepositions'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.prep_chain.PrepChainRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.vocabulary.prep_chain.register"></a>

### hermeneia.rules.vocabulary.prep_chain.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.redundant_leadin"></a>

<a id="redundant-lead-in"></a>

## Redundant lead-in

Detect redundant lead-in phrases.

<a id="hermeneia.rules.vocabulary.redundant_leadin.RedundantLeadinRule"></a>

### *class* hermeneia.rules.vocabulary.redundant_leadin.RedundantLeadinRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Redundantleadinrule.

<a id="hermeneia.rules.vocabulary.redundant_leadin.RedundantLeadinRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.redundant_leadin', label='Avoid redundant lead-in scaffolding', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.redundant_leadin.RedundantLeadinRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.redundant_leadin.register"></a>

### hermeneia.rules.vocabulary.redundant_leadin.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.stacked_nominalization_chain"></a>

<a id="stacked-nominalization-chain"></a>

## Stacked nominalization chain

Detect stacked nominalization chains in a single phrase.

<a id="hermeneia.rules.vocabulary.stacked_nominalization_chain.StackedNominalizationChainRule"></a>

### *class* hermeneia.rules.vocabulary.stacked_nominalization_chain.StackedNominalizationChainRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Stackednominalizationchainrule.

<a id="hermeneia.rules.vocabulary.stacked_nominalization_chain.StackedNominalizationChainRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.stacked_nominalization_chain', label='Avoid stacked nominalization chains', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_chain': 3}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('chain_length', 'nominalizations'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.stacked_nominalization_chain.StackedNominalizationChainRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.vocabulary.stacked_nominalization_chain.register"></a>

### hermeneia.rules.vocabulary.stacked_nominalization_chain.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.vague_phrasing"></a>

<a id="vague-phrasing"></a>

## Vague phrasing

Vague mechanism-phrasing checks.

<a id="hermeneia.rules.vocabulary.vague_phrasing.VaguePhrasingRule"></a>

### *class* hermeneia.rules.vocabulary.vague_phrasing.VaguePhrasingRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Vaguephrasingrule.

<a id="hermeneia.rules.vocabulary.vague_phrasing.VaguePhrasingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.vague_phrasing', label='Avoid vague mechanism phrasing', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.vague_phrasing.VaguePhrasingRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.vague_phrasing.register"></a>

### hermeneia.rules.vocabulary.vague_phrasing.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.vague_procedural_nominalization"></a>

<a id="vague-procedural-nominalization"></a>

## Vague procedural nominalization

Detect vague procedural nominalizations with missing argument structure.

<a id="hermeneia.rules.vocabulary.vague_procedural_nominalization.VagueProceduralNominalizationRule"></a>

### *class* hermeneia.rules.vocabulary.vague_procedural_nominalization.VagueProceduralNominalizationRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Vagueproceduralnominalizationrule.

<a id="hermeneia.rules.vocabulary.vague_procedural_nominalization.VagueProceduralNominalizationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.vague_procedural_nominalization', label='Procedural nominalization should name its arguments', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('term', 'signal'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.vague_procedural_nominalization.VagueProceduralNominalizationRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.vague_procedural_nominalization.register"></a>

### hermeneia.rules.vocabulary.vague_procedural_nominalization.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.vocabulary.verbose_preamble"></a>

<a id="verbose-preamble"></a>

## Verbose preamble

Detect verbose preambles that delay the operative statement.

<a id="hermeneia.rules.vocabulary.verbose_preamble.VerbosePreambleRule"></a>

### *class* hermeneia.rules.vocabulary.verbose_preamble.VerbosePreambleRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Verbosepreamblerule.

<a id="hermeneia.rules.vocabulary.verbose_preamble.VerbosePreambleRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='vocabulary.verbose_preamble', label='Avoid verbose preambles before the main claim', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.vocabulary.verbose_preamble.VerbosePreambleRule.check_source"></a>

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

<a id="hermeneia.rules.vocabulary.verbose_preamble.register"></a>

### hermeneia.rules.vocabulary.verbose_preamble.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
