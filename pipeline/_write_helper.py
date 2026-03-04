"""Helper para escribir párrafos desde script, sin interactividad."""

import sys
import json
from pipeline.db.schema import init_db
from pipeline.db.operations import (
    create_session, insert_paragraph, link_paragraph_chunk,
    update_session_status,
)
from pipeline.db.models import Paragraph
from pipeline.writing.retriever import retrieve_chunks
from pipeline.writing.composer import compose_paragraph
from pipeline.writing.verifier import verify_paragraph
from pipeline.writing.citation_formatter import extract_and_register_citations

init_db()


def search_chunks(query, top_k=10):
    """Busca chunks relevantes y los muestra."""
    ranked = retrieve_chunks(query, top_k=top_k)
    results = []
    for i, rc in enumerate(ranked):
        meta = rc["metadata"]
        cite = f"({meta.get('authors', '?').split(';')[0].split(',')[0]}, {meta.get('year', '?')})"
        results.append({
            "rank": i + 1,
            "score": round(rc["score"], 3),
            "cite": cite,
            "section": meta.get("section", "")[:40],
            "text_preview": rc["text"][:150].replace("\n", " "),
            "chunk_id": rc["chunk_id"],
            "full_text": rc["text"],
            "metadata": meta,
        })
    return results, ranked


def write_paragraph(topic, outline, selected_chunks, context_paragraphs=None, extra=""):
    """Compone un párrafo con Gemini usando los chunks seleccionados."""
    text = compose_paragraph(
        selected_chunks, topic, outline,
        context_paragraphs=context_paragraphs or [],
        extra_instruction=extra,
    )
    return text


def verify(text, selected_chunks):
    """Verifica un párrafo."""
    return verify_paragraph(text, selected_chunks)


def save_paragraph(session_id, para_num, text, selected_chunks, all_ranked):
    """Guarda párrafo aprobado en DB."""
    para = Paragraph(
        session_id=session_id,
        paragraph_order=para_num,
        text=text,
        status="approved",
    )
    para_id = insert_paragraph(para)

    for rc in all_ranked:
        was_sel = rc in selected_chunks
        link_paragraph_chunk(
            para_id, rc["chunk_id"],
            similarity_score=rc["score"],
            was_selected=was_sel,
        )

    extract_and_register_citations(para_id, text)
    return para_id


if __name__ == "__main__":
    action = sys.argv[1] if len(sys.argv) > 1 else "search"

    if action == "search":
        query = sys.argv[2]
        results, _ = search_chunks(query, top_k=10)
        for r in results:
            print(f"[{r['rank']}] score={r['score']} {r['cite']} | {r['section']}")
            print(f"    {r['text_preview']}")
            print()

    elif action == "create_session":
        chapter = int(sys.argv[2])
        section = sys.argv[3]
        outline = sys.argv[4] if len(sys.argv) > 4 else ""
        sid = create_session(chapter, section, outline)
        print(f"SESSION_ID={sid}")

    elif action == "compose":
        topic = sys.argv[2]
        outline = sys.argv[3]
        # Chunk indices from stdin as JSON
        chunk_data = json.loads(sys.stdin.read())
        selected = chunk_data.get("selected_chunks", [])
        context = chunk_data.get("context", [])
        extra = chunk_data.get("extra", "")
        text = write_paragraph(topic, outline, selected, context, extra)
        print(text)
