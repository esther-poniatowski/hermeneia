# Prose Audit Protocol

This document defines how to audit technical prose quality with explicit evidence and deterministic reporting.
It applies to technical, academic, mathematical, teaching, and pedagogical documents.

It does not restate all rule-level checks already encoded in hermeneia.
Instead, it extends the automated pipeline with review constraints that remain judgment-dependent.

## Purpose

Use this protocol to evaluate prose quality with a consistent audit method and output contract.

Automated criteria are maintained in:
- [Rule Registry](rule-registry.md)
- hermeneia configuration and profile defaults

This protocol focuses on audit behavior that cannot be fully reduced to rule matching.
Accordingly, use it after running the operational workflow in [Usage](usage.md).

## Scope

By default, in scope:
- research papers and preprints
- lecture notes and pedagogical handouts
- technical reports and design notes
- mathematical exposition and proof-oriented prose
- repository documentation (README, guides, ADRs)

Out of scope:
- code comments
- docstrings
- fenced code blocks
- generated API reference content

## Non-Encodable Normative Policy

The following constraints are normative and require human audit judgment.

1. Pre-output audit gate: do not publish final prose before lint and audit checks complete.
2. Conflict precedence: when rewrites conflict, preserve this order:
   1. technical correctness
   2. hard-blocker compliance
   3. document structure and modularity
   4. pedagogical clarity
   5. local elegance
3. Dependency-order review: section and paragraph order should follow prerequisite-before-consequence flow.
4. Reader-first ordering: purpose should appear before procedures, and interpretation should appear before implementation detail when possible.
5. Cross-document consistency: when auditing a document set, parallel documents should keep aligned heading conventions, section sequencing, and voice.

## Audit Workflow

1. Run hermeneia with the profile that matches the document audience and genre.
2. Review findings with evidence/confidence/rationale fields.
3. Manually assess the non-encodable policies listed above.
4. Produce a bounded findings report (maximum 15 findings).
5. Classify the document verdict using the severity model below.

## Finding Record Contract

Each finding must include:
- exact location (file + line, page + line, or quoted sentence)
- violated criterion (rule id or policy clause)
- concise explanation of reader cost
- concrete rewrite or structural correction
- frequency label: `isolated`, `recurring`, or `systemic`

Invalid findings:
- generic style advice without evidence
- opinions not linked to a criterion
- remediations without explicit rewrite/structure target

## Severity Model

- `critical`: systemic defect with high reader cost and blocker impact
- `high`: blocker defect in high-visibility sections or repeated pattern
- `medium`: clear readability cost, limited frequency or local scope
- `low`: secondary issue with minor comprehension impact

## Verdict Model

Classify each audited document as exactly one:
- `compliant`
- `mostly compliant`
- `non-compliant`
- `severely non-compliant`

Verdict justification must cite dominant evidence patterns, not isolated examples.

## Related References

- [Writing Quality Model](writing-quality-model.md): conceptual baseline
- [Sources and Further Reading](sources-and-further-reading.md): external sources that justify criteria
