"""Script temporal para buscar y seleccionar papers en batch."""

from pipeline.db.schema import init_db
from pipeline.db.operations import insert_paper, get_paper_by_doi
from pipeline.db.models import Paper
from pipeline.discovery.openalex import search_openalex
from pipeline.discovery.crossref import search_crossref

init_db()

QUERIES = [
    "control interno gestión financiera microempresas México",
    "accounting information systems impact small business performance",
    "diagnóstico financiero pequeñas empresas análisis documental",
    "qualitative research methodology case study small enterprise",
    "entrevista semiestructurada investigación cualitativa empresas",
]

all_results = []
seen_dois = set()

for query in QUERIES:
    print(f"\n{'='*60}")
    print(f"BUSCANDO: {query}")
    print('='*60)

    results_oa = search_openalex(query, max_results=15)
    results_cr = search_crossref(query, max_results=15)

    for r in results_oa + results_cr:
        doi = r.get("doi", "")
        if not doi or doi in seen_dois:
            continue
        seen_dois.add(doi)
        all_results.append(r)
        print(f"  [{r.get('source', '?')}] ({r.get('year', '?')}) {r.get('authors', '?')[:40]} — {r.get('title', '?')[:60]}")

print(f"\n\nTotal resultados únicos: {len(all_results)}")

# Filtrar: solo artículos con DOI, año >= 2015, que tengan autores y título
RELEVANCE_KEYWORDS = [
    "microempresa", "pyme", "small enterprise", "small business", "sme",
    "financial", "financier", "contab", "accounting", "control interno",
    "internal control", "gestión", "management", "información", "information",
    "diagnóstico", "diagnostic", "qualitative", "cualitativ", "entrevista",
    "interview", "case study", "estudio de caso", "documental", "document",
    "impacto", "impact", "decisiones", "decision", "sistema", "system",
]

def relevance_score(r):
    score = 0
    text = f"{r.get('title', '')} {r.get('abstract', '')}".lower()
    for kw in RELEVANCE_KEYWORDS:
        if kw in text:
            score += 1
    # Bonus por año reciente
    year = r.get("year") or 0
    if year >= 2020:
        score += 3
    elif year >= 2015:
        score += 1
    return score

scored = [(relevance_score(r), r) for r in all_results]
scored.sort(key=lambda x: x[0], reverse=True)

# Seleccionar top 15
top = scored[:15]

print(f"\n\n{'='*60}")
print("TOP 15 MÁS RELEVANTES — Agregando a SQLite...")
print('='*60)

added = 0
for score, r in top:
    doi = r.get("doi")
    if get_paper_by_doi(doi):
        print(f"  [YA EXISTE] ({r.get('year')}) {r['title'][:60]}")
        continue

    paper = Paper(
        doi=doi,
        title=r["title"],
        authors=r["authors"],
        year=r.get("year"),
        journal=r.get("journal"),
        abstract=r.get("abstract"),
        openalex_id=r.get("openalex_id"),
    )
    pid = insert_paper(paper)
    added += 1
    print(f"  [id={pid}] (score={score}, {r.get('year')}) {r['title'][:70]}")

print(f"\n{added} papers nuevos agregados como pending.")
