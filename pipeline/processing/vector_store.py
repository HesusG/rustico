"""ChromaDB: almacenamiento y búsqueda de embeddings."""

import chromadb
from pipeline.config import CHROMA_DIR, CHROMA_COLLECTION

_client = None
_collection = None


def get_store():
    """Retorna la colección de ChromaDB (singleton)."""
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        _collection = _client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def query_similar(query_embedding: list, top_k: int = 15) -> dict:
    """Busca los chunks más similares al embedding dado."""
    collection = get_store()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )
    return results


def count_vectors() -> int:
    """Retorna el número de vectores en la colección."""
    collection = get_store()
    return collection.count()
