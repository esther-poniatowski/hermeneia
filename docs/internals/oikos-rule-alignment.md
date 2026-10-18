# Alignment with the oikos prose rules

The rules of hermeneia and the prose rules of the oikos control hub must enforce the same requirements, since oikos runs hermeneia as its linter. The two rule sets have drifted apart. Each divergence must be settled by changing hermeneia, by changing oikos, or by recording the difference as intended.

## Decisions

All items were opened on 2026-09-26. The following pairs, classified under distinct requirements, must be settled:

- [ ] Sentence adverbials
- [ ] Passive voice
- [ ] Compound modifiers
- [ ] Nominalizations
- [ ] Counts delivered by a colon
- [ ] Link text
- [ ] References to the text
- [ ] Sentence length
- [ ] Inline enumerations
- [ ] Claim calibration
- [ ] Citation roles and keys
- [ ] Heading case
- [ ] Heading content
- [ ] Audit protocols

Three further actions are open:

- [x] Implement a hermeneia rule for each oikos rule listed with a scan key under rules in oikos only.
- [ ] Correct the two mismatches inside hermeneia.
- [ ] Restore or renumber the missing item 2 of `conflict-resolution` in the oikos `prose-writing-style.md`.

## Distinct requirements

In each pair below, the two sides flag different constructions. The first seven pairs conflict: hermeneia flags a construction prescribed by oikos, or admits a construction banned by oikos. The probe column records the behavior of `hermeneia lint` on planted sentences, where it was tested.

| Pair | oikos | hermeneia | Divergence | Probe |
| --- | --- | --- | --- | --- |
| Sentence adverbials | `explicit-connectors`, `name-the-claim-kind` | `linkage.banned_transition`, `vocabulary.abstract_framing`, `vocabulary.redundant_leadin` | oikos requires a sentence adverbial such as "Therefore," at the front of its sentence, and accepts "therefore", "serves" and "in order to" as markers of a claim kind. hermeneia flags "therefore", "hence" and "then" at the start of a line. hermeneia also flags "serves to" as abstract framing and "in order to" as a redundant lead-in. | "Therefore, …" is flagged. |
| Passive voice | `topic-first`, `active-voice` | `syntax.passive_voice` | oikos requires the passive whenever it keeps the topic in subject position. hermeneia flags every passive, and exempts only a sentence opening on "This/That X is" with a lexical overlap of at least 0.22 with the previous sentence. | Two model sentences of oikos are flagged. |
| Compound modifiers | `no-compound-noun-stacks` | `vocabulary.abstract_compound_modifier`, `vocabulary.noun_cluster` | oikos admits a single conventional compound such as "context-dependent" and bans any stack of two or more pre-nominal terms. hermeneia flags a single compound ending in one of ten suffixes, five of them absent from oikos (`specific`, `based`, `oriented`, `related`, `centric`). Its noun-cluster rule flags a run of nouns only from five tokens. | "context-dependent" is flagged, and "model parameter initialization strategy" passes. |
| Nominalizations | `verb-over-process-noun` | `vocabulary.nominalization` | oikos bans a process noun in subject or object position, and exempts a named quantity used across several sentences. hermeneia matches by suffix and exempts six listed nouns only. Beyond the subject and the object, the rule fires after a preposition, on an attribute, and within two tokens of "be". | "condition", "quantity", "argument", "section" and "dimension" are flagged. |
| Counts delivered by a colon | `colon-for-announce-deliver` | `vocabulary.cardinality_framing` | oikos recommends a count followed by a colon delivering its members. hermeneia flags a number followed by one of eight taxonomy nouns, whatever follows. The oikos examples pass only because "factors" and "limitations" are absent from the hermeneia lexicon. | "Four dimensions … : …" is flagged. |
| Link text | `no-procedural-link-text` | `reference.generic_link_text` | oikos bans an article, a clause, a category word and a file name inside link brackets. hermeneia flags a bare label such as "Lemma 3" and five procedural nouns. The [rule registry](../guide/rule-registry.md) recommends `[normal overlaps yield independent mode contributions]`, a clause banned by oikos. | A file-name link and a clause link pass. |
| References to the text | `no-imprecise-references-to-text`, `no-decorative-numbering` | `reference.cross_reference`, `reference.structural_metalanguage` | oikos bans "the previous section" and numbered references such as "Section 5", and exempts an object introduced by a colon or unique in the document. hermeneia exempts every line naming a section, a table or a theorem, and recommends "As shown in Proposition 2". hermeneia also flags any bare "later" or "next". | "the previous section" passes, and "a later recommendation" is flagged. |
| Sentence length | `short-sentences` | `syntax.sentence_length`, `syntax.subordinate_clause` | oikos splits a sentence above 30 words, or holding more than one subordinate clause before its main verb. hermeneia splits above 28 words, or above two subordinate clauses at any position of the sentence. | |
| Inline enumerations | `list-over-inline-enumeration` | `syntax.long_inline_enumeration`, `paragraph.inline_enumeration_overload` | oikos promotes three or more items carrying a verb, a modifier or a complement, and keeps up to three bare items after a colon. hermeneia counts every comma of the sentence, adds one for a final "and", and fires above four items whatever their content. | |
| Claim calibration | `calibrate-assertion` | `evidence.claim_calibration`, `evidence.imprecise_quantifier_without_citation` | oikos requires a quantifier or a scope on a present-tense generalization about a class. hermeneia requires a citation, a theorem or an equation near a strong-claim word, and a citation beside "several" or "others". The hermeneia support detector does not recognize `[authYYYY]` keys, so a citation in the oikos format never counts as support. | |
| Citation roles and keys | `result-not-author`, `literature-references` | `reference.citation_as_agent`, the citation style patterns | oikos bans a citation after "by" and a plain author name holding a grammatical role, and admits keys of the form `authYYYY_short-title`. hermeneia omits "by" and matches bracketed keys only. Its default key pattern rejects `authYYYY_short-title`, so such keys escape every citation rule. | |
| Heading case | `headings-with-sentence-case` | `structure.heading_capitalization` | oikos requires sentence case. hermeneia requires only that sibling headings share one style, so a set of Title Case headings passes. | |
| Heading content | `headings-declarative-keywords` | `structure.declarative_heading` | oikos requires topical keywords and bans generic headings such as "Analysis". hermeneia bans questions and imperative verbs. | |
| Audit protocols | `audit-protocol` | [prose audit protocol](../guide/prose-audit-protocol.md) | The scopes differ: hermeneia excludes docstrings and code comments, whereas oikos includes them together with YAML values. The reports differ too: hermeneia caps a report at 15 findings, each with a severity, and assigns a verdict. By contrast, oikos requires a complete report (every hit quoted, every finding resolved as fixed, exempt or kept, the coverage stated, and a review by a second agent). | |

