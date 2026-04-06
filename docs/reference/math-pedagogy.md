# Mathematical Pedagogy

This file defines pedagogical requirements for all mathematical notes. These requirements operate at the level of sections and paragraphs, below structural requirements and above the sentence-level rules in `hard-rules.md`.

## Math Writing Audit Dimensions

Writing-quality dimensions for post-draft verification of mathematical notes.
These dimensions assess prose clarity, argumentative structure, and expositional
coherence — independent of mathematical correctness or note-governance concerns.

1. **Coherence** — logical flow between sentences, paragraphs, and sections;
   topic-stress progression; discourse connective structure.
2. **Redundancy** — cross-paragraph semantic overlap; duplicated explanations;
   content that can be consolidated without loss.
3. **Argumentative structure** — whether claims are supported, whether the
   argument follows a dependency-respecting order, whether each section
   advances the stated objective.
4. **Motivation** — whether each formal construct (definition, assumption,
   derivation) is preceded by a statement of purpose explaining what it
   controls or why it is needed.

These dimensions originate from the eight-dimension post-draft audit framework
used in mathematical research note production. The remaining four dimensions
(contract compliance, mathematical rigor, terminology, integration) are
governance concerns maintained in the note-production workflow.

---

## Section opening

Every section opens with three elements, in order:

1. The problem or question the section addresses
2. The approach or strategy
3. The rationale — why this approach, what failure it prevents or what mechanism it controls

Do not begin a section with a definition or a display equation. Begin with a plain-language statement of purpose.

---

## Assumption motivation

When stating a formal assumption or condition, explain its role before writing the formal statement. The motivation must answer: what mechanism does this assumption control, or what failure does it prevent?

Pattern:
- "To ensure uniqueness, assume …" — acceptable (purpose before assumption)
- "Assume …" — forbidden (assumption before purpose)
- "To …, impose …" — acceptable

---

## Proof placement

When a section contains a formal condition or result followed by a proof, the proof must come after the interpretive context. The correct ordering is:

1. Condition or result statement
2. Interpretive paragraph (what the condition means, what it controls)
3. Examples (e.g., $\tanh$)
4. Boundary cases (e.g., the linear network)
5. *Proof.*
6. $\square$

A proof placed immediately after a formal statement, before any interpretation, is a structural violation.

If a proof ends with $\square$, begin it with `*Proof.*` on the first line.

---

## Formula interpretation

Every non-trivial formula must be followed by an interpretive sentence naming the mathematical object, the operation, and the consequence. The interpretive sentence must appear in the body, not only in a callout.

Do not use content-free transitional phrases to introduce the interpretive sentence. Name the specific operation that produced the formula, or name the quantity the formula represents.

---

## Lead-in sentences for display equations

Every display equation must be preceded by a sentence that:
- states what the equation represents, or
- names the specific mathematical operation that produces it, or
- states its role in the argument

Forbidden lead-ins (content-free): "Therefore:", "Then:", "Hence:", "More explicitly:", "This gives:", "Equivalently:".

Required forms:
- "Differentiating the eigenbasis expansion with respect to the gain $g$ yields:"
- "Substituting the amplification-factor derivative into the bilinear form yields the componentwise expression:"
- "The asymptotic gain-decay rate satisfies:"

---

## Object introduction

Introduce new objects by role before notation. State what the object is used for, then give the definition.

When multiple objects must be introduced for a single computation step, state the collective purpose once and introduce all objects together in a single display block. Do not give each object its own paragraph and display equation.

Forbidden anti-pattern (three display blocks in a row with no stated motivation):
> "The dominant amplification factor is: [display]. The projected drive component satisfies: [display]. Substituting into the bound yields: [display]."

Required form:
> "To make the dependence on the regime parameter explicit, the dominant amplification factor $A_1(g) = g/(1 - g\lambda_1)$ and the projected drive $\xi_1 = \|\mathbf{u}\|\,\mathbf{v}_1^\ast\boldsymbol{\Sigma}^{(nI)}\mathbf{s}$ are substituted into the lower bound:"

---

## Mathematical typesetting

**Display equations.** Use `$$ … $$` blocks for all equations and derivations. No punctuation inside the display block. A display equation must be preceded by a lead-in sentence (see above).

**Inline math.** Use `$…$` for symbols and short expressions. Avoid inline math containing `=` or spanning multiple operators, except in the following permitted contexts:
- trivial equalities and identifiers: `$\lambda=0$`, `$j=k$`, `$g^\ast=g(\Delta^\ast)$`
- chained trivial equalities: `$\alpha_1 = \alpha_2 = 1/2$`
- parenthetical labels: `($d = 2$)`, `(embedding dimension $d > d_0$)`
- callout, list-item, and table-cell contexts where a display block would fragment the structure

**Prose paraphrase rules.** Do not replace a mathematical relation with prose. Do not use "times" or "multiplied by" for a product; use an explicit product in math. Do not use "of order …" for asymptotics; use `$\mathcal{O}(\cdot)$`. Do not write "converges to one" when `$\to 1$` is available.

**New notation.** Do not introduce notation for a trivial quantity unless the shorthand is used heavily and materially improves clarity.

---

## Sentence structure for mathematical prose

**Sentence length.** Split any sentence exceeding roughly 40 words or containing more than two clauses. A sentence that requires holding more than one subordinate clause in working memory before reaching the main verb is too long.

**Verb placement.** Place the main verb early. When a sentence contains an enumeration or parenthetical, place the verb before the enumeration.

**Paragraphs.** Use explicit logical connectors between sentences: causation (since, because, therefore, so), contrast (however, whereas, in contrast), elaboration (specifically, in particular), consequence (accordingly, as a result). A semicolon between two independent clauses must include a connector unless the clauses are strictly parallel statements of fact.

**Inline enumerations.** When a sentence contains two or more labeled items or three or more comma-separated clauses each containing a verb or multi-word argument, convert to a bulleted list with a lead-in sentence.

**Case distinctions.** When presenting distinct cases, use a bulleted list with a lead-in sentence. The semicolon-joined conditional pattern ("When X, result is Y; when Z, result is W") must be converted to a bulleted list.

---

## Emphasis

Use **bold** in running text to highlight key terms, mechanisms, or conclusions. Bold individual keywords or short noun phrases, not full sentences or clauses.

---

## Banned words in lead-ins and transitions

The following words and phrases are forbidden in lead-in sentences and transitions:

- Vague transitions: `clearly`, `obviously`, `naturally`, `of course`, `straightforward`, `it can be shown`, `it is easy to see`
- Content-free lead-ins: `more explicitly`, `equivalently`, `this gives`, `rewriting`, `therefore:`, `hence:`, `then:`, `note that`, `notice that`, `recall that`, `observe that`
- Prose paraphrases of math: "of order …", "times", "multiplied by", "given by" (use `$=$`), "converges to one" (use `$\to 1$`)
- Vague mechanism phrases: "in … ways", "in ways that …" — state the specific mechanism

---

## Qualitative claims

Every qualitative claim must be supported by a precise, quantitative argument: a bound, an estimate, a derivation, or a dominance argument against a well-defined baseline with explicit scaling factors. "Clearly", "obviously", and "it can be shown" are not support.

If a result is stated without proof, cite a specific block anchor in the source note.

---

## TODO markers

Preserve `==TODO==` markers when editing. When a question appears within `==…==` markers, propose an answer.
