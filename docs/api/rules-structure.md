<a id="rules-document-structure"></a>

# Rules — document structure

Document-structure rules covering headings, section ordering, and section openers.

<a id="module-hermeneia.rules.structure.declarative_heading"></a>

<a id="declarative-heading"></a>

## Declarative heading

Detect non-declarative heading forms.

<a id="hermeneia.rules.structure.declarative_heading.DeclarativeHeadingRule"></a>

### *class* hermeneia.rules.structure.declarative_heading.DeclarativeHeadingRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Declarativeheadingrule.

<a id="hermeneia.rules.structure.declarative_heading.DeclarativeHeadingRule.options_model"></a>

#### options_model

alias of `_DeclarativeHeadingOptions`

<a id="hermeneia.rules.structure.declarative_heading.DeclarativeHeadingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.declarative_heading', label='Headings should state a declarative deliverable', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'forbid_question_headings': True, 'forbid_imperative_headings': True, 'imperative_verbs': ('define', 'assume', 'let', 'fix', 'set', 'check', 'show', 'prove', 'consider', 'use', 'apply', 'derive')}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'heading_text'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.declarative_heading.DeclarativeHeadingRule.check"></a>

#### check(doc, ctx)

Check.

<a id="hermeneia.rules.structure.declarative_heading.register"></a>

### hermeneia.rules.structure.declarative_heading.register(registry)

Register.

<a id="module-hermeneia.rules.structure.heading_capitalization"></a>

<a id="heading-capitalization"></a>

## Heading capitalization

Sibling-heading capitalization consistency checks.

<a id="hermeneia.rules.structure.heading_capitalization.HeadingCapitalizationRule"></a>

### *class* hermeneia.rules.structure.heading_capitalization.HeadingCapitalizationRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Headingcapitalizationrule.

<a id="hermeneia.rules.structure.heading_capitalization.HeadingCapitalizationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.heading_capitalization', label='Sibling headings should share capitalization convention', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('actual_style', 'expected_style', 'level'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.heading_capitalization.HeadingCapitalizationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.heading_capitalization.register"></a>

### hermeneia.rules.structure.heading_capitalization.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.heading_level_skip"></a>

<a id="heading-level-skip"></a>

## Heading level skip

Detect heading-level skips in document outline.

<a id="hermeneia.rules.structure.heading_level_skip.HeadingLevelSkipRule"></a>

### *class* hermeneia.rules.structure.heading_level_skip.HeadingLevelSkipRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Headinglevelskiprule.

<a id="hermeneia.rules.structure.heading_level_skip.HeadingLevelSkipRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.heading_level_skip', label='Heading levels should not skip depth', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('previous_level', 'current_level'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.heading_level_skip.HeadingLevelSkipRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.heading_level_skip.register"></a>

### hermeneia.rules.structure.heading_level_skip.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.heading_parallelism"></a>

<a id="heading-parallelism"></a>

## Heading parallelism

Sibling-heading frame consistency heuristics.

<a id="hermeneia.rules.structure.heading_parallelism.HeadingParallelismRule"></a>

### *class* hermeneia.rules.structure.heading_parallelism.HeadingParallelismRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Headingparallelismrule.

<a id="hermeneia.rules.structure.heading_parallelism.HeadingParallelismRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.heading_parallelism', label='Sibling headings are not frame-parallel', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('actual_frame', 'expected_frame', 'level'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.heading_parallelism.HeadingParallelismRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.heading_parallelism.register"></a>

### hermeneia.rules.structure.heading_parallelism.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.opening_message_focus"></a>

<a id="opening-message-focus"></a>

## Opening message focus

Detect opening sentences where enumeration blurs the core message.

<a id="hermeneia.rules.structure.opening_message_focus.OpeningMessageFocusRule"></a>

### *class* hermeneia.rules.structure.opening_message_focus.OpeningMessageFocusRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Openingmessagefocusrule.

<a id="hermeneia.rules.structure.opening_message_focus.OpeningMessageFocusRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.opening_message_focus', label='Opening sentence should state one clear purpose before enumeration', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_enumeration_items': 4, 'min_opening_words': 8}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'enumeration_items', 'purpose_markers'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.opening_message_focus.OpeningMessageFocusRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.opening_message_focus.register"></a>

### hermeneia.rules.structure.opening_message_focus.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.opening_sentence_presence"></a>

<a id="opening-sentence-presence"></a>

## Opening sentence presence

Detect missing opening sentence before structured content.

<a id="hermeneia.rules.structure.opening_sentence_presence.OpeningSentencePresenceRule"></a>

