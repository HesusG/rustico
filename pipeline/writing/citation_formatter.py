"""Genera citas inline APA 7 y sección de Referencias."""

import re
from pipeline.db.operations import (
    get_all_papers, get_paper, insert_citation, get_cited_paper_ids,
)
from pipeline.db.models import Citation


def extract_inline_citations(text: str) -> list[dict]:
    """Extrae citas inline del texto: (Autor, Año) → lista de dicts."""
    # Patrones APA 7: (Autor, 2021), (Autor y Autor, 2021), (Autor et al., 2021)
    pattern = r'\(([^)]+?,\s*\d{4}[a-z]?)\)'
    matches = re.findall(pattern, text)

    citations = []
    for match in matches:
        # Separar autor y año
        parts = match.rsplit(",", 1)
        if len(parts) == 2:
            author_key = parts[0].strip()
            try:
                year = int(parts[1].strip().rstrip("abcdef"))
            except ValueError:
                year = None
            citations.append({
                "inline_text": f"({match})",
                "author_key": author_key,
                "year": year,
            })

    return citations


def match_citation_to_paper(author_key: str, year: int | None) -> int | None:
    """Intenta encontrar el paper en SQLite que corresponde a una cita inline."""
    papers = get_all_papers()

    # Normalizar author_key
    key_lower = author_key.lower().replace("et al.", "").strip()

    for paper in papers:
        if paper.download_status not in ("downloaded", "manual"):
            continue

        # Verificar año
        if year and paper.year and paper.year != year:
            continue

        # Verificar autor
        authors_lower = paper.authors.lower()
        # Buscar primer apellido del author_key en los autores del paper
        first_surname = key_lower.split(" y ")[0].split(",")[0].strip()
        if first_surname and first_surname in authors_lower:
            return paper.id

    return None


def extract_and_register_citations(paragraph_id: int, text: str):
    """Extrae citas de un párrafo y las registra en SQLite."""
    citations = extract_inline_citations(text)

    for cit in citations:
        paper_id = match_citation_to_paper(cit["author_key"], cit["year"])
        status = "verified" if paper_id else "unverified"

        citation = Citation(
            paragraph_id=paragraph_id,
            paper_id=paper_id,
            inline_text=cit["inline_text"],
            author_key=cit["author_key"],
            year=cit["year"],
            verification_status=status,
        )
        insert_citation(citation)


def generate_references_section(session_id: int) -> str:
    """Genera la sección ## Referencias APA 7 para una sesión."""
    paper_ids = get_cited_paper_ids(session_id)
    if not paper_ids:
        return ""

    papers = [get_paper(pid) for pid in paper_ids]
    papers = [p for p in papers if p]
    papers.sort(key=lambda p: (p.authors.split(";")[0].split(",")[0], p.year or 0))

    lines = ["## Referencias\n"]
    for paper in papers:
        lines.append(paper.apa_reference + "\n")

    return "\n".join(lines)
