# Consolidated Proposal: A Profile-Aware, Stratified Writing Diagnostics Engine

**Authority relationship.** This document provides the theoretical motivation, criterion justification, and evaluation methodology for hermeneia. `docs/adr/architecture-plan.md` is the implementation specification. Where they overlap (tractability tiers, module decomposition, rule schema, phasing), the architecture plan is authoritative for implementation decisions. This document is authoritative for theoretical grounding, design rationale, and evaluation design. If a future edit introduces a contradiction, the architecture plan governs code and this document governs intent.

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

**Suggestion.** For each detected violation, the system proposes one or more concrete revision tactics — ranging from template-based syntactic rewrites for determinate cases to higher-level tactic suggestions where full rewriting would be underdetermined. Constrained generative rewriting remains a future extension, not a v1 assumption.

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

The most consequential design decision is still the classification of criteria by computational tractability before implementation. The earlier A/B/C split, however, was too narrow: it collapsed bounded semantic heuristics into the same bucket as full semantic judgment and therefore overstated what must be deferred to a language model.

The revised stratification is:

**Class A — Fully deterministic surface and structural rules.** These criteria are computable via lexical pattern matching, exact structural context, formulaic counting, or bounded syntactic queries with no semantic fusion step. Representative criteria include sentence-length distribution, contraction bans, inline/display math formatting rules, acronym tracking, and heading-capitalization consistency.

**Class B — Parser-local linguistic rules.** These criteria depend on POS tags, dependency arcs, sentence segmentation, or other bounded linguistic analyses, but they still operate locally on annotated text spans. Representative criteria include subject-verb distance, subordinate-clause count, nominalization with weak support verbs, prepositional-chain length, and noun-cluster density. These rules remain deterministic conditioned on a fixed annotation pipeline, but they are parser-sensitive and therefore require reliability gates.

**Class H — Bounded semantic heuristics.** These criteria use fixed-model or deterministic proxies for semantically richer phenomena without claiming to recover full propositional meaning. Representative criteria include paragraph redundancy candidate detection via embeddings plus corroborating overlap signals, topic-sentence detection via position plus lexical centrality, transition support-gap heuristics based on local evidence cues, and claim-evidence calibration proxies based on claim-strength markers and nearby evidence signals. These rules are still auditable and reproducible, but they must emit evidence, confidence, and abstention conditions.

**Class C — Semantically irreducible.** These criteria still require richer discourse or semantic judgment than v1 can justify. Representative criteria include topic-stress chain progression, rhetorical move classification, and abstract-body semantic alignment. These remain candidates for a future constrained semantic auditor, not for the v1 runtime.

This revised stratification preserves the important improvement introduced by the architecture work: semantic heuristics are legitimate first-class components when they are bounded, evidence-bearing, and validated against target text. They are neither mere regex rules nor full semantic understanding.

---

## 5. Layered Fault Model

Detection operates across five analytically distinct layers. The ordering is still dependency-sensitive: structural faults at higher layers make lower-layer rewrites less meaningful. The detection modes for each layer, however, must reflect the revised tractability model.

**Layer 1 — Surface style.** Objective: local clarity and concision at the sub-sentence level. Typical faults: passive voice in topic position, nominalization with weak verb support, noun-cluster density, excessive prepositional chaining, overlong sentences, formatting faults around math, and banned formulaic scaffolding. Detection mode: primarily Class A and Class B.

**Layer 2 — Local discourse.** Objective: sentence-to-sentence flow and information management. Typical faults: buried stress position, subject-verb separation exceeding register thresholds, weak local connective support, and limited forms of referential ambiguity. Detection mode: Class B and Class H, with Class C reserved for fuller topic-stress analysis.

**Layer 3 — Paragraph rhetoric.** Objective: paragraph-level coherence and move structure. Typical faults: absent or weak topic sentence, mixed-topic paragraphs, digressions interrupting progression, local redundancy, and rhythmic monotony. Detection mode: Class B and Class H in v1; richer move classification remains Class C.

**Layer 4 — Document structure.** Objective: global organization and structural integrity. Typical faults: orphan headings, non-parallel heading syntax across siblings, redundancy clusters, and asymmetric section balance. Detection mode: Class H in v1 for bounded structural heuristics; Class C remains reserved for abstract-body alignment and broader discourse judgments.

