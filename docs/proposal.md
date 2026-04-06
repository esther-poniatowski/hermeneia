# Consolidated Proposal: A Profile-Aware, Stratified Writing Diagnostics Engine

---

## 1. Problem Statement

### 1.1 The Target Quality Criterion

The writing materials under consideration — research notes, lecture expositions, pedagogical explanations — share a common and demanding requirement: the simultaneous maintenance of conceptual depth and expositional accessibility. These two properties are not in natural tension, but they demand a writing style that departs systematically from the conventions of research articles and academic textbooks. Academic prose, optimized for peer-reviewed publication, prioritizes exhaustive qualification, nominal density, and syntactic complexity over the communicative properties that facilitate knowledge transfer to diverse audiences. The writer's materials must instead prioritize reader expectation management, fluidity at the discourse level, and conceptual sequencing calibrated to the target reader's prior knowledge — without sacrificing the precision required by technically demanding content.

### 1.2 The Failure Mode of AI-Assisted Editing

Generative language models, when deployed as writing auditors or revision agents, systematically reproduce the very conventions that the present tool must circumvent. The mechanism is structurally explicable: reinforcement learning from human feedback (RLHF) reward models, trained predominantly on annotators familiar with academic and professional registers, incentivize fluency as those annotators define it — that is, the lexical density, nominalization patterns, and hedging conventions characteristic of formal research prose. The consequence is a systematic regression toward the academic mean: either the model preserves technical depth by reinforcing opaque syntax, or it increases apparent accessibility by reducing conceptual specificity. The intersection of depth and accessibility is outside the distribution the model has been trained to reward.

This failure is not principally a model capability limitation. It is a prompt-specification and evaluation-criteria failure. The model's implicit rubric differs from the writer's explicit one. Correcting this failure therefore requires the explicit formalization of the writer's own criteria, injected as structured constraints rather than left as implicit defaults. This observation is foundational to the present architecture.

### 1.3 The Case for Explicit, Programmatic Criteria

The alternative pursued here is a programmatic encoding of observable writing-quality criteria into a structured, auditable rule system. This approach is motivated by two convergent considerations. First, a substantial body of reader-centered rhetoric, plain-language research, and computational discourse analysis has already demonstrated that a significant proportion of writing quality is expressible as detectable, operational regularities — sentence-level syntactic patterns, paragraph-level discourse structures, document-level redundancy clusters. These regularities are assessable without delegating judgment to an unconstrained generative agent. Second, programmatic encoding ensures reproducibility, configurability, and transparency: each diagnostic finding is traceable to a declared rule, each rule is parameterizable by context profile, and the full system behavior is inspectable without opaque inference.

---

## 2. Design Goals

The tool pursues four primary objectives:

**Detection.** Given a text, the system identifies formulations that violate declared quality criteria at the sentence, paragraph, or document level. Each detected violation is attributed to a specific rule, assigned a severity grade, and localized to a text span.

**Suggestion.** For each detected violation, the system proposes one or more concrete revision tactics — ranging from template-based syntactic rewrites (for determinate violation types) to rubric-constrained regenerative suggestions (for semantically complex violations).

**Global structural analysis.** Beyond local violations, the system characterizes macro-level properties of the text: redundancy across paragraphs, structural incoherence in heading organization, misalignment between abstract and body, and degradation of topic progression across sections.

**Configurability and auditability.** All active rules, their severity thresholds, and their context-conditional modulations are declared in a normalized schema. No rule is implicit or hard-coded. The system's behavior is fully reproducible across runs and fully modifiable by the writer without code modification.

---

## 3. Theoretical Foundations

Before specifying the architecture, it is necessary to establish the theoretical basis from which the rule inventory derives its authority. The system is not grounded in a single tradition but in a convergent multi-source framework.

**Reader-expectation principles (Gopen).** The primary organizing principle for fluidity at the sentence and paragraph level is the management of reader expectation. Readers of English process text by assigning interpretive weight according to structural position: the topic position (sentence-initial constituents) signals what the sentence is about and anchors new information to known context; the stress position (sentence-final constituents) carries new, emphasized information. Violations of these positional conventions produce local comprehension failures that accumulate into perceived opaqueness. This framework operationalizes fluidity as a set of structural constraints on information placement, not as a vague stylistic preference.

