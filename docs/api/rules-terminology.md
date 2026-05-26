<a id="rules-terminology"></a>

# Rules — terminology

Terminology-layer rules covering acronyms, jargon, and defined terms.

<a id="module-hermeneia.rules.terminology.acronym_burden"></a>

<a id="acronym-burden"></a>

## Acronym burden

Acronym-definition and acronym-overuse checks.

<a id="hermeneia.rules.terminology.acronym_burden.AcronymDefinition"></a>

### *class* hermeneia.rules.terminology.acronym_burden.AcronymDefinition(acronym, full_form, sentence_id, sentence_ordinal)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Acronymdefinition.

<a id="hermeneia.rules.terminology.acronym_burden.AcronymDefinition.acronym"></a>

#### acronym *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.terminology.acronym_burden.AcronymDefinition.full_form"></a>

#### full_form *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.terminology.acronym_burden.AcronymDefinition.sentence_id"></a>

#### sentence_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.terminology.acronym_burden.AcronymDefinition.sentence_ordinal"></a>

#### sentence_ordinal *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.rules.terminology.acronym_burden.AcronymBurdenRule"></a>

### *class* hermeneia.rules.terminology.acronym_burden.AcronymBurdenRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Acronymburdenrule.

<a id="hermeneia.rules.terminology.acronym_burden.AcronymBurdenRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='terminology.acronym_burden', label='Acronyms should be defined first and kept secondary to full forms', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_acronym_mentions_for_overuse': 4, 'max_acronym_to_full_form_ratio': 2.0, 'ignore_sentence_patterns': ('^\\\\s\*\\\\[![A-Z][A-Z0-9_-]\*\\\\](?:\\\\s+.\*)?$',), 'ignore_annotation_flags': (), 'ignore_acronym_tokens': ('NOTE', 'TIP', 'TODO', 'WARNING', 'IMPORTANT', 'CAUTION')}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'acronym', 'full_form', 'acronym_mentions', 'full_form_mentions'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.terminology.acronym_burden.AcronymBurdenRule.options_model"></a>

#### options_model

alias of `_AcronymBurdenOptions`

<a id="hermeneia.rules.terminology.acronym_burden.AcronymBurdenRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.terminology.acronym_burden.register"></a>

### hermeneia.rules.terminology.acronym_burden.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.terminology.definition_before_use"></a>

<a id="definition-before-use"></a>

## Definition before use

First-use definition checks for mathematical symbols.

<a id="hermeneia.rules.terminology.definition_before_use.DefinitionBeforeUseRule"></a>

### *class* hermeneia.rules.terminology.definition_before_use.DefinitionBeforeUseRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Definitionbeforeuserule.

<a id="hermeneia.rules.terminology.definition_before_use.DefinitionBeforeUseRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='terminology.definition_before_use', label='First-use symbols should be defined in place', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset({'fragment_sentence', 'heavy_math_masking', 'symbol_dense_sentence'}), evidence_fields=('symbols', 'matched_markers', 'definition_signals'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.terminology.definition_before_use.DefinitionBeforeUseRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.terminology.definition_before_use.register"></a>

### hermeneia.rules.terminology.definition_before_use.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.terminology.jargon_density"></a>

<a id="jargon-density"></a>

## Jargon density

Audience-specific jargon-density heuristics.

<a id="hermeneia.rules.terminology.jargon_density.JargonDensityRule"></a>

### *class* hermeneia.rules.terminology.jargon_density.JargonDensityRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Jargondensityrule.

<a id="hermeneia.rules.terminology.jargon_density.JargonDensityRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='terminology.jargon_density', label='Jargon density exceeds audience target', layer=<Layer.AUDIENCE_FIT: 'audience_fit'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('jargon_terms', 'density', 'audience'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.terminology.jargon_density.JargonDensityRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.terminology.jargon_density.register"></a>

### hermeneia.rules.terminology.jargon_density.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
