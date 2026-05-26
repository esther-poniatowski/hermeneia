<a id="rules-reference"></a>

# Rules — reference

Reference-layer rules covering citations, cross-references, link text, and anchors.

<a id="module-hermeneia.rules.reference.bare_pronoun_opening"></a>

<a id="bare-pronoun-opening"></a>

## Bare pronoun opening

Hard rule for bare pronoun sentence openings in prose.

<a id="hermeneia.rules.reference.bare_pronoun_opening.BarePronounOpeningRule"></a>

### *class* hermeneia.rules.reference.bare_pronoun_opening.BarePronounOpeningRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Barepronounopeningrule.

<a id="hermeneia.rules.reference.bare_pronoun_opening.BarePronounOpeningRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.bare_pronoun_opening', label='Avoid bare pronoun sentence openings', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('pronoun', 'signal'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.bare_pronoun_opening.BarePronounOpeningRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.reference.bare_pronoun_opening.register"></a>

### hermeneia.rules.reference.bare_pronoun_opening.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.citation_as_agent"></a>

<a id="citation-as-agent"></a>

## Citation as agent

Detect citation tags used as grammatical actors instead of tail evidence tags.

<a id="hermeneia.rules.reference.citation_as_agent.CitationAsAgentRule"></a>

### *class* hermeneia.rules.reference.citation_as_agent.CitationAsAgentRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Citationasagentrule.

<a id="hermeneia.rules.reference.citation_as_agent.CitationAsAgentRule.options_model"></a>

#### options_model

alias of `_CitationAsAgentOptions`

<a id="hermeneia.rules.reference.citation_as_agent.CitationAsAgentRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.citation_as_agent', label='Citation tags should not act as grammatical agents', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'citation_styles': ('key_year_bracket',)}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'citation', 'matched'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.citation_as_agent.CitationAsAgentRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

<a id="hermeneia.rules.reference.citation_as_agent.register"></a>

### hermeneia.rules.reference.citation_as_agent.register(registry)

Register.

<a id="module-hermeneia.rules.reference.citation_styles"></a>

<a id="citation-styles"></a>

## Citation styles

Shared citation-style resolution helpers for reference rules.

<a id="hermeneia.rules.reference.citation_styles.resolve_citation_patterns"></a>

### hermeneia.rules.reference.citation_styles.resolve_citation_patterns(\*, citation_styles, citation_tag_pattern, citation_tag_patterns, default_styles=('key_year_bracket',))

Resolve citation regex patterns from style names and custom patterns.

<a id="hermeneia.rules.reference.citation_styles.citation_union_pattern"></a>

### hermeneia.rules.reference.citation_styles.citation_union_pattern(citation_patterns)

Build a non-capturing citation union regex fragment.

<a id="module-hermeneia.rules.reference.citation_tail_parenthetical"></a>

<a id="citation-tail-parenthetical"></a>

## Citation tail parenthetical

Enforce tail-parenthetical placement for inline citation tags.

<a id="hermeneia.rules.reference.citation_tail_parenthetical.CitationTailParentheticalRule"></a>

### *class* hermeneia.rules.reference.citation_tail_parenthetical.CitationTailParentheticalRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Citationtailparentheticalrule.

<a id="hermeneia.rules.reference.citation_tail_parenthetical.CitationTailParentheticalRule.options_model"></a>

#### options_model

alias of `_CitationTailParentheticalOptions`

<a id="hermeneia.rules.reference.citation_tail_parenthetical.CitationTailParentheticalRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.citation_tail_parenthetical', label='Citations should appear as tail parentheticals', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'citation_styles': ('key_year_bracket',)}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('citation', 'issue'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.citation_tail_parenthetical.CitationTailParentheticalRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

<a id="hermeneia.rules.reference.citation_tail_parenthetical.register"></a>

### hermeneia.rules.reference.citation_tail_parenthetical.register(registry)

Register.

<a id="module-hermeneia.rules.reference.cross_reference"></a>

<a id="cross-reference"></a>

## Cross-reference

Ambiguous cross-reference checks.

<a id="hermeneia.rules.reference.cross_reference.CrossReferenceRule"></a>

### *class* hermeneia.rules.reference.cross_reference.CrossReferenceRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Crossreferencerule.

<a id="hermeneia.rules.reference.cross_reference.CrossReferenceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.cross_reference', label='Cross-reference should target an explicit object', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('reference',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.cross_reference.CrossReferenceRule.check_source"></a>

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

<a id="hermeneia.rules.reference.cross_reference.register"></a>

### hermeneia.rules.reference.cross_reference.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.generic_link_text"></a>

<a id="generic-link-text"></a>

## Generic link text

Generic/procedural link-text checks.

<a id="hermeneia.rules.reference.generic_link_text.GenericLinkTextRule"></a>

### *class* hermeneia.rules.reference.generic_link_text.GenericLinkTextRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Genericlinktextrule.

