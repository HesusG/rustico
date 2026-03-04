"""Descargar PDF + validar (magic bytes, tamaño, hash)."""

import hashlib
import re
from pathlib import Path
import requests
from pipeline.config import PDFS_DIR


def download_pdf(url: str, doi: str) -> dict:
    """Descarga un PDF desde url, lo valida y retorna resultado."""
    # Nombre de archivo seguro a partir del DOI
    safe_name = re.sub(r'[^\w\-.]', '_', doi) + ".pdf"
    dest = PDFS_DIR / safe_name

    if dest.exists():
        file_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
        if _validate_pdf(dest):
            return {"success": True, "path": str(dest), "hash": file_hash}

    try:
        resp = requests.get(
            url, timeout=60, stream=True,
            headers={"User-Agent": "RusticoPipeline/1.0"},
        )
        resp.raise_for_status()

        # Escribir en disco
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=8192):
                f.write(chunk)

    except Exception as e:
        return {"success": False, "error": f"Download failed: {e}"}

    # Validar
    if not _validate_pdf(dest):
        dest.unlink(missing_ok=True)
        return {"success": False, "error": "Invalid PDF (magic bytes or too small)"}

    file_hash = hashlib.sha256(dest.read_bytes()).hexdigest()
    return {"success": True, "path": str(dest), "hash": file_hash}


def _validate_pdf(path: Path) -> bool:
    """Valida que el archivo sea un PDF real: magic bytes + tamaño mínimo."""
    if not path.exists():
        return False

    # Tamaño mínimo: 10KB
    if path.stat().st_size < 10240:
        return False

    # Magic bytes: %PDF-
    with open(path, "rb") as f:
        header = f.read(5)
    if header != b"%PDF-":
        return False

    # Verificar legibilidad con PyMuPDF
    try:
        import pymupdf
        doc = pymupdf.open(str(path))
        page_count = len(doc)
        doc.close()
        return page_count > 0
    except Exception:
        return False
