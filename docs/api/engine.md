<a id="engine"></a>

# Engine

Analysis runner, rule registry, and orchestration primitives.

<a id="module-hermeneia.engine.detector"></a>

<a id="detector"></a>

## Detector

Rule dispatch over a parsed, annotated document.

<a id="hermeneia.engine.detector.RuleDiagnostic"></a>

### *class* hermeneia.engine.detector.RuleDiagnostic(code, rule_id, message)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Rulediagnostic.

<a id="hermeneia.engine.detector.RuleDiagnostic.code"></a>

#### code *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.engine.detector.RuleDiagnostic.rule_id"></a>

#### rule_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.engine.detector.RuleDiagnostic.message"></a>

#### message *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.engine.detector.DetectionResult"></a>

### *class* hermeneia.engine.detector.DetectionResult(violations, diagnostics=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Detectionresult.

<a id="hermeneia.engine.detector.DetectionResult.violations"></a>

#### violations *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[Violation](rules-base.md#hermeneia.rules.base.Violation), ...]*

<a id="hermeneia.engine.detector.DetectionResult.diagnostics"></a>

#### diagnostics *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[RuleDiagnostic](#hermeneia.engine.detector.RuleDiagnostic), ...]* *= ()*

<a id="hermeneia.engine.detector.RuleDetector"></a>

### *class* hermeneia.engine.detector.RuleDetector(registry)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Ruledetector.