**Layer 5 — Audience fit.** Objective: register and accessibility calibration relative to the declared audience and genre. Typical faults: undefined technical terms before first use, acronym overload, jargon density, and strong claims presented without nearby evidence cues. Detection mode: Class A and Class H in v1; richer appropriateness judgments remain Class C.

---

## 6. System Architecture

The system comprises seven principal modules. Their interfaces are defined by typed data structures; no module should infer hidden state from another.

```
WritingAuditor
├── Preprocessor
│   ├── Markdown Parser / Future Format Parsers
│   ├── Block/Inline Document IR Builder
│   ├── Source View Builder          [raw-text rules consume this, not ad hoc strings]
│   ├── Text Projection Builder      [offset-preserving NLP projections]
│   └── English NLP Annotator        [v1]
│
├── LanguagePackRegistry
│   └── LanguagePack(code, model, lexicons, supported_rules)
│
├── ProfileResolver
│   ├── Rule Defaults
│   ├── Language-Pack Defaults
│   ├── Profile Defaults
│   └── User Overrides
│
├── FeatureStore
│   ├── Section / Heading Index
│   ├── Term / Symbol First-Use Index
│   ├── Support-Signal Index
│   ├── Lexical Overlap Tables
│   └── Redundancy Candidate Generator
│
├── RuleEngine                    [Class A + Class B + Class H]
│   ├── SourcePatternRules
│   ├── AnnotatedRules
│   └── HeuristicSemanticRules
│
├── SuggestionEngine
│   ├── RevisionPlanner
│   └── TemplateCandidateGenerator
│
├── HierarchicalScorer
│   ├── LayerScorers
│   ├── ContextProfileApplier
│   └── GlobalScoreAggregator
│
├── ReportGenerator
│   ├── DiagnosticReport
│   ├── SpanAnnotations
│   └── RevisionPlan
│
└── SemanticAuditor               [future optional Class C extension]
```

### 6.1 The Preprocessor

The Preprocessor no longer produces only a flat annotation object. It produces a typed document representation with three coordinated views:

- a block/inline IR that preserves authored markdown structure
- a source-oriented view for line-based pattern rules, already tagged with structural context such as list item, callout, table cell, code fence, or display math
- NLP projections for annotatable spans, each with explicit offset maps back to source

This is the necessary correction to the earlier claim that no downstream module should ever use raw text. Raw-text reasoning is valid for some criteria, but it must consume parser-derived source views, not re-derive structure independently from an opaque string.

### 6.2 The ProfileResolver

Before any rule is evaluated, the ProfileResolver reads the declared context configuration and produces a frozen resolved profile. The resolver now has a deterministic merge contract:

1. rule defaults
2. language-pack defaults
3. profile defaults
4. user overrides

Unknown rule ids or unknown override fields are configuration errors. This is necessary for the configuration file to remain a trustworthy contract rather than a best-effort suggestion to the runtime.

### 6.3 The RuleEngine

The RuleEngine implements all Class A, Class B, and Class H detectors. Each detector takes the preprocessed document views, the resolved profile, and the shared FeatureStore as input and produces typed `Violation` objects.

Determinism is retained in the following precise sense: given identical source text, identical config, identical model versions, and identical optional feature backends, the RuleEngine produces identical output.

For heuristic rules, the RuleEngine must also support:

- abstention when upstream signals are unreliable
- evidence-bearing diagnostics rather than bare messages
- conservative default severities until precision is measured

### 6.4 The SemanticAuditor

The SemanticAuditor is no longer part of the core v1 runtime. It remains a future optional module for Class C criteria that cannot be reduced to bounded heuristics with acceptable precision.

The motivation for retaining this future module is unchanged: some discourse and audience-fit criteria remain semantically irreducible. The change is narrower and more disciplined than before: the SemanticAuditor is reserved for what demonstrably fails under deterministic and heuristic methods, not for everything that sounds discourse-level.

### 6.5 The SuggestionEngine

The SuggestionEngine is invoked only after detection is complete. It is a revision-plan generator, not an auto-editor.

For v1 it operates in two modes:

- **Template candidate generation** for determinate cases where syntactic preconditions are satisfied
- **Tactic generation** for everything else, where the system can name the corrective move but should not fabricate a rewritten sentence

Examples:

- nominalization reversal only when a stable verbal form is available
- passive-to-active only when an actor is locally recoverable
- sentence splitting only when a stable clause boundary is available

The system must never modify the source file itself.

### 6.6 The HierarchicalScorer

Rather than aggregating all violations into a single scalar quality score, the HierarchicalScorer computes a score vector indexed by layer. At each layer, violations are aggregated by weighted sums modulated by the resolved profile.

Threshold values remain profile-dependent. Sentence length, for example, is still assessed against a register-appropriate target $\mu_{\text{profile}}$ with a tolerance $\sigma_{\text{profile}}$:

$$
\text{score}_{\text{length}}(s) = \max\left(0,\ \frac{|l_s - \mu_{\text{profile}}| - \sigma_{\text{profile}}}{\sigma_{\text{profile}}}\right)
$$

where $l_s$ is the word count of sentence $s$.

### 6.7 The ReportGenerator

Report quality is a first-class architectural concern. A diagnostic that cannot explain itself is not operationally useful. Therefore reports must expose, in text and JSON:

- the triggering rule id
- the exact source span
- the evidence features that caused the rule to fire
- any abstention or confidence-limiting conditions
- the corresponding rewrite tactics or revision-plan operations

---

## 7. Rule Formalization: The Normalized Rule Schema

Every criterion in the inventory remains a normalized rule object. The schema, however, must be rich enough to support evidence, language support, and abstention.

```yaml
id:               discourse.subject_verb_distance
label:            Subject and main verb are too far apart
layer:            local_discourse          # { surface_style | local_discourse |
                                           #   paragraph_rhetoric | document_structure | audience_fit }
tractability:     class_b                 # { class_a | class_b | class_h | class_c }
kind:             soft_heuristic          # { hard_constraint | soft_heuristic |
                                           #   diagnostic_metric | rhetorical_expectation | rewrite_tactic }
default_severity: warning                 # { info | warning | error }
supported_languages:
  - en
profiles_active:
  - generalist
  - pedagogical
  - interdisciplinary
detector:
  method:         dependency_distance
  arc:            nsubj_to_root
  threshold:
    default:      8
    pedagogical:  6
    research_note: 10
exceptions:
  - mathematical_definition
  - caption_fragment
  - enumeration_item
abstain_when:
  - annotation_flags.contains("heavy_math_masking")
  - annotation_flags.contains("symbol_dense_sentence")
evidence_fields:
  - distance
  - threshold
  - mask_ratio
rationale:
  principles:
    - reader_expectation_gopen
    - plain_language_opm
message: >
  The grammatical subject and the main verb are separated by {distance} tokens.
  This gap delays the reader's processing of the predication.
rewrite_tactics:
  - split_intervening_clause
  - move_context_to_prior_sentence
  - frontload_actor
suggestion_mode: template                 # { template | tactic_only | none }
weight:           0.7
evaluation:
  true_positive_examples:
    - "The results, which had been obtained using the revised experimental protocol described in Section 3, confirm the hypothesis."
  false_positive_examples:
    - "The matrix $A$, defined as $A_{ij} = \delta_{ij} \lambda_i$, is diagonal."
```

This schema preserves the earlier separation of concerns while correcting three omissions:

- `supported_languages` makes rule portability explicit rather than assumed
- `abstain_when` captures reliability limits
- `evidence_fields` defines the minimum explanation contract for reports

---

## 8. Revision Plan Generator and Dependency Order

The tool must not perform modifications in the source file. It must produce a revision plan that the writer can choose to implement.

The correct dependency order remains:

**Reorganize -> Link -> Rewrite locally**

### Step 1 — Reorganize (document and paragraph structure)

Sub-operations:

- identify redundancy candidates via bounded heuristic comparison
- flag mixed-topic paragraphs via topic-sentence weakness and local cohesion signals
- verify heading parallelism and orphan section absence
- produce structural operations such as `MERGE_PARAGRAPHS`, `SPLIT_PARAGRAPH`, `REORDER_SECTION`, or `REVIEW_REDUNDANCY_CLUSTER`

