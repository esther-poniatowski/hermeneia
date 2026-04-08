# ADR 0005: English-First Language Pack Strategy

- Status: Accepted
- Date: 2026-04-07

## Context

Many rules rely on language-specific syntax and rhetoric assumptions. Claiming generic multilingual support in v1 would be misleading.

## Decision

Ship v1 with an explicit English language pack only, while keeping the language-pack seam first-class:

- language code in config
- language registry
- per-pack lexicons/defaults/preprocessing policy
- per-pack optional supported-rule allowlist

## Alternatives Considered

1. Marketed multilingual abstraction with English behavior hard-coded underneath.
2. Directly embedding language assumptions into rule internals without a pack boundary.

Rejected because both approaches block safe future multilingual extension.

## Consequences

- Honest v1 capability boundary.
- Clear path to add future packs without re-architecting core contracts.
- Rule support and defaults can be constrained per language pack.
