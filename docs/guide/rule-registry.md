# Rule Registry

This registry lists all built-in rules shipped with hermeneia v1.

Rules are grouped by functional purpose rather than by module path.
Examples are illustrative.

## Surface Clarity and Precision

| Rule ID | Rule Name | Rationale | Violation example | Preferred |
| --- | --- | --- | --- | --- |
| `surface.sentence_length` | Sentence length target | Long sentences hide the main action and overload working memory. | One 45-word sentence | Split into two shorter statements |
| `surface.passive_voice` | Active opening preference | Passive openings often hide who acts and weaken sentence force. | "It was shown that \(f\) converges." | "Lemma 2 shows that \(f\) converges." |
| `surface.contraction` | Contraction avoidance | Formal technical prose should keep full forms for tone and precision. | "It’s clear that ..." | "It is clear that ..." |
| `surface.nominalization` | Verb-over-noun rewrite | Process nouns often bury agency and weaken directness. | "The implementation of the method" | "The method implements ..." |
| `surface.abstract_framing` | Abstract framing avoidance | Meta-framing can delay the operative statement and hide the mechanism. | "The fact that the residual decays implies stability." | "Residual decay implies stability." |
| `surface.abstract_compound_modifier` | Compound abstraction control | Hyphenated abstractions often hide the concrete dependency. | "a context-dependent strategy" | "a strategy that depends on context because ..." |
| `surface.assumption_hypothesis_framing` | Assumption framing clarity | "the ... assumption/hypothesis" nominal framing can obscure the proposition itself. | "the compactness assumption" | "the assumption of compactness" |
| `surface.prep_chain` | Preposition chain control | Dense prepositional stacks make relations hard to parse. | "A bound on the error in the estimate of the threshold in ..." | "The estimate for the threshold has error bound in ..." |
| `surface.noun_cluster` | Noun cluster control | Long noun stacks compress relationships that readers must unpack. | "A high-order sparse tensor factorization method" | "A method that factorizes sparse high-order tensors" |
| `surface.banned_transition` | Content-free transition ban | Empty scaffolding delays the claim without adding information. | "It should be noted that ..." | State the claim directly |
| `surface.pronoun` | Pronoun scaffolding control | Generic/first-person scaffolding can blur agency and reference. | "We now show ..." | "Section 3 shows ..." |
| `surface.vague_phrasing` | Mechanism specificity | Vague mechanism phrases obscure causal structure. | "This plays a role in convergence." | "This term controls convergence." |
| `surface.case_scaffolding` | Case-phrase rewrite | "the ... case" phrasing adds indirection and nominal clutter. | "In the commutative case ..." | "For commutative matrices ..." |
| `surface.cross_reference` | Explicit cross-reference target | Ambiguous references force readers to infer target objects. | "As discussed above" | "As shown in Proposition 2" |

## Discourse Linkage and Emphasis

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `discourse.subject_verb_distance` | Subject-verb distance | Long gaps weaken sentence core and increase parse effort. | "The theorem, after two technical lemmas, holds." | "After two technical lemmas, the theorem holds." |
| `discourse.subordinate_clause` | Clause load control | Too many subordinate clauses bury the main proposition. | "Although ... because ... if ..." in one sentence | Split into two sentences |
| `discourse.stress_position` | Stress-position quality | Weak sentence endings reduce emphasis and retention. | "From lemma 2, spectral convergence follows." | "The key implication of Lemma 2 is spectral convergence." |
| `discourse.transition_quality` | Transition articulation | Adjacent shifts should be articulated with connectors or explicit reference links when continuity is weak. | "Sentence A. Sentence B about a new step." | "Sentence A. Therefore, this step extends A by ..." |

