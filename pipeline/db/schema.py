"""DDL SQLite — 7 tablas para el pipeline académico."""

import sqlite3
from pipeline.config import SQLITE_DB

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS papers (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    doi             TEXT UNIQUE,
    title           TEXT NOT NULL,
    authors         TEXT NOT NULL,
    year            INTEGER,
    journal         TEXT,
    abstract        TEXT,
    openalex_id     TEXT,
    local_path      TEXT,
    file_hash       TEXT,
    download_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (download_status IN ('pending','downloading','downloaded','failed','manual')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS chunks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paper_id        INTEGER NOT NULL REFERENCES papers(id),
    section_title   TEXT,
    page            INTEGER,
    chunk_index     INTEGER NOT NULL,
    text            TEXT NOT NULL,
    char_count      INTEGER NOT NULL,
    chroma_id       TEXT UNIQUE,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS writing_sessions (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    chapter         INTEGER NOT NULL,
    section         TEXT NOT NULL,
    outline         TEXT,
    status          TEXT NOT NULL DEFAULT 'active'
        CHECK (status IN ('active','paused','completed')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS paragraphs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id      INTEGER NOT NULL REFERENCES writing_sessions(id),
    paragraph_order INTEGER NOT NULL,
    text            TEXT NOT NULL,
    prompt_used     TEXT,
    status          TEXT NOT NULL DEFAULT 'draft'
        CHECK (status IN ('draft','approved','rejected','rewrite_requested')),
    created_at      TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS paragraph_chunks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paragraph_id    INTEGER NOT NULL REFERENCES paragraphs(id),
    chunk_id        INTEGER NOT NULL REFERENCES chunks(id),
    similarity_score REAL,
    was_selected    INTEGER NOT NULL DEFAULT 0,
    UNIQUE(paragraph_id, chunk_id)
);

CREATE TABLE IF NOT EXISTS citations (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    paragraph_id        INTEGER NOT NULL REFERENCES paragraphs(id),
    paper_id            INTEGER REFERENCES papers(id),
    inline_text         TEXT NOT NULL,
    author_key          TEXT,
    year                INTEGER,
    verification_status TEXT NOT NULL DEFAULT 'pending'
        CHECK (verification_status IN ('pending','verified','unverified','hallucinated')),
    similarity_to_source REAL,
    created_at          TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE TABLE IF NOT EXISTS verification_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    paragraph_id    INTEGER REFERENCES paragraphs(id),
    citation_id     INTEGER REFERENCES citations(id),
    check_type      TEXT NOT NULL,
    passed          INTEGER NOT NULL,
    details         TEXT,
    created_at      TEXT NOT NULL DEFAULT (datetime('now'))
);

CREATE INDEX IF NOT EXISTS idx_papers_doi ON papers(doi);
CREATE INDEX IF NOT EXISTS idx_papers_status ON papers(download_status);
CREATE INDEX IF NOT EXISTS idx_chunks_paper ON chunks(paper_id);
CREATE INDEX IF NOT EXISTS idx_chunks_chroma ON chunks(chroma_id);
CREATE INDEX IF NOT EXISTS idx_paragraphs_session ON paragraphs(session_id);
CREATE INDEX IF NOT EXISTS idx_citations_paragraph ON citations(paragraph_id);
"""


def init_db():
    """Crea la base de datos y todas las tablas si no existen."""
    conn = sqlite3.connect(str(SQLITE_DB))
    conn.executescript(SCHEMA_SQL)
    conn.close()


def get_connection() -> sqlite3.Connection:
    """Retorna una conexión SQLite con row_factory habilitado."""
    conn = sqlite3.connect(str(SQLITE_DB))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
