<a id="rules-base-infrastructure"></a>

# Rules — base infrastructure

Rule-domain types, base classes, shared helpers, loaders, and pattern utilities.

<a id="module-hermeneia.rules.base"></a>

<a id="base-classes"></a>

## Base classes

Rule-domain types and base classes.

<a id="hermeneia.rules.base.Layer"></a>

### *class* hermeneia.rules.base.Layer(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Layer.

<a id="hermeneia.rules.base.Layer.SURFACE_STYLE"></a>

#### SURFACE_STYLE *= 'surface_style'*

<a id="hermeneia.rules.base.Layer.LOCAL_DISCOURSE"></a>

#### LOCAL_DISCOURSE *= 'local_discourse'*

<a id="hermeneia.rules.base.Layer.PARAGRAPH_RHETORIC"></a>

#### PARAGRAPH_RHETORIC *= 'paragraph_rhetoric'*

<a id="hermeneia.rules.base.Layer.DOCUMENT_STRUCTURE"></a>

#### DOCUMENT_STRUCTURE *= 'document_structure'*

<a id="hermeneia.rules.base.Layer.AUDIENCE_FIT"></a>

#### AUDIENCE_FIT *= 'audience_fit'*

<a id="hermeneia.rules.base.Tractability"></a>

### *class* hermeneia.rules.base.Tractability(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Tractability.

<a id="hermeneia.rules.base.Tractability.CLASS_A"></a>

#### CLASS_A *= 'class_a'*

<a id="hermeneia.rules.base.Tractability.CLASS_B"></a>

#### CLASS_B *= 'class_b'*

<a id="hermeneia.rules.base.Tractability.CLASS_H"></a>

#### CLASS_H *= 'class_h'*

<a id="hermeneia.rules.base.Tractability.CLASS_C"></a>

#### CLASS_C *= 'class_c'*

<a id="hermeneia.rules.base.Severity"></a>

### *class* hermeneia.rules.base.Severity(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Severity.

<a id="hermeneia.rules.base.Severity.INFO"></a>

#### INFO *= 'info'*

<a id="hermeneia.rules.base.Severity.WARNING"></a>

#### WARNING *= 'warning'*

<a id="hermeneia.rules.base.Severity.ERROR"></a>

#### ERROR *= 'error'*

<a id="hermeneia.rules.base.RuleKind"></a>

### *class* hermeneia.rules.base.RuleKind(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Execution contracts available for rules.

<a id="hermeneia.rules.base.RuleKind.HARD_CONSTRAINT"></a>

#### HARD_CONSTRAINT *= 'hard_constraint'*

<a id="hermeneia.rules.base.RuleKind.SOFT_HEURISTIC"></a>

#### SOFT_HEURISTIC *= 'soft_heuristic'*

<a id="hermeneia.rules.base.RuleKind.DIAGNOSTIC_METRIC"></a>

#### DIAGNOSTIC_METRIC *= 'diagnostic_metric'*

<a id="hermeneia.rules.base.RuleKind.RHETORICAL_EXPECTATION"></a>

#### RHETORICAL_EXPECTATION *= 'rhetorical_expectation'*

<a id="hermeneia.rules.base.RuleKind.REWRITE_TACTIC"></a>

#### REWRITE_TACTIC *= 'rewrite_tactic'*

<a id="hermeneia.rules.base.SuggestionMode"></a>

### *class* hermeneia.rules.base.SuggestionMode(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Suggestionmode.

<a id="hermeneia.rules.base.SuggestionMode.TEMPLATE"></a>

#### TEMPLATE *= 'template'*

<a id="hermeneia.rules.base.SuggestionMode.TACTIC_ONLY"></a>

#### TACTIC_ONLY *= 'tactic_only'*

<a id="hermeneia.rules.base.SuggestionMode.NONE"></a>

#### NONE *= 'none'*

<a id="hermeneia.rules.base.RuleMetadata"></a>

### *class* hermeneia.rules.base.RuleMetadata(rule_id, label, layer, tractability, kind, default_severity, supported_languages, default_weight=1.0, default_options=<factory>, profiles_active=frozenset({}), abstain_when_flags=frozenset({}), evidence_fields=(), suggestion_mode=SuggestionMode.TACTIC_ONLY, experimental=False)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Rulemetadata.

