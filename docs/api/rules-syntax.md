<a id="rules-syntax"></a>

# Rules — syntax

Syntax-layer rules covering sentence length, embedding depth, and clause structure.

<a id="module-hermeneia.rules.syntax.embedding_depth"></a>

<a id="embedding-depth"></a>

## Embedding depth

Detect sentences with high syntactic embedding depth.

<a id="hermeneia.rules.syntax.embedding_depth.EmbeddingDepthRule"></a>

### *class* hermeneia.rules.syntax.embedding_depth.EmbeddingDepthRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Embeddingdepthrule.

<a id="hermeneia.rules.syntax.embedding_depth.EmbeddingDepthRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.embedding_depth', label='Sentence embedding depth is likely to require multiple reads', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'apply_block_kinds': ('paragraph',), 'max_dependency_depth': 5, 'max_embedding_markers': 4, 'min_sentence_words': 14}, profiles_active=frozenset(), abstain_when_flags=frozenset({'blockquote_context', 'list_item_context', 'heading_context', 'heavy_math_masking', 'table_cell_context', 'symbol_dense_sentence'}), evidence_fields=('signal_source', 'dependency_depth', 'embedding_markers'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.embedding_depth.EmbeddingDepthRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.syntax.embedding_depth.register"></a>

### hermeneia.rules.syntax.embedding_depth.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.syntax.long_inline_enumeration"></a>

<a id="long-inline-enumeration"></a>

## Long inline enumeration

Detect long inline enumerations that should be converted to lists.

<a id="hermeneia.rules.syntax.long_inline_enumeration.LongInlineEnumerationRule"></a>

### *class* hermeneia.rules.syntax.long_inline_enumeration.LongInlineEnumerationRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Longinlineenumerationrule.

<a id="hermeneia.rules.syntax.long_inline_enumeration.LongInlineEnumerationRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.long_inline_enumeration', label='Long inline enumerations should be split into list format', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.HARD_CONSTRAINT: 'hard_constraint'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_items': 4}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('item_count', 'max_items'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.long_inline_enumeration.LongInlineEnumerationRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.syntax.long_inline_enumeration.register"></a>

### hermeneia.rules.syntax.long_inline_enumeration.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.syntax.multi_action_sentence"></a>

<a id="multi-action-sentence"></a>

## Multi-action sentence

Detect sentences that stack multiple load-bearing actions.

<a id="hermeneia.rules.syntax.multi_action_sentence.MultiActionSentenceRule"></a>

### *class* hermeneia.rules.syntax.multi_action_sentence.MultiActionSentenceRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Multiactionsentencerule.

<a id="hermeneia.rules.syntax.multi_action_sentence.MultiActionSentenceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.multi_action_sentence', label='Keep one primary action per sentence', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_load_bearing_verbs': 1, 'require_coordination_marker': True, 'apply_block_kinds': ('paragraph',), 'coordination_markers': ('and', 'while', 'whereas', 'then', ';')}, profiles_active=frozenset(), abstain_when_flags=frozenset({'blockquote_context', 'list_item_context', 'heading_context', 'heavy_math_masking', 'table_cell_context', 'fragment_sentence', 'symbol_dense_sentence'}), evidence_fields=('action_count', 'verbs', 'coordination_signal'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.multi_action_sentence.MultiActionSentenceRule.check"></a>

#### check(doc, ctx)

Check.

<a id="hermeneia.rules.syntax.multi_action_sentence.register"></a>

### hermeneia.rules.syntax.multi_action_sentence.register(registry)

Register.

<a id="module-hermeneia.rules.syntax.passive_voice"></a>

<a id="passive-voice"></a>

## Passive voice

Passive-voice diagnostics for sentence openings.

<a id="hermeneia.rules.syntax.passive_voice.PassiveVoiceRule"></a>

### *class* hermeneia.rules.syntax.passive_voice.PassiveVoiceRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Passivevoicerule.

<a id="hermeneia.rules.syntax.passive_voice.PassiveVoiceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.passive_voice', label='Prefer active voice in sentence openings', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'apply_block_kinds': ('paragraph',), 'allow_topic_preserving_passive': True, 'min_topic_overlap_for_passive_exemption': 0.22, 'topic_subject_determiners': ('this', 'that', 'these', 'those')}, profiles_active=frozenset(), abstain_when_flags=frozenset({'blockquote_context', 'list_item_context', 'heading_context', 'heavy_math_masking', 'table_cell_context', 'symbol_dense_sentence'}), evidence_fields=('auxiliary', 'participle', 'dependency_signal'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.passive_voice.PassiveVoiceRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.syntax.passive_voice.register"></a>

