<a id="infrastructure"></a>

# Infrastructure

Optional infrastructure adapters (e.g. embedding backends) used by semantic rules.

<a id="module-hermeneia.infrastructure.embeddings"></a>

<a id="embeddings"></a>

## Embeddings

Embedding backend implementations and composition helpers.

<a id="hermeneia.infrastructure.embeddings.SentenceTransformerEmbeddingBackend"></a>

### *class* hermeneia.infrastructure.embeddings.SentenceTransformerEmbeddingBackend(model_name)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Lazy sentence-transformers backend bound to a specific model id.

* **Parameters:**
  **model_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Input value for `model_name`.

<a id="hermeneia.infrastructure.embeddings.SentenceTransformerEmbeddingBackend.__init__"></a>

#### \_\_init_\_(model_name)

Initialize the instance.

<a id="hermeneia.infrastructure.embeddings.SentenceTransformerEmbeddingBackend.embed_text"></a>

#### embed_text(text)

Embed text.

* **Parameters:**
  **text** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Text content to process.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), …]

<a id="hermeneia.infrastructure.embeddings.build_embedding_backend"></a>

### hermeneia.infrastructure.embeddings.build_embedding_backend(config)

Create the configured embedding backend for pipeline injection.

* **Parameters:**
  **config** ([*EmbeddingConfig*](config.md#hermeneia.config.schema.EmbeddingConfig)) – Resolved configuration used by this operation.
* **Returns:**
  Resulting value produced by this call.
* **Return type:**
  [EmbeddingBackend](document.md#hermeneia.document.indexes.EmbeddingBackend) | None
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – Raised under documented error conditions.
