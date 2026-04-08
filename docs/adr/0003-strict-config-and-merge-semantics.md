# ADR 0003: Strict Configuration Validation and Deterministic Merge Semantics

- Status: Accepted
- Date: 2026-04-07

## Context

Configuration drives rule selection, thresholds, severities, and runtime behavior.
Silent fallbacks or ambiguous merges make diagnostics non-auditable.

## Decision

Use strict Pydantic schema validation and explicit merge semantics:

- unknown fields and unknown rule ids are errors
- rule settings resolve through fixed precedence layers
- mapping fields deep-merge
- list fields replace
- additive pattern fields concatenate by design

## Alternatives Considered

1. Best-effort parsing with ignored unknown fields.
2. Shallow merge via top-level `dict.update`.

Rejected because they allow accidental misconfiguration and hidden policy drift.

## Consequences

- Fail-fast behavior with clear error messages.
- Reproducible profile resolution.
- Safer evolution of rule options and language-pack defaults.
