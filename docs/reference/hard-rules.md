# Style Hard Rules

This file is the enforcement core. Every rule here is a **hard blocker**: text containing any violation must be revised before output. No exceptions at this tier. Fluency, conventional mathematical tone, and resemblance to textbook prose are not evidence of compliance — apply every check mechanically.

---

## Operative summary

Apply these ten rules at every sentence. The rest of this file specifies their application.

1. Use verbs, not process nouns.
2. State results directly, not the act of establishing them.
3. Make the mathematical object the grammatical subject.
4. Name the object before the symbol.
5. Expand compound modifiers into clauses.
6. Do not use imperative openings.
7. Do not use procedural link text.
8. Do not use bare pronouns after display equations.
9. Keep sections and paragraphs in dependency order.
10. Do not return text before the audit and lint passes complete.

## Hard blockers

The following patterns are forbidden in all prose outside code blocks. If any is present, revise before output.

### B1 — Nominalization

Any noun derived from a verb where the verb form is shorter or more direct is a violation.

Scope: nouns ending in `-tion`, `-ment`, `-ness`, `-ity`, `-ence`, `-ance`, `-al`, `-ing` when used as a process noun in subject or object position.

Permitted exceptions — none at this tier. The following are the only permitted nominalizations anywhere in the document:
- `existence` and `uniqueness` / `unicity` when naming the property under investigation (e.g., "proves existence of a solution")
- Named technical quantities defined with `:=` and used in five or more distinct sentences in the same note (e.g., "amplification selectivity", "drive selectivity")

All other nominalization rewrites are mandatory. Common cases:

| Violation | Rewrite |
|---|---|
| "the derivation of $X$ shows" | "deriving $X$ shows" |
| "the expansion in the eigenbasis leads to the separation of" | "expanding in the eigenbasis separates" |
| "the establishment of a condition guarantees" | "a condition ensures that" |
| "the modulation of gain" | "the transfer derivative controls gain" or "gain modulates" |
| "stimulus-dependent kernel variation" | "how the kernel varies with the stimulus" |
| "the imposition of the constraint ensures the uniqueness of" | "imposing the constraint ensures uniqueness" |
| "treatments of heterogeneous networks" | "theory for heterogeneous networks" |
| "differential amplification modulates" | "the amplification factors modulate" |
| "spectral reshaping produces" | "the spectrum is reshaped by" or rewrite with a named agent |

**Subject-position trap.** Process nominalizations used as sentence subjects are not exempt (e.g., "Spectral reshaping produces …" → rewrite so the mathematical object is the subject).

### B2 — Abstract framing

Any sentence that describes the act of establishing a result, instead of stating the result, is a violation.

Forbidden literal strings (search before output):

- `the role of`
- `the nature of`
- `the act of`
- `it can be shown`
- `it is possible to show`
- `plays a role in`
- `is responsible for`
- `serves to`
- `is involved in`

Also forbidden: vague procedural nominalizations that name a procedure without its operands.

| Violation | Rewrite |
|---|---|
| "the role of commutativity in determining whether" | "commutativity determines whether" |
| "mechanistic attribution" | "attributing each type to specific gain and projection mechanisms" |
| "decoder accessibility" | "which decoder classes can detect each type" |
| "mode-by-mode independence" | "each eigenmode contributes to the kernel independently through a scalar cross-gain factor" |
| "Gram-matrix coupling" | "the Gram matrix couples distinct eigenmodes through off-diagonal entries" |

Every noun phrase referring to a process, comparison, or relation must name its arguments explicitly. Do not leave operands implicit.

### B3 — Imperative mathematical openings

Sentences beginning with the following words are forbidden:

`Define`, `Let`, `Assume`, `Write`, `Set`, `Denote`

Exception: `Consider` is permitted when it introduces a scenario, specialization, or example.

Rewrites:
- "Define $X$ as …" → "The $X$ is defined as …" or introduce via `:=` in a display equation
- "Let $X$ be …" → "The $X$ is …" or introduce via `:=`
- "Assume that …" → "To [purpose], assume that …" or "To [purpose], impose …"

### B4 — Bare symbols

Every symbol appearing after a preposition, in a qualifier, in a condition, or in a monotonicity statement must be preceded by its object name.

| Violation | Rewrite |
|---|---|
| "for all $p$" | "for all populations $p$" |
| "at fixed $g$" | "at fixed gain $g$" |
| "on $\Theta$" | "on the stimulus space $\Theta$" |
| "across $\Theta$" | "across the stimulus space $\Theta$" |
| "a bimodal $\phi'$" | "a bimodal transfer derivative $\phi'$" |
| "indexed by $g^\ast$" | "indexed by the gain $g^\ast$" |

