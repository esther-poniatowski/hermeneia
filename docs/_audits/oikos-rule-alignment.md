# Alignment with the oikos prose rules

Each oikos prose rule must be matched with its detectors among the hermeneia rules. The correspondence below supplies the detection part of the [rule specifications](../adr/0007-rule-specifications-in-yaml.md). Every oikos prose rule migrates into such a specification. Once every rule has migrated, the specifications hold the correspondence, so this inventory is retired. The [pairs in conflict](oikos-style-conflicts.md) are stated separately, each with a proposed resolution.

## Same requirement, documented differently

In each pair below, both sides enforce one requirement, but the names, the rationale or the recommended rewrites differ.

| oikos | hermeneia | Documentation difference |
| --- | --- | --- |
| `no-subjective-pronouns` | `reference.personal_pronoun`, `reference.generic_one` | Both flag the same pronouns, and hermeneia adds "I", "us" and "yours". The registry rewrites ("The next step shows …", "The argument derives …") put a procedure in the subject slot, against `direct-results-over-metasource`. The oikos rewrite puts the object of interest in that slot, in the passive when the object is acted upon. |
| `no-expletives` | `vocabulary.abstract_framing`, `paragraph.vague_rhetorical_opener` | hermeneia splits the four phrases of the "it can be shown" type between two rules named after other constructions. The expletive is never named, and "There is", "There are" and "It is the case that" go undetected. |
| `subject-verb-proximity` | `syntax.subject_verb_distance` | oikos names three interrupting constructions. hermeneia counts the tokens between the subject and the main verb, and fires above eight by default, or above ten in the `research` profile. Both recommend moving the interrupting material into a prefix clause. |
| `foreground-load-bearing-keywords`, and the given-before-new order of `topic-first` | `linkage.stress_position` | Both place the new element at the stressed end of the sentence. oikos states the placement of the keyword; hermeneia approximates the placement with a lexicon of weak final words. |

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

The following rules require judgment:

- `governing-object`
- `priority-core`
- `expository-register`
- `unifying-concept-over-enumeration`
- `argument-faithfulness`
- `highlight-callouts`

The rules `hermeneia-lint` and `discharge-each-finding` govern the use of the linter.

### Rules in hermeneia only

The following rules have counterparts in other oikos modules, left out of this comparison:

- the thirteen `math.*` rules, against `mathematical-exposition`;
- `paragraph.lexical_repetition`, `paragraph.sentence_redundancy`, `paragraph.paragraph_redundancy` and `paragraph.reformulation_inflation`, against `no-redundancy` in `reasoning-and-exposition`;
- `structure.section_opener_block_kind`, against `goal-oriented-section-opening`;
- `structure.opening_sentence_presence` and `structure.opening_message_focus`, against `goal-anchored-opening` in `user-documentation`.

The following rules have no oikos counterpart:

- vocabulary: `stacked_nominalization_chain`, `assumption_hypothesis_framing`, `prep_chain`, `verbose_preamble`, `double_negative`, `boilerplate_opener`;
- syntax: `embedding_depth`;
- linkage: the unmarked-shift, polarity-contrast and connector-underuse checks of `transition_quality`;
- paragraph: `topic_sentence`, `double_framing`, `concept_reference_drift`;
- structure: `heading_level_skip`, `heading_parallelism`, `section_balance`, `section_order_sequence`, `orphan_section`, `prose_outside_heading`;
- terminology: `definition_before_use`, `acronym_burden`, `jargon_density`;
- evidence: `qualitative_claim_without_quant_support`.

Three of these rules report sentences that follow the oikos style, so they are treated in the conflict report: `syntax.embedding_depth`, the checks of `linkage.transition_quality`, and `paragraph.topic_sentence`.

## Classification basis

- The first version of this inventory used hermeneia commit `f0ac157` and oikos commit `2d91bb9`, both of 2026-09-26. At oikos commit `7c1929a` of 2026-10-18, each cited label still exists. The coverage stated in the tables was not measured again at that commit.
- The oikos side is read from the rule text of the five prose modules in `instructions/tasks/`, and from the table of linter rules in `audit-protocol`.
- The hermeneia side is read from the code of each rule, since the registry and the code disagree in places.
- A pair is consistent when both sides enforce one requirement, even when hermeneia detects part of the class only.
- A pair is documented differently when the requirement matches and the names, the rationale or the recommended rewrites differ.
- A pair is in conflict when a threshold, an exemption or the target class differs, so that one side flags a construction admitted by the other.
- A rule belongs to one set only when the other set has no rule targeting the same construction.