**Rhetorical move analysis (Swales, Academic Phrasebank).** At the paragraph and section level, writing quality is analyzable in terms of rhetorical moves — conventionalized communicative acts that serve identifiable functions within a discourse genre. The presence, absence, or misplacement of expected moves produces discourse-level failures invisible to sentence-level analyzers. The analytical unit is the move sequence, not the individual sentence.

**Cohesion and discourse analysis (Coh-Metrix).** Classical readability formulas — Flesch Reading Ease, Gunning Fog, Flesch-Kincaid Grade Level — measure surface proxies (sentence length, syllabic complexity) that correlate weakly with actual comprehension difficulty. The Coh-Metrix framework demonstrated empirically that cohesion properties, referential continuity, and discourse connective structure predict comprehension outcomes substantially better than surface-length indices. The present system treats readability scores as secondary diagnostic features, not primary quality objectives.

**Plain-language conventions.** Official plain-language guidance formalizes a set of surface conventions — active voice preference, subject-verb proximity, one-topic paragraphs, defined acronyms — that are empirically associated with improved comprehension across general audiences. These conventions are treated as profile-dependent defaults, not universal mandates: their appropriate weighting varies by genre, audience, and section function.

---

## 4. Core Architectural Principle: Computational Tractability Stratification

The most consequential design decision is the classification of all criteria by their *computational tractability class* prior to implementation. Conflating criteria of fundamentally different computational character into a single processing pipeline produces an architecture whose implementation boundary is undefined and whose failure modes are entangled. The stratification below governs module assignment throughout the system.

**Class A — Fully deterministic (lexical and syntactic surface rules).** These criteria are computable with zero semantic ambiguity via lexical pattern matching, part-of-speech (POS) tag sequences, or dependency-parse queries. No language understanding beyond syntactic annotation is required. Representative criteria include: mean and variance of sentence length, passive-voice ratio (identified by `auxiliary be` + past participle dependency arc), nominalization density (suffix pattern matching against a nominalization lexicon: *-tion, -ment, -ance, -ity, -ness*), prepositional-phrase chain length, hedge-word and transition-word catalogue membership, contraction and compound-noun detection, and the standard readability indices. These criteria are fully unit-testable and introduce no stochastic behavior.

**Class B — Shallow NLP (syntactic parsing, coreference, or discourse tagging).** These criteria require syntactic dependency graphs or coreference resolution output but do not require semantic representation of propositional content. Representative criteria include: subject-verb token distance in the dependency tree (distance between the `nsubj` arc and the root verb node), subordinate clause count per sentence, pronoun-to-referent coreference chain coherence across adjacent sentences, parallelism detection (repeated syntactic frames in coordinated structures), and sentence-initial topic continuity (comparison of the syntactic subject constituent across consecutive sentences). These criteria are implementable with spaCy-level tooling and remain deterministic conditioned on parser output.

**Class C — Semantically irreducible.** These criteria cannot be evaluated without a representation of propositional meaning, not merely syntactic form. Representative criteria include: conceptual redundancy across paragraphs (whether two paragraphs express semantically equivalent propositions), topic-stress chain progression (whether the stress constituent of one sentence is coherently continued in the topic position of the next), whether a topic sentence correctly announces the paragraph's content, judgment-trap detection in context (the lexeme "shortcoming" is not invariably a judgment trap; its status is context-dependent), and appropriateness of hedge words relative to the epistemic strength of the accompanying claim. These criteria require language understanding that, in practice, necessitates a language model — but a *constrained and rubric-specified* one, not a free generative agent.

This stratification resolves the apparent contradiction in the proposal's motivation. The proposal correctly rejects unconstrained AI agents for writing assessment; it does not thereby reject language models as a component. Class C criteria cannot be assessed deterministically, but they can be assessed by a language model operating under a precisely specified rubric — one whose content is derived from the writer's own explicit criteria. The failure mode identified in the motivation (regression toward academic register) results from an underspecified evaluation rubric, not from the deployment of neural processing per se. The two-module architecture described in Section 6 implements this resolution.

---

## 5. Layered Fault Model

Detection operates across five analytically distinct layers. Each layer addresses a qualitatively different class of writing failure; each requires different detection mechanisms; and each produces different revision implications. The ordering is not merely taxonomic — it reflects a dependency structure: structural faults at higher layers propagate downward, making local sentence-level rewrites futile until the macro-structure is corrected. Revision suggestions must respect this dependency order, as detailed in Section 8.

