# Configuration

Configuration defines the effective lint policy: which rules run, how overrides resolve, and which report fields are emitted.
This page moves from structure to details: YAML shape, section responsibilities, field controls, then merge and validation behavior.
For execution workflow, see [Usage](usage.md); for rule behavior examples, see [Rule Registry](rule-registry.md); for command flags, see [CLI Reference](cli-reference.md).

> [!NOTE]
> The configuration file is strict YAML validated by Pydantic models, so unknown fields, unknown
> rule ids, and type mismatches fail early.

## Typical Format

Start from this YAML shape, then adjust each section in the field reference below.

```yaml
profile:
  name: research
  audience: specialist
  genre: research_note
  section: body
  register: formal

language:
  code: en

runtime:
  strict_validation: true
  experimental_rules: false
  debug: false
  embeddings:
    backend: none

rules:
  active:
    - syntax.sentence_length
    - syntax.passive_voice
    - paragraph.topic_sentence
  disabled:
    - vocabulary.contraction
  overrides:
    syntax.sentence_length:
      options:
        max_words: 24
      severity: warning
      weight: 1.1
    linkage.banned_transition:
      extra_patterns:
        - as a consequence
      silenced_patterns:
        - note that
    reference.generic_link_text:
      options:
        reference_labels: [lemma, theorem, corollary]
        procedural_terms: [note, analysis, specialization, derivation]
    structure.opening_sentence_presence:
      options:
        min_opening_words: 10
        forbidden_block_kinds: [list, table, code_block, display_math]
    structure.section_opener_block_kind:
      options:
        blocked_block_kinds: [list, table, code_block, display_math]
        apply_heading_levels: [2, 3]

scoring:
  aggregation: hierarchical
  output: [layer_scores, global_score, violation_list]

suggestions:
  enabled: true
  default_mode: tactic_only

reporting:
  format: text
  sort_by: severity_desc
```

## Section Overview

Use this map to locate the section that controls the behavior to tune.

| Section | What it controls |
| --- | --- |
| `profile` | Base preset and audience/genre metadata used to resolve rule policy context |
| `language` | Language-pack selection |
| `runtime` | Validation strictness, debug/experimental flags, external modules, embedding backend |
| `rules` | Active/disabled rule sets and per-rule overrides |
| `scoring` | Score aggregation mode and emitted score payload fields |
| `suggestions` | Revision-plan generation and default suggestion mode |
| `reporting` | Render format and report sort preference |

## Field Reference

This reference is organized by top-level section in the same order as the YAML template.

### Profile

`profile` selects the base preset and optional contextual metadata overrides.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `name` | `str` | `research` | Selects the profile preset used for active rules and preset overrides |
| `audience` | `str \| null` | preset value | Overrides resolved profile audience metadata |
| `genre` | `str \| null` | preset value | Overrides resolved profile genre metadata |
| `section` | `str \| null` | preset value | Overrides resolved profile section metadata |
| `register` | `str \| null` | preset value | Overrides resolved profile register metadata |

`audience`, `genre`, `section`, and `register` do not select rules directly; they expose contextual metadata to rule logic and reporting.

### Language

`language` controls which language pack contributes lexicons and defaults.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `code` | `str` | `en` | Selects the language pack loaded by the runtime |
| `pack` | `str \| null` | `null` | Reserved for pack variants; parsed but not applied by the current CLI runtime |

### Runtime

`runtime` controls optional runtime capabilities and validation behavior.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `strict_validation` | `bool` | `true` | Enables strict config/rule-id validation |
| `experimental_rules` | `bool` | `false` | Enables rules marked experimental |
| `debug` | `bool` | `false` | Propagates debug capability to rule runtime context |
| `external_rule_modules` | `list[str]` | `[]` | Loads external modules exposing `register(registry)` before analysis |
| `embeddings.backend` | `none \| sentence_transformers` | `none` | Selects optional embedding backend |
| `embeddings.model` | `str` | `sentence-transformers/all-MiniLM-L6-v2` | Model identifier used when embeddings backend is enabled |

### Rules

`rules` controls activation sets and per-rule policy overrides.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `active` | `list[str] \| null` | `null` | Explicit active rule set; when omitted, profile preset active rules are used |
| `disabled` | `list[str]` | `[]` | Rule ids removed after active-set resolution |
| `overrides` | `map[str, override]` | `{}` | Per-rule override objects keyed by rule id |

Override object fields:

| Field | Type | Control |
| --- | --- | --- |
| `enabled` | `bool \| null` | Enables/disables one rule explicitly |
| `severity` | `info \| warning \| error \| null` | Overrides default severity |
| `weight` | `float \| null` | Overrides scoring weight |
| `options` | `map[str, object]` | Rule-specific options validated by each rule options model |
| `extra_patterns` | `list[str]` | Additive pattern extensions for rules that consume pattern lists |
| `silenced_patterns` | `list[str]` | Additive pattern silencing for rules that consume pattern lists |

### Scoring

`scoring` controls score computation mode and emitted score payload fields.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `aggregation` | `str` | `hierarchical` | Selects scoring aggregation strategy; current runtime accepts `hierarchical` only |
| `output` | `list[str]` | `["layer_scores", "global_score", "violation_list"]` | Selects score payload fields emitted in reports |

If `output` omits both `layer_scores` and `global_score`, score computation is skipped.

### Suggestions

`suggestions` controls revision-plan generation behavior.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `enabled` | `bool` | `true` | Enables revision-plan generation |
| `default_mode` | `str` | `tactic_only` | Default suggestion mode used by the revision planner |

### Reporting

`reporting` controls output rendering defaults.

| Field | Type | Default | Control |
| --- | --- | --- | --- |
| `format` | `text \| json` | `text` | Selects CLI output format when `--format` is not passed |
| `sort_by` | `str` | `severity_desc` | Parsed and validated; not yet applied by current renderer |

## Merge and Resolution Semantics

After parsing, the engine combines multiple policy layers into one effective rule policy.

Rule settings are resolved in this order:

1. Rule metadata defaults
2. Language-pack defaults
3. Profile preset overrides
4. User overrides

Field semantics:

- Scalars replace.
- Mappings deep-merge recursively.
- Lists replace.
- `extra_patterns` and `silenced_patterns` are additive (concatenated by layer).

## Strict Validation Rules

These checks prevent silent policy drift and keep rule behavior auditable across runs.

- Unknown rule ids in `active`, `disabled`, `overrides`, language defaults, or profile defaults are errors.
- Unknown override fields are errors.
- Options model validation errors are surfaced with rule id context.
- `reference.generic_link_text` options accept only `reference_labels` and `procedural_terms`.
- `structure.opening_sentence_presence` options accept `min_opening_words` and `forbidden_block_kinds`.
- `structure.section_opener_block_kind` options accept `blocked_block_kinds` and `apply_heading_levels`.
- Language-pack `supported_rules` (when declared) is enforced as a rule allowlist.

## Heuristic Sensitivity Tuning

The rule set mixes deterministic constraints and heuristic diagnostics.
Specifically, deterministic checks encode direct policy requirements, whereas heuristic checks surface likely reader-friction signals.
Accordingly, use severities, weights, and profile overrides to tune tolerance without disabling entire quality dimensions.
