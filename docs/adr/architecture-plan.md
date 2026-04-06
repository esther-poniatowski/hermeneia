# Hermeneia Architecture and Implementation Plan

**Authority relationship.** This document is the implementation specification. `docs/proposal.md` is the theoretical motivation and design rationale. Where they overlap (tractability tiers, module decomposition, rule schema, phasing), this document is authoritative for implementation decisions. The proposal is authoritative for theoretical grounding, criterion justification, and evaluation methodology. If a future edit to either document introduces a contradiction, this document governs code and the proposal governs intent.

## Context

Hermeneia is a profile-aware writing diagnostics engine for research, pedagogical, and mathematical prose. The project is at v0.0.0 with only a CLI skeleton (`src/hermeneia/cli.py`, `__init__.py`, `__main__.py`). A comprehensive design proposal exists at `docs/proposal.md`, and a monolithic reference linter at `docs/reference/lint-rules-reference.py` demonstrates the raw-text math checks that must be preserved where they remain valid.

This plan establishes the package architecture, core data structures, module boundaries, and phased implementation order. It borrows proven ideas from static analyzers such as mypy, pylint, pyright, ruff, and black, but it does not assume that prose can be treated as source code with a single AST and a single-pass local checker model.

**Scope of v1**:

- Deterministic and heuristic analysis only. No LLM-backed runtime in the core pipeline.
- Semantic heuristics are retained in v1, but they are treated as bounded, evidence-bearing approximations rather than as full semantic judgments.
- v1 ships with an English language pack only. The architecture must support future language packs immediately, but rule-specific multilingual calibration is deferred.

---

## Architectural Classification

**Hermeneia is a rule-driven document analyzer with shared structural annotation and bounded semantic heuristics.**

This remains closer to linter architecture than to a cross-file type checker, but the analogy holds only partially:

- Documents are self-contained analysis units. There is no cross-document dependency graph, SCC computation, or fixpoint iteration.
- The engine is still rule-driven and registry-based.
- The pipeline is bounded and staged, but it is **not** a single left-to-right pass over a formal syntax tree. Prose rules may require whole-document indexes, paragraph-pair candidate generation, and support-signal lookback windows.
- Raw-text pattern rules, parser-based rules, and heuristic semantic rules must share a common structural substrate. A split between "real IR rules" and "string-only rules" is not acceptable.

The practical consequence is:

- **Document-local staged analysis**, not "file-local bounded pass" in the strict pylint sense.
- **Shared derived views**, not one privileged AST plus disconnected raw-text scans.
- **Evidence-bearing diagnostics**, not opaque boolean flags for heuristic rules.

---

## Eight Key Design Decisions

### 1. Evaluation Scheduling: Document-Local Staged Analysis

Each document goes through a fixed, non-iterative orchestration pipeline:

**parse -> build structural views -> build NLP projections -> annotate -> derive features -> detect -> score -> report**

Important clarification: this is bounded, but not single-pass. The engine may build whole-document indexes before rule evaluation:

- section and heading hierarchy
- first-use index for terms, symbols, and acronyms
- support-signal index for citations, theorem references, displayed equations, quantitative evidence, and contrast markers
- lexical-overlap tables for adjacent sentences and paragraphs
- embedding candidate sets for redundancy checks

This avoids the false assumption that paragraph-level or cross-paragraph rules can be implemented as isolated local checks while still avoiding fixpoint-style convergence logic.

### 2. Source Representation: Block/Inline Document IR with Derived Section Views

The primary IR is a typed block/inline tree that preserves authored markdown structure. The current strict hierarchy `Document -> Sections -> Paragraphs -> Sentences -> Tokens` is too narrow for real markdown.

The IR must represent at least:

- headings
- paragraphs
- list blocks and list items
- block quotes and callouts
- tables, rows, and cells
- code fences
- display math blocks
- footnotes and admonitions as generic container blocks when the parser cannot give them stronger semantics
- inline text runs, inline math, and inline code inside prose blocks

`Section` remains useful, but it becomes a **derived view** over heading blocks rather than the sole top-level organizational primitive.

Three rules follow from this:

- There is one structural source of truth: the block/inline tree.
- Convenience indexes such as `math_nodes`, `code_nodes`, or `sections` are derived indexes, not second representations with independent semantics.
- Not every block is NLP-annotated. The annotator follows a block-type policy that determines which blocks receive sentence segmentation, text projection, and dependency parsing:

| BlockKind | Sentence-segmented | NLP-annotated | Rationale |
| --- | --- | --- | --- |
| `PARAGRAPH` | Yes | Yes | Primary analysis target |
| `HEADING` | Single sentence, no segmentation | Yes (POS/dep for parallelism and nominalization checks) | Headings are short; segmentation is trivial but parse is useful |
| `LIST_ITEM` | Yes, if the item contains prose with terminal punctuation; otherwise treated as a fragment sentence | Yes, with `list_item_fragment` flag when no terminal punctuation | List items may contain multi-sentence prose or terse fragments |
| `TABLE_CELL` | Yes, with `table_cell_context` flag on all resulting sentences | Yes, but rules may abstain | Cells often contain fragments or abbreviations |
| `BLOCK_QUOTE` | Yes (recurse into child blocks) | Yes | Block quotes contain normal prose |
| `ADMONITION` | Yes (recurse into child blocks) | Yes | Admonitions contain normal prose |
| `FOOTNOTE` | Yes (recurse into child blocks) | Yes | Footnotes contain normal prose |
| `CODE_BLOCK` | No | No | Not prose |
| `DISPLAY_MATH` | No | No | Not prose |
| `TABLE` / `TABLE_ROW` / `LIST` | No (container only) | No (recurse into children) | Structural containers; their children are the annotatable units |

