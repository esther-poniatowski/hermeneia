# Rule Registry

This registry lists all built-in rules shipped with hermeneia, grouped by functional purpose. Each
rule is illustrated by brief examples. Pair it with [Configuration](configuration.md) for activation
and override semantics.

## Surface Clarity and Precision

| Rule ID | Rule Name | Rationale | Violation example | Preferred |
| --- | --- | --- | --- | --- |
| `surface.sentence_length` | Sentence length target | Long sentences hide the main action and overload working memory. | One 45-word sentence | Split into two shorter statements |
| `surface.passive_voice` | Active opening preference | Passive openings often hide who acts and weaken sentence force. | "It was shown that \(f\) converges." | "Lemma 2 shows that \(f\) converges." |
| `surface.contraction` | Contraction avoidance | Formal technical prose should keep full forms for tone and precision. | "It doesn't satisfy" | "It does not satisfy" |
| `surface.nominalization` | Nominalization clarity | Flags process nouns used as weak-support constructions, abstract noun phrases, or core argument placeholders. | "The composition of \(f\) with \(g\) yields ..." / "The derivation is ..." | "Composing \(f\) with \(g\) yields ..." / direct verb framing |
| `surface.stacked_nominalization_chain` | Nominalization chain control | Long nominalization stacks compress several actions into one noun phrase and obscure dependencies. | "Optimization regularization stabilization calibration pipeline ..." | "Optimizing and regularizing ... stabilizes calibration ..." |
| `surface.abstract_framing` | Abstract framing avoidance | Meta-framing can delay the operative statement and hide the mechanism. | "The role of commutativity is ..." / "It can be shown that ..." | "Commutativity determines ..." / direct claim statement |
| `surface.vague_procedural_nominalization` | Procedural-argument specificity | Procedural nouns should name arguments explicitly rather than float as abstract placeholders. | "The comparison remains inconclusive." | "The comparison between X and Y remains inconclusive." |
| `surface.concrete_subject` | Concrete-subject enforcement | Document/tool subjects often hide the real mathematical actor. | "This section derives the factorization." | "The ratio factorizes as ..." |
| `surface.abstract_compound_modifier` | Compound abstraction control | Hyphenated or stacked pre-nominal abstractions often hide the concrete dependency. | "a context-dependent data-driven strategy" | "a strategy that depends on context and is driven by data" |
| `surface.assumption_hypothesis_framing` | Assumption framing clarity | "the ... assumption/hypothesis" nominal framing can obscure the proposition itself. | "the compactness assumption" | "the assumption of compactness" |
| `surface.prep_chain` | Preposition chain control | Dense prepositional stacks make relations hard to parse. | "A bound on the error in the estimate of the threshold in ..." | "The estimate for the threshold has error bound in ..." |
| `surface.noun_cluster` | Noun cluster control | Long noun stacks compress relationships that readers must unpack. | "A high-order sparse tensor factorization method" | "A method that factorizes sparse high-order tensors" |
| `surface.banned_transition` | Content-free transition ban | Content-free transition openers are blocked when they replace an explicit argumentative action. | "Therefore: ..." / "More explicitly: ..." | "Differentiating the eigenbasis expansion with respect to \(g\) yields: ..." |
| `surface.personal_pronoun` | First/second-person pronoun control | Direct writer/reader address weakens impersonal technical style. | "We now show ..." / "You can verify ..." | "The next step shows ..." |
| `surface.generic_one` | Generic actor "one" control | Generic actor phrasing hides who or what performs the action. | "One can derive ..." | "The argument derives ..." |
| `surface.bare_pronoun_opening` | Bare-pronoun opening ban | Pronoun-opened sentences without explicit noun heads obscure references. | "It follows that ..." / "This is necessary." | "The bound implies ..." / "This constraint is necessary." |
| `surface.verbose_preamble` | Verbose preamble control | Long prefatory setup delays the main proposition. | "It provides the following benefits: ..." | "The method improves stability and speed." |
| `surface.redundant_leadin` | Redundant lead-in ban | Formulaic lead-ins add words without information gain. | "In order to prove convergence, ..." | "To prove convergence, ..." |
| `surface.long_inline_enumeration` | Long inline-enumeration control | Inlined sequences with too many items reduce scanability. | "alpha, beta, gamma, delta, epsilon, and zeta" | Lead-in sentence + bullet list |
| `surface.vague_phrasing` | Mechanism specificity | Vague mechanism phrases force readers to guess what drives the effect. | "The gain changes in several ways." | "Increasing \(g\) amplifies \(A_1(g)\), which tightens the decay bound." |
| `surface.double_negative` | Double-negative clarity | Double negatives can obscure polarity and force re-reading. | "The estimate is not without error." | "The estimate has error." |
| `surface.boilerplate_opener` | Boilerplate-opener control | Boilerplate openers delay the concrete claim. | "Recently, there has been an increasing interest in ..." | Start with the direct claim and supporting mechanism |
| `surface.indefinite_reference` | Indefinite reference specificity | Broad indefinite pronouns/adverbs blur object scope and mechanism. | "Everything improves somehow." | "The boundary estimate improves on the noisy subset because ..." |
| `surface.case_scaffolding` | Case-phrase rewrite | "the ... case" scaffolding (including plural and opener forms) adds indirection and nominal clutter. | "In the commutative cases ..." | "For commutative matrices ..." |
| `surface.numbered_case` | Numbered-case split control | Anonymous case numbering hides the semantic distinction between branches. | "Case 1: ... Case 2: ..." | "If the matrix is diagonal ... / If the matrix is singular ..." |
| `surface.cross_reference` | Explicit cross-reference target | Ambiguous references force readers to infer target objects and interrupt flow. | "As discussed above" | "As shown in Proposition 2 (#^prop-bound)" |
| `surface.heading_link` | Heading-slug link ban | Heading slugs are unstable; block anchors provide explicit and durable targets. | `[Main result](#main-result)` | `[Main result](#^main-result)` |
| `surface.see_link` | "See [link]" scaffolding control | Standalone "See" link lead-ins add indirection and weak rhetorical integration. | "See [Lemma 2](#^lemma-two)." | "Lemma 2 gives the bound [link]." |
| `surface.raw_anchor` | Raw-anchor token ban | Raw `^anchor` tokens in prose are implementation artifacts, not reader-facing references. | "Use ^lemma-two for details." | "Use [Lemma 2](#^lemma-two) for details." |
| `surface.generic_link_text` | Generic/procedural link text control | Label-only links and procedural/container labels hide what the link contributes. | `[Lemma (Bound)](#^lemma-two)` / `[normality specialization](...)` | `[Boundary bound in Lemma 2](#^lemma-two)` / `[normal overlaps yield independent mode contributions](...)` |