<a id="hermeneia.rules.base.RuleMetadata.rule_id"></a>

#### rule_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.RuleMetadata.label"></a>

#### label *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.RuleMetadata.layer"></a>

#### layer *: [Layer](#hermeneia.rules.base.Layer)*

<a id="hermeneia.rules.base.RuleMetadata.tractability"></a>

#### tractability *: [Tractability](#hermeneia.rules.base.Tractability)*

<a id="hermeneia.rules.base.RuleMetadata.kind"></a>

#### kind *: [RuleKind](#hermeneia.rules.base.RuleKind)*

<a id="hermeneia.rules.base.RuleMetadata.default_severity"></a>

#### default_severity *: [Severity](#hermeneia.rules.base.Severity)*

<a id="hermeneia.rules.base.RuleMetadata.supported_languages"></a>

#### supported_languages *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]*

<a id="hermeneia.rules.base.RuleMetadata.default_weight"></a>

#### default_weight *: [float](https://docs.python.org/3/library/functions.html#float)* *= 1.0*

<a id="hermeneia.rules.base.RuleMetadata.default_options"></a>

#### default_options *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]*

<a id="hermeneia.rules.base.RuleMetadata.profiles_active"></a>

#### profiles_active *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.rules.base.RuleMetadata.abstain_when_flags"></a>

#### abstain_when_flags *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.rules.base.RuleMetadata.evidence_fields"></a>

#### evidence_fields *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.rules.base.RuleMetadata.suggestion_mode"></a>

#### suggestion_mode *: [SuggestionMode](#hermeneia.rules.base.SuggestionMode)* *= 'tactic_only'*

<a id="hermeneia.rules.base.RuleMetadata.experimental"></a>

#### experimental *: [bool](https://docs.python.org/3/library/functions.html#bool)* *= False*

<a id="hermeneia.rules.base.RuleEvidence"></a>

### *class* hermeneia.rules.base.RuleEvidence(features, score=None, threshold=None, upstream_limits=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Ruleevidence.

<a id="hermeneia.rules.base.RuleEvidence.features"></a>

#### features *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

<a id="hermeneia.rules.base.RuleEvidence.score"></a>

#### score *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.rules.base.RuleEvidence.threshold"></a>

#### threshold *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.rules.base.RuleEvidence.upstream_limits"></a>

#### upstream_limits *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.rules.base.Violation"></a>

### *class* hermeneia.rules.base.Violation(rule_id, message, span, severity, layer, evidence=None, confidence=None, rationale=None, rewrite_tactics=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Violation.

<a id="hermeneia.rules.base.Violation.rule_id"></a>

#### rule_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.Violation.message"></a>

#### message *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.Violation.span"></a>

#### span *: [Span](document.md#hermeneia.document.model.Span)*

<a id="hermeneia.rules.base.Violation.severity"></a>

#### severity *: [Severity](#hermeneia.rules.base.Severity)*

<a id="hermeneia.rules.base.Violation.layer"></a>

#### layer *: [Layer](#hermeneia.rules.base.Layer)*

<a id="hermeneia.rules.base.Violation.evidence"></a>

#### evidence *: [RuleEvidence](#hermeneia.rules.base.RuleEvidence) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.rules.base.Violation.confidence"></a>

#### confidence *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.rules.base.Violation.rationale"></a>

#### rationale *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.rules.base.Violation.rewrite_tactics"></a>

#### rewrite_tactics *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.rules.base.ResolvedRuleSettings"></a>

### *class* hermeneia.rules.base.ResolvedRuleSettings(metadata, enabled, severity, weight, options=<factory>, extra_patterns=(), silenced_patterns=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Resolvedrulesettings.

<a id="hermeneia.rules.base.ResolvedRuleSettings.metadata"></a>

#### metadata *: [RuleMetadata](#hermeneia.rules.base.RuleMetadata)*

<a id="hermeneia.rules.base.ResolvedRuleSettings.enabled"></a>

