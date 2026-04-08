# Language and NLP

## Language Pack Model

`LanguagePack` encapsulates:

- language code/name
- parser model id
- preprocessing policy thresholds
- lexicons
- per-rule defaults
- optional `supported_rules` allowlist

Current shipped pack: `en`.

`LanguageLexicons` is the canonical source for language-sensitive inventories used by rules and
index builders. It includes:

- claim markers and weak sentence-final words
- transition connectors and reference heads
- topic-sentence and rhetorical-opener phrase inventories
- banned transitions and abstract-framing phrase inventories
- concept-label and reformulation markers
- acronym policy lexicons (allowlist, definition stopwords)
- definitional markers and assumption/hypothesis framing exceptions

## English Runtime

- Parser model id: `en_core_web_sm`
- Pinned version policy is tested via integration snapshots.
- Model availability degradation is explicit (diagnostic emitted).

## Pattern Compilation Strategy

Language-sensitive regex skeletons are centralized in `rules/patterns.py`:

- `compile_leading_phrase_regex(...)`
- `compile_inline_phrase_regex(...)`
- `compile_prefixed_term_regex(...)`
- `compile_hyphen_suffix_regex(...)`

Rules pass lexicon values from `RuleContext.language_pack` into these builders. This keeps rule
modules focused on detection logic while keeping pattern inventories discoverable in one place.

## Annotation Behavior

`SpaCyDocumentAnnotator` attempts spaCy load lazily. On unavailability:

- falls back to regex tokenization
- preserves token/source span contracts
- emits backend diagnostics so parser-local rules can abstain conservatively

## Reliability and Abstention

Sentence flags from projection/source stages are designed to let rules abstain when
parser reliability is reduced (heavy masking, symbol density, fragment contexts).

The abstention policy keeps class-B/class-H diagnostics evidence-bearing and conservative rather than opaque.

## Marker Matching Semantics

Marker checks in annotated rules use shared helpers (`rules/common.py`) that prefer lemma-aware
matching when token annotations are available, with bounded string fallback otherwise. This avoids
requiring every inflected form (`prove`, `proves`, `proved`, ...) to be listed explicitly.
