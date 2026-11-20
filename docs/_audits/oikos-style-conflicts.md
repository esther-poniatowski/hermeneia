# Conflicts with the oikos style

The oikos style is the [reference style of hermeneia](../adr/0006-oikos-style-as-reference.md). Therefore, when a hermeneia rule and an oikos rule disagree on a construction, the conflict must be settled, and by default the hermeneia rule changes. Each conflict below carries its evidence and a proposed resolution, for approval or amendment.

## Baseline and method

The conflicts were measured against the following state:

- hermeneia at commit `d7e525c`, run with the `research` profile and without a project configuration;
- oikos at commit `7c1929a` of 2026-10-18, with its rules read from the five prose modules of `instructions/tasks/` (`prose-writing-style`, `sentence-construction`, `prose-structures`, `reasoning-and-exposition`, `referencing-and-citations`);
- probes run on 2026-10-23.

Each probe is a Markdown document holding an H1 heading and the probe sentence. Its verdict under oikos is either *conforms* or *violates*. Two outcomes count as a conflict:

- a **false positive**: hermeneia reports a probe that conforms;
- a **miss**: hermeneia stays silent on a probe that violates.

The findings of `structure.orphan_section` and `structure.opening_message_focus` are left out of the probe tables, since a document holding one sentence triggers both. Once settled, each conflict must be recorded in the YAML specification of its rule, the format fixed by the [decision on rule specifications](../adr/0007-rule-specifications-in-yaml.md).

## Summary

| Conflict | False positives | Misses | Resolution |
| --- | --- | --- | --- |
| Sentence adverbials and claim-kind markers | `therefore`, `hence` and `then` opening a line; `serves to` | — | lift the bans on the adverbials and on the markers |
| Passive voice | passives that keep the topic as subject | — | test the subject against the previous sentence |
| Compound modifiers | `context-dependent` | a stack of four nouns | read conventional compounds from a lexicon; count modifiers from the parse |
| Nominalizations | nouns denoting entities; named quantities | — | report only an event reading of a noun derived from a verb |
| Counts delivered by a colon | a count followed by its members | — | retire the rule |
| Link text | — | a clause; a file name | add the three classes missing from the rule |
| References to the text | the colon exception; "later"; the oikos repair form | "the previous section"; "Section 5" | match both word orders and numbered references |
| Sentence length | clauses after the main verb | 31 to 34 words | one threshold of 30 words; count clauses before the verb |
| Inline enumerations | — | three items carrying verbs | count conjuncts from the parse |
| Claim calibration | a claim about the artifact; a cited claim | an unqualified generalization | implement the key of `calibrate-assertion` |
| Citation roles and keys | — | `by` a citation; long keys | add `by` and the long key pattern |
| Heading case | — | Title Case siblings | check sentence case directly |
| Heading content | — | generic headings | add a lexicon of generic headings |
| Audit protocols | — | — | retire the hermeneia protocol |
| Stress position | a sentence ending on "follows" | — | keep only pronouns and demonstratives |
| Discourse continuity | topic chains; enumerative openers | — | measure continuity on entities |
| Embedding depth | ordinary sentences | — | retire the rule, or measure clausal depth |
| Subject–verb distance | coordinated clauses | — | pair each subject with its own verb |

The first fourteen conflicts were recorded on 2026-09-26 and remain open. The last four were found by this audit, on sentences that follow the oikos style.

## Sentence adverbials and claim-kind markers

**oikos.** `explicit-connectors` places a sentence adverbial at the front of its sentence (for instance `therefore`, `hence`, `thus` or `then`). `name-the-claim-kind` accepts five markers of a claim kind (`therefore`, `follows`, `gains`, `serves`, `in order to`).

**hermeneia.** Three rules ban these words, each at severity `error`:

- `linkage.banned_transition` flags 16 phrases at the start of a source line, among them `therefore`, `hence` and `then`;
- `vocabulary.abstract_framing` flags `serves to`;
- `vocabulary.redundant_leadin` flags `in order to` at the start of a source line.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `Therefore, a researcher names only the quantities already declared.`, opening the paragraph | conforms | `linkage.banned_transition` (error), `linkage.unstated_modality` (info) |
| `Then, the checker resolves each symbol against the schema.` | conforms | `linkage.banned_transition` (error) |
| `The bound holds for every width. Hence, the estimate transfers to deep networks.` | conforms | `linkage.unstated_modality` (info) |
| `The index serves to orient a reader toward the note that answers a question.` | conforms | `vocabulary.abstract_framing` (error), `vocabulary.nominalization` on `question` (error), `syntax.embedding_depth` (warning) |
| `The checker reads the schema in order to report each undeclared key.` | conforms | none |

In the third probe, the adverbial opens a sentence in the middle of a line and escapes the ban. Therefore, the ban depends on the position of the line break rather than on the construction.

**Resolution.** Lift the bans on the five words, held by three lexicons of hermeneia:

- `therefore`, `hence` and `then`, in the banned transitions;
- `serves to`, in the abstract framing phrases;
- `in order to`, in the redundant lead-ins.

Assign each remaining banned phrase to the oikos rule that bans it, such as `this gives` to `explicit-antecedent` and `clearly` to `precise-over-vague-terms`. A phrase banned by no oikos rule falls under the decision on hermeneia-only rules, stated in the closing section on required decisions. The `linkage.unstated_modality` finding on the first probe follows `state-the-modality`. That finding reveals a contradiction between two oikos rules, listed with the other contradictions inside oikos.

## Passive voice

**oikos.** `topic-first` declares the passive correct whenever it keeps the topic in subject position. On that point, `topic-first` overrides the default of `active-voice`. `no-subjective-pronouns` also prescribes the passive when the object of interest is acted upon.

**hermeneia.** `syntax.passive_voice` (warning) flags every passive in a paragraph. The rule exempts a passive only when its subject opens on a demonstrative and the sentence shares at least 22 % of its words with the previous sentence. Neither of its two labels matches this behavior: the code calls the rule "Prefer active voice in sentence openings", and the [rule registry](../guide/rule-registry.md) calls it "Active opening preference".

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The gradient descent algorithm converges under standard regularity conditions. This convergence is guaranteed by a convex loss.` | conforms | `syntax.passive_voice` (warning), `vocabulary.nominalization` on `condition` and `convergence` (error) |
| `A model describes the network dynamics. The network dynamics are described by a model with two populations.` | conforms | `syntax.passive_voice` (warning), `vocabulary.nominalization` on `population` (error) |
| `The rule is stated once.` | conforms | `syntax.passive_voice` (warning) |

The first probe adapts the model sentence of `topic-first` to the passive. Its subject opens on "This" and repeats "convergence". Even so, the exemption does not apply.

**Resolution.** Replace the overlap ratio with a test of the subject. A passive is exempt when the head noun of its subject recurs in the previous sentence, or when its subject is a pronoun or a demonstrative noun phrase. Report the remaining passives at severity `info`, as a question for the reading of `topic-first`, and align the label of the rule with its behavior.

## Compound modifiers

**oikos.** `no-compound-noun-stacks` bans a hyphenated modifier placed before a noun when it encodes a relation, and any stack of two or more terms placed before a noun. A conventional compound, such as `context-dependent`, is exempt outside a stack.

**hermeneia.** `vocabulary.abstract_compound_modifier` (error) flags a hyphenated modifier ending in one of ten suffixes, and exempts five listed adjectives. `vocabulary.noun_cluster` (warning) fires only on a run of five nouns or more.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The context-dependent gain decays with the input.` | conforms | `vocabulary.abstract_compound_modifier` (error) |
| `The model parameter initialization strategy is fixed before training.` | violates | no compound finding; `syntax.passive_voice` (warning), `vocabulary.nominalization` on `training` (error) |
| `Stimulus-modulated kernel variation shapes the response.` | violates | `vocabulary.abstract_compound_modifier` (error), `vocabulary.nominalization` on `variation` (error) |