Blocks that are not sentence-segmented have empty `sentences` and `tokens` lists. Their `inline_nodes` are still populated for `SourcePatternRule` access. This policy is enforced by the annotator and is not configurable per rule -- it is a property of the document model.

### 3. Text Projection and Offset Reconciliation

NLP annotation cannot operate directly on raw source slices when inline math and inline code are interleaved with prose. Instead, the preprocessor builds a `TextProjection` for every annotatable sentence or heading.

Each projection stores:

- normalized text sent to spaCy
- a character-level map from normalized offsets back to source offsets
- the masked source segments and the placeholder inserted for each segment

Key rules:

- Inline math and inline code are **replaced**, not deleted, before NLP. Deletion destroys offset alignment and often collapses syntax.
- Placeholder choice is typed, not generic. For example, a single-symbol inline math span and a full equation-like span should not receive the same placeholder token.
- Tokens keep both projection-local offsets and source spans.
- Parser-sensitive rules must be allowed to **abstain** or downgrade confidence when a sentence is heavily masked, symbol-dense, or otherwise outside the reliable operating range of the parser.

This is the only defensible way to preserve exact source spans while still running NLP over prose that contains notation.

**Concrete placeholder tokens.** The placeholder must occupy a syntactic role compatible with what it replaced, so that the dependency parse of the surrounding prose remains valid. The projection builder classifies each masked segment and selects a placeholder accordingly:

| Masked content | Classification heuristic | Placeholder token | Rationale |
| --- | --- | --- | --- |
| Single-letter variable: `$x$`, `$A$` | Content matches `^[A-Za-z][A-Za-z0-9']*$` | `MATHSYM` | Short alphabetic marker for a nominal slot; chosen to be minimally disruptive when the parser encounters a masked variable |
| Numeric or simple expression: `$3$`, `$n+1$` | Content matches a numeric or short arithmetic pattern | `MATHNUM` | Distinguishes quantity-like math from symbolic identifiers for downstream heuristics, without assuming a stable POS tag |
| Complex expression or equation fragment: `$\frac{a}{b}$`, `$f(x) = g(x)$` | Anything else, or content length above a threshold | `MATHEXPR` | Coarse marker for a substantive masked expression; lets rules detect that a complex math span occupied this position |
| Inline code: `` `foo` `` | Always | `CODEID` | Marker for an inline code identifier or code-like token |
| Link target: `[text](url)` | Always | (keep anchor text, drop URL) | Anchor text is prose and should be parsed; only the URL is noise |

These tokens are chosen to be lightweight synthetic markers, but the architecture does **not** assume a guaranteed POS tag or dependency behavior for them. Their role is twofold:

- preserve token boundaries and offset alignment
- let downstream rules and diagnostics know what kind of material was masked

Because parser behavior on synthetic tokens is model-dependent, any sentence whose analysis materially depends on the masked content must be handled through abstention flags or reduced confidence. The projection builder must ensure that exactly one whitespace character separates each placeholder from adjacent text.

**Annotation flags: population and thresholds.** The projection builder populates `Sentence.annotation_flags` during construction, before the annotator runs. The following flags are defined:

| Flag | Populated by | Condition |
| --- | --- | --- |
| `heavy_math_masking` | Projection builder | More than 40% of the sentence's character length is masked inline math |
| `symbol_dense_sentence` | Projection builder | The sentence contains 4 or more distinct masked math segments |
| `fragment_sentence` | Projection builder | The projected text after masking contains fewer than 4 word-boundary tokens |
| `code_dominant` | Projection builder | More than 50% of the sentence's character length is masked inline code |
| `table_cell_context` | Source view builder | The sentence originates from a `TABLE_CELL` block |
| `list_item_fragment` | Source view builder | The sentence originates from a `LIST_ITEM` block and contains no terminal punctuation |

Rules reference these flags in their `abstain_when` conditions. The annotator still runs on flagged sentences (the tokens may be useful to other rules), but any rule that declares an abstention condition on a flag present in the sentence must skip that sentence and not emit a violation for it. The thresholds above (40%, 4 segments, 4 tokens, 50%) are initial default values supplied by the active language pack's preprocessing policy and resolved through the same config path as other preprocessing settings. They are implemented in `document/projection.py`, but they are not semantically hard-coded there: the projection builder reads them from resolved settings, not from fixed literals baked into rule logic.

### 4. Analysis Composition: Shared Feature Store and Context Views

The rule hierarchy becomes:

