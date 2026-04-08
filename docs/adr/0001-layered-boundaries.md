# ADR 0001: Layered Boundaries (Domain / Application / Infrastructure / Adapters)

- Status: Accepted
- Date: 2026-04-07

## Context

The project needs strong modularity, explicit failure boundaries, and predictable extension seams.
Early monolithic designs mixed parsing, rule policy, I/O, and reporting concerns.

## Decision

Adopt a strict layered architecture:

- Domain: pure analysis concepts and rule contracts
- Application: orchestration, resolution, sequencing, diagnostics policy
- Infrastructure: parser/NLP/embedding/YAML integrations
- Adapters: CLI composition and rendering

## Alternatives Considered

1. Monolithic linter module with shared mutable state.
2. Thin wrappers around legacy mixed-concern functions.

Both alternatives were rejected because they hide boundaries and make evolution high-risk.

## Consequences

- Clear dependency direction and test boundaries.
- Lower coupling for future rule/language/backend additions.
- Slightly higher upfront structure, with significantly lower long-term churn.