Exception: if the symbol was named in the immediately preceding clause and repeating the name would produce an awkward reading, the bare symbol is permitted for that single occurrence only.

### B5 — Procedural link text

Link text that names a note, container, analysis, specialization, or derivation is forbidden. Link text must describe a result, object, or mathematical property.

| Violation | Rewrite |
|---|---|
| `[the normality specialization](…)` | `[normal overlaps yield independent mode contributions](…)` |
| `[resolvent amplification note](…)` | `[amplification factors](…)` |
| `[the five-factor decomposition note](…)` | `[the five-factor output decomposition](…)` |
| `[the non-normal coupling analysis](…)` | `[non-normal overlaps couple eigenmodes through the Gram matrix](…)` |

This rule applies to every link in the document, including links carried over from earlier drafts.

### B6 — Bare pronoun after display

A sentence beginning with `It`, `This`, `They`, or `These` immediately after a `$$…$$` display equation, without a descriptive noun phrase, is a violation.

| Violation | Rewrite |
|---|---|
| "It follows that …" (after display) | "The bound implies that …" |
| "This gives …" (after display) | "This ratio …" or "The expression …" |

### B7 — Heading-slug links

Cross-references using heading-slug fragments (`#heading-name`) are forbidden. Use block anchors (`#^anchor-name`) only.

### B8 — Punctuation inside display equations

Periods, commas, and all other punctuation marks inside `$$…$$` blocks are forbidden. Place punctuation in prose after the display block when needed.

---

## Mandatory rewrite operators

Apply these five operators mechanically during generation, not during post-hoc audit. Before placing each noun or modifier, test whether an operator applies and apply it before continuing.

### Operator 1 — Verb-first

When reaching for a noun ending in `-tion`, `-ment`, `-ity`, etc.: stop, identify the corresponding verb, and use the verb form instead.

Pattern: `[process noun] + [weak verb]` → `[corresponding verb] + [object]`

### Operator 2 — Concrete subject

When a sentence makes the note, section, or analysis the grammatical subject: stop and rewrite so that the mathematical object or result is the subject and the verb names the mathematical operation.

Pattern: "this section derives the factorization of $X$" → "the ratio $X$ factorizes into …"

This operator applies with full force inside `[!QUOTE] Contributions` bullets and `[!TIP] Roadmap` items. Every contribution bullet must take the form: **[mathematical object] + [active verb] + [result]**. The note is never the grammatical subject of a contribution bullet.

### Operator 3 — Clause expansion

When reaching for a hyphenated pre-nominal modifier that encodes a prepositional or clausal relationship (`-dependent`, `-determined`, `-weighted`, `-driven`, `-modulated`): expand to a clause or prepositional phrase.

Pattern: `[X]-dependent [noun]` → `[noun] that depends on [X]`

Exception: a compound is permitted if it is defined with `:=` in the current note and appears in five or more distinct sentences.

### Operator 4 — Named object

Before placing any symbol in a qualifier, condition, preposition, or monotonicity context: insert the object name immediately before the symbol.

### Operator 5 — Result link

Before finalizing any Markdown link: verify that the link text names a result or object, not a container note, procedure, or analysis. Rewrite if it names a procedure.

---

## Compound-modifier rule

Any pre-nominal compound modifier that encodes a prepositional or clausal relationship must be expanded, without exception at this tier. This includes `-dependent`, `-determined`, `-driven`, `-weighted`, `-modulated`, and any stacked modifier sequence of two or more pre-nominal terms.

---

## Case-scaffolding rule

"The … case" as a noun phrase, and "In the … case" as a sentence opener, are forbidden. Use the prepositional form:

| Violation | Rewrite |
|---|---|
| "in the single-population case" | "for a single population" |
| "the commutative case" | "with commutative overlaps" |
| "absent from the non-normal case" | "absent with non-normal overlaps" |

---

## Forbidden strings — mechanical search before output

Search the final text for each string below outside code blocks. Any match requires revision.

```
the role of
the nature of
the act of
it can be shown
it is possible to show
plays a role in
is responsible for
serves to
is involved in
In the ... case
the ... case
Define
Let
Assume
Write
Set
Denote
Note that
Observe that
Recall that
More explicitly
Equivalently
This gives
Therefore:
Hence:
Then:
in ... ways
```

---

## Conflict resolution

When two rules produce tension, preserve in this order:

1. Mathematical correctness
2. Hard blockers (this file)
3. Note modularity (`note-template.md`)
4. Pedagogical clarity (`math-pedagogy.md`)
5. Local elegance
