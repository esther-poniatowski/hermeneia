# Writing Quality Model

This page defines the conceptual quality model used by hermeneia.
Accordingly, the model maps each rule family to a specific reader-comprehension constraint.
Therefore, read the page as a dependency chain: problem -> quality priorities -> reader expectations -> measurable signals -> operational use.

## Problem Framing

Technical and mathematical prose can become difficult to process when it hides action, weakens argument links, or delays the core claim.

Generic grammar tools mostly detect local form errors.
However, these tools usually do not evaluate discourse continuity, paragraph progression, structural ordering, or audience calibration.

Because this failure mode spans multiple scales, hermeneia organizes checks by layer rather than by isolated grammar patterns.

## Quality Priorities

Hermeneia evaluates prose with six priorities:

1. Directness: state the operative claim and mechanism without rhetorical detours.
2. Clarity: keep subject-action relations explicit and close.
3. Fluency: maintain predictable reader progression across sentences and sections.
4. Precision: avoid vague placeholders when arguments or operands should be explicit.
5. Structure: organize content by dependency order, not drafting chronology.
6. Audience fit: calibrate claims, terms, and notation to target readership.

These priorities map directly to rule families in [Rule Registry](rule-registry.md).

## Reader-Expectation Principles

- Topic control: sentence openings should anchor known context.
- Stress control: sentence endings should carry new, decision-relevant information.
- Transition clarity: consecutive sentences should expose logical links.
- Concept stability: one concept should keep a stable label unless meaning changes.
- Section signaling: headings and opening sentences should reveal purpose early.

These principles explain the intended reading path of the document, not only local sentence form.

## Readability Statistics

Readability metrics are supporting signals, not standalone quality proof:

- sentences per paragraph
- words per sentence
- verb density
- pronoun density
- passive-voice rate
- Flesch-Kincaid Grade Level
- Flesch Reading Ease
- Gunning-Fog index

Use these metrics as triage inputs after rule findings, not as a replacement for argument-level review.

Gunning-Fog formula:

$$
\text{Fog} = 0.4 \times \left(\frac{\#\text{words}}{\#\text{sentences}} + 100 \times \frac{\#\text{complex words}}{\#\text{words}}\right)
$$

## How To Use This Model

Move from concept to action in this order:

1. Inspect concrete checks in [Rule Registry](rule-registry.md).
2. Run and tune the tool with [Usage](usage.md) and [Configuration](configuration.md).
3. Apply human-audit constraints with [Prose Audit Protocol](prose-audit-protocol.md).
4. Consult external grounding in [Sources and Further Reading](sources-and-further-reading.md).