#### enabled *: [bool](https://docs.python.org/3/library/functions.html#bool)*

<a id="hermeneia.rules.base.ResolvedRuleSettings.severity"></a>

#### severity *: [Severity](#hermeneia.rules.base.Severity)*

<a id="hermeneia.rules.base.ResolvedRuleSettings.weight"></a>

#### weight *: [float](https://docs.python.org/3/library/functions.html#float)*

<a id="hermeneia.rules.base.ResolvedRuleSettings.options"></a>

#### options *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]*

<a id="hermeneia.rules.base.ResolvedRuleSettings.extra_patterns"></a>

#### extra_patterns *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.rules.base.ResolvedRuleSettings.silenced_patterns"></a>

#### silenced_patterns *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.rules.base.ResolvedRuleSettings.int_option"></a>

#### int_option(key, default)

Int option.

* **Parameters:**
  * **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `key`.
  * **default** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `default`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="hermeneia.rules.base.ResolvedRuleSettings.float_option"></a>

#### float_option(key, default)

Float option.

* **Parameters:**
  * **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `key`.
  * **default** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Input value for `default`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="hermeneia.rules.base.ResolvedRuleSettings.bool_option"></a>

#### bool_option(key, default)

Bool option.

* **Parameters:**
  * **key** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `key`.
  * **default** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Input value for `default`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – Raised under documented error conditions.

<a id="hermeneia.rules.base.ResolvedProfile"></a>

### *class* hermeneia.rules.base.ResolvedProfile(profile_name, audience, genre, section, register, language, strict_validation, enable_experimental, rules)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Resolvedprofile.

<a id="hermeneia.rules.base.ResolvedProfile.profile_name"></a>

#### profile_name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.ResolvedProfile.audience"></a>

#### audience *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.ResolvedProfile.genre"></a>

#### genre *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.ResolvedProfile.section"></a>

#### section *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.ResolvedProfile.register"></a>

#### register *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.ResolvedProfile.language"></a>

#### language *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.rules.base.ResolvedProfile.strict_validation"></a>

#### strict_validation *: [bool](https://docs.python.org/3/library/functions.html#bool)*

<a id="hermeneia.rules.base.ResolvedProfile.enable_experimental"></a>

#### enable_experimental *: [bool](https://docs.python.org/3/library/functions.html#bool)*

<a id="hermeneia.rules.base.ResolvedProfile.rules"></a>

#### rules *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [ResolvedRuleSettings](#hermeneia.rules.base.ResolvedRuleSettings)]*

<a id="hermeneia.rules.base.ResolvedProfile.active_rules"></a>

#### active_rules()

