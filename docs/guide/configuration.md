# Configuration

Hermeneia configuration is strict YAML validated by Pydantic models.

Unknown fields, unknown rule ids, and type mismatches fail early.

Profiles and options let teams calibrate diagnostics to audience and document genre while keeping
one shared rule engine.

Use this page after [Usage](usage.md): first run default lint, then tune policy with explicit overrides.

## Example

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
    - surface.sentence_length
    - surface.passive_voice
    - paragraph.topic_sentence
  disabled:
    - surface.contraction
  overrides:
    surface.sentence_length:
      options:
        max_words: 24
      severity: warning
      weight: 1.1
    surface.banned_transition:
      extra_patterns:
        - as a consequence
      silenced_patterns:
        - note that
    surface.generic_link_text:
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

## Merge and Resolution Semantics

This section explains how the engine combines configuration layers into one effective rule policy.

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

These checks prevent silent policy drift and keep rule behavior auditable across teams.

- Unknown rule ids in `active`, `disabled`, `overrides`, language defaults, or profile defaults are errors.
- Unknown override fields are errors.
- Options model validation errors are surfaced with rule id context.
- `surface.generic_link_text` options accept only `reference_labels` and `procedural_terms`.
- `structure.opening_sentence_presence` options accept `min_opening_words` and `forbidden_block_kinds`.
- `structure.section_opener_block_kind` options accept `blocked_block_kinds` and `apply_heading_levels`.
- Language-pack `supported_rules` (when declared) is enforced as a rule allowlist.

## Runtime Flags

Runtime flags control optional capabilities without changing core rule definitions.

- `runtime.experimental_rules`: enables experimental rules.
- `runtime.debug`: propagated to rule runtime capability flags.
- `runtime.embeddings`: configures optional embedding backend.
- `runtime.external_rule_modules`: preloads external modules exposing `register(registry)`.

## Why Profiles Matter

Profile presets encode quality priorities for different writing contexts:

- `research`: emphasizes formal argument precision and evidence calibration
- `pedagogical`: tightens accessibility and jargon constraints
- `math`: strengthens notation, equation-context, and proof-flow checks

Starting from a profile avoids ad hoc per-rule toggling and keeps policy consistent across files.

## Scoring and Suggestions

These options control output behavior after rules execute.

- `scoring.output` controls emitted score payload fields.
  - If score fields are omitted, score computation is skipped.
- `suggestions.enabled: false` disables revision plan operations entirely.
- `suggestions.default_mode` controls fallback suggestion behavior.

## Statistics and Heuristics

Some checks are deterministic pattern constraints.
Conversely, other checks are heuristic diagnostics that expose potential reader-friction signals.
Accordingly, use weights, severities, and profile overrides to tune false-positive tolerance without disabling
entire quality dimensions.

## Reporting

- `reporting.format` is consumed by CLI output rendering (`text`/`json`).
- `reporting.sort_by` is currently validated and parsed but not yet applied in rendering order.

For the command-level switches that select config files and output mode, see [CLI Reference](cli-reference.md).

## Language

Current release ships with `language.code: en` only.

The language pack contributes:

- parser model id
- preprocessing policy
- lexicons (connectors, rhetorical openers, claim markers, definitional markers, etc.)
- rule defaults
- optional supported-rule allowlist
