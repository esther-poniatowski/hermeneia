"""Embedding backend implementations and composition helpers."""

from __future__ import annotations

import importlib
from typing import Any

from hermeneia.config.schema import EmbeddingConfig
from hermeneia.document.indexes import EmbeddingBackend


class SentenceTransformerEmbeddingBackend:
    """Lazy sentence-transformers backend bound to a specific model id.

    Parameters
    ----------
    model_name : str
        Input value for ``model_name``.
    """

    def __init__(self, model_name: str) -> None:
        """Initialize the instance."""
        self._model_name = model_name
        self._model: Any | None = None

    def embed_text(self, text: str) -> tuple[float, ...]:
        """Embed text.

        Parameters
        ----------
        text : str
            Text content to process.

        Returns
        -------
        tuple[float, ...]
            Resulting value produced by this call.
        """
        model = self._get_model()
        raw = model.encode(text, normalize_embeddings=True)
        return _coerce_vector(raw)

    def _get_model(self) -> Any:
        """Get model."""
        if self._model is not None:
            return self._model
        try:
            sentence_transformers = importlib.import_module("sentence_transformers")
        except ImportError as exc:  # pragma: no cover - dependency boundary
            raise RuntimeError(
                "Embedding backend 'sentence_transformers' requires the "
                "'sentence-transformers' package."
            ) from exc
        sentence_transformer_cls = getattr(
            sentence_transformers, "SentenceTransformer", None
        )
        if sentence_transformer_cls is None:
            raise RuntimeError(
                "Embedding backend 'sentence_transformers' is installed but does not expose "
                "SentenceTransformer."
            )
        self._model = sentence_transformer_cls(self._model_name)
        return self._model


def build_embedding_backend(config: EmbeddingConfig) -> EmbeddingBackend | None:
    """Create the configured embedding backend for pipeline injection.

    Parameters
    ----------
    config : EmbeddingConfig
        Resolved configuration used by this operation.

    Returns
    -------
    EmbeddingBackend | None
        Resulting value produced by this call.

    Raises
    ------
    ValueError
        Raised under documented error conditions.
    """

    if config.backend == "none":
        return None
    if config.backend == "sentence_transformers":
        return SentenceTransformerEmbeddingBackend(config.model)
    raise ValueError(f"Unsupported embedding backend '{config.backend}'")


def _coerce_vector(raw: object) -> tuple[float, ...]:
    """Coerce vector."""
    if hasattr(raw, "tolist"):
        raw = raw.tolist()
    if isinstance(raw, tuple):
        return tuple(float(value) for value in raw)
    if isinstance(raw, list):
        if raw and isinstance(raw[0], list):
            nested = raw[0]
            return tuple(float(value) for value in nested)
        return tuple(float(value) for value in raw)
    raise TypeError("Embedding backend returned an unsupported vector shape")
