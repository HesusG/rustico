"""Búsqueda de papers en CrossRef API (fallback)."""

import requests


CROSSREF_API = "https://api.crossref.org"


def search_crossref(query: str, max_results: int = 20) -> list[dict]:
    """Busca papers en CrossRef. Retorna lista de dicts normalizados."""
    params = {
        "query": query,
        "rows": min(max_results, 50),
        "filter": "has-full-text:true,type:journal-article",
        "sort": "relevance",
    }

    try:
        resp = requests.get(
            f"{CROSSREF_API}/works", params=params, timeout=15,
            headers={"User-Agent": "RusticoPipeline/1.0 (mailto:user@mail.com)"},
        )
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [CrossRef error: {e}]")
        return []

    results = []
    for item in data.get("message", {}).get("items", []):
        doi = item.get("DOI", "")
        if not doi:
            continue

        # Extraer autores
        author_list = item.get("author", [])
        authors = "; ".join(
            f"{a.get('family', '')}, {a.get('given', '')}"
            for a in author_list[:10]
        )

        # Título
        title_parts = item.get("title", ["Sin título"])
        title = title_parts[0] if title_parts else "Sin título"

        # Año
        date_parts = item.get("published-print", item.get("published-online", {}))
        year = None
        if date_parts and date_parts.get("date-parts"):
            year = date_parts["date-parts"][0][0]

        # Journal
        journal_list = item.get("container-title", [])
        journal = journal_list[0] if journal_list else ""

        results.append({
            "doi": doi,
            "title": title,
            "authors": authors,
            "year": year,
            "journal": journal,
            "abstract": item.get("abstract", "")[:1000],
            "source": "CrossRef",
        })

    return results