## Discourse Linkage and Emphasis

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `discourse.subject_verb_distance` | Subject-verb distance | Long gaps weaken sentence core and increase parse effort. | "The theorem, after two technical lemmas, holds." | "After two technical lemmas, the theorem holds." |
| `discourse.subordinate_clause` | Clause load control | Too many subordinate clauses bury the main proposition. | "Although ... because ... if ..." in one sentence | Split into two sentences |
| `discourse.embedding_depth` | Embedding-depth control | Deeply embedded sentence structure increases parse cost and often needs multiple reads. | "Although ..., which ..., when ..., ..." | Split into shorter sentences with one main action each |
| `discourse.stress_position` | Stress-position quality | Weak sentence endings reduce emphasis and retention. | "From lemma 2, spectral convergence follows." | "The key implication of Lemma 2 is spectral convergence." |
| `discourse.transition_quality` | Transition articulation | Flags weakly linked adjacent shifts and paragraph chains with low continuity and no explicit connectors/reference anchors. | "Sentence A. Sentence B about a new step." | "Sentence A. Therefore, this step extends A by ..." |
| `discourse.semicolon_connector` | Semicolon connector articulation | Semicolon-linked clauses need explicit connective framing unless strictly parallel. | "The bound tightens; the variance shrinks." | "The bound tightens; therefore, the variance shrinks." |