**Layer 1 — Surface style.** Objective: local clarity and concision at the sub-sentence level. Typical faults: passive voice in topic position, nominalization with weak verb support, noun cluster density, excessive prepositional chaining, overlong sentences (deviation from the register-appropriate target length). Detection mode: Class A rules exclusively.

**Layer 2 — Local discourse.** Objective: sentence-to-sentence flow and information management. Typical faults: buried stress position (emphasized information not placed sentence-finally), topic-position ambiguity, subject-verb separation exceeding the register-appropriate token threshold, unclear pronominal reference, absent topic-stress chain between adjacent sentences. Detection mode: Class B primarily, with Class C involvement for topic-stress chain analysis.

**Layer 3 — Paragraph rhetoric.** Objective: paragraph-level coherence and move structure. Typical faults: absent or misplaced topic sentence, mixed topics within a single paragraph, digressions interrupting topic progression, absent or inappropriate rhetorical move for the section function, rhythm failures (absence of sentence-length variation). Detection mode: Class B for topic-sentence position; Class C for content-based move identification and topic consistency.

**Layer 4 — Document structure.** Objective: global organization and structural integrity. Typical faults: orphan headings (sections with a single subsection), non-parallel heading syntax across siblings, title-to-abstract semantic misalignment, redundancy clusters (paragraphs sharing high semantic similarity), asymmetric section weighting relative to stated purpose. Detection mode: Class C exclusively, with semantic similarity measures for redundancy detection.

**Layer 5 — Audience fit.** Objective: register and accessibility calibration relative to the declared target audience and genre. Typical faults: undefined technical terms before first use, acronym overload (defined at first use but excessively dense thereafter), insufficient hedging for uncertain claims, overclaiming relative to evidence, jargon density mismatched to audience profile. Detection mode: Class A for acronym tracking and hedge-word presence; Class C for claim-calibration and jargon appropriateness judgments.

---

## 6. System Architecture

The system comprises six principal modules. Their interfaces are defined by typed data structures; no module depends on the internal implementation of any other.

```
WritingAuditor
├── Preprocessor
│   ├── Tokenizer / Sentence Segmenter
│   ├── POS Tagger
│   ├── Dependency Parser
│   └── Coreference Resolver
│
├── ProfileResolver
│   ├── AudienceProfile         { specialist | interdisciplinary | student | public }
│   ├── GenreProfile            { research_note | article | lecture_note | tutorial | abstract }
│   ├── SectionProfile          { introduction | method | result | discussion | caption }
│   └── RegisterProfile         { plain_language | reader_centered_academic | pedagogical }
│
├── RuleEngine                  [Class A + Class B — fully deterministic]
│   ├── Layer1_SurfaceRules
│   │   ├── SentenceLengthDetector
│   │   ├── PassiveVoiceDetector
│   │   ├── NominalizationDetector
│   │   ├── PrepositionalChainDetector
│   │   └── NounClusterDetector
│   ├── Layer2_LocalDiscourseRules
│   │   ├── SubjectVerbDistanceDetector
│   │   ├── SubordinateClauseCounter
│   │   ├── StressPositionAnalyzer
│   │   └── CoreferenceCoherenceChecker
│   └── Layer3_ParagraphRules
│       ├── TopicSentencePositionChecker
│       ├── ParallelismDetector
│       └── LexicalRepetitionAuditor
│
├── SemanticAuditor             [Class C — constrained LLM with injected rubric]
│   ├── TopicProgressionAnalyzer
│   │   └── modes: { CONSTANT_TOPIC | CHAIN | TOPIC_TO_SUBTOPIC }
│   ├── ConceptualRedundancyDetector    [Layers 3–4]
│   ├── RhetoricalMoveClassifier        [Layer 3]
│   ├── AudienceFitEvaluator            [Layer 5]
│   └── ClaimCalibrationAuditor         [Layer 5]
│
├── SuggestionEngine
│   ├── TemplateRewriter        [Class A violations: deterministic syntactic transforms]
│   └── ConstrainedGenerativeRewriter   [Class B/C violations: rubric-injected LLM]
│
├── HierarchicalScorer
│   ├── LayerScorers            [per-layer weighted aggregation]
│   ├── ContextProfileApplier   [threshold modulation per ProfileResolver output]
│   └── GlobalScoreAggregator   [hierarchical composition: sentence → paragraph → document]
│
└── ReportGenerator
    ├── DiagnosticReport        [ranked violations by severity and layer]
    ├── SpanAnnotations         [localized fault markers on input text]
    └── RevisionPlan            [ordered revision operations per dependency structure]
```

