"""RAG: consultar ChromaDB y presentar chunks relevantes."""

from pipeline.processing.embedder import get_embedder
from pipeline.processing.vector_store import query_similar
from pipeline.db.operations import get_chunk_by_chroma_id


def retrieve_chunks(query: str, top_k: int = 15) -> list[dict]:
    """Busca chunks relevantes para una consulta.

    Retorna lista de dicts con: chunk_id, text, score, metadata.
    """
    embedder = get_embedder()
    query_embedding = embedder.encode([query])[0].tolist()

    results = query_similar(query_embedding, top_k=top_k)

    if not results or not results.get("ids") or not results["ids"][0]:
        return []

    ranked = []
    for i, chroma_id in enumerate(results["ids"][0]):
        distance = results["distances"][0][i] if results.get("distances") else 0
        # ChromaDB cosine distance → similarity (1 - distance)
        similarity = 1.0 - distance

        doc = results["documents"][0][i] if results.get("documents") else ""
        meta = results["metadatas"][0][i] if results.get("metadatas") else {}

        # Buscar chunk_id en SQLite
        chunk = get_chunk_by_chroma_id(chroma_id)
        chunk_id = chunk.id if chunk else 0

        ranked.append({
            "chunk_id": chunk_id,
            "chroma_id": chroma_id,
            "text": doc,
            "score": similarity,
            "metadata": meta,
        })

    # Ordenar por score descendente
    ranked.sort(key=lambda x: x["score"], reverse=True)
    return ranked