| Base Class                    | Operates On                                 | Used By                                                                 |
| ---------------------------- | ------------------------------------------- | ----------------------------------------------------------------------- |
| `SourcePatternRule`          | Parser-derived `SourceView` and line spans  | Regex and structural-context rules such as math formatting constraints  |
| `AnnotatedRule`              | Annotated sentences/headings from the IR    | POS/dep-based rules and other parser-local diagnostics                  |
| `HeuristicSemanticRule`      | Document IR + `FeatureStore` + candidates   | Redundancy, topic-sentence heuristics, local support-gap heuristics     |

Every rule receives the same `RuleContext`, which includes:

- `ResolvedProfile`
- active `LanguagePack`
- `FeatureStore`
- runtime capability flags (embeddings available, debug mode, experimental rules enabled)

`SourcePatternRule` no longer bypasses the IR. It consumes a `SourceView` derived from the parsed document, where each line is already tagged with structural context such as:

- inside code fence
- inside display math
- inside list item
- inside callout/block quote
- inside table cell

This removes the representational schism that existed when raw rules had to rediscover markdown structure from `doc.source`.

### 5. Configuration: Declarative YAML with Deterministic, Validated Merge Semantics

The configuration system still centers on YAML, but the merge contract must be explicit.

`ProfileResolver` merges four layers in this order:

1. Rule-declared defaults
2. Language-pack defaults
3. Profile defaults (audience, genre, section, register)
4. User overrides

Merge semantics:

- scalars replace
- mappings deep-merge
- lists replace by default
- explicitly additive fields, such as `extra_patterns` and `silenced_patterns`, use a shared merge helper

Validation requirements:

- unknown rule ids are configuration errors
- unknown override fields are configuration errors
- type mismatches are configuration errors
- disabled or unsupported rules are reported explicitly

The output is a frozen `ResolvedProfile` with `ResolvedRuleSettings` for every active rule. Custom rules can attach their own Pydantic options model and participate in the same validation path as built-ins.

### 6. Extensibility: Unified Rule Registration Protocol

Built-in and external rules use the same module protocol:

- each rule module exports `register(registry)`
- the registry receives the rule class plus metadata such as config model, supported language packs, and whether the rule is experimental

Built-ins are discovered by package walk (`pkgutil.walk_packages`) rather than by a hand-maintained `rules/__init__.py` import chain. External modules loaded through `--load-rules` or YAML use the same `register(registry)` protocol.

This resolves two coherence problems:

- there is no hidden built-in registration path based on import side effects
- a custom rule can opt into the same pattern-merging and config-validation behavior as a built-in rule

Pattern-configurable rules share a common mixin or helper, so `extra_patterns` and `silenced_patterns` do not require each plugin author to reimplement merging logic.

### 7. NLP Strategy: English-First Language Packs with Reliability Gating

v1 is English-first, not multilingual-by-assertion.

The architecture must include:

- a `language` field in config
- a `LanguagePack` abstraction that supplies lexicons, defaults, parser model identifiers, and rule support metadata
- a registry that can later load additional language packs

v1 ships only:

- `language: en`
- an English spaCy pipeline pinned to a tested model version
- English lexicons and thresholds

Rules that depend on English-specific syntax or rhetoric, including:

- passive voice
- stress position
- subject-verb distance thresholds
- noun-cluster handling
- heading parallelism heuristics

must declare that they are validated only for the English pack. They are **not** inherently language-agnostic just because they consume UD-style labels.

`coreference` is removed from the required v1 path. The architecture reserves a slot for a coreference backend in the `FeatureStore`, but an actual `discourse.coreference` rule is deferred to an experimental extension phase until:

- a conservative backend is chosen
- confidence/abstention policy is defined
- precision is measured on target-domain text

### 8. Cross-Cutting Constraints: Explainability, Performance, and Testability

These are architectural requirements, not afterthoughts.

**Explainability**

- Every `Violation` must carry machine-readable evidence for why it fired.
- Heuristic rules must report at least the triggering score, threshold, matched signals, and any upstream reliability limitations.
- Reports must be able to show this evidence in text and JSON output.

**Performance**

- spaCy pipelines load lazily and are cached per language pack
- optional subsystems, such as embeddings, load only if active rules require them
- sentence and paragraph embeddings are computed once per document
- redundancy rules use candidate generation and blocking before pairwise similarity to avoid uncontrolled `O(n^2)` behavior on large documents

**Testability**

- rule logic should be testable against synthetic `Document` fixtures without invoking spaCy
- parser/NLP integration tests should use pinned model versions and frozen annotation snapshots
- only a small integration suite should depend on live model output

---

## Rule Naming and Identification

Rules continue to use a hierarchical dotted naming scheme:

```text
{layer}.{specific_rule}
```

Examples:

- `surface.nominalization`
- `surface.passive_voice`
- `discourse.subject_verb_distance`
- `paragraph.topic_sentence`
- `audience.claim_calibration`
- `math.bare_symbol`

**No numeric codes.** The inventory is small enough that readable identifiers remain preferable.

Rule ids are declared explicitly and remain stable across refactors.

---

## Tractability Classes

The tractability model is expanded to reflect the semantic heuristics that v1 intentionally preserves:

| Class     | Meaning                                                                                                   |
| --------- | --------------------------------------------------------------------------------------------------------- |
| `class_a` | Fully deterministic lexical, structural, or formulaic rules                                               |
| `class_b` | Parser-local NLP rules that depend on POS/dependency annotation or other bounded linguistic structure     |
| `class_h` | Bounded semantic heuristics using deterministic or fixed-model features, evidence fusion, and abstention  |
| `class_c` | Semantically irreducible criteria reserved for future extension modules                                    |

`class_h` is the missing category between shallow syntax and full semantic judgment. It preserves the v1 semantic heuristics without pretending they are equivalent either to regex rules or to full content understanding.

---

## Heuristic Semantic Rules in v1

The following rules remain in scope, but each must ship with guardrails, evidence output, and an initial severity/kind appropriate to its uncertainty.

| Criterion                   | v1 Strategy                  | Initial Kind            | Technique and Guardrails                                                                                                                                              |
| -------------------------- | ---------------------------- | ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Heading parallelism        | **Heuristic**                | `soft_heuristic`        | Normalize sibling heading frames; compare only within the same level and heading family; treat one-word nominal headings separately from clausal headings          |
| Heading capitalization     | **Deterministic**            | `hard_constraint`       | Compare casing convention across sibling headings at the same level                                                                                                  |
| Paragraph redundancy       | **Heuristic**                | `diagnostic_metric`     | Use embeddings for candidate generation only; require corroborating lexical overlap and shared discourse role; suppress when paragraphs introduce distinct claims   |
| Sentence redundancy        | **Heuristic**                | `soft_heuristic`        | Adjacent-sentence similarity plus lexical overlap; suppress when the later sentence introduces new notation, a citation, or a stronger claim                        |
| Topic sentence detection   | **Heuristic**                | `soft_heuristic`        | Multi-feature score: first/second-sentence position, lexical centrality, subject/topic continuity, and exception handling for transitional openers and examples    |
| Transition quality         | **Heuristic**                | `diagnostic_metric`     | Flag connector-driven support gaps only when a bounded lookback window lacks explicit support cues such as citations, theorem refs, equations, or causal markers   |
| Definition-before-use      | **Heuristic**                | `soft_heuristic`        | Build first-use index for terms and symbols; match against definitional patterns and section-local exceptions                                                       |
| Jargon density             | **Heuristic**                | `soft_heuristic`        | Audience-specific jargon lexicon plus local density thresholds                                                                                                      |
| Claim-evidence calibration | **Heuristic**                | `diagnostic_metric`     | Detect strong claim markers that lack nearby evidence signals such as citations, theorem/proof references, displayed math, or quantitative result cues             |
| Literary parallelism       | **Heuristic (experimental)** | `diagnostic_metric`     | Dependency-frame pattern matching with aggressive abstention on short or symbol-heavy clauses                                                                        |
| Topic-stress progression   | **Deferred**                 | --                      | Requires richer discourse semantics than v1 heuristics can support reliably                                                                                         |
| Rhetorical move analysis   | **Deferred**                 | --                      | Requires genre-aware discourse classification                                                                                                                       |
| Abstract-body alignment    | **Deferred**                 | --                      | Deferred until there is a validated section-level semantic comparison strategy                                                                                       |

Promotion rule:

- `class_h` rules begin as `info`, `diagnostic_metric`, or tightly scoped `warning`
- they are promoted only after corpus evaluation demonstrates acceptable precision on target text

---

## Package Structure

```text
src/hermeneia/
+-- __init__.py
+-- __main__.py
+-- cli.py
+-- config/
|   +-- __init__.py
|   +-- schema.py                   # Pydantic config models
|   +-- profile.py                  # ProfileResolver -> ResolvedProfile
|   +-- defaults.py                 # Profile and rule defaults
+-- document/
|   +-- __init__.py
|   +-- model.py                    # Block/inline IR, spans, tokens, violations
|   +-- projection.py               # TextProjection and offset maps
|   +-- source_view.py              # Line-oriented structural view for SourcePatternRule
|   +-- indexes.py                  # Section view, term index, support signals, pair candidates
|   +-- parser.py                   # Abstract parser interface
|   +-- markdown.py                 # Markdown -> Document IR
|   +-- annotator.py                # NLP annotation layer (spaCy)
+-- language/
|   +-- __init__.py
|   +-- base.py                     # LanguagePack protocol
|   +-- registry.py                 # Available language packs
|   +-- en.py                       # v1 English pack
+-- rules/
|   +-- __init__.py
|   +-- base.py                     # BaseRule hierarchy, Violation, RuleEvidence
|   +-- loader.py                   # Built-in and external rule loading
|   +-- common.py                   # Shared helpers and pattern-config mixins
|   +-- surface/
|   |   +-- sentence_length.py
|   |   +-- passive_voice.py
|   |   +-- nominalization.py
|   |   +-- prep_chain.py
|   |   +-- noun_cluster.py
|   |   +-- banned_transition.py
|   |   +-- contraction.py
|   |   +-- pronoun.py
|   |   +-- vague_phrasing.py
|   |   +-- case_scaffolding.py
|   |   +-- cross_reference.py
|   +-- discourse/
|   |   +-- subject_verb_distance.py
|   |   +-- subordinate_clause.py
|   |   +-- stress_position.py
|   |   +-- transition_quality.py
|   +-- paragraph/
|   |   +-- topic_sentence.py
|   |   +-- parallelism.py
|   |   +-- literary_parallelism.py
|   |   +-- lexical_repetition.py
|   |   +-- sentence_redundancy.py
|   |   +-- paragraph_redundancy.py
|   +-- structure/
|   |   +-- heading_parallelism.py
|   |   +-- heading_capitalization.py
|   |   +-- section_balance.py
|   +-- audience/
|   |   +-- acronym_burden.py
|   |   +-- definition_before_use.py
|   |   +-- jargon_density.py
|   |   +-- claim_calibration.py
|   +-- math/
|       +-- display_math.py
|       +-- bare_symbol.py
|       +-- imperative_opening.py
|       +-- abstract_framing.py
|       +-- prose_math.py
|       +-- proof_marker.py
+-- engine/
|   +-- __init__.py
|   +-- registry.py                 # RuleRegistry
|   +-- runner.py                   # AnalysisRunner
|   +-- detector.py                 # Rule dispatch
+-- scoring/
|   +-- __init__.py
|   +-- scorer.py
+-- suggest/
|   +-- __init__.py
|   +-- planner.py                  # Revision plan generator
|   +-- template.py                 # Guarded candidate rewrites
+-- report/
    +-- __init__.py
    +-- diagnostic.py               # Ranked violations
    +-- annotations.py              # Inline source annotations
    +-- revision_plan.py            # Ordered revision operations
```