## Same requirement, documented differently

In each pair below, both sides enforce one requirement, but the names, the rationale or the recommended rewrites differ.

| oikos | hermeneia | Documentation difference |
| --- | --- | --- |
| `no-subjective-pronouns` | `reference.personal_pronoun`, `reference.generic_one` | Both flag the same pronouns, and hermeneia adds "I", "us" and "yours". The registry rewrites ("The next step shows …", "The argument derives …") put a procedure in the subject slot, against `direct-results-over-metasource`. The oikos rewrite puts the object of interest in that slot, in the passive when the object is acted upon. |
| `no-expletives` | `vocabulary.abstract_framing`, `paragraph.vague_rhetorical_opener` | hermeneia splits the four phrases of the "it can be shown" type between two rules named after other constructions. The expletive is never named, and "There is", "There are" and "It is the case that" go undetected. |
| `subject-verb-proximity` | `syntax.subject_verb_distance` | oikos names three interrupting constructions. hermeneia counts the tokens between the subject and the main verb, and fires above eight. Both recommend moving the interrupting material into a prefix clause. |
| `foreground-load-bearing-keywords`, and the given-before-new order of `topic-first` | `linkage.stress_position` | Both place the new element at the stressed end of the sentence. oikos states the placement of the keyword; hermeneia approximates the placement with a lexicon of weak final words. |
| `conflict-resolution` | [prose audit protocol](../guide/prose-audit-protocol.md), conflict precedence | Both order correctness first, then structure and modularity, then pedagogical clarity, then local elegance. hermeneia inserts "hard-blocker compliance" at rank 2. The oikos list jumps from item 1 to item 3. |

## Consistent pairs

In each pair below, both sides enforce one requirement. The coverage column states which part of the oikos class hermeneia detects.

| oikos | hermeneia | Coverage |
| --- | --- | --- |
| `no-contractions` | `vocabulary.contraction` | The coverage is full, except for "what's", absent from the lexicon. |
| `target-anchors`, heading-slug links | `reference.heading_link` | The coverage is full. |
| `target-anchors`, raw anchor tokens | `reference.raw_anchor` | The coverage is full for anchor names containing a hyphen. |
| `integrated-links` | `reference.see_link` | The coverage is full. |
| `citation-by-tail-tag` | `reference.citation_tail_parenthetical` | The coverage is full for `[authYYYY]` keys. |
| `explicit-connectors`, semicolon clause | `linkage.semicolon_connector` | The coverage is full, and both exempt strictly parallel clauses. |
| `explicit-conditional-structure` | `linkage.transition_quality`, conditional check | Only the missing "then" is detected. A condition packed into a participle or a relative clause goes undetected. |
| `list-over-inline-enumeration`, cases joined by semicolons | `paragraph.inline_case_split` | The coverage is full. |
| `lists-for-explicit-structure`, parallel items | `paragraph.parallelism` | The coverage is full. |
| `one-load-bearing-verb-per-sentence` | `syntax.multi_action_sentence` | The contrast "Method A scales linearly, while method B scales quadratically" passes, as oikos requires. |
| `precise-over-vague-terms` | `vocabulary.filler_noun_scaffolding`, `vocabulary.indefinite_reference`, `vocabulary.vague_phrasing` | Filler nouns, indefinite pronouns, "kind of" and "sort of" are detected. The other families listed by oikos go undetected (intensifiers, hedges, informal comparatives, vague actions, hyperbole, coarse terms, and speech verbs attached to inanimate subjects). |
| `no-scaffolding` | `linkage.case_scaffolding` | Only "case" is detected, and "setting", "level" and "argument" go undetected. |
| `explicit-antecedent` | `reference.bare_pronoun_opening`, `linkage.stress_position` | The opening and the closing positions are detected. A bare pronoun after a preposition goes undetected. |
| `no-missing-operand` | `vocabulary.vague_procedural_nominalization` | Only twelve listed procedural nouns are detected. |
| `direct-results-over-metasource` | `vocabulary.concrete_subject`, `reference.structural_metalanguage` | A document or a tool named as subject before an action verb is detected at the start of a line. Three other sources in the subject slot go undetected: an act, a notation and a command. A sentence announcing a result without stating the result also goes undetected. The oikos exemption for overview paragraphs is absent. |
| `no-decorative-numbering` | `linkage.numbered_case` | Only "Case N" is detected. |

