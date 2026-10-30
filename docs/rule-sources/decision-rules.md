# Decision rules

These rules govern the production of a research note. They were transferred from gnomon, and await the decision on which rule sets migrate into the [rule specifications](../adr/0007-rule-specifications-in-yaml.md).

> [!TIP] Single source of truth
> This note holds the **authoritative definition** of each decision rule that governs the production of a note. A note contract, which specifies a note before it is drafted, and an audit checklist **instantiate** or **verify** these rules by their anchors, and never redefine them.

## Overview

**Priority stratification**: The rule system is organized by the aspect of note production each rule governs. The same rule may have different enforcement weight depending on the note type and workflow stage.

| Layer             | Governs                                                                                                                                                          | Priority | Enforcement                                                                        |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | ---------------------------------------------------------------------------------- |
| **Epistemic**     | *What is claimed* (what must be proven, which content may enter, why new objects are introduced, which proof route is allowed, which premises are legitimate...) | Highest  | Broad generation-time criteria held in working memory during planning and drafting |
| **Argumentative** | *How the claim is articulated* (logical chaining, functional role separation, exposition of formal content, sequencing, transitions...)                          | Medium   | Narrower operators enforced at planning time and audit                             |
| **Stylistic**     | *How the result is expressed* (prose register, paragraph construction, notation formatting, terminological coherence...)                                         | Lowest   | Writing principles and lints at draft time                                         |

**Rule structure.** Each decision rule specifies simultaneously:

- a **normative constraint**: the quality criterion it enforces,
- the **checks** by which any workflow stage may verify compliance.

Post-hoc routing protocols are external to the rule system and belong to procedural workflows (e.g. divergence resolution, contract amendment).

## Epistemic layer

### Scope admissibility ^scope-admissibility

**Failure prevented.** Content is individually correct but lies outside the project's declared scope — because each extension appears as a natural next step.

**Scope.** Notes, sections, and derivations against the scope that the project declares.

**Normative constraint.** Every note, section, or derivation must serve an established contractual need, operate within the project's declared domains and generality ceilings, and avoid forbidden or deferred content. The argument that a development is "natural", "illuminating", or "closely related" is not an admissibility criterion.

**Checks.** All the following must hold:

1. Is it required to establish a result in an active contract?
2. Does the result lie on a directed path to the main thesis in the dependency graph of the project, with the contract naming the immediate downstream node?
3. Is its mathematical domain admissible (or exception-authorized by the contract)?
4. Is its generality within the declared ceiling (or exception-authorized)?
5. Is it free of forbidden or deferred objects?
6. Is it free of forbidden or deferred questions?

**Drift taxonomy.** Three named drift types, each locally justified but globally harmful:

- **Lateral drift**: pursuing a mathematically adjacent object that was never part of the argument
- **Depth overrun**: developing a tool or construction beyond the level of generality the project needs
- **Premature synthesis**: drawing conclusions that require results not yet established

**Exclusion tiers.** Each excluded item in the project scope is classified:

| Tier | Meaning | Contract override |
| --- | --- | --- |
| **Admissible by default** | Within declared scope; no justification needed | N/A |
| **Exception-requiring** | Outside default scope but legitimately needed by some downstream notes | Yes, with justification |
| **Deferred** | Potentially valuable but not needed now | No |
| **Forbidden** | Must never be introduced regardless of local plausibility | No |

---

### Objective unity ^atomicity-criterion

**Failure prevented.** A single note answers multiple questions, producing a sprawling document that mixes independent inferential objectives.

**Scope.** Whole notes and their major sections.

**Normative constraint.** A note must be organized around a single inferential objective. Multiple outputs are legitimate when all serve the same question; independent objectives — outputs whose consumers and dependency paths diverge — must not coexist in the same note.

**Checks.** A note is atomic if it passes both tests:

- **Output declaration.** Does each major section name its local output and its immediate downstream consumer (a later section or an external consumer named in the contract)?

- **Path alignment.** Does each section's output lie on the dependency path to the main result (or is it a declared companion output in the same result family)? Could any section's output be imported independently by a consumer that would not need the main result?

