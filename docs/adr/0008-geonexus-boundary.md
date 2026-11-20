# ADR 0008: Boundary between hermeneia and the geonexus checkers

- Status: Accepted
- Date: 2026-10-23
- Amended: 2026-11-02 by the decision of `geonexus` on [designation and typography](https://github.com/esther-poniatowski/geonexus/blob/584a14f134e7b6231eeae31518622439acf10d00/docs/_decisions/designation-and-typography.md): Onomasia, the designation tool, owns the checks of the terms bound by a glossary and of the symbols bound by a notation; hermeneia owns the checks of the form of a gloss, reads the term table of Onomasia, takes its inline regions from Merismos, the span library, moves its rules on link forms to Anagraphe, and reads its prose profile from a binding key of its own.

## Context

Three checkers test the form of a gloss: two geonexus checkers and the hermeneia rule `structure.field_form`. Similarly, the geonexus link checker and the hermeneia rule `reference.heading_link` both report links to heading slugs. Two checkers of one form can disagree, and a fix to one leaves the other unchanged.

## Decision

hermeneia owns sentence-level prose, meaning the wording and the form of every prose string in the files read by hermeneia. Conversely, geonexus implements no checker that could carry this concern.

A check carries a concern of hermeneia when it reads the wording or the form of a prose string (its capitalization, final punctuation, number of sentences or opening). A check stays with geonexus when it reads the structural data of the vault, such as a schema, a path, a link target or an identifier.

The boundary holds for the present state of both projects. A later decision may revise this boundary.

## Alternatives considered

1. **geonexus keeps the form checks of the fields declared by its schemas.** Rejected: three checkers would keep testing one form.
2. **hermeneia leaves structured fields to the checkers of each project.** Rejected: `structure.field_form` serves every project linted by hermeneia, whereas a geonexus checker serves one vault.

## Consequences

- Six kinds of finding move from geonexus to hermeneia, once the [tests missing from `structure.field_form`](../_audits/geonexus-boundary.md) are added.
- The moved kinds stay in the commit gate of geonexus only if that gate runs hermeneia under a baseline.
- Three groups of kinds have no owner yet (the terms bound by a glossary, the symbols bound by a notation file, and the fragments of a link).