## Rules in one set only

### Rules in oikos only

The rules carrying a scan key in the oikos audit protocol now have a hermeneia rule each:

| oikos | hermeneia |
| --- | --- |
| `no-claim-in-relative-tail` | `syntax.relative_tail_claim` |
| `explicit-relative-pronoun` | `syntax.missing_relative_pronoun` |
| `name-the-object` | `reference.free_relative` |
| `no-counterfactual-detour` | `syntax.counterfactual_detour` |
| `no-familiar-register`, aphorism class | `vocabulary.aphorism` |
| `topic-first`, sentence opening on an indefinite article | `linkage.indefinite_opening`, at severity info |
| `explicit-connectors`, sentence adverbial placed inside its clause | `linkage.adverbial_position` |
| `state-the-modality` | `linkage.unstated_modality`, at severity info |
| `one-relation-per-noun-phrase` | `syntax.object_relative` |
| `prose-in-structured-fields` | `structure.field_form`, on the structured sources |
| `no-condition-in-relative-subject` | `syntax.condition_in_subject` |

The following rules could be detected by pattern and carry no scan key:

- `no-informal-judgment`, detected by hermeneia for "better" and "worse" only, as qualitative claims
- `no-verbose-tuples`
- `no-adjacent-repeated-roots`
- `selected-emphasis`
- `headings-concise`
- `no-scaffolding-nouns-for-basic-ideas`
- `md-links-cross-refs`
- `explicit-connectors`, default "and"

The following rules require judgment: `governing-object`, `priority-core`, `expository-register`, `unifying-concept-over-enumeration`, `argument-faithfulness` and `highlight-callouts`. The rules `hermeneia-lint` and `discharge-each-finding` govern the use of the linter.

### Rules in hermeneia only

The following rules have counterparts in other oikos modules, left out of this comparison:

- the thirteen `math.*` rules, against `mathematical-exposition`;
- `paragraph.lexical_repetition`, `paragraph.sentence_redundancy`, `paragraph.paragraph_redundancy` and `paragraph.reformulation_inflation`, against `no-redundancy` in `reasoning-and-exposition`;
- `structure.section_opener_block_kind`, against `goal-oriented-section-opening`;
- `structure.opening_sentence_presence` and `structure.opening_message_focus`, against `goal-anchored-opening` in `user-documentation`.

The following rules have no oikos counterpart:

- vocabulary: `stacked_nominalization_chain`, `assumption_hypothesis_framing`, `prep_chain`, `verbose_preamble`, `redundant_leadin`, `double_negative`, `boilerplate_opener`;
- syntax: `subordinate_clause`, `embedding_depth`;
- linkage: the unmarked-shift, polarity-contrast and connector-underuse checks of `transition_quality`;
- paragraph: `topic_sentence`, `double_framing`, `concept_reference_drift`, `inline_enumeration_overload`;
- structure: `heading_level_skip`, `heading_parallelism`, `section_balance`, `section_order_sequence`, `orphan_section`, `prose_outside_heading`;
- terminology: `definition_before_use`, `acronym_burden`, `jargon_density`;
- evidence: `qualitative_claim_without_quant_support`.

## Mismatches inside hermeneia

- The registry names `syntax.passive_voice` "Active opening preference", whereas the rule flags every passive sentence.
- `vocabulary.redundant_leadin` and `linkage.banned_transition` match at the start of a source line only, so a sentence starting in mid-line escapes both.

## Classification basis

- The baseline is hermeneia commit `f0ac157` and oikos commit `2d91bb9`, both of 2026-09-26.
- The oikos side is read from `prose-writing-style.md`, `audit-protocol.md` and `referencing-and-citations.md` in the oikos `instructions/tasks/` directory. oikos has no executable checks, so its requirement is the rule text together with the scan key of its audit protocol.
- The hermeneia side is read from the code of each rule, since the registry and the code disagree in places.
- A pair is consistent when both sides enforce one requirement, even when hermeneia detects part of the class only.
- A pair is documented differently when the requirement matches and the names, the rationale or the recommended rewrites differ.
- A pair holds distinct requirements when a threshold, an exemption or the target class differs, so that one side flags a construction admitted by the other.
- A rule belongs to one set only when the other set has no rule targeting the same construction.