## Paragraph Coherence and Redundancy

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `paragraph.topic_sentence` | Topic sentence strength | Scores early sentences for paragraph-centrality and penalizes opener-only transitions as topic candidates. | Paragraph opens with setup detail only | First sentence states the governing claim |
| `paragraph.parallelism` | List-frame parallelism | Non-parallel list frames slow scanning and weaken structure. | Mixed verb/noun list items | Align all list items to one frame |
| `paragraph.inline_enumeration_overload` | Inline enumeration overload | Dense inline lists are hard to scan and hide item boundaries. | "We consider (i) ..., (ii) ..., (iii) ..." | Lead-in sentence + bullet list |
| `paragraph.inline_case_split` | Inline case split control | Case distinctions packed into one sentence reduce comparability and increase parsing load. | "When X ...; when Y ..." | Lead-in sentence + explicit case bullets |
| `paragraph.double_framing` | Double-framing control | Framing both the lead-in and each list item repeats rhetorical scaffolding without adding content. | "This section provides ...: - This point ... - This point ..." | Keep framing in the lead-in; make items directly informative |
| `paragraph.lexical_repetition` | Non-adjacent restatement detection | Flags high-overlap non-adjacent sentence pairs when the later sentence does not add clear support signals. | "Claim X. [intervening sentence]. Claim X." | Keep one formulation and add genuinely new contribution |
| `paragraph.concept_reference_drift` | Concept label stability | Flags paragraphs that rotate labels for likely the same referent while sentence overlap suggests shared meaning. | "the method ... the approach ... the framework ..." | Keep one canonical label for one concept |
| `paragraph.reformulation_inflation` | Reformulation inflation control | Flags reformulation markers ("in other words", "equivalently", etc.) when adjacent overlap is high and support signals are absent. | "Claim X. In other words, Claim X." | Replace restatement with evidence, scope, or consequence |
| `paragraph.sentence_redundancy` | Adjacent sentence redundancy | Back-to-back restatements reduce information density. | Two adjacent sentences restate same claim | Keep one and add new support |
| `paragraph.paragraph_redundancy` | Cross-paragraph redundancy | Repeated paragraphs waste space and blur progression. | Two paragraphs state same result | Merge or differentiate roles |
| `paragraph.vague_rhetorical_opener` | Vague rhetorical opener control *(experimental)* | Vague rhetorical lead-ins delay the claim without adding technical content. | "In this context, ..." / "It should be noted that ..." | Start with the concrete claim or operation |

## Document Structure and Navigation

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `structure.heading_parallelism` | Heading frame parallelism | Sibling headings should present a consistent grammatical frame. | "Define Objects" / "Main Result" / "Applying the Theorem" | Normalize to one frame type |
| `structure.heading_capitalization` | Heading capitalization consistency | Mixed heading styles create visual and navigational friction. | "Main Result" / "Main derivation" | Apply one style across siblings |
| `structure.heading_level_skip` | Heading-level continuity | Skipping heading depth (for example H1 → H3) breaks navigational hierarchy. | `# Setup` then `### Details` | Insert `##` intermediate level |
| `structure.section_balance` | Section balance | Severe length imbalance often signals argument underdevelopment. | One section is much longer than all siblings | Redistribute material or split scope |
| `structure.section_order_sequence` | Reader-sequence ordering | Purpose and usage context should appear before setup/configuration/advanced sections. | `Installation` before `Overview` | Move overview/purpose first, then setup and advanced details |
| `structure.section_opener_block_kind` | Section opener framing | Sections should open with purpose-oriented prose before blocked structured blocks or definition-style openers; heading levels and blocked block kinds are configurable. | Heading followed immediately by display math, list, table, code block, or definition-style opener | Start with one sentence stating the section question/strategy |
| `structure.opening_sentence_presence` | Opening sentence presence | Documents should begin with one purpose sentence before configured structured content block kinds. | File starts with a list/table/code/display block | Add one opening sentence before structured content |
| `structure.opening_message_focus` | Opening-message focus | Opening sentence should communicate one core purpose before dense enumeration. | "Clear, concise, convincing, ... prose matters." | State one purpose sentence, then enumerate supporting dimensions |
| `structure.orphan_section` | Orphan-section shell detection | A heading with one direct child and little parent prose weakens hierarchy clarity. | `# Methods` followed only by `## Algorithm` | Merge shell heading or add parent-level framing prose |
| `structure.prose_outside_heading` | Prose-under-heading discipline | Significant prose before any heading weakens document structure. | Long paragraph appears before first heading | Move prose under an explicit heading |