### 6.1 The Preprocessor

The Preprocessor produces a typed annotation object from raw text input: tokenized and sentence-segmented text, POS tags (Universal Dependencies tagset), a dependency parse tree per sentence, and a within-document coreference chain set. All downstream modules operate on this annotation object; no module performs raw text access. This strict interface ensures that annotation quality failures are localized to a single module.

### 6.2 The ProfileResolver

Before any rule is evaluated, the ProfileResolver reads the declared context configuration and produces a resolved profile that parameterizes all subsequent processing. The profile determines: which rules are active; what threshold values apply; what severity grades are assigned to given violation magnitudes; and whether suggestion generation is enabled for a given rule. The profile is the mechanism through which the same rule inventory produces qualitatively different assessments for a pedagogical explanation versus a research note.

### 6.3 The RuleEngine

The RuleEngine implements all Class A and Class B detectors. Each detector takes the preprocessed annotation object and the resolved profile as input and produces a typed `Violation` object or null. The RuleEngine is the only module that carries a strict no-stochasticity guarantee: given identical input and profile, it produces identical output. This property is essential for reproducibility and for regression testing of the rule inventory.

### 6.4 The SemanticAuditor

The SemanticAuditor handles all Class C criteria. Crucially, it is not a free generative agent. It operates as a *constrained classifier and annotator*, not a prose generator. The language model it invokes receives a structured system prompt that encodes the writer's explicit quality rubric — the full set of active Layer 3–5 criteria expressed as evaluation dimensions with contrastive examples — and is instructed to return a structured JSON annotation, not free prose. The model's response is parsed deterministically; if parsing fails, the SemanticAuditor returns a null result (not a fallback text). This design localizes non-determinism to a bounded, auditable subsystem whose inputs and outputs are typed and logged.

The rubric injected into the SemanticAuditor is derived directly from the normalized rule inventory (Section 7), ensuring that the semantic auditor's evaluation criteria are identical in content to those of the RuleEngine, merely expressed in natural-language form for the model to apply.

### 6.5 The SuggestionEngine

The SuggestionEngine is invoked only after detection is complete — never during detection. It operates in two modes. For Class A violations, the TemplateRewriter applies deterministic syntactic transforms: nominalization reversal (e.g., `nominalization + weak verb → verbal form`), sentence splitting at coordinating conjunctions, passive-to-active actor insertion where the actor is recoverable from context. For Class B and Class C violations, the ConstrainedGenerativeRewriter invokes a language model under the same rubric-injection protocol as the SemanticAuditor, constrained to return a revised text span, a one-sentence rationale, and the specific criterion the revision addresses.

### 6.6 The HierarchicalScorer

Rather than aggregating all violations into a single scalar quality score — which erases the structural information essential for targeted revision — the HierarchicalScorer computes a score vector indexed by layer. At each layer, violations are aggregated by a weighted sum, where weights are declared in the configuration schema (Section 7) and are modulated by the resolved profile. The document-level score is a weighted composition of layer scores. The hierarchical structure means the writer can inspect both a global quality indicator and a per-layer breakdown, identifying whether failures are concentrated at the surface, the discourse, or the structural level.

Threshold values are not universal constants. Sentence length, for example, is assessed against a register-appropriate target $\mu_{\text{profile}}$ with a tolerance $\sigma_{\text{profile}}$:

$$
\text{score}_{\text{length}}(s) = \max\left(0,\ \frac{|l_s - \mu_{\text{profile}}| - \sigma_{\text{profile}}}{\sigma_{\text{profile}}}\right)
$$

where $l_s$ is the word count of sentence $s$. This continuous formulation avoids the discontinuities of binary threshold violations and supports smooth severity grading.

---

## 7. Rule Formalization: The Normalized Rule Schema

Every criterion in the rule inventory — whether a Class A surface heuristic or a Class C discourse judgment — is declared as a normalized rule object conforming to a common schema. The rule object is the unit of configuration, the unit of documentation, and the unit of evaluation. No rule exists outside this schema; no implicit or hard-coded behavior is permitted.