<a id="hermeneia.rules.reference.generic_link_text.GenericLinkTextRule.options_model"></a>

#### options_model

alias of `_GenericLinkTextOptions`

<a id="hermeneia.rules.reference.generic_link_text.GenericLinkTextRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.generic_link_text', label='Avoid generic or procedural markdown link text', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('link_text', 'signal', 'matched'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.generic_link_text.GenericLinkTextRule.check_source"></a>

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

<a id="hermeneia.rules.reference.generic_link_text.register"></a>

### hermeneia.rules.reference.generic_link_text.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.generic_one"></a>

<a id="generic-one"></a>

## Generic one

Hard rule for generic-actor ‘one’ scaffolding.

<a id="hermeneia.rules.reference.generic_one.GenericOneRule"></a>

### *class* hermeneia.rules.reference.generic_one.GenericOneRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Genericonerule.

<a id="hermeneia.rules.reference.generic_one.GenericOneRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.generic_one', label="Avoid generic actor 'one' in technical prose", layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('signal', 'phrase'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.generic_one.GenericOneRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.reference.generic_one.register"></a>

### hermeneia.rules.reference.generic_one.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.heading_link"></a>

<a id="heading-link"></a>

## Heading link

Heading-slug link checks.

<a id="hermeneia.rules.reference.heading_link.HeadingLinkRule"></a>

### *class* hermeneia.rules.reference.heading_link.HeadingLinkRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Headinglinkrule.

<a id="hermeneia.rules.reference.heading_link.HeadingLinkRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.heading_link', label='Avoid heading-slug fragments in markdown links', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('target',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.heading_link.HeadingLinkRule.check_source"></a>

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

<a id="hermeneia.rules.reference.heading_link.register"></a>

### hermeneia.rules.reference.heading_link.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.personal_pronoun"></a>

<a id="personal-pronoun"></a>

## Personal pronoun

Hard rule for first/second-person pronoun scaffolding.

<a id="hermeneia.rules.reference.personal_pronoun.PersonalPronounRule"></a>

### *class* hermeneia.rules.reference.personal_pronoun.PersonalPronounRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Personalpronounrule.

<a id="hermeneia.rules.reference.personal_pronoun.PersonalPronounRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.personal_pronoun', label='Avoid first/second-person pronouns in technical prose', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('pronoun',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.personal_pronoun.PersonalPronounRule.check_source"></a>

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

<a id="hermeneia.rules.reference.personal_pronoun.register"></a>

### hermeneia.rules.reference.personal_pronoun.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.raw_anchor"></a>

<a id="raw-anchor"></a>

## Raw anchor

Raw block-anchor token checks.

<a id="hermeneia.rules.reference.raw_anchor.RawAnchorRule"></a>

### *class* hermeneia.rules.reference.raw_anchor.RawAnchorRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Rawanchorrule.

<a id="hermeneia.rules.reference.raw_anchor.RawAnchorRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.raw_anchor', label='Avoid raw anchor tokens in running prose', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('anchor',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.raw_anchor.RawAnchorRule.check_source"></a>

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

<a id="hermeneia.rules.reference.raw_anchor.register"></a>

### hermeneia.rules.reference.raw_anchor.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.see_link"></a>

<a id="see-link"></a>

## See-link

See-link scaffolding checks.

<a id="hermeneia.rules.reference.see_link.SeeLinkRule"></a>

### *class* hermeneia.rules.reference.see_link.SeeLinkRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Seelinkrule.

<a id="hermeneia.rules.reference.see_link.SeeLinkRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.see_link', label="Avoid 'See [link]' scaffolding", layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('phrase',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.see_link.SeeLinkRule.check_source"></a>

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

<a id="hermeneia.rules.reference.see_link.register"></a>

### hermeneia.rules.reference.see_link.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.reference.structural_metalanguage"></a>

<a id="structural-metalanguage"></a>

## Structural metalanguage

Detect structural-metalanguage scaffolding in running prose.

<a id="hermeneia.rules.reference.structural_metalanguage.StructuralMetalanguageRule"></a>

### *class* hermeneia.rules.reference.structural_metalanguage.StructuralMetalanguageRule(settings)

Bases: [`SourcePatternRule`](rules-base.md#hermeneia.rules.base.SourcePatternRule)

Structuralmetalanguagerule.

<a id="hermeneia.rules.reference.structural_metalanguage.StructuralMetalanguageRule.options_model"></a>

#### options_model

alias of `_StructuralMetalanguageOptions`

<a id="hermeneia.rules.reference.structural_metalanguage.StructuralMetalanguageRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='reference.structural_metalanguage', label='Avoid structural metalanguage in prose claims', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.ERROR: 'error'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'term'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.reference.structural_metalanguage.StructuralMetalanguageRule.check_source"></a>

#### check_source(lines, doc, ctx)

Check source.

<a id="hermeneia.rules.reference.structural_metalanguage.register"></a>

### hermeneia.rules.reference.structural_metalanguage.register(registry)

Register.
