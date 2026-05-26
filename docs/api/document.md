<a id="document"></a>

# Document

Document intermediate representation, parsing, annotation, and source views.

<a id="module-hermeneia.document.model"></a>

<a id="model"></a>

## Model

Pure document-domain models for Hermeneia.

<a id="hermeneia.document.model.Span"></a>

### *class* hermeneia.document.model.Span(start, end, start_line, start_column, end_line, end_column)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Absolute and line-local coordinates for a source region.

<a id="hermeneia.document.model.Span.start"></a>

#### start *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Span.end"></a>

#### end *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Span.start_line"></a>

#### start_line *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Span.start_column"></a>

#### start_column *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Span.end_line"></a>

#### end_line *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Span.end_column"></a>

#### end_column *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Span.contains_offset"></a>

#### contains_offset(offset)

Return whether the span contains the offset.

* **Parameters:**
  **offset** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `offset`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.document.model.Span.overlaps"></a>

#### overlaps(other)

Overlaps.

* **Parameters:**
  **other** ([*Span*](#hermeneia.document.model.Span)) – Input value for `other`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.document.model.Span.line_tuple"></a>

#### line_tuple()

Line tuple.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)]

<a id="hermeneia.document.model.MaskedSegmentKind"></a>

### *class* hermeneia.document.model.MaskedSegmentKind(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Kinds of segments masked during text projection.

<a id="hermeneia.document.model.MaskedSegmentKind.INLINE_MATH"></a>

#### INLINE_MATH *= 'inline_math'*

<a id="hermeneia.document.model.MaskedSegmentKind.INLINE_CODE"></a>

#### INLINE_CODE *= 'inline_code'*

<a id="hermeneia.document.model.MaskedSegmentKind.LINK_TARGET"></a>

#### LINK_TARGET *= 'link_target'*

<a id="hermeneia.document.model.MaskedSegment"></a>

### *class* hermeneia.document.model.MaskedSegment(kind, source_span, placeholder)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

A source segment replaced or suppressed during NLP projection.

<a id="hermeneia.document.model.MaskedSegment.kind"></a>

#### kind *: [MaskedSegmentKind](#hermeneia.document.model.MaskedSegmentKind)*

<a id="hermeneia.document.model.MaskedSegment.source_span"></a>

#### source_span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.model.MaskedSegment.placeholder"></a>

#### placeholder *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.TextProjection"></a>

### *class* hermeneia.document.model.TextProjection(text, normalized_to_source, masked_segments=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Text sent to the annotator plus a character map back to source offsets.

<a id="hermeneia.document.model.TextProjection.text"></a>

#### text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.TextProjection.normalized_to_source"></a>

#### normalized_to_source *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None), ...]*

<a id="hermeneia.document.model.TextProjection.masked_segments"></a>

#### masked_segments *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[MaskedSegment](#hermeneia.document.model.MaskedSegment), ...]* *= ()*

<a id="hermeneia.document.model.TextProjection.source_offset_for"></a>

#### source_offset_for(projection_offset)

Source offset for.

* **Parameters:**
  **projection_offset** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `projection_offset`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int) | None

<a id="hermeneia.document.model.Token"></a>

### *class* hermeneia.document.model.Token(text, lemma, pos, dep, head_idx, source_span, projection_start, projection_end)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Annotated token aligned to both source and projection offsets.

<a id="hermeneia.document.model.Token.text"></a>

#### text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.Token.lemma"></a>

#### lemma *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.Token.pos"></a>

#### pos *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.document.model.Token.dep"></a>

#### dep *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.document.model.Token.head_idx"></a>

#### head_idx *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.document.model.Token.source_span"></a>

#### source_span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.model.Token.projection_start"></a>

#### projection_start *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.Token.projection_end"></a>

#### projection_end *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.model.BlockKind"></a>

### *class* hermeneia.document.model.BlockKind(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Kinds of block-level nodes in the document IR.

<a id="hermeneia.document.model.BlockKind.HEADING"></a>

#### HEADING *= 'heading'*

<a id="hermeneia.document.model.BlockKind.PARAGRAPH"></a>

#### PARAGRAPH *= 'paragraph'*