---

## Core Data Structures

### Document IR (`document/model.py`, `document/projection.py`, `document/source_view.py`)

```python
@dataclass(frozen=True)
class Span:
    start: int
    end: int
    start_line: int
    start_column: int
    end_line: int
    end_column: int


@dataclass(frozen=True)
class MaskedSegment:
    kind: Literal["inline_math", "inline_code", "link_target"]
    source_span: Span
    placeholder: str


@dataclass(frozen=True)
class TextProjection:
    text: str
    normalized_to_source: tuple[int | None, ...]
    masked_segments: tuple[MaskedSegment, ...]


@dataclass
class Token:
    text: str
    lemma: str
    pos: str | None
    dep: str | None
    head_idx: int | None
    source_span: Span
    projection_start: int
    projection_end: int


class BlockKind(StrEnum):
    HEADING = "heading"
    PARAGRAPH = "paragraph"
    LIST = "list"
    LIST_ITEM = "list_item"
    BLOCK_QUOTE = "block_quote"
    TABLE = "table"
    TABLE_ROW = "table_row"
    TABLE_CELL = "table_cell"
    CODE_BLOCK = "code_block"
    DISPLAY_MATH = "display_math"
    FOOTNOTE = "footnote"
    ADMONITION = "admonition"


class InlineKind(StrEnum):
    TEXT = "text"
    INLINE_MATH = "inline_math"
    INLINE_CODE = "inline_code"


@dataclass
class InlineNode:
    kind: InlineKind
    text: str
    span: Span


@dataclass
class Sentence:
    id: str
    source_text: str
    span: Span
    inline_nodes: list[InlineNode]
    projection: TextProjection
    tokens: list[Token]
    annotation_flags: frozenset[str]


@dataclass
class Block:
    id: str
    kind: BlockKind
    span: Span
    children: list["Block"] = field(default_factory=list)
    sentences: list[Sentence] = field(default_factory=list)
    inline_nodes: list[InlineNode] = field(default_factory=list)
    metadata: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SourceLine:
    text: str
    span: Span
    block_id: str | None
    container_kinds: tuple[BlockKind, ...]
    excluded_spans: tuple[Span, ...]


@dataclass
class SectionView:
    heading_block_id: str | None
    level: int
    block_ids: tuple[str, ...]
    span: Span


@dataclass(frozen=True)
class SentenceRef:
    id: str
    block_id: str
    ordinal: int          # document-wide sentence order
    span: Span


@dataclass
class DocumentIndexes:
    sections: list[SectionView]
    sentences: tuple[SentenceRef, ...]
    math_block_ids: tuple[str, ...]
    code_block_ids: tuple[str, ...]
    term_first_use: dict[str, Span]
    symbol_first_use: dict[str, Span]
    support_signals: list["SupportSignal"]


@dataclass
class Document:
    blocks: list[Block]
    source_lines: list[SourceLine]
    indexes: DocumentIndexes
    source: str
    path: Path | None
```

Important consequences:

- `math_block_ids` and similar fields are derived indexes over `Block` ids, not alternate storage.
- `SourceLine` gives source-pattern rules direct access to raw text plus parser-derived context.
- `Sentence.projection` is the contract for offset reconciliation.
- `Sentence.id` and `DocumentIndexes.sentences` provide the canonical document-wide sentence identity and order used by support lookback, overlap, and embedding features.

### Block ID Generation

`Block.id` values are deterministic positional identifiers of the form `b{sequence}`, assigned by a depth-first traversal of the block tree during parsing. The sequence is a zero-padded integer incremented for every block node visited: `b000`, `b001`, `b002`, etc. This scheme is:

- **stable across re-parses** of identical source (same traversal order produces the same ids)
- **cheap to generate** (no content hashing)
- **not stable across source edits** (inserting a paragraph shifts all subsequent ids)

For v1 this is acceptable: there is no cross-run caching that depends on id stability across edits. If incremental analysis is added later, the id scheme can be upgraded to content-hash-based ids without changing any downstream interface, because all consumers reference ids as opaque `str` values.

### Sentence ID Generation

`Sentence.id` values use the analogous positional scheme `s{sequence}`, assigned in document order after block parsing and sentence segmentation: `s000`, `s001`, `s002`, etc. The canonical sentence order is stored in `DocumentIndexes.sentences` as `SentenceRef` entries.

This scheme is:

- **stable across re-parses** of identical source and identical segmentation output
- **sufficient for document-local feature indexing** in v1
- **not stable across source edits** or segmentation policy changes, which is acceptable because sentence ids are only document-local runtime identifiers

All `FeatureStore` sentence-oriented APIs use these ids rather than anonymous integers so that rules do not depend on an unstated flattening convention.

### Support Signals (`document/indexes.py`)

```python
class SupportSignalKind(StrEnum):
    CITATION = "citation"
    THEOREM_REF = "theorem_ref"
    PROOF_REF = "proof_ref"
    DISPLAYED_EQUATION = "displayed_equation"
    QUANTITATIVE_RESULT = "quantitative_result"
    CONTRAST_MARKER = "contrast_marker"
    EXAMPLE_MARKER = "example_marker"
    DEFINITION_MARKER = "definition_marker"


@dataclass(frozen=True)
class SupportSignal:
    kind: SupportSignalKind
    span: Span
    block_id: str
    sentence_id: str | None      # None for block-level signals like displayed equations
```

Support signals are detected during the feature-building pass (Phase 3) by a combination of:

- regex patterns for citations (`[Author, Year]`, `\cite{...}`, numbered references)
- structural context for displayed equations (blocks with `kind == DISPLAY_MATH`)
- lexical patterns for theorem/proof references ("Theorem 3", "by Lemma", "Proof.")
- hedge/strength lexicons for contrast markers ("however", "in contrast", "conversely")
- quantitative cue patterns ("Table 1 shows", "Figure 2", "p < 0.05", percentage patterns)

The `SupportSignal` list in `DocumentIndexes` is ordered by source position. Rules that need support lookback (transition quality, claim-evidence calibration) query this list with a bounded window anchored on a canonical sentence id: given a sentence id, they scan backward through the signal list for signals within a configurable sentence or token distance.

### Feature Store (`document/indexes.py`)

```python
class FeatureStore:
    """Precomputed document-level features shared across rules.

    Built once per document during the feature-building pass.
    Immutable after construction. Passed to rules via RuleContext.
    """

    def __init__(
        self,
        doc: Document,
        indexes: DocumentIndexes,
        embedding_backend: EmbeddingBackend | None = None,
    ) -> None:
        self._doc = doc
        self._indexes = indexes
        self._embedding_backend = embedding_backend
        self._sentence_embedding_cache: dict[str, NDArray[np.float32]] = {}
        self._paragraph_embedding_cache: dict[str, NDArray[np.float32]] = {}
        self._sentence_overlap_cache: dict[tuple[str, str], float] | None = None
        self._paragraph_overlap_cache: dict[tuple[str, str], float] | None = None

    # --- Term and symbol tracking ---

    def term_first_use(self, term: str) -> Span | None:
        """Source span of the first use of a normalized term, or None."""
        return self._indexes.term_first_use.get(term)

    def symbol_first_use(self, symbol: str) -> Span | None:
        """Source span of the first use of a math symbol, or None."""
        return self._indexes.symbol_first_use.get(symbol)

    # --- Support signals ---

    def support_signals_in_window(
        self, anchor_sentence_id: str, max_sentences_back: int = 3
    ) -> list[SupportSignal]:
        """Return support signals within a bounded lookback window."""
        ...

    # --- Lexical overlap ---

    def sentence_overlap(self, sent_a_id: str, sent_b_id: str) -> float:
        """Lemma-based Jaccard overlap between two sentences. Cached by sentence id."""
        ...

    def paragraph_overlap(self, block_id_a: str, block_id_b: str) -> float:
        """Lemma-based Jaccard overlap between two paragraph blocks. Cached."""
        ...

    # --- Embeddings (optional) ---

    @property
    def embeddings_available(self) -> bool:
        """Whether an embedding backend is configured and can be used on demand."""
        return self._embedding_backend is not None

    def sentence_embedding(self, sent_id: str) -> NDArray[np.float32] | None:
        """Embedding for a sentence id, loaded and cached on demand."""
        ...

    def paragraph_embedding(self, block_id: str) -> NDArray[np.float32] | None:
        """Embedding for a paragraph block id, loaded and cached on demand."""
        ...

    def redundancy_candidates(
        self, similarity_threshold: float = 0.85
    ) -> list[tuple[str, str, float]]:
        """Paragraph-block id pairs with embedding similarity above threshold.
        Computed once using blocking heuristics, not exhaustive O(n^2)."""
        ...

    # --- Section structure ---

    @property
    def sections(self) -> list[SectionView]:
        return self._indexes.sections

    def sibling_headings(self, level: int) -> list[Block]:
        """All heading blocks at the given level that share the same parent section."""
        ...
```