**Resolution.** Read the conventional compounds from a lexicon file extensible by each project, seeded with the example of oikos. Count the nouns and the hyphenated modifiers before the head noun from the parse, and fire from two. One case remains open: `no-compound-noun-stacks` does not state whether a plain adjective, as in `large random matrix`, counts as a term of a stack.

## Nominalizations

**oikos.** `verb-over-process-noun` bans a process nominalization in subject or object position. Two kinds of noun are exempt: a conventional term naming the property of interest ("existence", "uniqueness"), and a named technical quantity used in distinct sentences of one document.

**hermeneia.** `vocabulary.nominalization` (error) flags a noun ending in one of nine derivational suffixes (`tion`, `ment`, `ity`, `al`, `ing` and four others). The rule fires on such a noun in four positions:

- a core argument of its clause;
- the complement of a weak support verb;
- an abstract noun phrase;
- a stack of nominalizations.

Six listed nouns are exempt.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The application of regularization results in a reduction of overfitting.` | violates | `vocabulary.nominalization` on `application` (error) |
| `The section states the bound, and each question names its material.` | conforms | `vocabulary.nominalization` on `section` (error) |
| `The amplification selectivity grows with the gain. The amplification selectivity saturates at high gain.` | conforms | `vocabulary.nominalization` on `amplification` and `selectivity` (error) |
| `A cascade is a sequence of transmissions between subsystems.` | conforms | `vocabulary.nominalization` on `sequence` (error) |

On the rule notes of geonexus, this rule reports 627 errors. The nouns reported most often name entities or results, led by `action` (51 findings), `material` (31) and `question` (24). To silence such reports, the geonexus configuration declares 26 nouns as project terms.

**Resolution.** Rebuild the rule in four steps:

- restrict the candidates to nouns derived from a verb, listed in a lexicon built offline from NOMLEX or from the derivational links of WordNet, and shipped as data;
- report only an event reading: the noun realizes an argument of its verb through an of-phrase, a genitive or a by-phrase, as in "the application of regularization";
- exempt a noun phrase recurring in two distinct sentences of the document, as a named technical quantity;
- report at severity `warning`, with the weak support verb ("perform an analysis") as the signal of highest confidence.

A plural, counted or argument-less use denotes a result or an entity, so the second step leaves it unreported.

## Counts delivered by a colon

**oikos.** `colon-for-announce-deliver` recommends a count followed by a colon that delivers its members. The motivating paragraph of `writing-exemplars` also delivers a count in the next sentences: "Two limitations are commonly observed …. First, … Second, …".

**hermeneia.** `vocabulary.cardinality_framing` (warning) flags a number word followed by one of 16 taxonomy nouns (such as `levels`, `types` or `dimensions`), regardless of the words after the noun.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `Four dimensions organize the space: width, depth, rank and spread.` | conforms | `vocabulary.cardinality_framing` (warning), `vocabulary.nominalization` on `dimension` (error) |
| `Four factors jointly shape the learned geometry: the inputs, the nonlinearity, the depth, and the regime.` | violates `list-over-inline-enumeration` | `syntax.long_inline_enumeration` (warning) |

The second probe passes `vocabulary.cardinality_framing` only because "factors" is absent from its lexicon.

**Resolution.** Retire the rule. oikos admits both deliveries of a count, by a colon and by the next sentences. Consequently, no construction targeted by the rule remains banned.

## Link text

**oikos.** `no-procedural-link-text` bans four constructions inside the brackets of a link:

- a leading article;
- a clause;
- a category word or a container title without its message;
- a file name, a path or an extension.

**hermeneia.** `reference.generic_link_text` (error) flags a bare label such as "Lemma 3" and ten procedural nouns, such as `note`, `analysis` and `derivation`. The [rule registry](../guide/rule-registry.md) recommends a clause as link text: `[normal overlaps yield independent mode contributions]`.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The proof is given in [normal overlaps yield independent mode contributions](proof.md).` | violates | no link finding |
| `The bound is stated in [proof.md](proof.md).` | violates | no link finding |
| `The bound is stated in [the coupling analysis](proof.md).` | violates | `reference.generic_link_text` (error) |
| `The bound follows from [Lemma 3](proof.md).` | violates | `reference.generic_link_text` (error) |

