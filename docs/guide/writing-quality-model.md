# Writing Quality Model

This guide explains how hermeneia models writing quality.
The model links each rule family to a reader-facing effect, so findings stay tied to comprehension rather than isolated grammar form.
Use this page as the conceptual bridge between [Usage](usage.md) and [Rule Registry](rule-registry.md).

## Rationale

Technical and mathematical prose fails most often when readers cannot track the argument path.
That failure appears at several scales: sentence phrasing, paragraph progression, section ordering, and audience calibration.

Generic grammar tools mostly detect local form errors such as agreement and punctuation.
By contrast, hermeneia also checks discourse continuity, concept stability, structural dependency order, and pedagogical fit.
Because these failures interact across scales, hermeneia organizes checks by layered quality priorities.

## Quality Priorities and Rule Families

Hermeneia evaluates prose with six priorities:

1. Directness: state what acts, what changes, and why it matters.
2. Clarity: keep subject-action relations explicit and local.
3. Fluency: guide sentence-to-sentence and section-to-section movement.
4. Precision: replace vague placeholders with concrete references.
5. Structure: order content by logical dependency.
6. Audience fit: define terms, calibrate claims, and manage notation load.

These priorities map to concrete checks in [Rule Registry](rule-registry.md).

## Reader-Expectation Principles

The priorities above become operational through recurring reader expectations:

- Topic control: sentence openings should anchor known context.
- Stress control: sentence endings should carry new, decision-relevant information.
- Transition clarity: consecutive sentences should expose logical links.
- Concept stability: one concept should keep a stable label unless meaning changes.
- Section signaling: headings and opening sentences should reveal purpose early.

Together, these principles describe how a reader should move through the argument path.

## Supporting Metrics

Readability metrics are supporting signals, not standalone quality proof.
For metric definitions, formulas, and interpretation limits, see [Metrics](metrics.md).

## How To Use This Model

Apply the model in this order:

1. Inspect concrete checks in [Rule Registry](rule-registry.md).
2. Use [Metrics](metrics.md) to contextualize density and readability signals.
3. Run and tune the tool with [Usage](usage.md) and [Configuration](configuration.md).
4. Apply human-audit constraints with [Prose Audit Protocol](prose-audit-protocol.md).
5. Consult conceptual grounding in [Sources and Further Reading](sources-and-further-reading.md).
