"""Verificación anti-alucinación: 3 capas automáticas."""

import re
from pipeline.db.operations import (
    get_all_papers, log_verification,
)
from pipeline.writing.citation_formatter import extract_inline_citations, match_citation_to_paper
from pipeline.processing.embedder import get_embedder


def verify_paragraph(
    text: str,
    selected_chunks: list[dict],
    paragraph_id: int = None,
) -> dict:
    """Ejecuta 3 verificaciones sobre un párrafo.

    Retorna dict con resultado de cada check.
    """
    results = {
        "citation_exists": _check_citations_exist(text, paragraph_id),
        "claim_similarity": _check_claim_similarity(text, selected_chunks, paragraph_id),
        "no_orphan_claims": _check_no_orphan_claims(text, paragraph_id),
        "all_passed": True,
        "warnings": [],
    }

    for check_name in ["citation_exists", "claim_similarity", "no_orphan_claims"]:
        check = results[check_name]
        if not check["passed"]:
            results["all_passed"] = False
        results["warnings"].extend(check.get("warnings", []))

    return results


def _check_citations_exist(text: str, paragraph_id: int = None) -> dict:
    """Capa 4: Verifica que cada (Author, Year) tenga paper descargado en SQLite."""
    citations = extract_inline_citations(text)
    warnings = []
    all_ok = True

    for cit in citations:
        paper_id = match_citation_to_paper(cit["author_key"], cit["year"])
        if not paper_id:
            all_ok = False
            warnings.append(f"Cita no encontrada en DB: {cit['inline_text']}")

        if paragraph_id:
            log_verification(
                paragraph_id=paragraph_id,
                check_type="citation_exists",
                passed=bool(paper_id),
                details=f"{cit['inline_text']} → paper_id={paper_id}",
            )

    return {"passed": all_ok, "warnings": warnings, "count": len(citations)}


def _check_claim_similarity(
    text: str, selected_chunks: list[dict], paragraph_id: int = None
) -> dict:
    """Capa 5: Verifica que las claims del párrafo coincidan con chunks fuente."""
    if not selected_chunks:
        return {"passed": True, "warnings": [], "avg_similarity": 0}

    from pipeline.config import MIN_SIMILARITY_THRESHOLD

    # Dividir párrafo en oraciones
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if not sentences:
        return {"passed": True, "warnings": [], "avg_similarity": 0}

    # Obtener embeddings de oraciones y chunks
    embedder = get_embedder()
    chunk_texts = [c["text"] for c in selected_chunks]

    sent_embeddings = embedder.encode(sentences)
    chunk_embeddings = embedder.encode(chunk_texts)

    import numpy as np
    warnings = []
    similarities = []

    for i, (sent, sent_emb) in enumerate(zip(sentences, sent_embeddings)):
        # Cosine similarity contra cada chunk
        sims = []
        for chunk_emb in chunk_embeddings:
            cos_sim = np.dot(sent_emb, chunk_emb) / (
                np.linalg.norm(sent_emb) * np.linalg.norm(chunk_emb) + 1e-8
            )
            sims.append(float(cos_sim))

        max_sim = max(sims) if sims else 0
        similarities.append(max_sim)

        if max_sim < MIN_SIMILARITY_THRESHOLD:
            short_sent = sent[:80] + "..." if len(sent) > 80 else sent
            warnings.append(f"Baja similitud ({max_sim:.2f}): \"{short_sent}\"")

        if paragraph_id:
            log_verification(
                paragraph_id=paragraph_id,
                check_type="claim_similarity",
                passed=max_sim >= MIN_SIMILARITY_THRESHOLD,
                details=f"sim={max_sim:.3f} sent={sent[:100]}",
            )

    avg_sim = sum(similarities) / len(similarities) if similarities else 0
    passed = len(warnings) == 0

    return {"passed": passed, "warnings": warnings, "avg_similarity": avg_sim}


def _check_no_orphan_claims(text: str, paragraph_id: int = None) -> dict:
    """Verifica que no haya afirmaciones fuertes sin cita."""
    # Buscar oraciones con afirmaciones fuertes sin cita
    sentences = re.split(r'(?<=[.!?])\s+', text)
    warnings = []

    # Patrones que sugieren una afirmación que necesita cita
    strong_claim_patterns = [
        r'(?:según|de acuerdo con|como señala|estudios (?:muestran|indican|demuestran))',
        r'(?:se ha (?:demostrado|comprobado|evidenciado))',
        r'(?:\d+%|\d+ por ciento)',
        r'(?:investigaciones? (?:recientes?|previas?))',
    ]

    combined_pattern = "|".join(strong_claim_patterns)

    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue

        has_strong_claim = re.search(combined_pattern, sent, re.IGNORECASE)
        has_citation = re.search(r'\([^)]*\d{4}[^)]*\)', sent)

        if has_strong_claim and not has_citation:
            short = sent[:80] + "..." if len(sent) > 80 else sent
            warnings.append(f"Claim sin cita: \"{short}\"")

    passed = len(warnings) == 0

    if paragraph_id:
        log_verification(
            paragraph_id=paragraph_id,
            check_type="no_orphan_claims",
            passed=passed,
            details=f"{len(warnings)} claims huérfanas",
        )

    return {"passed": passed, "warnings": warnings}
