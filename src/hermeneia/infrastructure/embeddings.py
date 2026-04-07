"""Embedding backend implementations and composition helpers."""

from __future__ import annotations

from typing import Any

from hermeneia.config.schema import EmbeddingConfig
from hermeneia.document.indexes import EmbeddingBackend


class SentenceTransformerEmbeddingBackend:
    """Lazy sentence-transformers backend bound to a specific model id."""

    def __init__(self, model_name: str) -> None:
        self._model_name = model_name
        self._model: Any | None = None

    def embed_text(self, text: str) -> tuple[float, ...]:
        model = self._get_model()
        raw = model.encode(text, normalize_embeddings=True)
        return _coerce_vector(raw)

    def _get_model(self) -> Any:
        if self._model is not None:
            return self._model
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError as exc:  # pragma: no cover - dependency boundary
            raise RuntimeError(
                "Embedding backend 'sentence_transformers' requires the "
                "'sentence-transformers' package."
            ) from exc
        self._model = SentenceTransformer(self._model_name)
        return self._model


def build_embedding_backend(config: EmbeddingConfig) -> EmbeddingBackend | None:
    """Create the configured embedding backend for pipeline injection."""

    if config.backend == "none":
        return None
    if config.backend == "sentence_transformers":
        return SentenceTransformerEmbeddingBackend(config.model)
    raise ValueError(f"Unsupported embedding backend '{config.backend}'")


def _coerce_vector(raw: object) -> tuple[float, ...]:
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

