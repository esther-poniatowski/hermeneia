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

## English Runtime

- Parser model id: `en_core_web_sm`
- Pinned version policy is tested via integration snapshots.
- Model availability degradation is explicit (diagnostic emitted).

## Annotation Behavior

`SpaCyDocumentAnnotator` attempts spaCy load lazily. On unavailability:

- falls back to regex tokenization
- preserves token/source span contracts
- emits backend diagnostics so parser-local rules can abstain conservatively

## Reliability and Abstention

Sentence flags from projection/source stages are designed to let rules abstain when
parser reliability is reduced (heavy masking, symbol density, fragment contexts).

The abstention policy keeps class-B/class-H diagnostics evidence-bearing and conservative rather than opaque.
