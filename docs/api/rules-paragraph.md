<a id="rules-paragraph-rhetoric"></a>

# Rules — paragraph rhetoric

Paragraph-rhetoric rules covering topic sentences, redundancy, parallelism, and pacing.

<a id="module-hermeneia.rules.paragraph.concept_reference_drift"></a>

<a id="concept-reference-drift"></a>

## Concept reference drift

Concept-reference drift within a paragraph.

<a id="hermeneia.rules.paragraph.concept_reference_drift.ConceptReferenceDriftRule"></a>

### *class* hermeneia.rules.paragraph.concept_reference_drift.ConceptReferenceDriftRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Conceptreferencedriftrule.

<a id="hermeneia.rules.paragraph.concept_reference_drift.ConceptReferenceDriftRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.concept_reference_drift', label='Paragraph varies concept labels in ways that may obscure referential stability', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_distinct_labels': 3, 'min_sentence_count': 3, 'min_average_overlap': 0.35}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('labels', 'sentence_ids', 'average_overlap'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.concept_reference_drift.ConceptReferenceDriftRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.concept_reference_drift.register"></a>

### hermeneia.rules.paragraph.concept_reference_drift.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.double_framing"></a>

<a id="double-framing"></a>

## Double framing

Detect double framing in list lead-ins and list items.

<a id="hermeneia.rules.paragraph.double_framing.DoubleFramingRule"></a>

### *class* hermeneia.rules.paragraph.double_framing.DoubleFramingRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Doubleframingrule.

<a id="hermeneia.rules.paragraph.double_framing.DoubleFramingRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.double_framing', label='Avoid double framing around list introductions', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('list_item_count', 'reframed_item_count'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.double_framing.DoubleFramingRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.double_framing.register"></a>

### hermeneia.rules.paragraph.double_framing.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.inline_case_split"></a>

<a id="inline-case-split"></a>

## Inline case split

Inline case-split checks.

<a id="hermeneia.rules.paragraph.inline_case_split.InlineCaseSplitRule"></a>

### *class* hermeneia.rules.paragraph.inline_case_split.InlineCaseSplitRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Inlinecasesplitrule.

<a id="hermeneia.rules.paragraph.inline_case_split.InlineCaseSplitRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.inline_case_split', label='Inline semicolon case splits should be rendered as lists', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('pattern',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.inline_case_split.InlineCaseSplitRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.inline_case_split.register"></a>

### hermeneia.rules.paragraph.inline_case_split.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.inline_enumeration_overload"></a>

<a id="inline-enumeration-overload"></a>

## Inline enumeration overload

Inline-enumeration overload checks.

<a id="hermeneia.rules.paragraph.inline_enumeration_overload.InlineEnumerationOverloadRule"></a>

### *class* hermeneia.rules.paragraph.inline_enumeration_overload.InlineEnumerationOverloadRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Inlineenumerationoverloadrule.

<a id="hermeneia.rules.paragraph.inline_enumeration_overload.InlineEnumerationOverloadRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.inline_enumeration_overload', label='Dense inline enumerations should be converted to lists', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_inline_commas': 2, 'min_words_for_clause_mode': 28}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('issue', 'comma_count', 'label_count'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.inline_enumeration_overload.InlineEnumerationOverloadRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.inline_enumeration_overload.register"></a>

### hermeneia.rules.paragraph.inline_enumeration_overload.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.lexical_repetition"></a>

<a id="lexical-repetition"></a>

## Lexical repetition

Paragraph-level lexical repetition as a redundancy proxy.

<a id="hermeneia.rules.paragraph.lexical_repetition.LexicalRepetitionRule"></a>

### *class* hermeneia.rules.paragraph.lexical_repetition.LexicalRepetitionRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Lexicalrepetitionrule.

<a id="hermeneia.rules.paragraph.lexical_repetition.LexicalRepetitionRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.lexical_repetition', label='Paragraph repeats equivalent claims with limited new contribution', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_nonadjacent_overlap': 0.7, 'min_redundant_pairs': 1, 'min_sentence_count': 3}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('redundant_pairs', 'max_overlap', 'sentence_count'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.lexical_repetition.LexicalRepetitionRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.lexical_repetition.register"></a>

### hermeneia.rules.paragraph.lexical_repetition.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.paragraph_redundancy"></a>

<a id="paragraph-redundancy"></a>

## Paragraph redundancy

Cross-paragraph redundancy candidate diagnostics.

<a id="hermeneia.rules.paragraph.paragraph_redundancy.ParagraphRedundancyRule"></a>

### *class* hermeneia.rules.paragraph.paragraph_redundancy.ParagraphRedundancyRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Paragraphredundancyrule.