**Resolution.** Add the three classes missing from the rule:

- a leading article;
- a clause, detected from the parse as a finite verb inside the brackets;
- a file name, a path or an extension.

Replace the example of the registry with a keyword label.

## References to the text

**oikos.** `no-imprecise-references-to-text` bans four references by position (`the above table`, `the list below`, `the previous section`, `the next section`). Its repair names the content, as in `in the previous section on X`. The rule exempts an object introduced immediately by a colon, or unique in the document. `no-decorative-numbering` also bans a numbered reference such as "Section 5".

**hermeneia.** Two rules address references to the text:

- `reference.structural_metalanguage` (error) flags a structural noun followed by a position word, as in `the list below`, and a structural noun followed by `of` or `on`;
- `reference.cross_reference` (info) flags a bare `later` or `next`, and exempts every line naming a section, a table or a theorem.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The previous section states the bound.` | violates | no reference finding; `vocabulary.nominalization` on `section` (error) |
| `The bound is stated in Section 5.` | violates | no reference finding |
| `The bound supports a later recommendation on the step size.` | conforms | `reference.cross_reference` (info) |
| `The list below holds the three cases: small, medium and large widths.` | conforms, by the colon exception | `reference.structural_metalanguage` (error), `reference.cross_reference` (info), `linkage.case_scaffolding` (error) |
| `The bound is derived in the previous section on convergence.` | conforms, as the repair form | `reference.structural_metalanguage` (error) |

The first probe escapes because the patterns expect the position word after the noun. The last probe receives an error for the exact form prescribed by oikos as the repair.

**Resolution.** Match a structural noun beside a position word in both orders, and match a numbered reference such as "Section 5" or "Table 2". Exempt a sentence that delivers its object after a colon, and a structural noun followed by "on" that names the content. Restrict "later" and "next" to phrases naming a part of the text.

## Sentence length

**oikos.** `short-sentences` splits a sentence above 30 words. Below that threshold, it splits a sentence holding more than one subordinate clause before its main verb.

**hermeneia.** `syntax.sentence_length` (warning) reads its threshold from three layers. The rule and the language pack both set 28 words. The profiles override them with 34 words for `research`, 30 for `mathematical`, and 22 for `strict` and `pedagogical`. `syntax.subordinate_clause` (warning) fires above two subordinate clauses, wherever they stand in the sentence.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| a sentence of 30 words | conforms | no length finding |
| a sentence of 32 words | violates | no length finding |
| `Because the drive shifts while the gain rescales the modes, the response grows.` | violates | `syntax.subordinate_clause` (warning) |
| `The response grows when the drive shifts, because the gain rescales the modes that the input excites.` | conforms | `syntax.subordinate_clause` (warning) |

The report of 2026-09-26 gave 28 words as the threshold of hermeneia. That number is the default of the rule, whereas the `research` profile applies 34 words.

**Resolution.** Declare a single threshold of 30 words in the specification of the rule, in place of the overrides of the profiles. When a profile needs another threshold, its definition must state the reason. Count only the subordinate clauses that precede the main verb, from the parse, and fire from two.

## Inline enumerations

**oikos.** `list-over-inline-enumeration` admits at most three items after a colon, each a single word or a bare noun phrase of two words. A bulleted list is required for four items or more, and for any item carrying a verb, a modifier or a complement.

**hermeneia.** `syntax.long_inline_enumeration` (warning) counts the commas of the sentence, adds one for a final "and", and fires above four items. `paragraph.inline_enumeration_overload` (info) fires above two commas in a sentence of 28 words or more.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `Only three slots remain: identification, delivery, and exit.` | conforms | no enumeration finding; `vocabulary.nominalization` on `identification` (error) |
| `The checker reads the schema, resolves each symbol, and reports every undeclared key.` | violates | `syntax.multi_action_sentence` (warning) only |
| `The vault holds notes, tasks, glossaries, indexes and templates.` | violates | `syntax.long_inline_enumeration` (warning) |

The second probe is reported by a rule whose repair splits the sentence, whereas oikos tries an umbrella concept first and a bulleted list second.

**Resolution.** Count the conjuncts of one head from the parse instead of the commas. Fire on four conjuncts or more. Fire also on three conjuncts when one of them carries a verb, a modifier or a complement. Exempt three bare items after a colon.

## Claim calibration

**oikos.** `calibrate-assertion` requires a quantifier or a scope on a present-tense generalization about a class. Five constructions are exempt:

- a definition;
- a stated rule;
- a theorem;
- a claim about the artifact at hand;
- the *Why* clause of a rule.

**hermeneia.** Two rules check whether a claim is supported, both at severity `info`:

- `evidence.claim_calibration` requires a citation, a theorem or an equation within three sentences of a strong-claim word (such as `prove`, `show`, `always` or `never`);
- `evidence.imprecise_quantifier_without_citation` requires a citation beside `several` or `others`.

The support detector of both rules ignores the citation keys of the oikos format.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `A research project accumulates definitions that prose cannot track.` | violates | no calibration finding |
| `The induction shows that the bound holds for every width.` | conforms, as a claim about the artifact | `evidence.claim_calibration` (info) |
| `The bound was proved by [smith2020].` | conforms for calibration, since it cites its support | `evidence.claim_calibration` (info) |

**Resolution.** Replace the test for a nearby citation with the key of `calibrate-assertion`. The key matches a present-tense sentence whose subject is a generic noun of a class, such as a bare plural or a singular with an indefinite article. A matching sentence is reported at severity `info` when it carries neither a quantifier nor an adverbial of scope. Recognize the keys `[authYYYY]` and `[authYYYY_short-title]` as support in every evidence rule that remains.

## Citation roles and keys

**oikos.** `result-not-author` bans a citation or an author name in any grammatical role (subject, object, modifier, possessive, or object of a preposition such as `by` or `of`). `literature-references` admits the keys `authYYYY` and `authYYYY_short-title`.

**hermeneia.** `reference.citation_as_agent` (error) matches a citation in three positions:

- before one of 18 agent verbs;
- after one of 10 object verbs;
- after one of four prepositions (`in`, `from`, `of`, `per`).

The rule reads only the bracketed keys of one default pattern.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `[smith2020] proves the bound for every width.` | violates | `reference.citation_as_agent` (error), `reference.citation_tail_parenthetical` (error) |
| `The bound was proved by [smith2020].` | violates | no citation finding |
| `[smith2020_wide-networks] proves the bound for every width.` | violates | no citation finding |
| `The bound holds for every width [smith2020_wide-networks].` | conforms | none |

**Resolution.** Add `by` to the forbidden prepositions, and accept the key pattern `authYYYY_short-title`. Detect a plain author name holding a grammatical role from the entities of the parse (label `PERSON`). The oikos exception for a sentence about authorship is left to manual reading.

## Heading case

**oikos.** `headings-with-sentence-case` requires sentence case: only the first word and the proper nouns take a capital.

**hermeneia.** `structure.heading_capitalization` (warning) requires only that sibling headings share one style.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| sibling headings `## Results Of The Analysis` and `## Proof Of The Bound` | violates | none |

