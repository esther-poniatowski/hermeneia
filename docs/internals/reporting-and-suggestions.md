# Reporting, Scoring, and Suggestions

## Scoring

`HierarchicalScorer` computes per-layer penalties and a global score from:

- violation severity multipliers
- per-rule resolved weights

Scoring execution is policy-driven:

- if `scoring.output` excludes score fields, score computation is skipped

## Suggestions and Revision Plan

`RevisionPlanner` orders operations by revision phase:

1. document structure
2. paragraph rhetoric
3. local discourse
4. audience fit
5. surface style

Deterministic templates are emitted only when preconditions are met (for example:
contraction expansion, proof marker insertion, stable nominalization rewrites,
passive voice with identifiable actor). Otherwise tactic-only guidance is emitted.

## Report Payloads

`DiagnosticReport` carries:

- violations
- optional scorecard (policy-controlled)
- revision plan

Text output includes source span annotations and evidence details.
JSON output is structured for downstream tooling.
