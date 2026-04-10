# Rules and Detection

## Grouping Axes

Hermeneia uses three distinct axes for rules. These axes are intentionally independent.

1. Namespace (in `rule_id`): topical ownership and discoverability.
   - Examples: `vocabulary.*`, `syntax.*`, `linkage.*`, `reference.*`, `paragraph.*`, `structure.*`, `terminology.*`, `evidence.*`, `math.*`
2. Layer (`RuleMetadata.layer`): reader-impact dimension used by scoring and reporting.
   - `surface_style`, `local_discourse`, `paragraph_rhetoric`, `document_structure`, `audience_fit`
3. Runtime class (base type): execution strategy.
   - `SourcePatternRule`, `AnnotatedRule`, `HeuristicSemanticRule`

Because these axes serve different purposes, they do not always align one-to-one.
For example, `math.*` rules are math-scoped by namespace, but can map to different layers:
`math.display_math` -> `surface_style`, `math.display_followup_interpretation` -> `local_discourse`,
`math.proof_placement_context` -> `document_structure`, and
`math.assumption_motivation_order` -> `audience_fit`.

Accordingly, rule placement is **not** based on textual unit alone (sentence/paragraph/section).
A sentence-level check may belong to different namespaces depending on the phenomenon it diagnoses.

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

`layer` is not cosmetic metadata:

- violation contracts enforce `Violation.layer == RuleMetadata.layer`
- hierarchical scoring aggregates penalties by `Layer`

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