**Resolution.** Check sentence case directly. Every word after the first takes lowercase, except the words exempted for the project (proper nouns, acronyms, code spans and declared terms).

## Heading content

**oikos.** `headings-declarative-keywords` requires topical keywords in a heading, and its ✗ example is the generic heading "Analysis". `headings-concise` bans a long sentence, a leading article, and a code or math symbol in a heading.

**hermeneia.** `structure.declarative_heading` (warning) bans a question and a heading opening on one of 12 imperative verbs.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| sibling headings `## Analysis` and `## Discussion` | violates | none |

**Resolution.** Add a lexicon of generic headings, extensible by each project. Add also the three bans of `headings-concise`. oikos does not ban questions or imperatives in headings, so those two checks fall under the decision on hermeneia-only rules.

## Audit protocols

**oikos.** The `audit-protocol` module covers every prose string, including docstrings, code comments and YAML values. The module requires a complete report, in three parts:

- each finding, quoted and resolved as fixed, exempt or kept;
- the coverage figures;
- a review by a second agent.

**hermeneia.** The [prose audit protocol](../guide/prose-audit-protocol.md) leaves docstrings and code comments out of its scope. Its report holds at most 15 findings and closes on a verdict.

The two protocols also order the conflicts between rules differently:

| Rank | oikos, `conflict-resolution` | hermeneia, prose audit protocol |
| --- | --- | --- |
| 1 | mathematical correctness | technical correctness |
| 2 | no redundancy, modularity | compliance with hard blockers |
| 3 | the constructions of the register | structure and modularity |
| 4 | local stylistic choices | pedagogical clarity |
| 5 | — | local elegance |