<a id="hermeneia.document.model.BlockKind.LIST"></a>

#### LIST *= 'list'*

<a id="hermeneia.document.model.BlockKind.LIST_ITEM"></a>

#### LIST_ITEM *= 'list_item'*

<a id="hermeneia.document.model.BlockKind.BLOCK_QUOTE"></a>

#### BLOCK_QUOTE *= 'block_quote'*

<a id="hermeneia.document.model.BlockKind.TABLE"></a>

#### TABLE *= 'table'*

<a id="hermeneia.document.model.BlockKind.TABLE_ROW"></a>

#### TABLE_ROW *= 'table_row'*

<a id="hermeneia.document.model.BlockKind.TABLE_CELL"></a>

#### TABLE_CELL *= 'table_cell'*

<a id="hermeneia.document.model.BlockKind.CODE_BLOCK"></a>

#### CODE_BLOCK *= 'code_block'*

<a id="hermeneia.document.model.BlockKind.DISPLAY_MATH"></a>

#### DISPLAY_MATH *= 'display_math'*

<a id="hermeneia.document.model.BlockKind.FOOTNOTE"></a>

#### FOOTNOTE *= 'footnote'*

<a id="hermeneia.document.model.BlockKind.ADMONITION"></a>

#### ADMONITION *= 'admonition'*

<a id="hermeneia.document.model.InlineKind"></a>

### *class* hermeneia.document.model.InlineKind(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Kinds of inline nodes captured in the document IR.

<a id="hermeneia.document.model.InlineKind.TEXT"></a>

#### TEXT *= 'text'*

<a id="hermeneia.document.model.InlineKind.INLINE_MATH"></a>

#### INLINE_MATH *= 'inline_math'*

<a id="hermeneia.document.model.InlineKind.INLINE_CODE"></a>

#### INLINE_CODE *= 'inline_code'*

<a id="hermeneia.document.model.InlineKind.LINK_TARGET"></a>

#### LINK_TARGET *= 'link_target'*

<a id="hermeneia.document.model.InlineNode"></a>

### *class* hermeneia.document.model.InlineNode(kind, text, span)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

A source-aligned inline fragment embedded in a prose block.

<a id="hermeneia.document.model.InlineNode.kind"></a>

#### kind *: [InlineKind](#hermeneia.document.model.InlineKind)*

<a id="hermeneia.document.model.InlineNode.text"></a>

#### text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.InlineNode.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.model.Sentence"></a>

### *class* hermeneia.document.model.Sentence(id, source_text, span, inline_nodes, projection, tokens=<factory>, annotation_flags=frozenset({}))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

A sentence or sentence-fragment extracted from an annotatable block.

<a id="hermeneia.document.model.Sentence.id"></a>

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.Sentence.source_text"></a>

#### source_text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.Sentence.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.model.Sentence.inline_nodes"></a>

#### inline_nodes *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[InlineNode](#hermeneia.document.model.InlineNode)]*

<a id="hermeneia.document.model.Sentence.projection"></a>

#### projection *: [TextProjection](#hermeneia.document.model.TextProjection)*

<a id="hermeneia.document.model.Sentence.tokens"></a>

#### tokens *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[Token](#hermeneia.document.model.Token)]*

<a id="hermeneia.document.model.Sentence.annotation_flags"></a>

#### annotation_flags *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]* *= frozenset({})*

<a id="hermeneia.document.model.Sentence.token_text"></a>

#### token_text()

Token text.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="hermeneia.document.model.Block"></a>

### *class* hermeneia.document.model.Block(id, kind, span, children=<factory>, sentences=<factory>, inline_nodes=<factory>, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

A block-level node in the canonical document IR.

<a id="hermeneia.document.model.Block.id"></a>

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.Block.kind"></a>

#### kind *: [BlockKind](#hermeneia.document.model.BlockKind)*

<a id="hermeneia.document.model.Block.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.model.Block.children"></a>

#### children *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[Block](#hermeneia.document.model.Block)]*

<a id="hermeneia.document.model.Block.sentences"></a>

#### sentences *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[Sentence](#hermeneia.document.model.Sentence)]*

<a id="hermeneia.document.model.Block.inline_nodes"></a>