No sentence-level rewriting is proposed at this step.

### Step 2 — Link (discourse and sentence chaining)

Sub-operations:

- flag local connective support gaps
- identify weak topic continuity across adjacent sentences
- flag locally ambiguous reference patterns where deterministic heuristics suffice
- ensure old information is not systematically buried

This step remains local and bounded in v1. Fuller topic-stress chain analysis remains future work.

### Step 3 — Rewrite locally (surface style)

Sub-operations:

- reverse targeted nominalizations where a stable verbal form exists
- convert unjustified passive constructions where actor recovery is possible
- split overloaded sentences where a safe boundary is available
- reduce prepositional chain length or subject-verb distance through tactic suggestions

This ordering is not merely organizational. Applying local rewrites before structural fixes still optimizes syntax inside a deficient macro-organization.

---

## 9. Criterion Inventory: Revisions to the Original Checklist

The original checklist still requires revision on three grounds: some criteria need sharper operationalization, some must be removed, and some semantic heuristics deserve a narrower but real implementation path.

### 9.1 Criteria Retained and Reformulated

- **Sentence length** is retained as a distributional metric, not a single average. The target remains profile-parameterized.
- **Passive voice** is retained as a conditional warning, not a blanket prohibition. In v1 it is explicitly validated only for English.
- **Nominalization** is retained, but detection targets only harmful cases: nominalization plus weak verbal support, with technical-term exceptions.
- **Paragraph topic sentence** is retained, but no longer as a bare positional rule. It becomes a bounded heuristic combining sentence position, lexical centrality, topic continuity, and exception handling for transitional openers and motivating examples.
- **Transition quality** is retained as a bounded support-gap heuristic, not as a ban on specific connective words and not as a claim to detect full logical warrant.
- **Claim-evidence calibration** is retained as a local evidence-signal mismatch heuristic, not as a complete epistemic judgment.
- **Semantic redundancy** is retained as a candidate-detection heuristic, with corroborating evidence required before a paragraph pair is reported.

### 9.2 Criteria Demoted or Removed

- **"Prefer monosyllabic Saxon nouns"** is removed. The criterion is etymologically crude and misaligned with specialist prose.
- **"Use catchy words in title and abstract"** is separated into a discoverability module orthogonal to clarity.
- **"Avoid dangerous transition words"** is removed as a token-ban formulation. The real target is the bounded support-gap heuristic described above.
- **"Style: positively charged"** is replaced by constructive and calibrated evaluative language, implemented in v1 only through narrow heuristics and explicit lexicons.
- **Gunning Fog Index** is retained only as a secondary diagnostic metric, with the corrected formula:

$$
\text{GFI} = 0.4 \left( \frac{N_{\text{words}}}{N_{\text{sentences}}} + 100 \cdot \frac{N_{\text{complex}}}{N_{\text{words}}} \right)
$$

where $N_{\text{complex}}$ counts words of three or more syllables, excluding proper nouns, compound familiar words, and two-syllable verb forms created by `-ed` or `-es`.

### 9.3 Criteria Added

The following criteria remain important additions to the inventory:

- Acronym burden: definition-lag detection and density monitoring
- Noun cluster density: sequences of three or more consecutive nouns in a noun-phrase head chain
- Local lexical cohesion: overlap and continuity signals between adjacent sentences
- Semantic redundancy candidate detection: bounded similarity checks across paragraphs
- Heading parallelism: syntactic frame consistency across sibling headings
- Definition-before-use: first-use tracking for technical terms and symbols
- Claim-evidence calibration proxy: strong claim markers without nearby evidence signals

The following remain deferred from the v1 core runtime:

- topic-stress progression
- rhetorical move classification
- abstract-body alignment
- full coreference-based referential analysis

---

## 10. Configuration Schema Architecture

The system's behavior is still governed by a declarative configuration file, but the schema must expose language selection, strict validation, and rule-level overrides with explicit structure.

