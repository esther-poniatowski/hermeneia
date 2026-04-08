# ADR 0004: Unified Rule Registration Protocol

- Status: Accepted
- Date: 2026-04-07

## Context

Built-in and external rules must use the same integration seam to avoid hidden behavior and plugin divergence.

## Decision

All rule modules expose:

```python
def register(registry): ...
```

Built-ins are discovered by package walk and imported explicitly. External modules loaded through CLI/config use the same contract.

## Alternatives Considered

1. Import-time decorators with implicit global registration.
2. Separate plugin-only registration API.

Rejected because they obscure load order and fragment extension behavior.

## Consequences

- Symmetric built-in and external rule integration.
- Explicit load boundaries and better diagnostics.
- Easier testability of custom rules.