```yaml
id:               discourse.subject_verb_distance
label:            Subject and main verb are too far apart
layer:            local_discourse          # { surface_style | local_discourse |
                                           #   paragraph_rhetoric | document_structure | audience_fit }
tractability:     class_b                 # { class_a | class_b | class_c }
kind:             soft_heuristic          # { hard_constraint | soft_heuristic | diagnostic_metric |
                                           #   rhetorical_expectation | rewrite_tactic }
default_severity: warning                 # { info | warning | error }
profiles_active:
  - generalist
  - pedagogical
  - interdisciplinary
detector:
  method:         dependency_distance
  arc:            nsubj_to_root
  threshold:
    default:      8                       # tokens
    pedagogical:  6
    research_note: 10
exceptions:
  - mathematical_definition
  - caption_fragment
  - enumeration_item
rationale:
  principles:
    - reader_expectation_gopen
    - plain_language_opm
message: >
  The grammatical subject and the main verb are separated by {distance} tokens.
  This gap delays the reader's processing of the predication. Move intervening
  material to a preceding sentence or a following subordinate clause.
rewrite_tactics:
  - split_intervening_clause
  - move_context_to_prior_sentence
  - frontload_actor
suggestion_mode: template               # { template | constrained_generative | none }
weight:           0.7                   # contribution to layer score aggregation
evaluation:
  true_positive_examples:
    - "The results, which had been obtained using the revised experimental protocol described in Section 3, confirm the hypothesis."
  false_positive_examples:
    - "The matrix $A$, defined as $A_{ij} = \delta_{ij} \lambda_i$, is diagonal."
```

This schema enforces the separation of concerns required for a maintainable rule inventory. The `tractability` field determines the module to which the rule is dispatched. The `kind` field determines how the score is interpreted. The `profiles_active` field implements the profile-conditional behavior without branching logic in the engine. The `exceptions` field encodes domain-specific immunity conditions. The `evaluation` field provides the minimum substrate for per-rule precision testing.

---

## 8. Revision Pipeline and Dependency Order

FIX: The tool must not perform modifications in the source file. It must only produce a revision
plan that the writer can choose to implement. Therefore, he "revision pipeline" below must be reformulated as a "revision plan generator" that produces an ordered list of revision operations, each linked to specific violations and their corresponding criteria.

The three-step rewriting protocol (Reorganize → Link → Rewrite locally) represents a correct dependency ordering, but requires operationalization to be executable. The following decomposition converts each abstract step into a sequence of testable sub-operations.

**Step 1 — Reorganize (document and paragraph structure).**
Sub-operations: (a) identify redundancy clusters via semantic similarity thresholding across paragraphs; (b) flag mixed-topic paragraphs via topic sentence mismatch detection; (c) verify heading parallelism and orphan section absence; (d) assess abstract-to-body alignment via semantic embedding comparison; (e) produce a structural revision plan as an ordered sequence of typed operations (`MERGE_PARAGRAPHS`, `SPLIT_PARAGRAPH`, `REORDER_SECTION`, `DELETE_REDUNDANT_CLUSTER`). No sentence-level rewriting is proposed at this step.

**Step 2 — Link (discourse and sentence chaining).**
Sub-operations, applied only after Step 1 operations are resolved: (a) verify topic-stress chain continuity between adjacent sentences; (b) identify and flag implicit discourse transitions where inferential gaps are present; (c) repair pronominal reference ambiguity by flagging underspecified antecedents; (d) ensure old information occupies topic position across sentence boundaries.

**Step 3 — Rewrite locally (surface style).**
Sub-operations, applied only after Steps 1 and 2 operations are resolved: (a) reverse targeted nominalizations; (b) convert unjustified passive constructions; (c) split overloaded sentences at the dependency parse level; (d) reduce prepositional chain length via verb strengthening; (e) reduce subject-verb distance by extracting intervening clauses.

This ordering is not merely organizational. Applying Step 3 before Step 1 optimizes syntax within a structurally deficient macro-architecture, producing locally improved sentences that still fail to communicate the intended argument. The pipeline enforces the correct precedence.

---

## 9. Criterion Inventory: Revisions to the Original Checklist

The original checklist requires revision on three grounds: certain criteria are reformulated for operational precision; certain criteria are demoted or removed on theoretical and empirical grounds; and a set of criteria absent from the original inventory must be added.

### 9.1 Criteria Retained and Reformulated

