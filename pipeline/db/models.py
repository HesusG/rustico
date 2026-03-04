"""Dataclasses para el pipeline académico."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Paper:
    id: Optional[int] = None
    doi: Optional[str] = None
    title: str = ""
    authors: str = ""
    year: Optional[int] = None
    journal: Optional[str] = None
    abstract: Optional[str] = None
    openalex_id: Optional[str] = None
    local_path: Optional[str] = None
    file_hash: Optional[str] = None
    download_status: str = "pending"

    @property
    def apa_author(self) -> str:
        """Formato corto para cita inline: 'García et al.' o 'García y López'."""
        parts = [a.strip() for a in self.authors.split(";")]
        if len(parts) == 1:
            return parts[0].split(",")[0].strip()
        elif len(parts) == 2:
            a1 = parts[0].split(",")[0].strip()
            a2 = parts[1].split(",")[0].strip()
            return f"{a1} y {a2}"
        else:
            return f"{parts[0].split(',')[0].strip()} et al."

    @property
    def apa_reference(self) -> str:
        """Referencia completa APA 7."""
        authors_list = [a.strip() for a in self.authors.split(";")]
        if len(authors_list) <= 2:
            author_str = " y ".join(authors_list)
        else:
            author_str = ", ".join(authors_list[:-1]) + " y " + authors_list[-1]
        ref = f"{author_str} ({self.year}). {self.title}."
        if self.journal:
            ref += f" *{self.journal}*."
        if self.doi:
            ref += f" https://doi.org/{self.doi}"
        return ref


@dataclass
class Chunk:
    id: Optional[int] = None
    paper_id: int = 0
    section_title: Optional[str] = None
    page: Optional[int] = None
    chunk_index: int = 0
    text: str = ""
    char_count: int = 0
    chroma_id: Optional[str] = None


@dataclass
class Paragraph:
    id: Optional[int] = None
    session_id: int = 0
    paragraph_order: int = 0
    text: str = ""
    prompt_used: Optional[str] = None
    status: str = "draft"


@dataclass
class Citation:
    id: Optional[int] = None
    paragraph_id: int = 0
    paper_id: Optional[int] = None
    inline_text: str = ""
    author_key: Optional[str] = None
    year: Optional[int] = None
    verification_status: str = "pending"
    similarity_to_source: Optional[float] = None