**Resolution.** Retire the hermeneia protocol. The user guide keeps only the contract of the linter report: the fields of a finding and the meaning of each severity. For a manual audit, the guide names the oikos protocol as the reference.

## Stress position

**oikos.** `name-the-claim-kind` models the sentence "One design goal follows". `explicit-antecedent` bans a bare demonstrative or pronoun at the end of a sentence.

**hermeneia.** `linkage.stress_position` (info) flags a sentence ending on one of 16 weak words. The list mixes two classes: the pronouns `it`, `this` and `that`, and other words such as `follows`, `result` and the forms of `be`.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The schema fixes every field. One design goal follows.` | conforms | `linkage.stress_position` (info), `linkage.transition_quality` (info), `paragraph.topic_sentence` (info) |

**Resolution.** Restrict the list to the demonstratives and pronouns that `explicit-antecedent` bans in terminal position.

## Discourse continuity

**oikos.** `topic-first` carries the topic through the subject slot, as in "This convergence relies on a convex loss". The motivating paragraph of `writing-exemplars` opens successive sentences on "First," and "Second,".

**hermeneia.** Two rules measure continuity, both at severity `info`, through three checks:

- `linkage.transition_quality` reports an unmarked shift when two adjacent sentences share less than 15 % of their words and the second carries no listed connector;
- the same rule reports a lack of connectors when the mean overlap of a paragraph stays below 30 %;
- `paragraph.topic_sentence` scores the first sentences of a paragraph by their position and by their lexical centrality.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `The gradient descent algorithm converges under standard regularity conditions. This convergence is guaranteed by a convex loss.` | conforms | `linkage.transition_quality` (info), `paragraph.topic_sentence` (info) |
| `The bound fails for narrow networks. First, the kernel loses rank. Second, the gradient vanishes at initialization.` | conforms | `linkage.transition_quality` (info), twice |
| the exemplar paragraph "A theoretical research project typically holds …", from `writing-exemplars` | conforms | `linkage.transition_quality` (info), three times; `paragraph.topic_sentence` (info) |

The lexicon of connectors holds no enumerative marker, so "First," and "Second," count as missing transitions.

**Resolution.** Measure continuity on entities instead of word overlap. Two sentences are linked when the head noun of a subject or an object recurs, or when the second sentence opens on a demonstrative noun phrase or an enumerative marker. Both rules move to the experimental tier until the [calibration corpus](state-assessment.md) fixes their thresholds.

## Embedding depth

**oikos.** No rule bounds the depth of a parse tree. The nearest rules are `short-sentences`, counting the subordinate clauses before the main verb, and `subject-verb-proximity`.

**hermeneia.** `syntax.embedding_depth` (warning) combines the depth of the dependency tree with the density of punctuation and of subordinate markers, and fires above 6.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| `A candidate answer proposes a model of the target system, built from units, quantities, and laws. …`, from `writing-exemplars` | conforms | `syntax.embedding_depth` (warning), at depth 9 |
| `The index serves to orient a reader toward the note that answers a question.` | conforms | `syntax.embedding_depth` (warning) |

Across the six exemplars of the [precision baseline](state-assessment.md), the rule reports four sentences.

**Resolution.** Retire the rule in favor of the count of subordinate clauses before the main verb, proposed in the section on sentence length. Alternatively, the rule can measure the depth of nested clauses (`advcl`, `ccomp`, `relcl`, `acl`, `xcomp`), if a reading of the calibration corpus shows a defect missed by the count.

## Subject–verb distance

**oikos.** `subject-verb-proximity` names three constructions that separate a subject from its verb: a long inline enumeration, a nested clause, and an overloaded subject.

**hermeneia.** `syntax.subject_verb_distance` (warning) counts the tokens between a subject and the main verb, and fires above 10 in the `research` profile.

| Probe | Verdict | hermeneia findings |
| --- | --- | --- |
| a sentence of 30 words made of two coordinated clauses, `The estimator converges … and its rate of convergence matches …` | conforms | `syntax.subject_verb_distance` (warning), at a distance of 18 |

The rule pairs `rate`, the subject of the second clause, with `converges`, the root verb of the first clause. Therefore, the reported distance separates two clauses rather than a subject and its verb.

**Resolution.** Pair each subject with the verb that governs it, instead of the root of the sentence. Then report only the three constructions named by oikos.

## Contradictions inside hermeneia

Three contradictions sit inside hermeneia and must be settled together with the conflicts above:

- `therefore` and `hence` are banned by `linkage.banned_transition`, yet `linkage.transition_quality` reports a transition lacking such a connector;
- `in order to` is banned as a redundant lead-in, yet it also counts among the purpose markers of an assumption;
- `linkage.banned_transition` and `vocabulary.redundant_leadin` match only at the start of a source line, so a sentence starting in the middle of a line escapes both.

## Contradictions inside oikos

Three model sentences of oikos break another oikos rule. A linter that enforces both rules of a pair must flag the model of one of them. Therefore, each model must be rewritten in oikos:

- the model of `explicit-connectors`, `Therefore, a researcher names only the quantities already declared.`, is the ✗ example of `state-the-modality`;
- the model of `colon-for-announce-deliver` delivers four modified items inline: `Four factors jointly shape the learned geometry: the geometry of the inputs, the nonlinearity, the network depth, and the training regime.` From four items, `list-over-inline-enumeration` requires a bulleted list;
- the model of `no-procedural-link-text`, `the tests that each candidate answer must pass`, holds an object relative clause, banned by `one-relation-per-noun-phrase`.

## Decisions required

Two decisions are needed before the resolutions above can be applied:

- **Hermeneia-only rules.** Several hermeneia rules target constructions addressed by no oikos rule, such as the bans of questions and imperatives in headings, or `vocabulary.double_negative`. Each such rule can be kept as an extension, proposed to oikos as a new rule, or retired. The recommendation is to keep a rule as an extension only when it never fires on the conforming part of the calibration corpus, and to propose or retire the others.
- **Profile thresholds.** `short-sentences` splits every sentence above 30 words, whereas the `strict` and `pedagogical` profiles of hermeneia flag sentences above 22 words. On 2026-10-23, the shorter length was reclassified from an obligation into a target. The proposed resolution separates two quantities. First, every profile reports a sentence above 30 words, at severity `warning`. Second, a profile may set a target for the mean sentence length of a document. That target is reported at severity `info`, as a measurement of the document rather than as a finding on one sentence. The values of the targets remain to be chosen.
