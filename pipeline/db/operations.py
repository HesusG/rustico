"""CRUD sobre SQLite para el pipeline académico."""

import sqlite3
from typing import Optional
from pipeline.db.schema import get_connection
from pipeline.db.models import Paper, Chunk, Paragraph, Citation


# ── Papers ──────────────────────────────────────────────────────────────

def insert_paper(paper: Paper) -> int:
    conn = get_connection()
    try:
        cur = conn.execute(
            """INSERT INTO papers (doi, title, authors, year, journal, abstract,
               openalex_id, local_path, file_hash, download_status)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (paper.doi, paper.title, paper.authors, paper.year, paper.journal,
             paper.abstract, paper.openalex_id, paper.local_path, paper.file_hash,
             paper.download_status),
        )
        conn.commit()
        return cur.lastrowid
    except sqlite3.IntegrityError:
        # DOI duplicado → retornar el existente
        row = conn.execute("SELECT id FROM papers WHERE doi = ?", (paper.doi,)).fetchone()
        return row["id"] if row else -1
    finally:
        conn.close()


def get_paper(paper_id: int) -> Optional[Paper]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM papers WHERE id = ?", (paper_id,)).fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_paper(row)


def get_paper_by_doi(doi: str) -> Optional[Paper]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM papers WHERE doi = ?", (doi,)).fetchone()
    conn.close()
    if not row:
        return None
    return _row_to_paper(row)


def get_papers_by_status(status: str) -> list[Paper]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM papers WHERE download_status = ? ORDER BY id", (status,)
    ).fetchall()
    conn.close()
    return [_row_to_paper(r) for r in rows]


def get_all_papers() -> list[Paper]:
    conn = get_connection()
    rows = conn.execute("SELECT * FROM papers ORDER BY id").fetchall()
    conn.close()
    return [_row_to_paper(r) for r in rows]


def update_paper_status(paper_id: int, status: str, **kwargs):
    conn = get_connection()
    sets = ["download_status = ?", "updated_at = datetime('now')"]
    vals = [status]
    for k, v in kwargs.items():
        sets.append(f"{k} = ?")
        vals.append(v)
    vals.append(paper_id)
    conn.execute(f"UPDATE papers SET {', '.join(sets)} WHERE id = ?", vals)
    conn.commit()
    conn.close()


def _row_to_paper(row) -> Paper:
    return Paper(
        id=row["id"], doi=row["doi"], title=row["title"], authors=row["authors"],
        year=row["year"], journal=row["journal"], abstract=row["abstract"],
        openalex_id=row["openalex_id"], local_path=row["local_path"],
        file_hash=row["file_hash"], download_status=row["download_status"],
    )


# ── Chunks ──────────────────────────────────────────────────────────────

def insert_chunk(chunk: Chunk) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO chunks (paper_id, section_title, page, chunk_index,
           text, char_count, chroma_id)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (chunk.paper_id, chunk.section_title, chunk.page, chunk.chunk_index,
         chunk.text, chunk.char_count, chunk.chroma_id),
    )
    conn.commit()
    chunk_id = cur.lastrowid
    conn.close()
    return chunk_id


def get_chunks_by_paper(paper_id: int) -> list[Chunk]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM chunks WHERE paper_id = ? ORDER BY chunk_index", (paper_id,)
    ).fetchall()
    conn.close()
    return [_row_to_chunk(r) for r in rows]


def get_chunk(chunk_id: int) -> Optional[Chunk]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM chunks WHERE id = ?", (chunk_id,)).fetchone()
    conn.close()
    return _row_to_chunk(row) if row else None


def get_chunk_by_chroma_id(chroma_id: str) -> Optional[Chunk]:
    conn = get_connection()
    row = conn.execute("SELECT * FROM chunks WHERE chroma_id = ?", (chroma_id,)).fetchone()
    conn.close()
    return _row_to_chunk(row) if row else None


def count_chunks() -> int:
    conn = get_connection()
    row = conn.execute("SELECT COUNT(*) as cnt FROM chunks").fetchone()
    conn.close()
    return row["cnt"]


def paper_has_chunks(paper_id: int) -> bool:
    conn = get_connection()
    row = conn.execute(
        "SELECT COUNT(*) as cnt FROM chunks WHERE paper_id = ?", (paper_id,)
    ).fetchone()
    conn.close()
    return row["cnt"] > 0


def _row_to_chunk(row) -> Chunk:
    return Chunk(
        id=row["id"], paper_id=row["paper_id"], section_title=row["section_title"],
        page=row["page"], chunk_index=row["chunk_index"], text=row["text"],
        char_count=row["char_count"], chroma_id=row["chroma_id"],
    )


# ── Writing Sessions ───────────────────────────────────────────────────

def create_session(chapter: int, section: str, outline: str = "") -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO writing_sessions (chapter, section, outline)
           VALUES (?, ?, ?)""",
        (chapter, section, outline),
    )
    conn.commit()
    sid = cur.lastrowid
    conn.close()
    return sid


