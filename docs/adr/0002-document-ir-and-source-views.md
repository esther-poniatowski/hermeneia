# ADR 0002: Block/Inline IR with Derived Source Views

- Status: Accepted
- Date: 2026-04-07

## Context

Rules require both structural markdown context and NLP annotation while preserving exact source spans.
Raw rescanning duplicates parser logic and breaks consistency across rule families.

## Decision

Use a single canonical block/inline `Document` IR with:

- typed blocks and inline nodes
- sentence ids and block ids
- projection-based NLP text with offset reconciliation
- derived `SourceLine` views for source-pattern rules
- shared `DocumentIndexes` and `FeatureStore`

## Alternatives Considered

1. Independent raw-text scanning for source rules.
2. Flat sentence/token model without block-level IR.

Both were rejected due to duplicated structure inference and weaker span accuracy.

## Consequences

- One structural source of truth across rule types.
- Reliable source annotations and evidence spans.
- Shared indexes reduce duplicated computation.