## Paragraph Coherence and Redundancy Control

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `paragraph.topic_sentence` | Topic sentence strength | Paragraphs should open with a clear controlling claim. | Paragraph opens with detail only | First sentence states the paragraph claim |
| `paragraph.parallelism` | List-frame parallelism | Non-parallel list frames slow scanning and weaken structure. | Mixed verb/noun list items | Align all list items to one frame |
| `paragraph.lexical_repetition` | Non-adjacent restatement detection | Repeated wording across separated sentences can indicate semantic redundancy. | "Claim X. [intervening sentence]. Claim X." | Keep one formulation and add genuinely new contribution |
| `paragraph.concept_reference_drift` | Concept label stability | Naming the same concept with multiple labels can mislead readers about conceptual distinctions. | "the method ... the approach ... the framework ..." | Keep one canonical label for one concept |
| `paragraph.reformulation_inflation` | Reformulation inflation control | Marker-led paraphrases can inflate prose without adding meaning. | "Claim X. In other words, Claim X." | Replace restatement with evidence, scope, or consequence |
| `paragraph.sentence_redundancy` | Adjacent sentence redundancy | Back-to-back restatements reduce information density. | Two adjacent sentences restate same claim | Keep one and add new support |
| `paragraph.paragraph_redundancy` | Cross-paragraph redundancy | Repeated paragraphs waste space and blur progression. | Two paragraphs state same result | Merge or differentiate roles |
| `paragraph.vague_rhetorical_opener` | Vague rhetorical opener control | Vague rhetorical lead-ins delay the claim without adding technical content. | "In this context, ..." / "It should be noted that ..." | Start with the concrete claim or operation |

## Document Structure and Navigation

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `structure.heading_parallelism` | Heading frame parallelism | Sibling headings should present a consistent grammatical frame. | "Define Objects" / "Main Result" / "Applying the Theorem" | Normalize to one frame type |
| `structure.heading_capitalization` | Heading capitalization consistency | Mixed heading styles create visual and navigational friction. | "Main Result" / "Main derivation" | Apply one style across siblings |
| `structure.section_balance` | Section balance | Severe length imbalance often signals argument underdevelopment. | One section is much longer than all siblings | Redistribute material or split scope |

## Audience Fit and Evidence Discipline

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `audience.definition_before_use` | Define before first use | New symbols should be defined when they first appear. | "Substitute in \(T(x)\) ..." with no local definition | Define \(T\) at first mention |
| `audience.acronym_burden` | Acronym definition and dominance | Acronyms should be defined before use and should not dominate over their full forms. | "The PDE ..." with no prior expansion, or "PDE" repeated while full form appears once | Expand first, then keep full form primary in prose |
| `audience.jargon_density` | Jargon density by audience | Dense specialist jargon can exclude target readers. | Jargon-heavy sentence in learner profile | Replace or define terms |
| `audience.claim_calibration` | Claim-evidence calibration | Strong claims should carry nearby support cues. | "This clearly proves ..." with no support signal | Add citation, equation, or result reference |

## Mathematical Exposition Discipline

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `math.display_math` | Display math lead-in and punctuation | Displayed equations should be introduced and punctuated coherently. | Standalone display equation with no lead-in | Add lead-in sentence |
| `math.bare_symbol` | Bare symbol qualifier control | Qualifier/prepositional phrases should name mathematical objects. | "growth in \(P\)" with no object context | "growth in the power function \(P\)" |
| `math.imperative_opening` | Imperative opening avoidance | Imperative proof prose can read as shorthand rather than explanation. | "Let \(x\in X\)" | "For any fixed input \(x\in X\)" |
| `math.prose_math` | Prose relation paraphrase control | Explicit symbolic relations are clearer than verbose paraphrases. | "Since \(x\) times \(y\) equals \(1\)" | "Since \(x \times y = 1\)" |
| `math.proof_marker` | Proof marker opener requirement | End markers should pair with an explicit proof opener. | Paragraph ends with `□` only | Open with "Proof." and close with `□` |

## Notes

- Profiles control which rules run by default.
- Rule options, severities, and weights are configurable.
- See [Configuration](configuration.md) for activation and override semantics.
