"""Resolver DOI → URL de PDF open access via Unpaywall API + fallback DOI redirect."""

import requests
from pipeline.config import UNPAYWALL_EMAIL


UNPAYWALL_API = "https://api.unpaywall.org/v2"


def resolve_pdf_url(doi: str) -> str | None:
    """Dado un DOI, retorna la URL del PDF open access si existe."""
    # 1. Intentar Unpaywall
    url = _try_unpaywall(doi)
    if url:
        return url

    # 2. Fallback: resolver DOI y buscar PDF en la landing page
    url = _try_doi_redirect(doi)
    if url:
        return url

    return None


def _try_unpaywall(doi: str) -> str | None:
    email = UNPAYWALL_EMAIL
    if not email or email == "user@example.com":
        return None  # Unpaywall requiere email real

    try:
        resp = requests.get(
            f"{UNPAYWALL_API}/{doi}",
            params={"email": email},
            timeout=15,
        )
        if resp.status_code in (404, 422):
            return None
        resp.raise_for_status()
        data = resp.json()
    except Exception:
        return None

    best = data.get("best_oa_location")
    if best:
        pdf_url = best.get("url_for_pdf") or best.get("url")
        if pdf_url:
            return pdf_url

    for loc in data.get("oa_locations", []):
        pdf_url = loc.get("url_for_pdf") or loc.get("url")
        if pdf_url:
            return pdf_url

    return None


def _try_doi_redirect(doi: str) -> str | None:
    """Resuelve DOI → landing page → intenta encontrar enlace a PDF."""
    try:
        resp = requests.get(
            f"https://doi.org/{doi}",
            headers={
                "User-Agent": "RusticoPipeline/1.0",
                "Accept": "application/pdf",
            },
            timeout=15,
            allow_redirects=True,
        )
        # Si el servidor devolvió un PDF directamente
        content_type = resp.headers.get("Content-Type", "")
        if "pdf" in content_type and len(resp.content) > 10240:
            return resp.url

        # Si es HTML, buscar enlace a PDF
        if "html" in content_type:
            return _find_pdf_link(resp.text, resp.url)

    except Exception:
        pass

    return None


def _find_pdf_link(html: str, base_url: str) -> str | None:
    """Busca enlaces a PDF en el HTML de una landing page de journal."""
    import re
    from urllib.parse import urljoin

    # Patrones comunes de enlaces a PDF en journals OA
    patterns = [
        r'href="([^"]*\.pdf[^"]*)"',
        r'href="([^"]*download[^"]*pdf[^"]*)"',
        r'href="([^"]*galley[^"]*)"',
        r'content="([^"]*\.pdf[^"]*)"',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, html, re.IGNORECASE)
        for match in matches:
            url = urljoin(base_url, match)
            # Verificar que no sea un CSS/JS
            if ".css" not in url and ".js" not in url:
                return url

    return None
