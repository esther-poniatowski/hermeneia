# Configuration

Hermeneia configuration is strict YAML validated by Pydantic models.

Unknown fields, unknown rule ids, and type mismatches fail early.

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

- Unknown rule ids in `active`, `disabled`, `overrides`, language defaults, or profile defaults are errors.
- Unknown override fields are errors.
- Options model validation errors are surfaced with rule id context.
- Language-pack `supported_rules` (when declared) is enforced as a rule allowlist.

## Runtime Flags

- `runtime.experimental_rules`: enables experimental rules.
- `runtime.debug`: propagated to rule runtime capability flags.
- `runtime.embeddings`: configures optional embedding backend.

## Scoring and Suggestions

- `scoring.output` controls emitted score payload fields.
  - If score fields are omitted, score computation is skipped.
- `suggestions.enabled: false` disables revision plan operations entirely.
- `suggestions.default_mode` controls fallback suggestion behavior.

## Language

Current release ships with `language.code: en` only.

The language pack contributes:

- parser model id
- preprocessing policy
- lexicons
- rule defaults
- optional supported-rule allowlist