def get_session(session_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM writing_sessions WHERE id = ?", (session_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def update_session_status(session_id: int, status: str):
    conn = get_connection()
    conn.execute(
        "UPDATE writing_sessions SET status = ?, updated_at = datetime('now') WHERE id = ?",
        (status, session_id),
    )
    conn.commit()
    conn.close()


# ── Paragraphs ──────────────────────────────────────────────────────────

def insert_paragraph(para: Paragraph) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO paragraphs (session_id, paragraph_order, text, prompt_used, status)
           VALUES (?, ?, ?, ?, ?)""",
        (para.session_id, para.paragraph_order, para.text, para.prompt_used, para.status),
    )
    conn.commit()
    pid = cur.lastrowid
    conn.close()
    return pid


def get_paragraphs_by_session(session_id: int) -> list[Paragraph]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM paragraphs WHERE session_id = ? ORDER BY paragraph_order",
        (session_id,),
    ).fetchall()
    conn.close()
    return [_row_to_paragraph(r) for r in rows]


def get_paragraphs_by_status(session_id: int, status: str) -> list[Paragraph]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM paragraphs WHERE session_id = ? AND status = ? ORDER BY paragraph_order",
        (session_id, status),
    ).fetchall()
    conn.close()
    return [_row_to_paragraph(r) for r in rows]


def update_paragraph(paragraph_id: int, **kwargs):
    conn = get_connection()
    sets = ["updated_at = datetime('now')"]
    vals = []
    for k, v in kwargs.items():
        sets.append(f"{k} = ?")
        vals.append(v)
    vals.append(paragraph_id)
    conn.execute(f"UPDATE paragraphs SET {', '.join(sets)} WHERE id = ?", vals)
    conn.commit()
    conn.close()


def _row_to_paragraph(row) -> Paragraph:
    return Paragraph(
        id=row["id"], session_id=row["session_id"],
        paragraph_order=row["paragraph_order"], text=row["text"],
        prompt_used=row["prompt_used"], status=row["status"],
    )


# ── Paragraph ↔ Chunks ─────────────────────────────────────────────────

def link_paragraph_chunk(paragraph_id: int, chunk_id: int,
                         similarity_score: float = 0.0, was_selected: bool = False):
    conn = get_connection()
    try:
        conn.execute(
            """INSERT INTO paragraph_chunks (paragraph_id, chunk_id, similarity_score, was_selected)
               VALUES (?, ?, ?, ?)""",
            (paragraph_id, chunk_id, similarity_score, int(was_selected)),
        )
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # ya vinculados
    finally:
        conn.close()


def get_paragraph_chunk_ids(paragraph_id: int, selected_only: bool = False) -> list[int]:
    conn = get_connection()
    sql = "SELECT chunk_id FROM paragraph_chunks WHERE paragraph_id = ?"
    if selected_only:
        sql += " AND was_selected = 1"
    rows = conn.execute(sql, (paragraph_id,)).fetchall()
    conn.close()
    return [r["chunk_id"] for r in rows]


# ── Citations ───────────────────────────────────────────────────────────

def insert_citation(cit: Citation) -> int:
    conn = get_connection()
    cur = conn.execute(
        """INSERT INTO citations (paragraph_id, paper_id, inline_text,
           author_key, year, verification_status, similarity_to_source)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (cit.paragraph_id, cit.paper_id, cit.inline_text, cit.author_key,
         cit.year, cit.verification_status, cit.similarity_to_source),
    )
    conn.commit()
    cid = cur.lastrowid
    conn.close()
    return cid


def get_citations_by_paragraph(paragraph_id: int) -> list[Citation]:
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM citations WHERE paragraph_id = ? ORDER BY id", (paragraph_id,)
    ).fetchall()
    conn.close()
    return [_row_to_citation(r) for r in rows]


def get_cited_paper_ids(session_id: int) -> list[int]:
    """Retorna IDs de papers citados en párrafos aprobados de una sesión."""
    conn = get_connection()
    rows = conn.execute(
        """SELECT DISTINCT c.paper_id FROM citations c
           JOIN paragraphs p ON c.paragraph_id = p.id
           WHERE p.session_id = ? AND p.status = 'approved'
           AND c.paper_id IS NOT NULL""",
        (session_id,),
    ).fetchall()
    conn.close()
    return [r["paper_id"] for r in rows]


def _row_to_citation(row) -> Citation:
    return Citation(
        id=row["id"], paragraph_id=row["paragraph_id"], paper_id=row["paper_id"],
        inline_text=row["inline_text"], author_key=row["author_key"],
        year=row["year"], verification_status=row["verification_status"],
        similarity_to_source=row["similarity_to_source"],
    )


# ── Verification Log ───────────────────────────────────────────────────

def log_verification(paragraph_id: int = None, citation_id: int = None,
                     check_type: str = "", passed: bool = True, details: str = ""):
    conn = get_connection()
    conn.execute(
        """INSERT INTO verification_log (paragraph_id, citation_id, check_type, passed, details)
           VALUES (?, ?, ?, ?, ?)""",
        (paragraph_id, citation_id, check_type, int(passed), details),
    )
    conn.commit()
    conn.close()


# ── Stats ───────────────────────────────────────────────────────────────

def get_stats() -> dict:
    conn = get_connection()
    stats = {}
    for table in ["papers", "chunks", "writing_sessions", "paragraphs", "citations"]:
        row = conn.execute(f"SELECT COUNT(*) as cnt FROM {table}").fetchone()
        stats[table] = row["cnt"]
    # Desglose papers por status
    rows = conn.execute(
        "SELECT download_status, COUNT(*) as cnt FROM papers GROUP BY download_status"
    ).fetchall()
    stats["papers_by_status"] = {r["download_status"]: r["cnt"] for r in rows}
    # Desglose párrafos por status
    rows = conn.execute(
        "SELECT status, COUNT(*) as cnt FROM paragraphs GROUP BY status"
    ).fetchall()
    stats["paragraphs_by_status"] = {r["status"]: r["cnt"] for r in rows}
    conn.close()
    return stats