```yaml
profile:
  audience: interdisciplinary
  genre: lecture_note
  section: introduction
  register: pedagogical

language:
  code: en
  pack: builtin_en

runtime:
  strict_validation: true
  experimental_rules: false

rules:
  active:
    - surface.sentence_length
    - surface.passive_voice
    - surface.nominalization
    - discourse.subject_verb_distance
    - paragraph.topic_sentence
    - paragraph.paragraph_redundancy
    - audience.acronym_burden
  overrides:
    surface.sentence_length:
      threshold:
        default: 18
      weight: 0.9
    surface.banned_transition:
      extra_patterns:
        - "as a consequence"
      silenced_patterns:
        - "note that"
    audience.claim_calibration:
      severity: info

scoring:
  aggregation: hierarchical
  output: [layer_scores, global_score, violation_list]

suggestions:
  enabled: true
  default_mode: tactic_only

reporting:
  format: annotated_markdown
  sort_by: severity_desc
```

This configuration-as-data design remains analogous to systems such as Vale and LanguageTool, but with two stricter requirements:

- unknown rules or unknown fields are invalid, not silently ignored
- additive rule fields such as pattern extensions are declared explicitly, not inferred from ad hoc merge behavior

---

## 11. Evaluation Methodology

The tool still cannot be evaluated by face validity alone. A gold-standard evaluation corpus remains the minimum viable substrate, but the methodology must now account for fixed-model heuristics and parser-dependent behavior.

**Corpus construction.** A representative set of the writer's own texts — spanning research notes, lecture materials, and pedagogical expositions — is collected. For each text, a revised version is produced by the writer, with explicit annotations of the specific violations corrected and the criterion motivating each correction. This yields a corpus of `(original, revised, annotation)` triples.

**Per-rule precision measurement.** For each rule, precision is defined as the proportion of system-flagged violations that correspond to annotated violations in the gold standard. Precision is evaluated before recall. A rule whose precision falls below the declared threshold is demoted, narrowed, or disabled.

**Heuristic promotion policy.** Class H rules start conservatively. They are promoted from `info` or `diagnostic_metric` severity only after the measured precision on target text is acceptable.

**Model-version control.** Parser-dependent evaluation must pin exact model versions. Rule tests should be split into:

- logic tests against frozen annotated fixtures
- integration tests against live models on a smaller corpus

This prevents upstream NLP model updates from masquerading as hermeneia regressions.

**Hierarchical evaluation.** Evaluation is conducted separately per layer. A surface detector is not penalized by paragraph-level failures, and vice versa.

**Suggestion acceptance rate.** Acceptance and rejection of template rewrite candidates and tactic suggestions are logged per rule. This is the primary quality metric for the SuggestionEngine.

**Performance evaluation.** The system must be benchmarked for:

- cold-start and warm-start single-document latency
- batch throughput
- scaling behavior on large documents with many paragraphs

This is necessary because embeddings, parser startup, and pairwise comparisons are real architectural costs, not incidental implementation details.

---

## 12. Summary of Architectural Decisions

The table below consolidates the revised principal decisions and their rationale.

| Decision | Specification | Rationale |
|---|---|---|
| Tractability stratification | Criteria classified as Class A, B, H, or C before implementation | Prevents undefined boundaries and preserves bounded semantic heuristics without overstating them |
| Structured preprocessor outputs | Block/inline IR, source views, and offset-preserving NLP projections | Removes the false dichotomy between raw-text rules and annotated rules |
| RuleEngine scope | RuleEngine handles Class A, B, and H | Keeps v1 deterministic/heuristic while admitting evidence-bearing semantic proxies |
| Future semantic auditor | SemanticAuditor reserved for demonstrably irreducible Class C criteria | Prevents premature LLM dependence while keeping an escape hatch for true semantic limits |
| English-first language architecture | v1 ships English only, but language packs are a first-class structural concept | Anticipates multilingual support without making unjustified language-agnostic claims |
| Strict profile resolution | Defaults and overrides merge deterministically with validation errors on unknown fields | Keeps configuration auditable and prevents silent misconfiguration |
| Explainable diagnostics | Violations carry evidence, confidence, and rewrite tactics | Makes false positives diagnosable and heuristics auditable |
| Revision-plan generator | Reorganize -> Link -> Rewrite locally, with no source auto-editing | Preserves correct revision precedence and keeps the tool advisory |
| Model-aware evaluation | Pinned NLP models, frozen fixtures, heuristic promotion gates, and performance benchmarks | Prevents unstable tests and grounds heuristics in measured precision |

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