### hermeneia.rules.syntax.passive_voice.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.syntax.sentence_length"></a>

<a id="sentence-length"></a>

## Sentence length

Sentence-length diagnostics.

<a id="hermeneia.rules.syntax.sentence_length.SentenceLengthRule"></a>

### *class* hermeneia.rules.syntax.sentence_length.SentenceLengthRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Sentencelengthrule.

<a id="hermeneia.rules.syntax.sentence_length.SentenceLengthRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.sentence_length', label='Sentence exceeds the profile target length', layer=<Layer.SURFACE_STYLE: 'surface_style'>, tractability=<Tractability.CLASS_A: 'class_a'>, kind=<RuleKind.DIAGNOSTIC_METRIC: 'diagnostic_metric'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_words': 28}, profiles_active=frozenset(), abstain_when_flags=frozenset(), evidence_fields=('word_count',), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.sentence_length.SentenceLengthRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.syntax.sentence_length.register"></a>

### hermeneia.rules.syntax.sentence_length.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.syntax.subject_verb_distance"></a>

<a id="subject-verb-distance"></a>

## Subject-verb distance

Subject-to-main-verb distance diagnostics.

<a id="hermeneia.rules.syntax.subject_verb_distance.SubjectVerbDistanceRule"></a>

### *class* hermeneia.rules.syntax.subject_verb_distance.SubjectVerbDistanceRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Subjectverbdistancerule.

<a id="hermeneia.rules.syntax.subject_verb_distance.SubjectVerbDistanceRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.subject_verb_distance', label='Subject and main verb are too far apart', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_distance': 8, 'apply_block_kinds': ('paragraph',)}, profiles_active=frozenset(), abstain_when_flags=frozenset({'blockquote_context', 'list_item_context', 'heading_context', 'heavy_math_masking', 'table_cell_context', 'fragment_sentence', 'symbol_dense_sentence'}), evidence_fields=('distance', 'subject_token', 'root_token'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.subject_verb_distance.SubjectVerbDistanceRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.syntax.subject_verb_distance.register"></a>

### hermeneia.rules.syntax.subject_verb_distance.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.syntax.subordinate_clause"></a>

<a id="subordinate-clause"></a>

## Subordinate clause

Subordinate-clause load diagnostics.

<a id="hermeneia.rules.syntax.subordinate_clause.SubordinateClauseRule"></a>

### *class* hermeneia.rules.syntax.subordinate_clause.SubordinateClauseRule(settings)

Bases: [`AnnotatedRule`](rules-base.md#hermeneia.rules.base.AnnotatedRule)

Subordinateclauserule.

<a id="hermeneia.rules.syntax.subordinate_clause.SubordinateClauseRule.metadata"></a>

#### metadata *: ClassVar[[RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)]* *= RuleMetadata(rule_id='syntax.subordinate_clause', label='Sentence carries too many subordinate clauses', layer=<Layer.LOCAL_DISCOURSE: 'local_discourse'>, tractability=<Tractability.CLASS_B: 'class_b'>, kind=<RuleKind.SOFT_HEURISTIC: 'soft_heuristic'>, default_severity=<Severity.WARNING: 'warning'>, supported_languages=frozenset({'en'}), default_weight=1.0, default_options={'max_subordinate_clauses': 2, 'apply_block_kinds': ('paragraph',)}, profiles_active=frozenset(), abstain_when_flags=frozenset({'blockquote_context', 'list_item_context', 'heading_context', 'heavy_math_masking', 'table_cell_context', 'symbol_dense_sentence'}), evidence_fields=('subordinate_count', 'signal_source'), suggestion_mode=<SuggestionMode.TACTIC_ONLY: 'tactic_only'>, experimental=False)*

Configured value for `metadata`.

<a id="hermeneia.rules.syntax.subordinate_clause.SubordinateClauseRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Document instance to inspect.
  * **ctx** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [object](https://docs.python.org/3/library/functions.html#object)

<a id="hermeneia.rules.syntax.subordinate_clause.register"></a>

### hermeneia.rules.syntax.subordinate_clause.register(registry)

Register.

* **Parameters:**
  **registry** ([*object*](https://docs.python.org/3/library/functions.html#object)) – Rule registry used to resolve implementations.
