# Pipeline

Hermeneia runs a bounded document-local pipeline:

1. Parse markdown into block/inline `Document` IR.
2. Build source-line structural views (`SourceLine`).
3. Build sentence projections with offset reconciliation.
4. Annotate projected text (spaCy or explicit fallback).
5. Build indexes and shared features (`FeatureStore`), including language-pack-driven support signals.
6. Run rule detection through the registry.
7. Score violations (when enabled).
8. Build revision plan (when enabled).
9. Emit report payloads (text/json).

## Failure Boundaries

The runner isolates operational failures and continues batch execution when possible:

- parse failures -> `parse_failure` diagnostics
- annotation failures -> `annotation_failure` diagnostics
- annotation backend degradation -> `annotation_backend` diagnostics
- rule instantiation/execution/contract failures -> rule diagnostics

Rules are never allowed to crash the whole run.

## Determinism

Given identical:

- source text
- config/profile
- active rule set
- model/backend versions

the pipeline output is deterministic.