<a id="hermeneia.rules.paragraph.paragraph_redundancy.ParagraphRedundancyRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.paragraph_redundancy', label='Paragraph pair appears redundant', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_similarity': 0.88, 'min_lexical_overlap': 0.35, 'max_findings': 5}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('similarity', 'lexical_overlap', 'left_block_id', 'right_block_id'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.paragraph_redundancy.ParagraphRedundancyRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.paragraph_redundancy.register"></a>

### hermeneia.rules.paragraph.paragraph_redundancy.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.parallelism"></a>

<a id="parallelism"></a>

## Parallelism

List-item parallelism checks.

<a id="hermeneia.rules.paragraph.parallelism.ParagraphParallelismRule"></a>

### *class* hermeneia.rules.paragraph.parallelism.ParagraphParallelismRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Paragraphparallelismrule.

<a id="hermeneia.rules.paragraph.parallelism.ParagraphParallelismRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.parallelism', label='List items should be frame-parallel', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('actual_frame', 'expected_frame', 'list_size'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.parallelism.ParagraphParallelismRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.parallelism.register"></a>

### hermeneia.rules.paragraph.parallelism.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.reformulation_inflation"></a>

<a id="reformulation-inflation"></a>

## Reformulation inflation

Detect rhetorical reformulations that restate the same proposition.

<a id="hermeneia.rules.paragraph.reformulation_inflation.ReformulationInflationRule"></a>

### *class* hermeneia.rules.paragraph.reformulation_inflation.ReformulationInflationRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Reformulationinflationrule.

<a id="hermeneia.rules.paragraph.reformulation_inflation.ReformulationInflationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.reformulation_inflation', label='Avoid rhetorical reformulation when it adds no new contribution', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_overlap': 0.62}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('marker', 'overlap', 'left_sentence_id', 'right_sentence_id'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.reformulation_inflation.ReformulationInflationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.reformulation_inflation.register"></a>

### hermeneia.rules.paragraph.reformulation_inflation.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.sentence_redundancy"></a>

<a id="sentence-redundancy"></a>

## Sentence redundancy

Adjacent-sentence redundancy heuristics.

<a id="hermeneia.rules.paragraph.sentence_redundancy.SentenceRedundancyRule"></a>

### *class* hermeneia.rules.paragraph.sentence_redundancy.SentenceRedundancyRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Sentenceredundancyrule.

<a id="hermeneia.rules.paragraph.sentence_redundancy.SentenceRedundancyRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.sentence_redundancy', label='Adjacent sentences appear redundant', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'min_overlap': 0.78}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('overlap', 'left_sentence_id', 'right_sentence_id'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.sentence_redundancy.SentenceRedundancyRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.sentence_redundancy.register"></a>

### hermeneia.rules.paragraph.sentence_redundancy.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.topic_sentence"></a>

<a id="topic-sentence"></a>

## Topic sentence

Topic-sentence heuristics.

<a id="hermeneia.rules.paragraph.topic_sentence.TopicSentenceRule"></a>

### *class* hermeneia.rules.paragraph.topic_sentence.TopicSentenceRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Topicsentencerule.

<a id="hermeneia.rules.paragraph.topic_sentence.TopicSentenceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.topic_sentence', label='Paragraph lacks a strong topic sentence', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_H: 'class_h'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'minimum_score': 0.45, 'apply_block_kinds': ('paragraph',)}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('first_score', 'second_score', 'sentence_count'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.topic_sentence.TopicSentenceRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.topic_sentence.register"></a>

### hermeneia.rules.paragraph.topic_sentence.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.paragraph.vague_rhetorical_opener"></a>

<a id="vague-rhetorical-opener"></a>

## Vague rhetorical opener

Vague rhetorical opener checks.

<a id="hermeneia.rules.paragraph.vague_rhetorical_opener.VagueRhetoricalOpenerRule"></a>

### *class* hermeneia.rules.paragraph.vague_rhetorical_opener.VagueRhetoricalOpenerRule(settings)

Bases: [`HeuristicSemanticRule`](rules-base.md#hermeneia.rules.base.HeuristicSemanticRule)

Vaguerhetoricalopenerrule.

<a id="hermeneia.rules.paragraph.vague_rhetorical_opener.VagueRhetoricalOpenerRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='paragraph.vague_rhetorical_opener', label='Avoid vague rhetorical openers that delay the claim', layer=<Layer.PARAGRAPH_RHETORIC: 'paragraph_rhetoric'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.RHETORICAL_EXPECTATION: 'rhetorical_expectation'>, default_severity=<Severity.INFO: 'info'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('opener',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=True)*

Configured value for `metadata`.

<a id="hermeneia.rules.paragraph.vague_rhetorical_opener.VagueRhetoricalOpenerRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.paragraph.vague_rhetorical_opener.register"></a>

### hermeneia.rules.paragraph.vague_rhetorical_opener.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