**Atomic ≠ minimal.**

|Term|Meaning|
|---|---|
|**Minimal**|contains the least material strictly necessary|
|**Atomic**|organized around one local inferential objective|

A note may legitimately gather several outputs that reinforce each other (a theorem and its natural variants, a proof and a sharp limitation, a result and its immediate interpretation) provided all parts answer the same local question.

_Example: variant theorems._ A note with the objective "Determine under which assumptions the decomposition theorem holds, and how the statement changes between strong and weak equivariance" may legitimately contain the theorem in both forms, a comparison identifying the exact gain and loss, and an interpretation of what this difference means operationally. It would become non-atomic if it also added an empirical diagnostic construction, a literature comparison with three alternative frameworks, or a speculative discussion of learning dynamics.

---

### Local necessity ^admissibility-rule

**Failure prevented.** The note derives on technically sophisticated but tangential content — sections that "complete the thought", paragraphs that feel continuous with the material but serve no inferential role.

**Scope.** Content units (sections, paragraphs, remarks, examples, asides) inside an already atomic note. The [interpretive sub-criterion](#^bounded-interpretive-radius) is built into the Intelligibility condition; the [functional motivation rule](#^functional-motivation) specializes the Setup condition for major constructs.

**Normative constraint.** Every content unit must contribute to establishing, delimiting, or making intelligible the note's target result. For emergent content not part of the planned target family, contract authorization is additionally required.

**Checks.** A content unit is admissible if it passes the following tests:

- **Admissibility conditions.** Does the content unit satisfy at least one of the following?

  1. **Establishment.** Does it state or derive the target result or one of its necessary intermediate steps?
  2. **Setup.** Does it introduce an object, assumption, or distinction used in the note's argument? When the item qualifies as a **major construct**, does it additionally satisfy the [functional motivation rule](#^functional-motivation)?
  3. **Discrimination.** Does it compare cases, regimes, or formulations to determine the scope, applicability, or meaning of the target result?
  4. **Boundary.** Does it record a failure mode or boundary case of the target result?
  5. **Intelligibility.** Does it provide an interpretation, example, or illustration that makes the result operationally intelligible, or that a downstream consumer requires?

  **Interpretive sub-criterion.** Does the interpretive passage answer one of the following, without introducing new concepts, launching cross-module synthesis, or developing commentary not required for reuse? ^bounded-interpretive-radius
  - what structural mechanism the result isolates?
  - what distinction between cases it reveals?
  - what concrete downstream use it enables?
  - what failure would occur if a key assumption were dropped?

- **Contract-authorization test.** For content not part of the planned target family: does it appear in the contracted section skeleton, the target result family, or the declared deliverables? ^forbid-free-expansion

- **Primary-label test.** Does the unit carry exactly one **primary admissibility label** from the five conditions? A secondary label is permitted only when the unit genuinely serves two roles.

- **Objective-preservation test.** After removing a candidate content unit:
  1. Does the note still fully answer its declared local objective?
  2. Does the reader lose a distinction necessary to know what exactly was proved?
  3. Does a downstream note lose information required for correct reuse?

**Coverage assessment.**

| Content type | Admitted by | Excluded when |
| --- | --- | --- |
| Derivation steps, intermediate results | Establishment | the step is not on the path to the target result |
| Case distinctions within the proof | Establishment | the cases are not exhaustive or not needed for the target |
| Definitions, assumptions, setup | Setup | the object is not used in the note's argument |
| Motivation paragraphs (obstacle, missing info) | Setup | the motivation is generic rather than tied to a specific obstacle |
| Regime comparisons, alternative approaches | Discrimination | the comparison does not sharpen the target result's scope or meaning |
| Relevant comparisons (what changes between cases) | Discrimination | the comparison opens an independent research question |
| Failure modes, boundary cases | Boundary | the failure mode concerns a different result or a speculative extension |
| Interpretations (mechanistic, operational) | Intelligibility | the interpretation fails the [interpretive sub-criterion](#^bounded-interpretive-radius) |
| Examples, worked instances | Intelligibility | the example illustrates a different result or an unrelated phenomenon |
| Illustrations, schematic diagrams | Intelligibility | the illustration is decorative rather than discriminative |

---

### Functional motivation ^functional-motivation

**Failure prevented.** Concepts are introduced because they are topically proximate — motivation is rhetorical ("To provide intuition, introduce...", "This motivates the following concept...") rather than as a functional justification.

**Scope.** Major constructs: objects, definitions, constructions, or distinctions that appear in the main result family, in the proof strategy, or in more than one derivation step. Minor notational abbreviations are exempt.

**Normative constraint.** Every major construct must bridge a specific obstacle to a specific later step. Generic phrases ("it is natural to consider…", "to gain intuition…") are not functional motivation.

**Checks.** An introduction is functionally motivated if all the following can be answered:

- What obstacle blocks progress?
- What information are the current objects missing?
- What is the proposed construction?
- What is the first step that cannot proceed without this construct?
- What information does this object make visible that previous objects hid?
- What nearby alternative objects were available, and why are they less appropriate?

---

### Proof strategies ^proof-strategies

**Failure prevented.** Proofs are initiated without committing to a route, producing derivations that are technically dense but never identify the structural reason the result holds.

**Scope.** Non-trivial proofs and their route commitment and explanatory target.

**Normative constraint.** Every non-trivial proof must commit to an explicit route and identify the structural reason the result holds — a mathematical property whose absence would make the result fail.

**Checks.** A proof satisfies this rule if all the following hold:

- **Schema completeness.** Does the proof strategy satisfy all fields? ^proof-strategy-schema
  - **Proof family**: the primary family from the taxonomy below
  - **Objective**: what must be shown exactly
  - **Obstacle**: what makes the proof non-trivial
  - **Route**: the chosen proof path
  - **Key idea**: the central construction or insight
  - **Essential assumptions**: which hypotheses are load-bearing
  - **Why this route over nearby alternatives**: justification for the chosen path
  - **Explanatory target**: one sentence of the form _"The derivation reveals that [result] holds because [structural reason]."_ The structural reason must name a mathematical property whose absence would make the result fail — not a verification procedure ("verify by direct computation," "enumerate all cases," "check that both sides are equal"). ^explanatory-target

- **Constructive-direction test.** Does the derivation build the decisive mechanism forward from the problem rather than stating the answer and verifying it after the fact? The expected forward direction depends on the proof family:
  - **Constructive families** (synthesis, reduction, invariant propagation, case partition, induction, classification): constructing the answer from premises or constraints
  - **Contradiction / obstruction and extremal / variational**: building forward toward the decisive obstruction or certificate

  When backward verification is genuinely necessary (e.g., checking that a constructed solution satisfies remaining constraints), it must be recognizable as a post-construction verification step, not as the primary derivation route.

- **Mechanism correspondence.** Does the structural reason named in the explanatory target appear in the decisive inferential step, not only in retrospective commentary?

- **Counterfactual load-bearing test.** Does the derivation make clear that without the named structural property, the route would fail or change?

**Proof-family taxonomy.** The route must be classified using one primary family:

- **Constructive synthesis**: build the target object directly from constraints or requirements
- **Reduction / normal form**: transform the problem to an equivalent representation where the mechanism is explicit
- **Invariant propagation**: identify a structural quantity or property and propagate it through the derivation
- **Case partition**: split the domain into exhaustive, mutually exclusive branches and prove each branch
- **Contradiction / obstruction**: assume the target fails and isolate an impossible or excluded structure
- **Extremal / variational**: characterize the answer through optimization, comparison, or extremal certificates
- **Induction / recursion**: establish a base and propagate the claim through recursive or hierarchical structure
- **Classification / representation**: show that every admissible object has a specified form, then read the result from that form

---

### Premise legitimacy ^premise-legitimacy

**Failure prevented.** Premises are used implicitly (not declared) or without justification, or the proof rederives material already established elsewhere to produce self-contained documents.

**Scope.** Premises used in the note's argument, and imported background from elsewhere in the vault.

**Normative constraint.** Every non-trivial premise must be either proved locally or declared as an import or explicit assumption. Background already established elsewhere must not be rederived.

**Checks.** The note satisfies premise legitimacy if all the following tests pass:

- **Provenance test.** Is the premise either:
  - proved locally within the note (a derivation step, a lemma, a construction), or
  - declared as an import (typed import from a source note) or an explicit assumption (stated in `[!WARNING] Applicability` or the assumptions section)?

- **Non-trivial premise threshold.** Is the premise non-trivial? It counts as non-trivial if at least one of the following holds (a mere direct substitution, one-line rearrangement, restatement of a hypothesis, or symbol expansion does not meet this threshold):
  1. It is imported from another note or would require citation if stated independently.
  2. It asserts a substantive property not obtained by one-step substitution or local symbol unpacking.
  3. It compresses more than one elementary algebraic or logical step.
  4. Removing it would force a separate lemma, sub-proof, or explicit appeal to a prior result.

- **Background-restatement test.** Is each restated background item justified by one of:
  1. Genuine local ambiguity — the reader cannot resolve the expression or assumption from the surrounding context or from the linked source?
  2. Immediate readability — the next proof step uses the background and would be unreadable without an inline recall?
  3. Local specialization — the imported result needs a one-line adaptation (e.g., substituting specific values)?

  The threshold for genuine ambiguity may be adjusted by the [audience calibration](#^audience-calibration) parameter.

- **Symbol-restatement test.** For each imported expression: does the current step decompose the expression and operate on a specific constituent? If not, referencing the expression as a whole suffices — individual symbol definitions are not needed.

---

### Non-redundancy ^non-redundancy

**Failure prevented.** The same contribution is restated in multiple forms — a display equation followed by a prose paraphrase, a setup paragraph and a concluding takeaway making the same point, two examples illustrating the same distinction.

**Scope.** Pairwise or small-group overlap between content units within a note.

**Normative constraint.** When one unit can absorb the substantive contribution of another without loss of function, the weaker must be merged or removed.

**Checks.** Two units are redundant if the following sequence confirms overlap:

- **Candidate-overlap identification.** Do the two units:
  - cite the same output or distinction?
  - carry the same primary label and address the same target?
  - paraphrase the same content across two representation types?

  At least one must hold for the pair to be a candidate.

- **Absorption test.** After preserving all unique content: can one unit absorb the other without loss of function?

**Tie-break order.** When overlap is confirmed, the higher-ranked unit is kept unless the lower contributes content not already supplied: Claim > Derivation > Interpretation > Example. A claim is never removed if it is the only statement of the result; a derivation is never removed if it is the only justification.

---

### Evidence-to-claim proportionality ^evidence-claim-proportionality

**Failure prevented.** Interpretive, comparative, or generalization claims are stated with the confidence of proven theorems while the supporting argument is incomplete, selective, or absent.

**Scope.** Non-formal claims (interpretive, comparative, conceptual) in notes where the evidence relation is argumentative rather than deductive.

**Normative constraint.** Every non-formal claim must not assert more than what the locally supplied evidence establishes — in scope, confidence, or generality.

**Checks.** A non-formal claim is proportionate only if the applicable test is satisfied:

- **Comparative claim:** Does it name its comparison dimensions, supply evidence on each, and state what would change the comparison?
- **Interpretive claim:** Is it anchored to a specific formal result without exceeding its assumptions and conclusions?
- **Generalization claim:** Does it identify the assumptions required for the extension and state whether they have been verified or are conjectural?
- **Any claim stated as established:** Is the supporting argument complete and non-selective?

---

## Argumentative layer

### Deductive continuity ^deductive-articulation

**Failure prevented.** Sections are organized by topic, discovery order, or narrative convenience, producing an "essay disguised as a proof" where major steps lack explicit logical dependence.

**Scope.** Adjacent content units at every argument level: section-to-section, lemma-to-corollary, proof-step-to-proof-step.

**Normative constraint.** Every section after the first must use a specific output of a preceding section as input. The section skeleton's decomposition must mirror the problem's natural structure, not the discovery order or a generic template.

**Checks.** The argument is deductively continuous if it passes both tests:

- **Dependency test.** Can each section after the first name a specific output from a preceding section that it uses as input?

- **Problem-structure correspondence.** Does the section skeleton name one primary **decomposition pattern** from the following admissible list, rather than organizing by topic, discovery order, or a generic template?
  - **Dependency chain**: each section proves a prerequisite used by the next
  - **Case partition**: sections follow an exhaustive, mutually exclusive branch structure
  - **Construction pipeline**: sections define an object, establish its properties, and assemble the main result
  - **Reduction / transfer**: sections move to an auxiliary representation, solve there, then transfer back
  - **Parameter or hypothesis sweep**: sections vary one degree of freedom while holding the objective fixed
  - **Boundary / failure split**: sections establish the main result, then isolate the limiting regime or failure mode

---

### Functional integrity ^functional-integrity

^claim-derivation-interpretation-separation

**Failure prevented.** Certain passages mix roles: a result statement that hides proof work, a derivation paragraph that drifts into commentary, an interpretation that merely restates the preceding claim.

**Scope.** Argumentative roles (claim, derivation, interpretation) and their functional identity within each content unit.

**Normative constraint.** Each content unit must perform one dominant role — claim, derivation, or interpretation — without usurping another. Interpretation may be placed adjacent to a milestone when it clarifies the mechanism, case distinction, or consequence just established.

**Checks.** A content unit has functional integrity if it passes both tests:

- **Role-marking test.** Does the unit carry one dominant role (`claim`, `derivation`, or `interpretation`)? Are roles merged only when the local integration exception applies and the reason is stated explicitly?

- **Forbidden-pattern test.** Does the unit exhibit:
  - **Proof usurpation**: interpretation that performs derivation work?
  - **Restatement**: interpretation that merely paraphrases the claim or replays the proof without adding content?
  - **Scope expansion**: interpretation that introduces broader objectives or cross-module synthesis not established by the anchoring formal object?
  - **Positional disruption**: interpretation inserted between two formally adjacent steps in a way that severs the derivational thread?

**Role definitions.**

1. **Claim units** state what is true under which assumptions. They must not perform proof work or compress a derivation step into an asserted conclusion.
2. **Derivation units** justify why the claim follows. They may include brief signposts for branch selection; they must not carry interpretation beyond what the next inferential move requires.
3. **Interpretation units** make a result operationally intelligible. They must not substitute for the proof role, restate the claim without added content, or open a new branch.

---

### Mathematical exposition ^mathematical-exposition

**Failure prevented.** Derivations are formally correct but expositionally opaque: steps that skip intermediate reasoning, display equations with no prose framing, assumptions used silently.

**Scope.** Interface between formal notation and natural language: how displayed equations, formal objects, and proof steps are embedded in a logical narrative.

**Normative constraint.** Every formal object — display equation, proof step, assumption — must be embedded in a prose narrative that makes its role, meaning, and connection to neighboring steps explicit.

**Checks.** A draft satisfies mathematical exposition if all the following hold:

- **Explicitness.** Are non-immediate steps written explicitly enough to be followed? A step is non-immediate when it:
  - compresses more than one elementary operation
  - invokes a non-obvious property
  - requires an unstated intermediate inference
- **Display framing.** Is every displayed equation preceded by a lead-in sentence stating what it represents, what operation produces it, or what role it plays? Is every non-trivial displayed equation followed by an interpretive sentence?
- **Assumption surfacing.** Are assumptions explicit at the point of use? When a formal condition is stated, is its role explained before the formal statement?
- **Failure-mode recording.** When a result depends strongly on its assumptions, is at least one failure mode recorded?

---

### Intra-unit ordering ^intra-unit-ordering

**Failure prevented.** Ideas are presented in an order that impairs their understanding: a formal proof before a qualitative interpretation, a technical step before the question it answers, an object before its role is motivated.

**Scope.** Ordering of ideas within a section or passage.

**Normative constraint.** Ideas within a section must appear in an order that reflects their inferential and explanatory dependencies — no idea before the premise it requires, no interpretation before the derivation it interprets.

**Checks.** A section's ordering is admissible if:

- **Pattern commitment.** Does the section follow a declared ordering pattern? The default derivation pattern is:
  1. Purpose and problem statement
  2. Setup and definitions
  3. General derivation
  4. Result statement
  5. Interpretation
  6. Specializations and examples
  7. Failure modes and boundary cases

- **Hard constraints** (apply regardless of note type and pattern):
  - Does every specialization follow the general result it instantiates?
  - Does every interpretation follow the derivation it interprets (unless the note type explicitly supports result-first exposition)?
  - When a note treats multiple cases, do the shared setup and general result precede all case-specific sections?

**Admissible variations** by note type:

- **Constructive notes** may introduce the object before the theorem when the construction motivates it.
- **Obstacle-driven sections** may open with the obstacle before the claim.
- **Expository notes** may state the result before the derivation, or open with interpretation to frame the question.
- **Case-partition sections** may interleave claim-derivation-interpretation within each case, provided the shared framework precedes all cases.

---

### Transition quality ^transition-quality

**Failure prevented.** Passages are locally coherent but their argumentative connections are never made explicit — the reader cannot determine what was just established, what gap remains, or why the next move follows.

**Scope.** Move boundaries at every granularity level. A "move" is any inferential step whose output is consumed by the next step.

**Normative constraint.** At every move boundary, the prose must make the argumentative connection between the preceding step and the next step recoverable by the reader — what was established, what gap remains, and why the next step follows.

**Checks.** At every move boundary, can the reader answer three questions from the prose?

1. **What was just established?** Is the preceding move's output identifiable?
2. **What gap remains?** Is the question the next move addresses stated or clearly implied?
3. **Why does the next move follow?** Is the connection between the preceding output and the next move's objective legible?

A transition need not answer all three with dedicated sentences — a well-constructed lead-in can address all three.

---

### Interpretive integration ^interpretive-integration

**Failure prevented.** Derivations are not *locally* attached to an interpretation — meaning is deferred to a terminal block or omitted entirely, leaving the reader to reconstruct structural significance post hoc.

**Scope.** Derivational milestones and their accompanying interpretive units.

**Normative constraint.** Every significant derivational milestone must be accompanied by a locally proximate interpretive unit. The admissible content is governed by [functional integrity's local integration clause](#^functional-integrity).

**Checks.** A milestone is adequately accompanied if:

- **Milestone significance.** Does the milestone produce a result, resolve a case distinction, or complete a construction that a downstream consumer will reuse?
- **Proximity.** Is the interpretive unit locally proximate to the milestone it accompanies?
- **Global-deferral test.** If interpretation is deferred to a terminal section:
  - Does the note type or contract explicitly designate a terminal interpretive section and identify which milestones it covers?
  - Are the derivational steps sufficiently atomic that no individual milestone produces a result whose structural meaning is required to follow subsequent steps?
  - Does the terminal section map each interpretive unit to its specific milestone anchor?

---

### Audience calibration ^audience-calibration

**Failure prevented.** The tone defaults to either excessive compression, verbose technical or academic writing style, or redundant pedagogical expansion, instead of adjusting to a declared audience.

**Scope.** Compression level and implicit-knowledge threshold, conditioning the thresholds of several other rules.

**Normative constraint.** Exposition must be calibrated to the declared audience: no assumed knowledge beyond the declared background, no redundant explication, and a consistent compression level.

**Checks.** A violation occurs when any of the following hold:

- Does the draft assume knowledge outside the declared assumed background without explicit import or recall?
- Does it restate material the declared audience can be assumed to know, without justification by local ambiguity or readability?
- Does it compress steps the audience cannot reconstruct, or expand steps the audience can perform?

**Parameter fields.** Audience calibration is specified through four fields:

- **Assumed background**: what the intended reader is assumed to know
- **Implicit-knowledge threshold**: what can remain implicit without restatement or recall
- **Recall threshold**: what may require one-line recall but not full development
- **Compression level**: what degree of compression is acceptable (e.g., "research-level" vs. "pedagogical")

---

## Stylistic layer

### Writing principles ^writing-principles

**Failure prevented.** Prose employs uneven register, heavy or indirect sentence construction, and paragraph boundaries that do not correspond to argumentative shifts.

**Scope.** Expression-level choices that apply uniformly to all prose.

**Normative constraint.** All prose must be stylistically controlled: register, sentence form, and paragraph structure must serve readability and argumentative clarity, not default to the model's habitual patterns.

**Checks.** Prose satisfies this rule if all the following hold:

- **Register and tone**: Is the prose register consistent and appropriate to the note type? Are there uneven shifts between formal and informal registers?
- **Sentence construction**: Are sentences well-formed and grammatically direct? Does the main verb appear early? Are qualifiers and enumerations attached after the verb?
- **Paragraph construction**: Does each paragraph advance one point? Do explicit logical connectors link sentences? Do paragraph boundaries correspond to shifts in the argument?

---

### Mathematical display ^mathematical-display

**Failure prevented.** The argument uses conflicting notation conventions, embeds complex expressions inline, introduces unnecessary symbols, or places punctuation inside display blocks.

**Scope.** Visual and formatting conventions for mathematical notation.

**Normative constraint.** Mathematical notation must follow uniform formatting conventions — consistent symbol usage, appropriate display/inline choices, no unnecessary notation.

**Checks.** A note's notation satisfies this rule if all the following hold:

- Do **display equations** use `$$ … $$` blocks with no punctuation inside the display block?
- Is **inline math** restricted to symbols and short expressions? Is inline math containing `=` or spanning multiple operators limited to permitted contexts (trivial equalities, parenthetical labels, callout/list/table contexts)?
- Is **notation consistent** within the note — the same object denoted by the same symbol throughout, related objects using related notation?
- Is **new notation** introduced only when the shorthand is used heavily and materially improves clarity?

---

### Terminology ^terminology

**Failure prevented.** The argument silently introduces multiple names for the same object, uses overloaded symbols without disambiguation, or denotes related objects with unrelated notation.

**Scope.** Terms and notation within a note and across notes in a module.

**Normative constraint.** Terms and notation must be stable within a note and coherent across a module. Overloaded symbols must be disambiguated; related objects must use related notation.

**Checks.** Two dimensions, either of which can fail independently:

- **Notational stability:**
  - **Intra-note**: Does any object silently acquire multiple symbols? If a symbol change is necessary, is the reassignment explicit?
  - **Inter-note**: Does notation align across notes within the module, or is a justified local override declared? The authoritative source is the notation of the project, under the [decision on terminology, audience and project specifications of gnomon](https://github.com/esther-poniatowski/gnomon/blob/main/docs/adr/terminology-audience-project-specifications.md).
  - **Disambiguation**: When a symbol is overloaded, is the intended sense marked at the point of use?
  - **Semantic lineage**: Do related objects (e.g., a matrix and its entries) use related symbols?

- **Terminological stability:**
  - **Intra-note**: Is the same concept referred to by the same term throughout? Is stylistic variation avoided unless terms are explicitly defined as synonymous?
  - **Inter-note**: Do terms for the same concept align across the module? Are departures from convention declared?

---

## Rule interactions and separation of concerns

### Admissibility hierarchy

| Rule | Scope | Test | Independence example |
| --- | --- | --- | --- |
| [Scope admissibility](#^scope-admissibility) | Project-level | Is the note's objective admissible within the project? | An atomic, locally necessary note can pursue an inadmissible objective |
| [Objective unity](#^atomicity-criterion) | Note-level | Does the note pursue one inferential objective? | A unit-level admissible paragraph can belong to a non-atomic note |
| [Local necessity](#^admissibility-rule) | Unit-level | Is each content unit necessary for that objective? | An atomic note can contain unnecessary padding |
| [Functional motivation](#^functional-motivation) | Unit-level (major constructs) | Does the introduced major construct satisfy the obstacle-to-tool template? | Specializes the Setup condition when the introduced item exceeds the major-construct threshold |
| [Non-redundancy](#^non-redundancy) | Pairwise within note | Can one unit absorb the other without loss? | Two individually admissible units can be jointly redundant — each passes the objective-preservation test alone, yet they largely overlap |

### Test types

| Rule | Test type | Evaluates |
| --- | --- | --- |
| [Local necessity](#^admissibility-rule) | Unary | One unit against the note's objective |
| [Deductive continuity](#^deductive-articulation) | Binary | Whether step *n+1* uses a specific output of step *n* |
| [Non-redundancy](#^non-redundancy) | Pairwise | Whether two units substantially overlap |

### Argumentative quartet

| Rule | Governs | Satisfiable while others fail because... |
| --- | --- | --- |
| [Deductive continuity](#^deductive-articulation) | Whether logical dependence between units *exists* | Logical dependence can exist without being legible in prose |
| [Functional integrity](#^functional-integrity) | Whether each passage performs *one* argumentative role | Roles can be distinct while transitions remain opaque or interpretation is absent |
| [Transition quality](#^transition-quality) | Whether logical movement is *legible in prose* | Prose can be legible without interpretation being present at milestones |
| [Interpretive integration](#^interpretive-integration) | Whether interpretation is *present and proximate* | Interpretation can be present without the transitions between it and the derivation being legible |

### Interpretation bounded from two directions

| Rule | Direction | Excludes |
| --- | --- | --- |
| [Local necessity's interpretive sub-criterion](#^bounded-interpretive-radius) | Outward expansion (above the derivation) | New objects, cross-module synthesis, external commentary beyond the result's scope |
| [Functional integrity](#^functional-integrity) | Backward regression (below the derivation) | Restatement of the claim without added content, replay of the proof, usurpation of derivation work |

### Evidence support by claim type

| Claim type | Governing rules | Rationale |
| --- | --- | --- |
| Formal (theorems, lemmas, propositions) | [Proof strategies](#^proof-strategies) (route commitment, explanatory target) + [Premise legitimacy](#^premise-legitimacy) (every premise proved or declared) | [Evidence-to-claim proportionality](#^evidence-claim-proportionality) does not apply — without this scoping it would duplicate or weaken the mathematical rules |
| Non-formal (interpretive, comparative, generalization) | [Evidence-to-claim proportionality](#^evidence-claim-proportionality) | Calibrates the required support to the claim type |

### Prose-formalism interface

| Rule | Governs | Example concern |
| --- | --- | --- |
| [Writing principles](#^writing-principles) | Form of all prose uniformly | Register, sentence construction, paragraph construction — independent of mathematical content |
| [Mathematical exposition](#^mathematical-exposition) | Integration of formalism with prose | Lead-in sentences, display framing, assumption surfacing, explicitness — prose-math flow and display-prose integration belong here |
| [Mathematical display](#^mathematical-display) | Formatting of notation | LaTeX conventions, inline math thresholds, display blocks — how symbols are typeset |
| [Terminology](#^terminology) | Naming system | Stability, coherence, disambiguation, semantic lineage — what symbols and terms denote |

### Audience calibration as cross-cutting parameter

| Conditioned rule | Threshold affected |
| --- | --- |
| [Premise legitimacy](#^premise-legitimacy) | When does implicit background need to be restated? (background-restatement test) |
| [Mathematical exposition](#^mathematical-exposition) | What proof steps must be made explicit? (explicitness criterion) |
| [Writing principles](#^writing-principles) | What degree of compression is acceptable? |
| [Intra-unit ordering](#^intra-unit-ordering) | When does a conventional ordering need to be stated explicitly versus assumed? |

### Sequencing scope

| Rule | Scope | Governs |
| --- | --- | --- |
| [Intra-unit ordering](#^intra-unit-ordering) | Within a section or passage | Order of ideas (questions, claims, definitions, derivations, interpretations, examples, boundary cases) |
| [Deductive continuity](#^deductive-articulation) | Between sections | Logical dependence (each section names a specific output from a preceding section as input) |