* **Parameters:**
  **registry** ([*RuleRegistry*](#hermeneia.engine.registry.RuleRegistry)) – Rule registry used to resolve implementations.

<a id="hermeneia.engine.detector.RuleDetector.__init__"></a>

#### \_\_init_\_(registry)

Initialize the instance.

<a id="hermeneia.engine.detector.RuleDetector.detect"></a>

#### detect(document, profile, language_pack, features, debug_mode=False)

Detect.

* **Parameters:**
  * **document** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
  * **profile** ([*ResolvedProfile*](rules-base.md#hermeneia.rules.base.ResolvedProfile)) – Resolved profile controlling rule behavior.
  * **language_pack** ([*LanguagePack*](language.md#hermeneia.language.base.LanguagePack)) – Input value for `language_pack`.
  * **features** ([*FeatureStore*](document.md#hermeneia.document.indexes.FeatureStore)) – Input value for `features`.
  * **debug_mode** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Input value for `debug_mode`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [DetectionResult](#hermeneia.engine.detector.DetectionResult)

<a id="module-hermeneia.engine.registry"></a>

<a id="registry"></a>

## Registry

Application-layer rule registry.

<a id="hermeneia.engine.registry.RuleRegistration"></a>

### *class* hermeneia.engine.registry.RuleRegistration(metadata, rule_cls)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Ruleregistration.

<a id="hermeneia.engine.registry.RuleRegistration.metadata"></a>

#### metadata *: [RuleMetadata](rules-base.md#hermeneia.rules.base.RuleMetadata)*

<a id="hermeneia.engine.registry.RuleRegistration.rule_cls"></a>

#### rule_cls *: [type](https://docs.python.org/3/library/functions.html#type)[[BaseRule](rules-base.md#hermeneia.rules.base.BaseRule)]*

<a id="hermeneia.engine.registry.RuleRegistry"></a>

### *class* hermeneia.engine.registry.RuleRegistry

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Ruleregistry.

<a id="hermeneia.engine.registry.RuleRegistry.__init__"></a>

#### \_\_init_\_()

Initialize the instance.

<a id="hermeneia.engine.registry.RuleRegistry.add"></a>

#### add(rule_cls)

Add.

* **Parameters:**
  **rule_cls** ([*type*](https://docs.python.org/3/library/functions.html#type) *[*[*BaseRule*](rules-base.md#hermeneia.rules.base.BaseRule) *]*) – Input value for `rule_cls`.

<a id="hermeneia.engine.registry.RuleRegistry.get"></a>

#### get(rule_id)

Get.

* **Parameters:**
  **rule_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `rule_id`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [RuleRegistration](#hermeneia.engine.registry.RuleRegistration)

<a id="hermeneia.engine.registry.RuleRegistry.instantiate"></a>

#### instantiate(settings)

Instantiate.

* **Parameters:**
  **settings** ([*ResolvedRuleSettings*](rules-base.md#hermeneia.rules.base.ResolvedRuleSettings)) – Input value for `settings`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [BaseRule](rules-base.md#hermeneia.rules.base.BaseRule)

<a id="hermeneia.engine.registry.RuleRegistry.all"></a>

#### all()

All.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[RuleRegistration](#hermeneia.engine.registry.RuleRegistration), …]

<a id="hermeneia.engine.registry.RuleRegistry.rule_ids"></a>

#### rule_ids()

Rule ids.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), …]

<a id="module-hermeneia.engine.runner"></a>

<a id="runner"></a>

## Runner

Application-level analysis orchestration.

<a id="hermeneia.engine.runner.AnalysisInput"></a>

### *class* hermeneia.engine.runner.AnalysisInput(path, source)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Analysisinput.

<a id="hermeneia.engine.runner.AnalysisInput.path"></a>

#### path *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.engine.runner.AnalysisInput.source"></a>

#### source *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.engine.runner.OperationalDiagnostic"></a>

### *class* hermeneia.engine.runner.OperationalDiagnostic(code, message, path=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Operationaldiagnostic.

<a id="hermeneia.engine.runner.OperationalDiagnostic.code"></a>

#### code *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.engine.runner.OperationalDiagnostic.message"></a>

#### message *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.engine.runner.OperationalDiagnostic.path"></a>

#### path *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.engine.runner.AnalysisResult"></a>

### *class* hermeneia.engine.runner.AnalysisResult(document, profile, violations, report, diagnostics=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Analysisresult.

<a id="hermeneia.engine.runner.AnalysisResult.document"></a>

#### document *: [Document](document.md#hermeneia.document.model.Document)*

<a id="hermeneia.engine.runner.AnalysisResult.profile"></a>

#### profile *: [ResolvedProfile](rules-base.md#hermeneia.rules.base.ResolvedProfile)*

<a id="hermeneia.engine.runner.AnalysisResult.violations"></a>

#### violations *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[Violation](rules-base.md#hermeneia.rules.base.Violation), ...]*

<a id="hermeneia.engine.runner.AnalysisResult.report"></a>

#### report *: [DiagnosticReport](report.md#hermeneia.report.diagnostic.DiagnosticReport)*

<a id="hermeneia.engine.runner.AnalysisResult.diagnostics"></a>

#### diagnostics *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[OperationalDiagnostic](#hermeneia.engine.runner.OperationalDiagnostic), ...]* *= ()*

<a id="hermeneia.engine.runner.BatchAnalysisResult"></a>

### *class* hermeneia.engine.runner.BatchAnalysisResult(results, diagnostics=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Batchanalysisresult.

<a id="hermeneia.engine.runner.BatchAnalysisResult.results"></a>

#### results *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[AnalysisResult](#hermeneia.engine.runner.AnalysisResult), ...]*

<a id="hermeneia.engine.runner.BatchAnalysisResult.diagnostics"></a>

#### diagnostics *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[OperationalDiagnostic](#hermeneia.engine.runner.OperationalDiagnostic), ...]* *= ()*

<a id="hermeneia.engine.runner.AnnotationResult"></a>

### *class* hermeneia.engine.runner.AnnotationResult(document, diagnostics=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Annotationresult.

<a id="hermeneia.engine.runner.AnnotationResult.document"></a>

#### document *: [Document](document.md#hermeneia.document.model.Document)*

<a id="hermeneia.engine.runner.AnnotationResult.diagnostics"></a>

#### diagnostics *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.engine.runner.AnalysisPolicy"></a>

### *class* hermeneia.engine.runner.AnalysisPolicy(scoring_aggregation='hierarchical', scoring_output=frozenset({'global_score', 'layer_scores', 'violation_list'}), debug_mode=False, suggestions_enabled=True, suggestion_default_mode=SuggestionMode.TACTIC_ONLY)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Analysispolicy.

<a id="hermeneia.engine.runner.AnalysisPolicy.scoring_aggregation"></a>

#### scoring_aggregation *: [str](https://docs.python.org/3/library/stdtypes.html#str)* *= 'hierarchical'*

<a id="hermeneia.engine.runner.AnalysisPolicy.scoring_output"></a>

#### scoring_output *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({'global_score', 'layer_scores', 'violation_list'})*

<a id="hermeneia.engine.runner.AnalysisPolicy.debug_mode"></a>

#### debug_mode *: [bool](https://docs.python.org/3/library/functions.html#bool)* *= False*

<a id="hermeneia.engine.runner.AnalysisPolicy.suggestions_enabled"></a>

#### suggestions_enabled *: [bool](https://docs.python.org/3/library/functions.html#bool)* *= True*

<a id="hermeneia.engine.runner.AnalysisPolicy.suggestion_default_mode"></a>

#### suggestion_default_mode *: [SuggestionMode](rules-base.md#hermeneia.rules.base.SuggestionMode)* *= 'tactic_only'*

<a id="hermeneia.engine.runner.DocumentAnnotator"></a>

### *class* hermeneia.engine.runner.DocumentAnnotator(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Documentannotator.

<a id="hermeneia.engine.runner.DocumentAnnotator.annotate"></a>

#### annotate(document, profile)

Annotate.

* **Parameters:**
  * **document** ([*Document*](document.md#hermeneia.document.model.Document)) – Document instance to inspect.
  * **profile** ([*ResolvedProfile*](rules-base.md#hermeneia.rules.base.ResolvedProfile)) – Resolved profile controlling rule behavior.
* **Raises:**
  [**NotImplementedError**](https://docs.python.org/3/library/exceptions.html#NotImplementedError) – Raised under documented error conditions.

<a id="hermeneia.engine.runner.AnalysisRunner"></a>

### *class* hermeneia.engine.runner.AnalysisRunner(parser, annotator, registry, language_pack, embedding_backend, policy=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Concrete orchestration for parse -> annotate -> feature -> detect -> score -> report.

* **Parameters:**
  * **parser** ([*DocumentParser*](document.md#hermeneia.document.parser.DocumentParser)) – Input value for `parser`.
  * **annotator** ([*DocumentAnnotator*](#hermeneia.engine.runner.DocumentAnnotator)) – Input value for `annotator`.
  * **registry** ([*RuleRegistry*](#hermeneia.engine.registry.RuleRegistry)) – Rule registry used to resolve implementations.
  * **language_pack** ([*LanguagePack*](language.md#hermeneia.language.base.LanguagePack)) – Input value for `language_pack`.
  * **embedding_backend** ([*EmbeddingBackend*](document.md#hermeneia.document.indexes.EmbeddingBackend) *|* *None*) – Input value for `embedding_backend`.
  * **policy** ([*AnalysisPolicy*](#hermeneia.engine.runner.AnalysisPolicy) *|* *None*) – Input value for `policy`.

<a id="hermeneia.engine.runner.AnalysisRunner.__init__"></a>

#### \_\_init_\_(parser, annotator, registry, language_pack, embedding_backend, policy=None)

Initialize the instance.

<a id="hermeneia.engine.runner.AnalysisRunner.analyze"></a>

#### analyze(inputs, profile)

Analyze.

* **Parameters:**
  * **inputs** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*AnalysisInput*](#hermeneia.engine.runner.AnalysisInput) *,*  *...* *]*) – Input value for `inputs`.
  * **profile** ([*ResolvedProfile*](rules-base.md#hermeneia.rules.base.ResolvedProfile)) – Resolved profile controlling rule behavior.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [BatchAnalysisResult](#hermeneia.engine.runner.BatchAnalysisResult)