The `FeatureStore` is constructed during Phase 3 (feature-building pass) and is immutable thereafter at the API level. It is passed to every rule via `RuleContext.features`. Rules must not mutate it or build competing indexes. Internal memoization of overlap tables or embeddings is permitted as a cache implementation detail and does not change the semantic contents of the store. Embedding computation is deferred until the first call to an embedding method; `embeddings_available` reports backend capability, not whether the cache has already been populated.

### Rule Base (`rules/base.py`)

```python
class Tractability(StrEnum):
    CLASS_A = "class_a"
    CLASS_B = "class_b"
    CLASS_H = "class_h"
    CLASS_C = "class_c"


class Severity(StrEnum):
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class RuleEvidence:
    features: Mapping[str, Any]
    score: float | None = None
    threshold: float | None = None
    upstream_limits: tuple[str, ...] = ()


@dataclass(frozen=True)
class Violation:
    rule_id: str
    message: str
    span: Span
    severity: Severity
    layer: Layer
    evidence: RuleEvidence | None = None
    confidence: float | None = None
    rationale: str | None = None
    rewrite_tactics: tuple[str, ...] = ()


@dataclass(frozen=True)
class RuleContext:
    profile: ResolvedProfile
    language_pack: LanguagePack
    features: FeatureStore
    enable_experimental: bool = False


class BaseRule(ABC):
    id: ClassVar[str]
    label: ClassVar[str]
    layer: ClassVar[Layer]
    tractability: ClassVar[Tractability]
    default_severity: ClassVar[Severity]
    supported_languages: ClassVar[frozenset[str]]
    options_model: ClassVar[type[BaseModel] | None] = None

    def __init__(self, settings: ResolvedRuleSettings) -> None:
        self.settings = settings

    @abstractmethod
    def check(self, doc: Document, ctx: RuleContext) -> list[Violation]: ...


class SourcePatternRule(BaseRule):
    @abstractmethod
    def check_source(
        self, lines: list[SourceLine], doc: Document, ctx: RuleContext
    ) -> list[Violation]: ...

    def check(self, doc: Document, ctx: RuleContext) -> list[Violation]:
        return self.check_source(doc.source_lines, doc, ctx)


class AnnotatedRule(BaseRule):
    pass


class HeuristicSemanticRule(BaseRule):
    pass
```

### Registry and Loading (`engine/registry.py`, `rules/loader.py`)

```python
class RuleRegistry:
    def add(self, rule_cls: type[BaseRule]) -> None: ...


def load_builtin_rules(registry: RuleRegistry) -> None:
    # Walk hermeneia.rules.* packages and call register(registry) where present.
    ...


def load_external_rules(module_name: str, registry: RuleRegistry) -> None:
    mod = importlib.import_module(module_name)
    mod.register(registry)
```

This removes the need for import-time decorators and hand-maintained import chains.

---

## Implementation Phases

### Phase 1 -- Foundation and Execution Contracts

**Scope**: Establish the structural contracts that every later phase depends on.

**Create**:

- `document/model.py`
- `document/projection.py`
- `document/source_view.py`
- `document/indexes.py`
- `config/schema.py`
- `config/profile.py`
- `config/defaults.py`
- `language/base.py`
- `language/registry.py`
- `language/en.py`
- `rules/base.py`
- `rules/common.py`
- `rules/loader.py`
- `engine/registry.py`
- `engine/runner.py` (skeleton only)
- `scoring/scorer.py` (interfaces and synthetic-violation support)
- `report/diagnostic.py` and `report/revision_plan.py` (interfaces only)

**Verify**:

- All core types instantiate with synthetic fixtures
- Merge precedence is deterministic and tested
- Unknown rule ids and unknown override fields fail validation
- Built-in and external rule loading use the same protocol
- Scoring and reporting operate on synthetic `Violation` lists before any real rule exists

### Phase 2 -- Markdown Parsing, Structured Source Views, and Projections

**Scope**: Parse markdown into the block/inline IR, build section views, build source-line views, and create NLP projections.

**Create**:

- `document/parser.py`
- `document/markdown.py`

**Key complexity**:

- headings and paragraphs
- nested lists
- block quotes and callouts
- tables and table cells
- code fences
- display math
- interleaved prose and inline math
- footnotes/admonitions captured as generic container blocks

**Verify**:

- Fixtures covering callouts, list items, and table cells parse into distinct container blocks
- Inline math inside prose creates `MaskedSegment` entries and valid offset maps
- `SourceLine.container_kinds` correctly marks list/callout/table contexts
- Span round-trip succeeds for blocks, inline nodes, and projections

### Phase 3 -- NLP Annotation, Feature Store, and Reliability Gates

**Scope**: Add English NLP annotation and build reusable document-level features.

**Create**:

