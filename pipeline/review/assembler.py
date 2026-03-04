"""Ensamblar capítulo final .md + copiar PDFs a referencias/."""

import shutil
from pathlib import Path
from pipeline.config import PROJECT_ROOT
from pipeline.db.operations import (
    get_paragraphs_by_session, get_cited_paper_ids, get_paper,
)
from pipeline.db.schema import get_connection
from pipeline.writing.citation_formatter import generate_references_section


def assemble_chapter(chapter: int) -> str | None:
    """Ensambla todos los párrafos aprobados de un capítulo en un .md.

    Retorna la ruta del archivo generado.
    """
    # Buscar todas las sesiones de este capítulo
    conn = get_connection()
    sessions = conn.execute(
        "SELECT * FROM writing_sessions WHERE chapter = ? ORDER BY id",
        (chapter,),
    ).fetchall()
    conn.close()

    if not sessions:
        return None

    # Directorio de salida
    chapter_dir = PROJECT_ROOT / f"capitulo_{chapter}"
    chapter_dir.mkdir(exist_ok=True)
    refs_dir = chapter_dir / "referencias"
    refs_dir.mkdir(exist_ok=True)

    # Ensamblar contenido
    lines = [f"# Capítulo {chapter}\n\n"]
    all_session_ids = []

    for session in sessions:
        session_id = session["id"]
        section = session["section"]
        all_session_ids.append(session_id)

        lines.append(f"## {section}\n\n")

        paragraphs = get_paragraphs_by_session(session_id)
        approved = [p for p in paragraphs if p.status == "approved"]

        for para in approved:
            lines.append(para.text + "\n\n")

    # Generar referencias
    all_paper_ids = set()
    for sid in all_session_ids:
        all_paper_ids.update(get_cited_paper_ids(sid))

    if all_paper_ids:
        lines.append("\n## Referencias\n\n")
        papers = [get_paper(pid) for pid in all_paper_ids]
        papers = [p for p in papers if p]
        papers.sort(key=lambda p: (p.authors.split(";")[0].split(",")[0], p.year or 0))

        for paper in papers:
            lines.append(paper.apa_reference + "\n\n")

            # Copiar PDF a referencias/
            if paper.local_path:
                src = Path(paper.local_path)
                if src.exists():
                    dest = refs_dir / src.name
                    if not dest.exists():
                        shutil.copy2(src, dest)

    # Escribir archivo
    output_path = chapter_dir / f"capitulo_{chapter}.md"
    output_path.write_text("".join(lines), encoding="utf-8")

    # Reporte de verificación
    _write_verification_report(chapter_dir, all_session_ids)

    return str(output_path)


def _write_verification_report(chapter_dir: Path, session_ids: list[int]):
    """Genera un reporte de verificación para el capítulo."""
    conn = get_connection()

    lines = ["# Reporte de Verificación\n\n"]

    for sid in session_ids:
        session = conn.execute(
            "SELECT * FROM writing_sessions WHERE id = ?", (sid,)
        ).fetchone()
        if not session:
            continue

        lines.append(f"## Sesión #{sid} — {session['section']}\n\n")

        # Párrafos y sus verificaciones
        paragraphs = conn.execute(
            "SELECT * FROM paragraphs WHERE session_id = ? ORDER BY paragraph_order",
            (sid,),
        ).fetchall()

        for para in paragraphs:
            lines.append(f"### Párrafo #{para['paragraph_order']} — {para['status']}\n\n")

            # Citas
            citations = conn.execute(
                "SELECT * FROM citations WHERE paragraph_id = ?", (para["id"],)
            ).fetchall()
            if citations:
                lines.append("**Citas:**\n")
                for cit in citations:
                    status_icon = "✓" if cit["verification_status"] == "verified" else "✗"
                    lines.append(f"- {status_icon} {cit['inline_text']} → {cit['verification_status']}\n")
                lines.append("\n")

            # Verificaciones
            verifications = conn.execute(
                "SELECT * FROM verification_log WHERE paragraph_id = ? ORDER BY id",
                (para["id"],),
            ).fetchall()
            if verifications:
                lines.append("**Verificaciones:**\n")
                for v in verifications:
                    icon = "✓" if v["passed"] else "✗"
                    lines.append(f"- {icon} {v['check_type']}: {v['details'][:100]}\n")
                lines.append("\n")

    conn.close()

    report_path = chapter_dir / "verificacion_reporte.md"
    report_path.write_text("".join(lines), encoding="utf-8")
