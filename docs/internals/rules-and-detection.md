# Rules and Detection

## Rule Taxonomy

Hermeneia supports three runtime rule base classes:

- `SourcePatternRule`: structured line/source-context checks
- `AnnotatedRule`: parser-local sentence/token checks
- `HeuristicSemanticRule`: bounded semantic heuristics over shared features

Language-sensitive inventories are not defined ad hoc in rule modules. They are read from
`RuleContext.language_pack.lexicons`, and rule modules consume shared regex builders from
`rules/patterns.py` where phrase skeletons are needed.

## Metadata Contract

Each rule class declares `RuleMetadata`:

- `rule_id`, `label`, `layer`, `tractability`, `kind`
- default severity/weight/options
- supported languages
- abstention flags
- required evidence fields
- suggestion mode
- experimental status

## Registration and Loading

- Built-ins: package walk + `register(registry)` protocol.
- External modules: same `register(registry)` contract via `--load-rules` or runtime config.

No import-time side-effect registration chain is required.

## Detection Runtime

`RuleDetector`:

1. Instantiates active rules from registry + resolved settings.
2. Executes checks with shared `RuleContext`.
3. Enforces violation contract:
   - matching rule id/layer
   - required evidence fields
   - class-H confidence/evidence requirements
4. Emits diagnostics for rule failures without terminating analysis.

`RuleContext` carries:

- resolved profile
- language pack
- shared `FeatureStore`
- runtime capabilities (`embeddings_available`, `debug_mode`, `experimental_rules_enabled`)

`RuleContext` also exposes convenience accessors for these capability flags directly.
