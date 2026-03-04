"""Chunking inteligente: respeta secciones, párrafos, oraciones."""

import re
from pipeline.config import CHUNK_TARGET_SIZE, CHUNK_OVERLAP, CHUNK_MIN_SIZE


def chunk_sections(sections: list[dict]) -> list[dict]:
    """Recibe secciones de pdf_extractor y produce chunks.

    Target: 800 chars, 100 overlap, mínimo 200 chars.
    Retorna lista de dicts: {section, page, text}
    """
    all_chunks = []

    for section in sections:
        text = section["text"]
        sec_name = section.get("section", "General")
        page = section.get("page", 0)

        if len(text) <= CHUNK_TARGET_SIZE:
            if len(text) >= CHUNK_MIN_SIZE:
                all_chunks.append({
                    "section": sec_name,
                    "page": page,
                    "text": text.strip(),
                })
            continue

        # Dividir en párrafos
        paragraphs = re.split(r'\n\s*\n', text)
        current_chunk = ""

        for para in paragraphs:
            para = para.strip()
            if not para:
                continue

            if len(current_chunk) + len(para) + 1 <= CHUNK_TARGET_SIZE:
                current_chunk += ("\n\n" if current_chunk else "") + para
            else:
                # Guardar chunk actual
                if len(current_chunk) >= CHUNK_MIN_SIZE:
                    all_chunks.append({
                        "section": sec_name,
                        "page": page,
                        "text": current_chunk.strip(),
                    })

                # Si el párrafo es demasiado largo, dividir por oraciones
                if len(para) > CHUNK_TARGET_SIZE:
                    sentence_chunks = _chunk_by_sentences(para, sec_name, page)
                    all_chunks.extend(sentence_chunks)
                    current_chunk = ""
                else:
                    # Overlap: tomar últimas chars del chunk anterior
                    if current_chunk and CHUNK_OVERLAP > 0:
                        overlap = current_chunk[-CHUNK_OVERLAP:]
                        current_chunk = overlap + "\n\n" + para
                    else:
                        current_chunk = para

        # Último chunk de la sección
        if current_chunk.strip() and len(current_chunk.strip()) >= CHUNK_MIN_SIZE:
            all_chunks.append({
                "section": sec_name,
                "page": page,
                "text": current_chunk.strip(),
            })

    return all_chunks


def _chunk_by_sentences(text: str, section: str, page: int) -> list[dict]:
    """Divide texto largo en chunks basándose en oraciones."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current = ""

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= CHUNK_TARGET_SIZE:
            current += (" " if current else "") + sentence
        else:
            if len(current) >= CHUNK_MIN_SIZE:
                chunks.append({
                    "section": section,
                    "page": page,
                    "text": current.strip(),
                })
            # Overlap
            if current and CHUNK_OVERLAP > 0:
                overlap = current[-CHUNK_OVERLAP:]
                current = overlap + " " + sentence
            else:
                current = sentence

    if current.strip() and len(current.strip()) >= CHUNK_MIN_SIZE:
        chunks.append({
            "section": section,
            "page": page,
            "text": current.strip(),
        })

    return chunks
