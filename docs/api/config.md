<a id="configuration"></a>

# Configuration

Strict project configuration, defaults, schema, profile resolution, and loading.

<a id="module-hermeneia.config.defaults"></a>

<a id="defaults"></a>

## Defaults

Built-in profile and runtime defaults.

<a id="hermeneia.config.defaults.ProfilePreset"></a>

### *class* hermeneia.config.defaults.ProfilePreset(name, audience, genre, section, register, active_rules, rule_overrides=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Profilepreset.

<a id="hermeneia.config.defaults.ProfilePreset.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.config.defaults.ProfilePreset.audience"></a>

#### audience *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.config.defaults.ProfilePreset.genre"></a>

#### genre *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.config.defaults.ProfilePreset.section"></a>

#### section *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.config.defaults.ProfilePreset.register"></a>

#### register *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.config.defaults.ProfilePreset.active_rules"></a>

#### active_rules *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

<a id="hermeneia.config.defaults.ProfilePreset.rule_overrides"></a>

#### rule_overrides *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]]*

<a id="module-hermeneia.config.schema"></a>

<a id="schema"></a>

## Schema

Strict configuration parsing and validation.

<a id="hermeneia.config.schema.ConfigError"></a>

### *exception* hermeneia.config.schema.ConfigError

Bases: [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError)

Raised when a configuration file is structurally invalid.

<a id="hermeneia.config.schema.ProfileConfig"></a>

### *class* hermeneia.config.schema.ProfileConfig(\*, name='research', audience=None, genre=None, section=None, register=None)

Bases: `_ConfigModel`

Profileconfig.

<a id="hermeneia.config.schema.ProfileConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True, 'populate_by_name': True, 'validate_by_alias': True, 'validate_by_name': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.ProfileConfig.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Profile name.

<a id="hermeneia.config.schema.ProfileConfig.audience"></a>

#### audience *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Configured audience profile.

<a id="hermeneia.config.schema.ProfileConfig.genre"></a>

#### genre *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Configured writing genre.

<a id="hermeneia.config.schema.ProfileConfig.section"></a>

#### section *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Section-oriented profile policy.

<a id="hermeneia.config.schema.ProfileConfig.register_name"></a>

#### register_name *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Optional register profile name.

<a id="hermeneia.config.schema.ProfileConfig.register"></a>

#### *property* register *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Register.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str) | None

<a id="hermeneia.config.schema.LanguageConfig"></a>

### *class* hermeneia.config.schema.LanguageConfig(\*, code='en', pack=None)

Bases: `_ConfigModel`

Languageconfig.

<a id="hermeneia.config.schema.LanguageConfig.code"></a>

#### code *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Language code for the active language pack.

<a id="hermeneia.config.schema.LanguageConfig.pack"></a>

#### pack *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Language pack implementation identifier.

<a id="hermeneia.config.schema.LanguageConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.EmbeddingConfig"></a>

### *class* hermeneia.config.schema.EmbeddingConfig(\*, backend='none', model='sentence-transformers/all-MiniLM-L6-v2')

Bases: `_ConfigModel`

Embeddingconfig.

<a id="hermeneia.config.schema.EmbeddingConfig.backend"></a>

#### backend *: Literal['none', 'sentence_transformers']*

Embedding backend identifier.

<a id="hermeneia.config.schema.EmbeddingConfig.model"></a>

#### model *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Model name used by the backend.

<a id="hermeneia.config.schema.EmbeddingConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.RuntimeConfig"></a>

### *class* hermeneia.config.schema.RuntimeConfig(\*, strict_validation=True, experimental_rules=False, debug=False, external_rule_modules=(), embeddings=<factory>)

Bases: `_ConfigModel`

Runtimeconfig.

<a id="hermeneia.config.schema.RuntimeConfig.strict_validation"></a>

#### strict_validation *: StrictBool*

Enable strict validation behavior.

<a id="hermeneia.config.schema.RuntimeConfig.experimental_rules"></a>

#### experimental_rules *: StrictBool*

Enable experimental rules.

<a id="hermeneia.config.schema.RuntimeConfig.debug"></a>

#### debug *: StrictBool*

Enable debug-mode diagnostics.

<a id="hermeneia.config.schema.RuntimeConfig.external_rule_modules"></a>

#### external_rule_modules *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

External modules that contribute rules.