- **Sentence length** is retained as a distributional metric, not a single average. The system monitors mean, median, and the proportion of sentences exceeding the profile-specific threshold. The register-appropriate target is profile-parameterized, not universal.
- **Passive voice** is retained as a conditional warning, not a blanket prohibition. The active-passive decision is assessed relative to section function and actor availability. Passive voice in methods sections with suppressed actor is not penalized under the `research_note` or `article` profiles.
- **Nominalization** is retained, but detection targets only harmful cases: nominalization paired with a semantically weak verbal support (e.g., *perform a measurement of* versus *measure*). Standalone nominalizations functioning as technical terms are excluded.
- **Topic-stress progression** is elevated to a first-class discourse module within the SemanticAuditor, replacing its current status as a marginal annotation.
- **Paragraph topic sentence** is retained and formalized as a paragraph-role position constraint: the topic sentence must occupy the first or second sentence of the paragraph in all non-exception contexts.

### 9.2 Criteria Demoted or Removed

- **"Prefer monosyllabic Saxon nouns"** is removed. The criterion is etymologically crude, corpus-dependent, and inapplicable to specialist prose where polysyllabic technical terms are precisely the appropriate lexical choices.
- **"Use catchy words in title and abstract"** is separated into a distinct *discoverability module* that is orthogonal to the clarity and fluidity objectives of the main system. It must not influence the clarity score.
- **"Avoid dangerous transition words"** is replaced by a *discourse relation auditor* that detects unsupported inferential or causal jumps — the actual failure the criterion targets. The problem is not the token *therefore*; it is the absence of an explicit warrant for the inferred relation.
- **"Style: positively charged"** is replaced by **constructive and calibrated evaluative language**, formalized as a combination of judgment-trap lexicon detection (Class A) and claim-calibration auditing (Class C).
- **Gunning Fog Index** is retained as a secondary diagnostic metric, but with the corrected formula:

$$
\text{GFI} = 0.4 \left( \frac{N_{\text{words}}}{N_{\text{sentences}}} + 100 \cdot \frac{N_{\text{complex}}}{N_{\text{words}}} \right)
$$

where $N_{\text{complex}}$ counts words of three or more syllables, excluding proper nouns, compound familiar words, and two-syllable verb forms created by *-ed* or *-es* suffixation.

### 9.3 Criteria Added

The following criteria are absent from the original inventory and must be incorporated:

- Referential clarity: pronoun-to-referent distance and uniqueness within the coreference chain.
- Acronym burden: definition-lag detection (acronym used before first definition) and density monitoring (acronym-to-word ratio per paragraph).
- Noun cluster density: sequences of three or more consecutive nouns in a noun-phrase head chain.
- Local lexical cohesion: lexical overlap coefficient between adjacent sentences as a proxy for topic continuity.
- Semantic redundancy: cosine similarity between paragraph embedding vectors, flagging pairs above a profile-specific threshold.
- Heading parallelism: syntactic frame consistency across sibling headings at the same structural level.
- Abstract-to-body alignment: semantic similarity between abstract content and the corresponding section content.
- Claim-evidence calibration: detection of strong epistemic claims (absence of hedges) where the evidence base is not signaled.
- Definition-before-use: detection of technical terms used before their first definition within the document.

---

## 10. Configuration Schema Architecture

The system's behavior is entirely governed by a declarative configuration file, not by code-level parameters. The configuration file declares: the active profile; the set of active rule identifiers; per-rule threshold overrides; per-rule weight overrides; the suggestion mode for each rule; and the output format. An illustrative top-level structure:

```yaml
profile:
  audience:  interdisciplinary
  genre:     lecture_note
  section:   introduction
  register:  pedagogical

rules:
  active:
    - surface.sentence_length
    - surface.passive_voice
    - surface.nominalization
    - discourse.subject_verb_distance
    - discourse.stress_position
    - paragraph.topic_sentence_position
    - document.semantic_redundancy
    - audience.acronym_burden
  overrides:
    surface.sentence_length:
      threshold.default: 18
      weight: 0.9
    surface.passive_voice:
      severity: info

scoring:
  aggregation: hierarchical
  output: [layer_scores, global_score, violation_list]

suggestions:
  enabled: true
  modes:
    class_a: template
    class_b: constrained_generative
    class_c: constrained_generative

reporting:
  format: annotated_markdown
  sort_by: severity_desc
```

