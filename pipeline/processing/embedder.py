"""Embeddings locales con sentence-transformers (jina-embeddings-v2-base-es)."""

from sentence_transformers import SentenceTransformer
from pipeline.config import EMBEDDING_MODEL

_model = None


def get_embedder() -> SentenceTransformer:
    """Retorna el modelo de embeddings (singleton)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(EMBEDDING_MODEL)
    return _model


def encode_texts(texts: list[str]) -> list:
    """Genera embeddings para una lista de textos."""
    model = get_embedder()
    return model.encode(texts, show_progress_bar=len(texts) > 10)
