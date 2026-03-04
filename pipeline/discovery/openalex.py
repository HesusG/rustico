"""Búsqueda de papers en OpenAlex API (gratis, 474M+ papers)."""

import requests


OPENALEX_API = "https://api.openalex.org"


def search_openalex(query: str, max_results: int = 20) -> list[dict]:
    """Busca papers en OpenAlex. Retorna lista de dicts normalizados."""
    params = {
        "search": query,
        "per_page": min(max_results, 50),
        "sort": "relevance_score:desc",
        "filter": "has_doi:true,type:article",
    }

    try:
        resp = requests.get(f"{OPENALEX_API}/works", params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  [OpenAlex error: {e}]")
        return []

    results = []
    for work in data.get("results", []):
        doi = (work.get("doi") or "").replace("https://doi.org/", "")
        if not doi:
            continue

        # Extraer autores
        authorships = work.get("authorships", [])
        authors = "; ".join(
            a.get("author", {}).get("display_name", "?")
            for a in authorships[:10]
        )

        results.append({
            "doi": doi,
            "title": work.get("title", "Sin título"),
            "authors": authors,
            "year": work.get("publication_year"),
            "journal": (work.get("primary_location") or {}).get("source", {}).get("display_name", ""),
            "abstract": _reconstruct_abstract(work.get("abstract_inverted_index")),
            "openalex_id": work.get("id", ""),
            "source": "OpenAlex",
        })

    return results


def _reconstruct_abstract(inverted_index: dict | None) -> str:
    """Reconstruye abstract desde el formato inverted index de OpenAlex."""
    if not inverted_index:
        return ""
    word_positions = []
    for word, positions in inverted_index.items():
        for pos in positions:
            word_positions.append((pos, word))
    word_positions.sort()
    return " ".join(w for _, w in word_positions)[:1000]