#### inline_nodes *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[InlineNode](#hermeneia.document.model.InlineNode)]*

<a id="hermeneia.document.model.Block.metadata"></a>

#### metadata *: [Mapping](https://docs.python.org/3/library/typing.html#typing.Mapping)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

<a id="hermeneia.document.model.Block.iter_blocks"></a>

#### iter_blocks()

Iter blocks.

* **Yields:**
  *Iterable[Block]* – Items yielded by this iterator.

<a id="hermeneia.document.model.SourceLine"></a>

### *class* hermeneia.document.model.SourceLine(text, span, block_id, container_kinds, excluded_spans=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

A raw source line tagged with parser-derived structural context.

<a id="hermeneia.document.model.SourceLine.text"></a>

#### text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.SourceLine.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.model.SourceLine.block_id"></a>

#### block_id *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.document.model.SourceLine.container_kinds"></a>

#### container_kinds *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[BlockKind](#hermeneia.document.model.BlockKind), ...]*

<a id="hermeneia.document.model.SourceLine.excluded_spans"></a>

#### excluded_spans *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[Span](#hermeneia.document.model.Span), ...]* *= ()*

<a id="hermeneia.document.model.Document"></a>

### *class* hermeneia.document.model.Document(blocks, source_lines, indexes, source, path=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Canonical source-of-truth document representation.

<a id="hermeneia.document.model.Document.blocks"></a>

#### blocks *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[Block](#hermeneia.document.model.Block)]*

<a id="hermeneia.document.model.Document.source_lines"></a>

#### source_lines *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[SourceLine](#hermeneia.document.model.SourceLine)]*

<a id="hermeneia.document.model.Document.indexes"></a>

#### indexes *: [DocumentIndexes](#hermeneia.document.indexes.DocumentIndexes)*

<a id="hermeneia.document.model.Document.source"></a>

#### source *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.model.Document.path"></a>

#### path *: Path | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.document.model.Document.iter_blocks"></a>

#### iter_blocks()

Iter blocks.

* **Yields:**
  *Iterable[Block]* – Items yielded by this iterator.

<a id="hermeneia.document.model.Document.block_by_id"></a>

#### block_by_id(block_id)

Block by id.

