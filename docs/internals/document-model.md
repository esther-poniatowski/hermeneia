# Document Model

Hermeneia uses a block/inline IR with stable positional ids and explicit span mapping.

## Core Types

- `Span`: absolute offsets + line/column coordinates.
- `Block`: block-level node (`heading`, `paragraph`, `list_item`, `table_cell`, `code_block`, `display_math`, etc.).
- `Sentence`: source span, inline nodes, projection, tokens, annotation flags.
- `TextProjection`: normalized text + projection-to-source mapping + masked segment metadata.
- `SourceLine`: raw line text with parser-derived container context and excluded spans.
- `DocumentIndexes`: canonical derived indexes (sections, sentence refs, first-use maps, support signals).

`DocumentIndexes.support_signals` is language-aware for contrast/definition detection: marker
inventories come from the active language pack lexicons at parse/index build time.

## Identity and Ordering

- `Block.id`: deterministic positional ids (`b000`, `b001`, ...).
- `Sentence.id`: deterministic document-order ids (`s000`, `s001`, ...).
- `SentenceRef.ordinal`: canonical sentence order for lookback and overlap logic.

## Projection and Masking

Inline segments are replaced with typed placeholders before NLP:

- math symbols/expressions -> `MATHSYM` / `MATHNUM` / `MATHEXPR`
- inline code -> `CODEID`
- link targets are masked as typed segments while keeping anchor prose parseable

The projection model preserves parseability and offset traceability simultaneously.

## Reliability Flags

Projection/source builders populate sentence-level flags such as:

- `heavy_math_masking`
- `symbol_dense_sentence`
- `fragment_sentence`
- `code_dominant`
- `table_cell_context`
- `list_item_fragment`

Rules can abstain based on these flags.
