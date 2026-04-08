# Configuration Resolution

## Schema Layer

`config/schema.py` defines strict Pydantic models for:

- `profile`
- `language`
- `runtime` (including `debug`, `experimental_rules`, embeddings backend)
- `rules` (active/disabled/overrides)
- `scoring`
- `suggestions`
- `reporting`

Unknown fields are rejected.

## Resolution Layer

`ProfileResolver` builds `ResolvedProfile` and `ResolvedRuleSettings` for each active rule.

Merge precedence:

1. Rule metadata defaults
2. Language-pack defaults
3. Profile preset overrides
4. User overrides

Merge semantics:

- scalars replace
- mappings deep-merge
- lists replace
- `extra_patterns` and `silenced_patterns` concatenate

## Validation Boundaries

Resolution fails early for:

- unknown rule ids in config/profile/language defaults
- invalid override field names
- unsupported language packs for rules
- language-pack `supported_rules` allowlist violations
- rule options model validation failures

The validation boundary keeps configuration behavior deterministic and auditable.