This configuration-as-data design, analogous to the rule declaration schemas used by Vale and LanguageTool, ensures that the system is reconfigurable without code modification and that distinct configurations for research notes, lecture slides, and tutorial expositions are maintainable as versioned artifacts.

---

## 11. Evaluation Methodology

The tool cannot be evaluated by face validity alone. A gold-standard evaluation corpus is the minimum viable substrate. The following protocol defines the evaluation methodology.

**Corpus construction.** A representative set of the writer's own texts — spanning research notes, lecture materials, and pedagogical expositions — is collected. For each text, a revised version is produced by the writer, with explicit annotations of the specific violations corrected and the criterion motivating each correction. This yields a corpus of `(original, revised, annotation)` triples.

**Per-rule precision measurement.** For each rule, precision is defined as the proportion of system-flagged violations that correspond to annotated violations in the gold standard. Precision is evaluated before recall: in a writing assistance context, false positives (spurious flags) are more damaging than missed detections, because they erode the writer's trust in the system and introduce revision overhead. A rule whose precision falls below a declared threshold is demoted to `info` severity or deactivated.

**Hierarchical evaluation.** Evaluation is conducted separately per layer. A surface-layer detector with high precision but low recall is not penalized by paragraph-level failures; the two layers address different phenomena and require independent calibration.

**Suggestion acceptance rate.** For each suggestion produced by the SuggestionEngine, the writer's acceptance or rejection is logged. Acceptance rate, stratified by rule and by suggestion mode (template versus constrained generative), is the primary quality metric for the SuggestionEngine. Low acceptance rates for constrained generative suggestions indicate rubric misspecification, not model incapability.

**Comparative baseline.** The system's precision and acceptance rate are compared against three baselines: classical readability formula output alone, a commercial prose linter (Readable or equivalent), and an unconstrained generative agent. The purpose is to establish that the constrained, stratified architecture materially outperforms both the purely deterministic baseline and the unconstrained AI baseline on the writer's own annotation corpus.

---

## 12. Summary of Architectural Decisions

The table below consolidates the principal design decisions and their motivating rationale.

| Decision | Specification | Rationale |
|---|---|---|
| Tractability stratification | All criteria classified as Class A, B, or C before implementation | Prevents undefined implementation boundaries; isolates stochastic behavior |
| Two-module detection | RuleEngine (A+B, deterministic) + SemanticAuditor (C, constrained LLM) | Resolves anti-AI motivation while accommodating semantically irreducible criteria |
| Rubric injection | SemanticAuditor system prompt derived from normalized rule inventory | Eliminates academic-register bias; makes LLM evaluation criteria identical to declared criteria |
| Profile layer | All thresholds and active rules modulated by resolved profile | Prevents over-prescription; adapts system to genre, audience, and section function |
| Separated detection and suggestion | SuggestionEngine invoked only after full detection pass | Prevents syntactic optimization within deficient macro-structure; enables independent evaluation |
| Hierarchical scoring | Layer-specific score vector, not scalar global score | Preserves structural diagnostic information; enables targeted revision |
| Dependency-ordered revision pipeline | Reorganize → Link → Rewrite locally | Enforces correct revision precedence; avoids local optimization in poor macro-structure |
| Normalized rule schema | Every criterion declared as typed YAML object | Enforces auditability, configurability, and per-rule unit testing |
| Gold-standard evaluation | Annotated corpus of writer's own texts | Prevents face-validity evaluation; grounds precision measurement in actual use |

---

## See Also

- The [initial proposal](docs/reference/initial-proposal.md) that motivated this design. It contains
  essential references and a preliminary checklist of criteria that the current proposal refines and
  expands.

- Various instruction files specifying writing standards have been gathered from the writer's own
  teaching materials and research notes. Some may be redundant or inconsistent, but may serve as a useful starting point for the rule inventory. They include:
  - [Writing standards](docs/reference/writing-standards.md)
  - [Documentation-specific standards](docs/reference/audit-documentation.md)
  - [Mathematical-specific standards](docs/reference/math-pedagogy.md)
  - [Hard rules](docs/reference/hard-rules.md)

- Initial [python implementation](docs/reference/lint-rules-reference.py) for mathematical writing.
  This python code is a monolothic implementation of a subset of the criteria focused on
  mathematical writing. The current proposal generalizes and refactors this code into a modular
  architecture with a broader criterion inventory.