## Audience Fit and Evidence Discipline

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `audience.definition_before_use` | Define before first use | Checks first symbol use against local definition signals (markers, assignment/copula patterns, symbol-binding frames). | "Substitute in \(T(x)\) ..." with no local definition | Define \(T\) at first mention |
| `audience.acronym_burden` | Acronym definition and dominance | Flags acronyms used before local definition and acronyms that over-dominate their full forms in running prose. | "The PDE ..." with no prior expansion, or repeated "PDE" after one expansion | Expand first, then keep full form primary in prose |
| `audience.jargon_density` | Jargon density by audience | Dense specialist jargon can exclude target readers. | Jargon-heavy sentence in learner profile | Replace or define terms |
| `audience.claim_calibration` | Claim-evidence calibration | Strong claims should carry nearby support cues. | "This clearly proves ..." with no support signal | Add citation, equation, or result reference |
| `audience.qualitative_claim_without_quant_support` | Qualitative claim support | Qualitative performance/stability claims should include nearby quantitative support cues. | "The method is robust across settings." | Add bound, estimate, theorem/equation reference, or citation |
| `audience.imprecise_quantifier_without_citation` | Imprecise-quantifier citation support | Quantifiers like "several" or "others" should be evidence-backed. | "Several methods succeed while others fail." | Add citation or replace with specific sourced claims |

## Mathematical Exposition

| Rule ID | Rule Name | Rationale | Violation | Preferred |
| --- | --- | --- | --- | --- |
| `math.display_math` | Display math lead-in and punctuation | Readers need to know what an equation is doing before they parse symbols, and line-boundary punctuation should stay in prose. | `Therefore:` then `$$ A_1(g)=\cdots , $$` | "Substituting into the lower bound yields:" then `$$ A_1(g)=\cdots $$` |
| `math.display_ambiguous` | Display delimiter disambiguation | Multiple display delimiters on one line make equation boundaries unclear. | "`$$ A(g)=\cdots $$ $$`" | Put each equation in its own `$$...$$` block |
| `math.display_unclosed` | Display delimiter closure | An unclosed display block breaks both readability and parser structure. | `$$` then equation lines with no closing delimiter | Add the matching closing `$$` |
| `math.display_followup_interpretation` | Post-display interpretation | Non-trivial display formulas should be followed by interpretive prose that states role or consequence. | Display equation followed by "The claim is immediate." | Follow with a sentence naming what the formula represents or controls |
| `math.consecutive_display_blocks_without_bridge` | Consecutive-display bridge | Chains of display equations need one motivating bridge sentence. | Two or more consecutive display blocks with no stated purpose | Add one motivation sentence before the chain |
| `math.inline_math` | Equation-like inline math control | Long or equation-like inline math burdens sentence parsing and hides argumentative structure. | "We use \(A_1(g)=\frac{g}{1-g\lambda_1}\) in the argument." | "The dominant amplification factor satisfies:" then `$$ A_1(g)=\frac{g}{1-g\lambda_1} $$` |
| `math.bare_symbol` | Bare symbol qualifier control | Qualifier/prepositional phrases should name mathematical objects. | "growth in \(P\)" with no object context | "growth in the power function \(P\)" |
| `math.shorthand` | Shorthand-introduction restraint | New notation has cognitive cost and should pay for itself through repeated use. | Introduce `\(\rho := \|\mathbf{u}\|\)` once and never reuse it | Keep `\(\|\mathbf{u}\|\)` inline unless the shorthand is reused substantially |
| `math.assumption_motivation_order` | Assumption motivation ordering | Assumptions should be introduced by purpose, not stated without role context. | "Assume the sequence is bounded." | "To ensure stability, assume the sequence is bounded." |
| `math.imperative_opening` | Imperative opening avoidance | Imperative proof prose can read as shorthand rather than explanation. | "Let \(x\in X\)" | "For any fixed input \(x\in X\)" |
| `math.prose_math` | Prose relation paraphrase control | Prose paraphrases of formal relations add words while reducing precision. | "Since \(x\) times \(y\) equals 1" / "the term is of order \(n^{-1}\)" | "Since \(xy=1\)" / "\(f(n)=\mathcal{O}(n^{-1})\)" |
| `math.proof_marker` | Proof marker opener requirement | A closing marker without a proof opener leaves proof scope implicit. | Body text ends with `□` but no opening | Open with `*Proof.*`, then close with `□` |
| `math.proof_placement_context` | Proof placement context | Proof opener should follow at least one interpretive bridge after formal statements. | "Lemma ... ." immediately followed by "Proof." | Insert a short interpretive paragraph before proof |

## Notes

- Profiles control which rules run by default.
- Rule options, severities, and weights are configurable.
- Most language-sensitive pattern inventories are provided by the active language pack.
- See [Configuration](configuration.md) for activation and override semantics.
