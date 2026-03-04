"""Extracción de texto de PDFs con pymupdf4llm → markdown con secciones."""

import re
import pymupdf4llm


def extract_pdf(pdf_path: str) -> list[dict]:
    """Extrae texto de un PDF y lo divide en secciones.

    Retorna lista de dicts: {section, page, text}
    """
    md_text = pymupdf4llm.to_markdown(pdf_path, page_chunks=True)

    sections = []
    for page_data in md_text:
        page_num = page_data.get("metadata", {}).get("page", 0)
        text = page_data.get("text", "")
        if not text.strip():
            continue

        # Dividir por headings markdown (## o #)
        parts = re.split(r'^(#{1,3}\s+.+)$', text, flags=re.MULTILINE)

        current_section = "General"
        current_text = ""

        for part in parts:
            part = part.strip()
            if not part:
                continue
            if re.match(r'^#{1,3}\s+', part):
                # Guardar sección anterior
                if current_text.strip():
                    sections.append({
                        "section": current_section,
                        "page": page_num,
                        "text": current_text.strip(),
                    })
                current_section = re.sub(r'^#{1,3}\s+', '', part).strip()
                current_text = ""
            else:
                current_text += part + "\n"

        # Última sección de la página
        if current_text.strip():
            sections.append({
                "section": current_section,
                "page": page_num,
                "text": current_text.strip(),
            })

    return sections