<a id="hermeneia.config.schema.RuntimeConfig.embeddings"></a>

#### embeddings *: [EmbeddingConfig](#hermeneia.config.schema.EmbeddingConfig)*

Enable embedding-backed features.

<a id="hermeneia.config.schema.RuntimeConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.RuleOverrideConfig"></a>

### *class* hermeneia.config.schema.RuleOverrideConfig(\*, enabled=None, severity=None, weight=None, options=<factory>, extra_patterns=(), silenced_patterns=())

Bases: `_ConfigModel`

Ruleoverrideconfig.

<a id="hermeneia.config.schema.RuleOverrideConfig.enabled"></a>

#### enabled *: StrictBool | [None](https://docs.python.org/3/library/constants.html#None)*

Whether the feature is enabled.

<a id="hermeneia.config.schema.RuleOverrideConfig.severity"></a>

#### severity *: [Severity](rules-base.md#hermeneia.rules.base.Severity) | [None](https://docs.python.org/3/library/constants.html#None)*

Severity assigned to the rule.

<a id="hermeneia.config.schema.RuleOverrideConfig.weight"></a>

#### weight *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Rule weight used by scoring.

<a id="hermeneia.config.schema.RuleOverrideConfig.options"></a>

#### options *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]*

Rule-specific option mapping.

<a id="hermeneia.config.schema.RuleOverrideConfig.extra_patterns"></a>

#### extra_patterns *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Additional user-defined patterns.

<a id="hermeneia.config.schema.RuleOverrideConfig.silenced_patterns"></a>

#### silenced_patterns *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Patterns excluded from matching.

<a id="hermeneia.config.schema.RuleOverrideConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.RulesConfig"></a>

### *class* hermeneia.config.schema.RulesConfig(\*, active=None, disabled=(), overrides=<factory>)

Bases: `_ConfigModel`

Rulesconfig.

<a id="hermeneia.config.schema.RulesConfig.active"></a>

#### active *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Explicitly activated rule identifiers.

<a id="hermeneia.config.schema.RulesConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.RulesConfig.disabled"></a>

#### disabled *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Explicitly disabled rule identifiers.

<a id="hermeneia.config.schema.RulesConfig.overrides"></a>

#### overrides *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [RuleOverrideConfig](#hermeneia.config.schema.RuleOverrideConfig)]*

Per-rule override configuration.

<a id="hermeneia.config.schema.ScoringConfig"></a>

### *class* hermeneia.config.schema.ScoringConfig(\*, aggregation='hierarchical', output=('layer_scores', 'global_score', 'violation_list'))

Bases: `_ConfigModel`

Scoringconfig.

<a id="hermeneia.config.schema.ScoringConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.ScoringConfig.aggregation"></a>

#### aggregation *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Score aggregation strategy.

<a id="hermeneia.config.schema.ScoringConfig.output"></a>

#### output *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Output configuration block.

<a id="hermeneia.config.schema.SuggestionConfig"></a>

### *class* hermeneia.config.schema.SuggestionConfig(\*, enabled=True, default_mode='tactic_only')

Bases: `_ConfigModel`

Suggestionconfig.

<a id="hermeneia.config.schema.SuggestionConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.SuggestionConfig.enabled"></a>

#### enabled *: StrictBool*

Whether the feature is enabled.

<a id="hermeneia.config.schema.SuggestionConfig.default_mode"></a>

#### default_mode *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Default suggestion mode.

<a id="hermeneia.config.schema.ReportingConfig"></a>

### *class* hermeneia.config.schema.ReportingConfig(\*, format='text', sort_by='severity_desc')

Bases: `_ConfigModel`

Reportingconfig.

<a id="hermeneia.config.schema.ReportingConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.ReportingConfig.format"></a>

#### format *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Report output format.

<a id="hermeneia.config.schema.ReportingConfig.sort_by"></a>

#### sort_by *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Diagnostic sorting strategy.

<a id="hermeneia.config.schema.ProjectConfig"></a>

### *class* hermeneia.config.schema.ProjectConfig(\*, profile=<factory>, language=<factory>, runtime=<factory>, rules=<factory>, scoring=<factory>, suggestions=<factory>, reporting=<factory>)

Bases: `_ConfigModel`

Projectconfig.

<a id="hermeneia.config.schema.ProjectConfig.model_config"></a>

#### model_config *: ClassVar[ConfigDict]* *= {'extra': 'forbid', 'frozen': True}*