### *class* hermeneia.rules.structure.opening_sentence_presence.OpeningSentencePresenceRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Openingsentencepresencerule.

<a id="hermeneia.rules.structure.opening_sentence_presence.OpeningSentencePresenceRule.options_model"></a>

#### options_model

alias of `_OpeningSentencePresenceOptions`

<a id="hermeneia.rules.structure.opening_sentence_presence.OpeningSentencePresenceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.opening_sentence_presence', label='Document should open with a purpose sentence before structured blocks', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_opening_words': 8, 'forbidden_block_kinds': ('list', 'table', 'code_block', 'display_math')}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('first_structured_kind',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.opening_sentence_presence.OpeningSentencePresenceRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.opening_sentence_presence.register"></a>

### hermeneia.rules.structure.opening_sentence_presence.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.orphan_section"></a>

<a id="orphan-section"></a>

## Orphan section

Detect orphaned section shells in heading hierarchies.

<a id="hermeneia.rules.structure.orphan_section.OrphanSectionRule"></a>

### *class* hermeneia.rules.structure.orphan_section.OrphanSectionRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Orphansectionrule.

<a id="hermeneia.rules.structure.orphan_section.OrphanSectionRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.orphan_section', label='Avoid orphan section shells', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_parent_words': 24}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'direct_children', 'parent_words'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.orphan_section.OrphanSectionRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.orphan_section.register"></a>

### hermeneia.rules.structure.orphan_section.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.prose_outside_heading"></a>

<a id="prose-outside-heading"></a>

## Prose outside heading

Detect significant prose that appears before any heading.

<a id="hermeneia.rules.structure.prose_outside_heading.ProseOutsideHeadingRule"></a>

### *class* hermeneia.rules.structure.prose_outside_heading.ProseOutsideHeadingRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Proseoutsideheadingrule.

<a id="hermeneia.rules.structure.prose_outside_heading.ProseOutsideHeadingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.prose_outside_heading', label='Significant prose should live under an explicit heading', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_words': 12}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('word_count',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.prose_outside_heading.ProseOutsideHeadingRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.prose_outside_heading.register"></a>

### hermeneia.rules.structure.prose_outside_heading.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.section_balance"></a>

<a id="section-balance"></a>

## Section balance

Section-balance heuristics.

<a id="hermeneia.rules.structure.section_balance.SectionBalanceRule"></a>

### *class* hermeneia.rules.structure.section_balance.SectionBalanceRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Sectionbalancerule.

<a id="hermeneia.rules.structure.section_balance.SectionBalanceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.section_balance', label='Section lengths are strongly imbalanced', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_ratio': 3.5}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('largest_words', 'smallest_words', 'ratio'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.section_balance.SectionBalanceRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.section_balance.register"></a>

### hermeneia.rules.structure.section_balance.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.section_opener_block_kind"></a>

<a id="section-opener-block-kind"></a>

## Section opener block kind

Section-opener block-kind and framing checks.

<a id="hermeneia.rules.structure.section_opener_block_kind.SectionOpenerBlockKindRule"></a>

### *class* hermeneia.rules.structure.section_opener_block_kind.SectionOpenerBlockKindRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Sectionopenerblockkindrule.

<a id="hermeneia.rules.structure.section_opener_block_kind.SectionOpenerBlockKindRule.options_model"></a>

#### options_model

alias of `_SectionOpenerBlockKindOptions`

<a id="hermeneia.rules.structure.section_opener_block_kind.SectionOpenerBlockKindRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.section_opener_block_kind', label='Section should open with purpose-oriented prose', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'blocked_block_kinds': ('display_math', 'code_block', 'list', 'table')}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'first_block_kind'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.section_opener_block_kind.SectionOpenerBlockKindRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.section_opener_block_kind.register"></a>

### hermeneia.rules.structure.section_opener_block_kind.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.structure.section_order_sequence"></a>

<a id="section-order-sequence"></a>

## Section order sequence

Detect section-order patterns that invert reader decision sequence.

<a id="hermeneia.rules.structure.section_order_sequence.SectionOrderSequenceRule"></a>

### *class* hermeneia.rules.structure.section_order_sequence.SectionOrderSequenceRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Sectionordersequencerule.

<a id="hermeneia.rules.structure.section_order_sequence.SectionOrderSequenceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='structure.section_order_sequence', label='Section ordering should follow reader decision sequence', layer=<Layer.DOCUMENT_STRUCTURE: 'document_structure'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'offending_heading', 'expected_before'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.structure.section_order_sequence.SectionOrderSequenceRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.structure.section_order_sequence.register"></a>

### hermeneia.rules.structure.section_order_sequence.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