* **Parameters:**
  **block_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `block_id`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Block](#hermeneia.document.model.Block) | None

<a id="hermeneia.document.model.Document.sentence_by_id"></a>

#### sentence_by_id(sentence_id)

Sentence by id.

* **Parameters:**
  **sentence_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `sentence_id`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Sentence](#hermeneia.document.model.Sentence) | None

<a id="hermeneia.document.model.Document.prose_blocks"></a>

#### prose_blocks()

Prose blocks.

* **Yields:**
  *Iterable[Block]* – Items yielded by this iterator.

<a id="module-hermeneia.document.markdown"></a>

<a id="markdown-parser"></a>

## Markdown parser

Markdown-it-backed parser into the Hermeneia document IR.

<a id="hermeneia.document.markdown.VisibleBuffer"></a>

### *class* hermeneia.document.markdown.VisibleBuffer(text, source_offsets, special_spans)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Visiblebuffer.

<a id="hermeneia.document.markdown.VisibleBuffer.text"></a>

#### text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.markdown.VisibleBuffer.source_offsets"></a>

#### source_offsets *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None), ...]*

<a id="hermeneia.document.markdown.VisibleBuffer.special_spans"></a>

#### special_spans *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[InlineSpan](#hermeneia.document.markdown.InlineSpan), ...]*

<a id="hermeneia.document.markdown.InlineSpan"></a>

### *class* hermeneia.document.markdown.InlineSpan(kind, start, end, span, text)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Inlinespan.

<a id="hermeneia.document.markdown.InlineSpan.kind"></a>

#### kind *: [InlineKind](#hermeneia.document.model.InlineKind)*

<a id="hermeneia.document.markdown.InlineSpan.start"></a>

#### start *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.markdown.InlineSpan.end"></a>

#### end *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.markdown.InlineSpan.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.markdown.InlineSpan.text"></a>

#### text *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.markdown.MarkdownDocumentParser"></a>

### *class* hermeneia.document.markdown.MarkdownDocumentParser(language_pack)

Bases: [`DocumentParser`](#hermeneia.document.parser.DocumentParser)

Parse markdown into the shared block/inline document IR.

* **Parameters:**
  **language_pack** ([*LanguagePack*](language.md#hermeneia.language.base.LanguagePack)) – Input value for `language_pack`.

<a id="hermeneia.document.markdown.MarkdownDocumentParser.__init__"></a>

#### \_\_init_\_(language_pack)

Initialize the instance.

<a id="hermeneia.document.markdown.MarkdownDocumentParser.parse"></a>

#### parse(request)

Parse.

* **Parameters:**
  **request** ([*ParseRequest*](#hermeneia.document.parser.ParseRequest)) – Structured request object for this operation.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Document](#hermeneia.document.model.Document)

<a id="module-hermeneia.document.parser"></a>

<a id="parser"></a>

## Parser

Application-facing parser contracts.

<a id="hermeneia.document.parser.ParseRequest"></a>

### *class* hermeneia.document.parser.ParseRequest(source, path=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Input payload for parsing a single source document.

<a id="hermeneia.document.parser.ParseRequest.source"></a>

#### source *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.parser.ParseRequest.path"></a>

#### path *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path) | [None](https://docs.python.org/3/library/constants.html#None)* *= None*

<a id="hermeneia.document.parser.DocumentParser"></a>

### *class* hermeneia.document.parser.DocumentParser(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for document parser implementations.

<a id="hermeneia.document.parser.DocumentParser.parse"></a>

#### parse(request)

Parse request.

* **Parameters:**
  **request** ([*ParseRequest*](#hermeneia.document.parser.ParseRequest)) – Structured request object for this operation.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Document](#hermeneia.document.model.Document)

<a id="module-hermeneia.document.annotator"></a>

<a id="annotator"></a>

## Annotator

NLP annotation integration with explicit fallback semantics.

<a id="hermeneia.document.annotator.AnnotationBackendStatus"></a>

### *class* hermeneia.document.annotator.AnnotationBackendStatus(backend, diagnostics=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Annotationbackendstatus.

<a id="hermeneia.document.annotator.AnnotationBackendStatus.backend"></a>

#### backend *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.annotator.AnnotationBackendStatus.diagnostics"></a>

#### diagnostics *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]* *= ()*

<a id="hermeneia.document.annotator.SpaCyDocumentAnnotator"></a>

### *class* hermeneia.document.annotator.SpaCyDocumentAnnotator(model_name)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Annotate sentences with spaCy when available, otherwise degrade explicitly.

* **Parameters:**
  **model_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*) – Input value for `model_name`.

<a id="hermeneia.document.annotator.SpaCyDocumentAnnotator.__init__"></a>

#### \_\_init_\_(model_name)

Initialize the instance.

<a id="hermeneia.document.annotator.SpaCyDocumentAnnotator.annotate"></a>

#### annotate(document, profile)

Annotate.

* **Parameters:**
  * **document** ([*Document*](#hermeneia.document.model.Document)) – Document instance to inspect.
  * **profile** ([*ResolvedProfile*](rules-base.md#hermeneia.rules.base.ResolvedProfile)) – Resolved profile controlling rule behavior.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [AnnotationResult](engine.md#hermeneia.engine.runner.AnnotationResult)

<a id="module-hermeneia.document.indexes"></a>

<a id="indexes"></a>

## Indexes

Document indexes and shared feature computations.

<a id="hermeneia.document.indexes.SectionView"></a>

### *class* hermeneia.document.indexes.SectionView(heading_block_id, level, block_ids, span)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Sectionview.

<a id="hermeneia.document.indexes.SectionView.heading_block_id"></a>

#### heading_block_id *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.document.indexes.SectionView.level"></a>

#### level *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.indexes.SectionView.block_ids"></a>

#### block_ids *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

<a id="hermeneia.document.indexes.SectionView.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.indexes.SentenceRef"></a>

### *class* hermeneia.document.indexes.SentenceRef(id, block_id, ordinal, span)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Sentenceref.

<a id="hermeneia.document.indexes.SentenceRef.id"></a>

#### id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.indexes.SentenceRef.block_id"></a>

#### block_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.indexes.SentenceRef.ordinal"></a>

#### ordinal *: [int](https://docs.python.org/3/library/functions.html#int)*

<a id="hermeneia.document.indexes.SentenceRef.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.indexes.SupportSignalKind"></a>

### *class* hermeneia.document.indexes.SupportSignalKind(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Kinds of parser-derived support signals.

<a id="hermeneia.document.indexes.SupportSignalKind.CITATION"></a>

#### CITATION *= 'citation'*

<a id="hermeneia.document.indexes.SupportSignalKind.THEOREM_REF"></a>

#### THEOREM_REF *= 'theorem_ref'*

<a id="hermeneia.document.indexes.SupportSignalKind.PROOF_REF"></a>

#### PROOF_REF *= 'proof_ref'*

<a id="hermeneia.document.indexes.SupportSignalKind.DISPLAYED_EQUATION"></a>

#### DISPLAYED_EQUATION *= 'displayed_equation'*

<a id="hermeneia.document.indexes.SupportSignalKind.QUANTITATIVE_RESULT"></a>

#### QUANTITATIVE_RESULT *= 'quantitative_result'*

<a id="hermeneia.document.indexes.SupportSignalKind.CONTRAST_MARKER"></a>

#### CONTRAST_MARKER *= 'contrast_marker'*

<a id="hermeneia.document.indexes.SupportSignalKind.EXAMPLE_MARKER"></a>

#### EXAMPLE_MARKER *= 'example_marker'*

<a id="hermeneia.document.indexes.SupportSignalKind.DEFINITION_MARKER"></a>

#### DEFINITION_MARKER *= 'definition_marker'*

<a id="hermeneia.document.indexes.SupportSignal"></a>

### *class* hermeneia.document.indexes.SupportSignal(kind, span, block_id, sentence_id)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Supportsignal.

<a id="hermeneia.document.indexes.SupportSignal.kind"></a>

#### kind *: [SupportSignalKind](#hermeneia.document.indexes.SupportSignalKind)*

<a id="hermeneia.document.indexes.SupportSignal.span"></a>

#### span *: [Span](#hermeneia.document.model.Span)*

<a id="hermeneia.document.indexes.SupportSignal.block_id"></a>

#### block_id *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

<a id="hermeneia.document.indexes.SupportSignal.sentence_id"></a>

#### sentence_id *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

<a id="hermeneia.document.indexes.DocumentIndexes"></a>

### *class* hermeneia.document.indexes.DocumentIndexes(sections, sentences, math_block_ids, code_block_ids, term_first_use, symbol_first_use, support_signals)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Precomputed indexes derived from a parsed document.

<a id="hermeneia.document.indexes.DocumentIndexes.sections"></a>

#### sections *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[SectionView](#hermeneia.document.indexes.SectionView)]*

<a id="hermeneia.document.indexes.DocumentIndexes.sentences"></a>

#### sentences *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[SentenceRef](#hermeneia.document.indexes.SentenceRef), ...]*

<a id="hermeneia.document.indexes.DocumentIndexes.math_block_ids"></a>

#### math_block_ids *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

<a id="hermeneia.document.indexes.DocumentIndexes.code_block_ids"></a>

#### code_block_ids *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

<a id="hermeneia.document.indexes.DocumentIndexes.term_first_use"></a>

#### term_first_use *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Span](#hermeneia.document.model.Span)]*

<a id="hermeneia.document.indexes.DocumentIndexes.symbol_first_use"></a>

#### symbol_first_use *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Span](#hermeneia.document.model.Span)]*

<a id="hermeneia.document.indexes.DocumentIndexes.support_signals"></a>

#### support_signals *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[SupportSignal](#hermeneia.document.indexes.SupportSignal)]*

<a id="hermeneia.document.indexes.EmbeddingBackend"></a>

### *class* hermeneia.document.indexes.EmbeddingBackend(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for embedding backend implementations.

<a id="hermeneia.document.indexes.EmbeddingBackend.embed_text"></a>

#### embed_text(text)

Embed text.

* **Parameters:**
  **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Text content to process.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), …]

<a id="hermeneia.document.indexes.FeatureStore"></a>

### *class* hermeneia.document.indexes.FeatureStore(doc, indexes, embedding_backend=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Precomputed document-level features shared across rules.

* **Parameters:**
  * **doc** ([*Document*](#hermeneia.document.model.Document)) – Document instance to inspect.
  * **indexes** ([*DocumentIndexes*](#hermeneia.document.indexes.DocumentIndexes)) – Input value for `indexes`.
  * **embedding_backend** ([*EmbeddingBackend*](#hermeneia.document.indexes.EmbeddingBackend) *|* *None*) – Input value for `embedding_backend`.

<a id="hermeneia.document.indexes.FeatureStore.__init__"></a>

#### \_\_init_\_(doc, indexes, embedding_backend=None)

Initialize the instance.

<a id="hermeneia.document.indexes.FeatureStore.term_first_use"></a>

#### term_first_use(term)

Term first use.

* **Parameters:**
  **term** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `term`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Span](#hermeneia.document.model.Span) | None

<a id="hermeneia.document.indexes.FeatureStore.symbol_first_use"></a>

#### symbol_first_use(symbol)

Symbol first use.

* **Parameters:**
  **symbol** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `symbol`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Span](#hermeneia.document.model.Span) | None

<a id="hermeneia.document.indexes.FeatureStore.support_signals_in_window"></a>

#### support_signals_in_window(anchor_sentence_id, max_sentences_back=3)

Support signals in window.

* **Parameters:**
  * **anchor_sentence_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `anchor_sentence_id`.
  * **max_sentences_back** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `max_sentences_back`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[SupportSignal](#hermeneia.document.indexes.SupportSignal)]

<a id="hermeneia.document.indexes.FeatureStore.sentence_overlap"></a>

#### sentence_overlap(sent_a_id, sent_b_id)

Sentence overlap.

* **Parameters:**
  * **sent_a_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `sent_a_id`.
  * **sent_b_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `sent_b_id`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="hermeneia.document.indexes.FeatureStore.paragraph_overlap"></a>

#### paragraph_overlap(block_id_a, block_id_b)

Paragraph overlap.

* **Parameters:**
  * **block_id_a** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `block_id_a`.
  * **block_id_b** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `block_id_b`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [float](https://docs.python.org/3/library/functions.html#float)

<a id="hermeneia.document.indexes.FeatureStore.embeddings_available"></a>

#### *property* embeddings_available *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Embeddings available.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [bool](https://docs.python.org/3/library/functions.html#bool)

<a id="hermeneia.document.indexes.FeatureStore.sentence_embedding"></a>

#### sentence_embedding(sent_id)

Sentence embedding.

* **Parameters:**
  **sent_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `sent_id`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), …] | None

<a id="hermeneia.document.indexes.FeatureStore.paragraph_embedding"></a>

#### paragraph_embedding(block_id)

Paragraph embedding.

* **Parameters:**
  **block_id** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `block_id`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), …] | None

<a id="hermeneia.document.indexes.FeatureStore.redundancy_candidates"></a>

#### redundancy_candidates(similarity_threshold=0.85)

Redundancy candidates.

* **Parameters:**
  **similarity_threshold** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Input value for `similarity_threshold`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str), [float](https://docs.python.org/3/library/functions.html#float)]]

<a id="hermeneia.document.indexes.FeatureStore.sections"></a>

#### *property* sections *: [list](https://docs.python.org/3/library/stdtypes.html#list)[[SectionView](#hermeneia.document.indexes.SectionView)]*

Sections.

* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[SectionView](#hermeneia.document.indexes.SectionView)]

<a id="hermeneia.document.indexes.FeatureStore.sibling_headings"></a>

#### sibling_headings(level)

Return sibling headings.

* **Parameters:**
  **level** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `level`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[Block](#hermeneia.document.model.Block)]

<a id="hermeneia.document.indexes.FeatureStore.sibling_heading_groups"></a>

#### sibling_heading_groups(level)

Return sibling heading groups.

* **Parameters:**
  **level** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Input value for `level`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[Block](#hermeneia.document.model.Block), …], …]

<a id="hermeneia.document.indexes.build_document_indexes"></a>

### hermeneia.document.indexes.build_document_indexes(doc, contrast_markers, definitional_markers)

Compute canonical derived indexes for a parsed document.

* **Parameters:**
  * **doc** ([*Document*](#hermeneia.document.model.Document)) – Document instance to inspect.
  * **contrast_markers** (*Iterable* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `contrast_markers`.
  * **definitional_markers** (*Iterable* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Input value for `definitional_markers`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [DocumentIndexes](#hermeneia.document.indexes.DocumentIndexes)

<a id="module-hermeneia.document.source_view"></a>

<a id="source-view"></a>

## Source view

Source-view construction for SourcePatternRule consumers.

<a id="hermeneia.document.source_view.build_source_lines"></a>

### hermeneia.document.source_view.build_source_lines(source, blocks)

Build line-oriented source views tagged with parser-derived context.

* **Parameters:**
  * **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Source text to parse or analyze.
  * **blocks** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*Block*](#hermeneia.document.model.Block) *]*) – Input value for `blocks`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[SourceLine](#hermeneia.document.model.SourceLine)]

<a id="hermeneia.document.source_view.rebind_source_view"></a>

### hermeneia.document.source_view.rebind_source_view(doc)

Return the document with its source-line view rebuilt from current blocks.

* **Parameters:**
  **doc** ([*Document*](#hermeneia.document.model.Document)) – Document instance to inspect.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [Document](#hermeneia.document.model.Document)

<a id="module-hermeneia.document.projection"></a>

<a id="projection"></a>

## Projection

Projection building and offset reconciliation for prose annotation.

<a id="hermeneia.document.projection.ProjectionSettings"></a>

### *class* hermeneia.document.projection.ProjectionSettings(heavy_math_masking_ratio=0.4, symbol_dense_threshold=4, fragment_token_threshold=4, code_dominant_ratio=0.5)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Projectionsettings.

<a id="hermeneia.document.projection.ProjectionSettings.heavy_math_masking_ratio"></a>

#### heavy_math_masking_ratio *: [float](https://docs.python.org/3/library/functions.html#float)* *= 0.4*

<a id="hermeneia.document.projection.ProjectionSettings.symbol_dense_threshold"></a>

#### symbol_dense_threshold *: [int](https://docs.python.org/3/library/functions.html#int)* *= 4*

<a id="hermeneia.document.projection.ProjectionSettings.fragment_token_threshold"></a>

#### fragment_token_threshold *: [int](https://docs.python.org/3/library/functions.html#int)* *= 4*

<a id="hermeneia.document.projection.ProjectionSettings.code_dominant_ratio"></a>

#### code_dominant_ratio *: [float](https://docs.python.org/3/library/functions.html#float)* *= 0.5*

<a id="hermeneia.document.projection.ProjectionResult"></a>

### *class* hermeneia.document.projection.ProjectionResult(projection, flags)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Projectionresult.

<a id="hermeneia.document.projection.ProjectionResult.projection"></a>

#### projection *: [TextProjection](#hermeneia.document.model.TextProjection)*

<a id="hermeneia.document.projection.ProjectionResult.flags"></a>

#### flags *: [frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)[[str](https://docs.python.org/3/library/stdtypes.html#str)]*

<a id="hermeneia.document.projection.classify_math_placeholder"></a>

### hermeneia.document.projection.classify_math_placeholder(raw_text)

Return the placeholder that best approximates the masked math slot.

* **Parameters:**
  **raw_text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `raw_text`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="hermeneia.document.projection.build_projection"></a>

### hermeneia.document.projection.build_projection(text, source_offsets, inline_nodes, settings)

Build a normalized projection and populate reliability flags.

* **Parameters:**
  * **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Text content to process.
  * **source_offsets** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *|* *None* *,*  *...* *]*) – Input value for `source_offsets`.
  * **inline_nodes** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*InlineNode*](#hermeneia.document.model.InlineNode) *]*) – Input value for `inline_nodes`.
  * **settings** ([*ProjectionSettings*](#hermeneia.document.projection.ProjectionSettings)) – Input value for `settings`.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [ProjectionResult](#hermeneia.document.projection.ProjectionResult)