Configuration for the model, should be a dictionary conforming to [ConfigDict][pydantic.config.ConfigDict].

<a id="hermeneia.config.schema.ProjectConfig.profile"></a>

#### profile *: [ProfileConfig](#hermeneia.config.schema.ProfileConfig)*

Configured value for `profile`.

<a id="hermeneia.config.schema.ProjectConfig.language"></a>

#### language *: [LanguageConfig](#hermeneia.config.schema.LanguageConfig)*

Language configuration block.

<a id="hermeneia.config.schema.ProjectConfig.runtime"></a>

#### runtime *: [RuntimeConfig](#hermeneia.config.schema.RuntimeConfig)*

Runtime configuration block.

<a id="hermeneia.config.schema.ProjectConfig.rules"></a>

#### rules *: [RulesConfig](#hermeneia.config.schema.RulesConfig)*

Rule-selection configuration block.

<a id="hermeneia.config.schema.ProjectConfig.scoring"></a>

#### scoring *: [ScoringConfig](#hermeneia.config.schema.ScoringConfig)*

Scoring configuration block.

<a id="hermeneia.config.schema.ProjectConfig.suggestions"></a>

#### suggestions *: [SuggestionConfig](#hermeneia.config.schema.SuggestionConfig)*

Suggestion configuration block.

<a id="hermeneia.config.schema.ProjectConfig.reporting"></a>

#### reporting *: [ReportingConfig](#hermeneia.config.schema.ReportingConfig)*

Reporting configuration block.

<a id="hermeneia.config.schema.parse_project_config"></a>

### hermeneia.config.schema.parse_project_config(raw)

Validate a raw mapping and return the typed config object.

* **Parameters:**
  **raw** (*Mapping* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*object*](https://docs.python.org/3/library/functions.html#object) *]*  *|* *None*) – Raw value before validation.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [ProjectConfig](#hermeneia.config.schema.ProjectConfig)

<a id="module-hermeneia.config.profile"></a>

<a id="profile-resolution"></a>

## Profile resolution

Resolved profile construction with strict merge semantics.

<a id="hermeneia.config.profile.CliOverrides"></a>

### *class* hermeneia.config.profile.CliOverrides(profile_name=None, rule_ids=(), disabled_rule_ids=(), reporting_format=None, enable_experimental=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Clioverrides.

<a id="hermeneia.config.profile.CliOverrides.profile_name"></a>

#### profile_name *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.config.profile.CliOverrides.rule_ids"></a>

#### rule_ids *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.config.profile.CliOverrides.disabled_rule_ids"></a>

#### disabled_rule_ids *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.config.profile.CliOverrides.reporting_format"></a>

#### reporting_format *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.config.profile.CliOverrides.enable_experimental"></a>

#### enable_experimental *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.config.profile.ProfileResolver"></a>

### *class* hermeneia.config.profile.ProfileResolver(registry)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Merge rule defaults, language defaults, profile defaults, and overrides.

* **Parameters:**
  **registry** ([*RuleRegistry*](engine.md#hermeneia.engine.registry.RuleRegistry)) – Rule registry used to resolve implementations.

<a id="hermeneia.config.profile.ProfileResolver.__init__"></a>

#### \_\_init_\_(registry)

Initialize the instance.

<a id="hermeneia.config.profile.ProfileResolver.resolve"></a>

#### resolve(config, language_pack, cli=None)

Resolve.

* **Parameters:**
  * **config** ([*ProjectConfig*](#hermeneia.config.schema.ProjectConfig)) – Resolved configuration used by this operation.
  * **language_pack** ([*LanguagePack*](language.md#hermeneia.language.base.LanguagePack)) – Input value for `language_pack`.
  * **cli** ([*CliOverrides*](#hermeneia.config.profile.CliOverrides) *|* *None*) – Input value for `cli`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [ResolvedProfile](rules-base.md#hermeneia.rules.base.ResolvedProfile)

<a id="module-hermeneia.config.loader"></a>

<a id="loader"></a>

## Loader

YAML configuration loading.

<a id="hermeneia.config.loader.load_project_config"></a>

### hermeneia.config.loader.load_project_config(path)

Load project config.

* **Parameters:**
  **path** (*Path* *|* *None*) – Filesystem path used by this operation.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [ProjectConfig](#hermeneia.config.schema.ProjectConfig)