- `document/annotator.py`
- `document/indexes.py` feature builders for:
  - first-use indexes
  - lexical overlap tables
  - support-signal detection
  - redundancy candidate generation

**Update**:

- `pyproject.toml`
- `environment.yml`

**Requirements**:

- pin the English spaCy model version used in tests
- do not require coreference in v1
- add abstention flags for symbol-dense or heavily masked sentences

**Verify**:

- Golden annotation snapshots for a small set of English fixtures
- Rule logic can run on frozen snapshots without invoking spaCy
- Math-heavy sentences trip abstention or confidence-downgrade flags rather than producing false precision
- Warm-run performance benchmark recorded for representative fixture sizes

### Phase 4 -- Real Engine, CLI, Scoring, and Reporting

**Scope**: Build the actual orchestration pipeline before rule inventory expansion.

**Create/Finalize**:

- `engine/runner.py` -- real `AnalysisRunner`
- `engine/detector.py`
- `scoring/scorer.py`
- `report/diagnostic.py`
- `report/annotations.py`
- `report/revision_plan.py`
- `cli.py` -- `lint` command wired to the real runner

**Verify**:

- `hermeneia lint` runs through the real runner, not a throwaway path
- JSON report includes evidence, confidence, and rationale fields
- Annotated output preserves source content and span accuracy
- Scoring tests run independently from real rule implementations

### Phase 5 -- Class A Deterministic Rules

**Scope**: Implement surface, math, and straightforward audience rules that do not depend on heuristic semantic fusion.

**Create**:

- `rules/surface/`
- `rules/math/`
- `rules/audience/acronym_burden.py`

**Rule mapping**:

- raw math and markdown-context rules become `SourcePatternRule`
- parser-based but deterministic surface rules become `AnnotatedRule`

**Verify**:

- true-positive and true-negative tests from reference fixtures
- structured-context exceptions covered by tests
- no rule re-parses markdown structure from raw source

### Phase 6 -- Class B and Class H Rules

**Scope**: Implement parser-local discourse rules and bounded semantic heuristics.

**Create**:

- `rules/discourse/`
- `rules/paragraph/`
- `rules/structure/`
- `rules/audience/definition_before_use.py`
- `rules/audience/jargon_density.py`
- `rules/audience/claim_calibration.py`

**Policy constraints**:

- heuristics must emit evidence
- heuristics must declare abstention conditions
- heuristics start at conservative severities/kinds until evaluation promotes them
- embeddings are optional; rules depending on them degrade explicitly, not silently

**Verify**:

- topic-sentence heuristics respect transitional-opener and motivating-example exceptions
- redundancy rules suppress known false-positive patterns such as same-object/different-claim paragraphs
- transition and claim-calibration rules test both positive and non-trigger cases with evidence fields asserted

### Phase 7 -- Revision Plan and Guarded Candidate Rewrites

**Scope**: Produce revision plans and template rewrites only when rewrite preconditions are satisfied.

**Create**:

- `suggest/planner.py`
- `suggest/template.py`

**Rules**:

- the system never edits the source file
- candidate rewrites are emitted only when the rewrite is structurally unambiguous
- otherwise the output is a tactic, not a rewritten sentence

**Verify**:

- nominalization rewrites only fire when a stable verbal form exists
- passive-to-active suggestions require an identifiable actor
- report distinguishes between concrete rewrite candidates and higher-level tactics

---

## Phase Dependencies

```text
Phase 1 (Foundation and Contracts)
  |
  v
Phase 2 (Parsing / Source Views / Projections)
  |
  v
Phase 3 (Annotation / Feature Store / Reliability)
  |
  v
Phase 4 (Real Engine / CLI / Scoring / Reporting)
  |
  +---> Phase 5 (Class A Rules) --------+
  |                                     |
  +---> Phase 6 (Class B + Class H) ----+
                                        |
                                        v
                              Phase 7 (Revision Plan / Suggestions)
```

Phases 5 and 6 can proceed in parallel after Phase 4, because the real execution path already exists.

---

## Dependencies

| Package                  | Version | Purpose                                                         |
| ------------------------ | ------- | --------------------------------------------------------------- |
| `markdown-it-py`         | >=3.0   | Markdown parsing                                                |
| `spacy`                  | >=3.7   | English tokenization, sentence segmentation, POS, dep, lemma    |
| `pydantic`               | >=2.0   | Config schema validation                                        |
| `pyyaml`                 | >=6.0   | YAML loading                                                    |
| `sentence-transformers`  | >=2.0   | Optional: embedding-based candidate generation for redundancy   |
| `en-core-web-sm`         | pinned  | v1 English spaCy model used in tests and runtime                |

Not required in v1 core:

- non-English spaCy models
- `coreferee` or any other coreference backend
- LLM runtime dependencies

---

## Future Extensions (Not In v1)

- Additional language packs (`fr`, `es`, `de`, etc.) with per-rule validation
- Experimental coreference backend and `discourse.coreference`
- LLM-backed `SemanticAuditor` for `class_c` criteria
- LLM-backed constrained suggestion generation
- LaTeX parser
- Editor integration
- Incremental analysis and persistent caching
- More scalable redundancy candidate search for very large corpora