Active rules.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ResolvedRuleSettings](#hermeneia.rules.base.ResolvedRuleSettings), …]

<a id="hermeneia.rules.base.RuntimeCapabilities"></a>

### *class* hermeneia.rules.base.RuntimeCapabilities(embeddings_available, debug_mode, experimental_rules_enabled)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Runtime capability flags available during rule execution.

<a id="hermeneia.rules.base.RuntimeCapabilities.embeddings_available"></a>

#### embeddings_available *: [bool](https://docs.python.org/3/library/functions.html#bool)*

<a id="hermeneia.rules.base.RuntimeCapabilities.debug_mode"></a>

#### debug_mode *: [bool](https://docs.python.org/3/library/functions.html#bool)*

<a id="hermeneia.rules.base.RuntimeCapabilities.experimental_rules_enabled"></a>

#### experimental_rules_enabled *: [bool](https://docs.python.org/3/library/functions.html#bool)*

<a id="hermeneia.rules.base.RuntimeCapabilities.defaults"></a>

#### *classmethod* defaults()

Defaults.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RuntimeCapabilities](#hermeneia.rules.base.RuntimeCapabilities)

<a id="hermeneia.rules.base.RuleContext"></a>

### *class* hermeneia.rules.base.RuleContext(profile, language_pack, features, capabilities=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Shared runtime context passed to rule evaluations.

<a id="hermeneia.rules.base.RuleContext.profile"></a>

#### profile *: [ResolvedProfile](#hermeneia.rules.base.ResolvedProfile)*

<a id="hermeneia.rules.base.RuleContext.language_pack"></a>

#### language_pack *: [LanguagePack](language.md#hermeneia.language.base.LanguagePack)*

<a id="hermeneia.rules.base.RuleContext.features"></a>

#### features *: [FeatureStore](document.md#hermeneia.document.indexes.FeatureStore)*

<a id="hermeneia.rules.base.RuleContext.capabilities"></a>

#### capabilities *: [RuntimeCapabilities](#hermeneia.rules.base.RuntimeCapabilities)*

<a id="hermeneia.rules.base.RuleContext.embeddings_available"></a>

#### *property* embeddings_available *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Embeddings available.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.rules.base.RuleContext.debug_mode"></a>

#### *property* debug_mode *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Debug mode.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.rules.base.RuleContext.enable_experimental"></a>

#### *property* enable_experimental *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Enable experimental.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.rules.base.BaseRule"></a>

### *class* hermeneia.rules.base.BaseRule(settings)

Bases: [`ABC`](https://docs.python.org/3/library/abc.html#abc.ABC)

Abstract base class for all Hermeneia rules.

* **Parameters:**
  **settings** ([*ResolvedRuleSettings*](#hermeneia.rules.base.ResolvedRuleSettings)) – Input value for `settings`.

<a id="hermeneia.rules.base.BaseRule.metadata"></a>

#### metadata *: [ClassVar](https://docs.python.org/3/library/typing.html#typing.ClassVar)[[RuleMetadata](#hermeneia.rules.base.RuleMetadata)]*

Configured value for `metadata`.

<a id="hermeneia.rules.base.BaseRule.options_model"></a>

#### options_model *: [ClassVar](https://docs.python.org/3/library/typing.html#typing.ClassVar)[[type](https://docs.python.org/3/library/functions.html#type)[[object](https://docs.python.org/3/library/functions.html#object)] | [None](https://docs.python.org/3/library/constants.html#None)]* *= None*

Configured value for `options_model`.

<a id="hermeneia.rules.base.BaseRule.__init__"></a>

#### \_\_init_\_(settings)

Initialize the instance.

<a id="hermeneia.rules.base.BaseRule.rule_id"></a>

#### *property* rule_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Rule id.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="hermeneia.rules.base.BaseRule.should_abstain"></a>

#### should_abstain(annotation_flags)

Should abstain.

* **Parameters:**
  **annotation_flags** ([*frozenset*](https://docs.python.org/3/library/stdtypes.html#frozenset) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `annotation_flags`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.rules.base.BaseRule.check"></a>

#### *abstractmethod* check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
  * **ctx** ([*RuleContext*](#hermeneia.rules.base.RuleContext)) – Rule evaluation context.

<a id="hermeneia.rules.base.SourcePatternRule"></a>

### *class* hermeneia.rules.base.SourcePatternRule(settings)

Bases: [`BaseRule`](#hermeneia.rules.base.BaseRule)

Rule base class for source-line and source-span checks.

<a id="hermeneia.rules.base.SourcePatternRule.check_source"></a>

#### *abstractmethod* check_source(lines, doc, ctx)

Check source.

* **Parameters:**
  * **lines** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*SourceLine*](document.md#hermeneia.document.model.SourceLine) *]*) – Source lines involved in this computation.
  * **doc** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
  * **ctx** ([*RuleContext*](#hermeneia.rules.base.RuleContext)) – Rule evaluation context.

<a id="hermeneia.rules.base.SourcePatternRule.check"></a>

#### check(doc, ctx)

Check.

* **Parameters:**
  * **doc** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
  * **ctx** ([*RuleContext*](#hermeneia.rules.base.RuleContext)) – Rule evaluation context.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[Violation](#hermeneia.rules.base.Violation)]

<a id="hermeneia.rules.base.AnnotatedRule"></a>

### *class* hermeneia.rules.base.AnnotatedRule(settings)

Bases: [`BaseRule`](#hermeneia.rules.base.BaseRule)

Annotatedrule.

<a id="hermeneia.rules.base.HeuristicSemanticRule"></a>

### *class* hermeneia.rules.base.HeuristicSemanticRule(settings)

Bases: [`BaseRule`](#hermeneia.rules.base.BaseRule)

Heuristicsemanticrule.

<a id="module-hermeneia.rules.common"></a>

<a id="common-helpers"></a>

## Common helpers

Shared helper logic for built-in rules.

<a id="hermeneia.rules.common.iter_sentences"></a>

### hermeneia.rules.common.iter_sentences(doc)

Iter sentences.

* **Parameters:**
  **doc** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
* **Yields:**
  *Iterable[Sentence]* – Items yielded by this iterator.

<a id="hermeneia.rules.common.iter_blocks"></a>

### hermeneia.rules.common.iter_blocks(doc, kinds=None)

Iter blocks.

* **Parameters:**
  * **doc** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
  * **kinds** ([*set*](https://docs.python.org/3/library/stdtypes.html#set) *[*[*BlockKind*](document.md#hermeneia.document.model.BlockKind) *]*  *|* *None*) – Input value for `kinds`.
* **Yields:**
  *Iterable[Block]* – Items yielded by this iterator.

<a id="hermeneia.rules.common.sentence_word_count"></a>

### hermeneia.rules.common.sentence_word_count(sentence)

Sentence word count.

* **Parameters:**
  **sentence** ([*Sentence*](document.md#hermeneia.document.model.Sentence)) – Input value for `sentence`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="hermeneia.rules.common.sentence_lemmas"></a>

### hermeneia.rules.common.sentence_lemmas(sentence)

Sentence lemmas.

* **Parameters:**
  **sentence** ([*Sentence*](document.md#hermeneia.document.model.Sentence)) – Input value for `sentence`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [set](https://docs.python.org/3/library/stdtypes.html#set)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="hermeneia.rules.common.matched_sentence_markers"></a>

### hermeneia.rules.common.matched_sentence_markers(sentence, markers)

Matched sentence markers.

* **Parameters:**
  * **sentence** ([*Sentence*](document.md#hermeneia.document.model.Sentence)) – Input value for `sentence`.
  * **markers** (*Iterable* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `markers`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), …]

<a id="hermeneia.rules.common.sentence_has_marker"></a>

### hermeneia.rules.common.sentence_has_marker(sentence, markers)

Sentence has marker.

* **Parameters:**
  * **sentence** ([*Sentence*](document.md#hermeneia.document.model.Sentence)) – Input value for `sentence`.
  * **markers** (*Iterable* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `markers`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.rules.common.text_has_marker"></a>

### hermeneia.rules.common.text_has_marker(text, markers)

Text has marker.

* **Parameters:**
  * **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Text content to process.
  * **markers** (*Iterable* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `markers`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.rules.common.line_text_outside_excluded"></a>

### hermeneia.rules.common.line_text_outside_excluded(line)

Line text outside excluded.

* **Parameters:**
  **line** ([*SourceLine*](document.md#hermeneia.document.model.SourceLine)) – Input value for `line`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="hermeneia.rules.common.match_allowed"></a>

### hermeneia.rules.common.match_allowed(line, pattern)

Match allowed.

* **Parameters:**
  * **line** ([*SourceLine*](document.md#hermeneia.document.model.SourceLine)) – Input value for `line`.
  * **pattern** ([*re.Pattern*](https://docs.python.org/3/library/re.html#re.Pattern) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `pattern`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [re.Match](https://docs.python.org/3/library/re.html#re.Match)[[str](https://docs.python.org/3/library/stdtypes.html#str)] | None

<a id="hermeneia.rules.common.block_text"></a>

### hermeneia.rules.common.block_text(block)

Block text.

* **Parameters:**
  **block** ([*Block*](document.md#hermeneia.document.model.Block)) – Input value for `block`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="hermeneia.rules.common.previous_prose_block"></a>

### hermeneia.rules.common.previous_prose_block(blocks, before_index)

Previous prose block.

* **Parameters:**
  * **blocks** (*Sequence* *[*[*Block*](document.md#hermeneia.document.model.Block) *]*) – Input value for `blocks`.
  * **before_index** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `before_index`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Block](document.md#hermeneia.document.model.Block) | None

<a id="hermeneia.rules.common.upstream_limits"></a>

### hermeneia.rules.common.upstream_limits(sentence)

Upstream limits.

* **Parameters:**
  **sentence** ([*Sentence*](document.md#hermeneia.document.model.Sentence)) – Input value for `sentence`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), …]

<a id="hermeneia.rules.common.span_from_lines"></a>

### hermeneia.rules.common.span_from_lines(start_line, end_line=None)

Span from lines.

* **Parameters:**
  * **start_line** ([*SourceLine*](document.md#hermeneia.document.model.SourceLine)) – Input value for `start_line`.
  * **end_line** ([*SourceLine*](document.md#hermeneia.document.model.SourceLine) *|* *None*) – Input value for `end_line`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Span](document.md#hermeneia.document.model.Span)

<a id="module-hermeneia.rules.loader"></a>

<a id="loader"></a>

## Loader

Built-in and external rule loading.

<a id="hermeneia.rules.loader.load_builtin_rules"></a>

### hermeneia.rules.loader.load_builtin_rules(registry)

Walk the built-in rule packages and call register(registry) where present.

* **Parameters:**
  **registry** ([*RuleRegistry*](engine.md#hermeneia.engine.registry.RuleRegistry)) – Rule registry used to resolve implementations.

<a id="hermeneia.rules.loader.load_external_rules"></a>

### hermeneia.rules.loader.load_external_rules(module_name, registry)

Load a plugin module exposing the same register(registry) protocol.

* **Parameters:**
  * **module_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `module_name`.
  * **registry** ([*RuleRegistry*](engine.md#hermeneia.engine.registry.RuleRegistry)) – Rule registry used to resolve implementations.

<a id="module-hermeneia.rules.patterns"></a>

<a id="patterns"></a>

## Patterns

Shared regex skeleton builders for rule matching.

<a id="hermeneia.rules.patterns.normalize_phrases"></a>

### hermeneia.rules.patterns.normalize_phrases(phrases)

Normalize phrases.

* **Parameters:**
  **phrases** (*Iterable* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `phrases`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), …]

<a id="hermeneia.rules.patterns.compile_leading_phrase_regex"></a>

### hermeneia.rules.patterns.compile_leading_phrase_regex(phrases)

Compile leading phrase regex.

* **Parameters:**
  **phrases** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Input value for `phrases`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [re.Pattern](https://docs.python.org/3/library/re.html#re.Pattern)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="hermeneia.rules.patterns.compile_inline_phrase_regex"></a>

### hermeneia.rules.patterns.compile_inline_phrase_regex(phrases)

Compile inline phrase regex.

* **Parameters:**
  **phrases** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Input value for `phrases`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [re.Pattern](https://docs.python.org/3/library/re.html#re.Pattern)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="hermeneia.rules.patterns.compile_structured_leading_term_regex"></a>

### hermeneia.rules.patterns.compile_structured_leading_term_regex(terms)

Compile structured leading term regex.

* **Parameters:**
  **terms** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Input value for `terms`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [re.Pattern](https://docs.python.org/3/library/re.html#re.Pattern)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="hermeneia.rules.patterns.compile_prefixed_term_regex"></a>

### hermeneia.rules.patterns.compile_prefixed_term_regex(prefixes, terms, anchored=False)

Compile prefixed term regex.

* **Parameters:**
  * **prefixes** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Input value for `prefixes`.
  * **terms** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Input value for `terms`.
  * **anchored** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Input value for `anchored`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [re.Pattern](https://docs.python.org/3/library/re.html#re.Pattern)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="hermeneia.rules.patterns.compile_hyphen_suffix_regex"></a>

### hermeneia.rules.patterns.compile_hyphen_suffix_regex(suffixes)

Compile hyphen suffix regex.

* **Parameters:**
  **suffixes** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Input value for `suffixes`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [re.Pattern](https://docs.python.org/3/library/re.html#re.Pattern)[[str](https://docs.python.org/3/library/stdtypes.html#str)]
