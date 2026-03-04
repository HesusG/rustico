"""Entry point CLI para el pipeline de escritura académica."""

import click
from rich.console import Console
from rich.table import Table

console = Console()


@click.group()
def cli():
    """Pipeline de escritura académica con APA 7 y fuentes verificadas."""
    from pipeline.db.schema import init_db
    init_db()


# ── status ──────────────────────────────────────────────────────────────

@cli.command()
def status():
    """Resumen del estado actual del pipeline."""
    from pipeline.db.operations import get_stats

    stats = get_stats()

    table = Table(title="Estado del Pipeline", show_lines=True)
    table.add_column("Recurso", style="cyan")
    table.add_column("Total", style="green", justify="right")
    table.add_column("Detalle", style="yellow")

    # Papers
    by_status = stats.get("papers_by_status", {})
    detail = ", ".join(f"{k}: {v}" for k, v in by_status.items()) if by_status else "-"
    table.add_row("Papers", str(stats["papers"]), detail)

    # Chunks
    table.add_row("Chunks", str(stats["chunks"]), "-")

    # Sesiones
    table.add_row("Sesiones de escritura", str(stats["writing_sessions"]), "-")

    # Párrafos
    by_status = stats.get("paragraphs_by_status", {})
    detail = ", ".join(f"{k}: {v}" for k, v in by_status.items()) if by_status else "-"
    table.add_row("Párrafos", str(stats["paragraphs"]), detail)

    # Citas
    table.add_row("Citas", str(stats["citations"]), "-")

    console.print(table)


# ── search ──────────────────────────────────────────────────────────────

@cli.command()
@click.argument("query")
@click.option("--max-results", "-n", default=20, help="Máximo de resultados")
def search(query, max_results):
    """Buscar papers académicos en OpenAlex + CrossRef."""
    from pipeline.discovery.openalex import search_openalex
    from pipeline.discovery.crossref import search_crossref
    from pipeline.db.operations import insert_paper, get_paper_by_doi
    from pipeline.db.models import Paper

    console.print(f"\n[bold]Buscando:[/bold] {query}\n")

    # OpenAlex
    console.print("[cyan]→ Consultando OpenAlex...[/cyan]")
    results_oa = search_openalex(query, max_results=max_results)

    # CrossRef
    console.print("[cyan]→ Consultando CrossRef...[/cyan]")
    results_cr = search_crossref(query, max_results=max_results)

    # Deduplicar por DOI
    seen_dois = set()
    all_results = []
    for r in results_oa + results_cr:
        doi = r.get("doi", "")
        if doi and doi in seen_dois:
            continue
        if doi:
            seen_dois.add(doi)
        all_results.append(r)

    if not all_results:
        console.print("[red]No se encontraron resultados.[/red]")
        return

    # Mostrar tabla
    table = Table(title=f"Resultados ({len(all_results)})", show_lines=True)
    table.add_column("#", style="bold", width=4)
    table.add_column("Año", width=6)
    table.add_column("Autores", max_width=30)
    table.add_column("Título", max_width=50)
    table.add_column("DOI", max_width=30)
    table.add_column("Fuente", width=10)

    for i, r in enumerate(all_results, 1):
        table.add_row(
            str(i), str(r.get("year", "?")),
            r.get("authors", "?")[:30],
            r.get("title", "?")[:50],
            r.get("doi", "-")[:30],
            r.get("source", "?"),
        )
    console.print(table)

    # Selección interactiva
    selection = console.input(
        "\n[bold]Selecciona papers (números separados por coma, o 'all', o Enter para cancelar):[/bold] "
    ).strip()

    if not selection:
        return

    if selection.lower() == "all":
        indices = list(range(len(all_results)))
    else:
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(",")]
        except ValueError:
            console.print("[red]Entrada inválida.[/red]")
            return

    added = 0
    for idx in indices:
        if 0 <= idx < len(all_results):
            r = all_results[idx]
            doi = r.get("doi")
            if doi and get_paper_by_doi(doi):
                console.print(f"  [yellow]Ya existe:[/yellow] {doi}")
                continue
            paper = Paper(
                doi=doi, title=r["title"], authors=r["authors"],
                year=r.get("year"), journal=r.get("journal"),
                abstract=r.get("abstract"), openalex_id=r.get("openalex_id"),
            )
            pid = insert_paper(paper)
            console.print(f"  [green]Guardado (id={pid}):[/green] {paper.title[:60]}")
            added += 1

    console.print(f"\n[bold green]{added} papers agregados como pending.[/bold green]")


# ── download ────────────────────────────────────────────────────────────

@cli.command()
@click.option("--pending", is_flag=True, help="Descargar todos los papers pendientes")
@click.option("--paper-id", type=int, help="Descargar un paper específico por ID")
def download(pending, paper_id):
    """Descargar PDFs de papers pendientes via Unpaywall."""
    from pipeline.discovery.unpaywall import resolve_pdf_url
    from pipeline.discovery.downloader import download_pdf
    from pipeline.db.operations import get_papers_by_status, get_paper, update_paper_status

    if paper_id:
        papers = [get_paper(paper_id)]
        papers = [p for p in papers if p]
    elif pending:
        papers = get_papers_by_status("pending")
    else:
        console.print("[yellow]Usa --pending o --paper-id N[/yellow]")
        return

    if not papers:
        console.print("[yellow]No hay papers para descargar.[/yellow]")
        return

    console.print(f"\n[bold]Descargando {len(papers)} papers...[/bold]\n")

    for paper in papers:
        console.print(f"  [{paper.id}] {paper.title[:60]}...")
        if not paper.doi:
            console.print("    [red]Sin DOI, no se puede resolver.[/red]")
            update_paper_status(paper.id, "failed")
            continue

        pdf_url = resolve_pdf_url(paper.doi)
        if not pdf_url:
            console.print("    [red]No se encontró PDF open access.[/red]")
            update_paper_status(paper.id, "failed")
            continue

        result = download_pdf(pdf_url, paper.doi)
        if result["success"]:
            update_paper_status(
                paper.id, "downloaded",
                local_path=result["path"],
                file_hash=result["hash"],
            )
            console.print(f"    [green]Descargado → {result['path']}[/green]")
        else:
            update_paper_status(paper.id, "failed")
            console.print(f"    [red]Error: {result['error']}[/red]")


# ── process ─────────────────────────────────────────────────────────────

@cli.command()
@click.option("--all-new", is_flag=True, help="Procesar todos los papers descargados sin chunks")
@click.option("--paper-id", type=int, help="Procesar un paper específico")
def process(all_new, paper_id):
    """Extraer texto, chunking y embeddings de PDFs descargados."""
    from pipeline.processing.pdf_extractor import extract_pdf
    from pipeline.processing.chunker import chunk_sections
    from pipeline.processing.embedder import get_embedder
    from pipeline.processing.vector_store import get_store
    from pipeline.db.operations import (
        get_papers_by_status, get_paper, paper_has_chunks, insert_chunk
    )
    from pipeline.db.models import Chunk

    if paper_id:
        papers = [get_paper(paper_id)]
        papers = [p for p in papers if p and p.local_path]
    elif all_new:
        downloaded = get_papers_by_status("downloaded") + get_papers_by_status("manual")
        papers = [p for p in downloaded if not paper_has_chunks(p.id)]
    else:
        console.print("[yellow]Usa --all-new o --paper-id N[/yellow]")
        return

    if not papers:
        console.print("[yellow]No hay papers nuevos para procesar.[/yellow]")
        return

    embedder = get_embedder()
    store = get_store()

    console.print(f"\n[bold]Procesando {len(papers)} papers...[/bold]\n")

    for paper in papers:
        console.print(f"  [{paper.id}] {paper.title[:60]}...")
        try:
            sections = extract_pdf(paper.local_path)
            chunks = chunk_sections(sections)
            console.print(f"    Extraídos {len(chunks)} chunks")

            texts = [c["text"] for c in chunks]
            embeddings = embedder.encode(texts)

            for i, (chunk_data, embedding) in enumerate(zip(chunks, embeddings)):
                chroma_id = f"paper_{paper.id}_chunk_{i}"
                chunk = Chunk(
                    paper_id=paper.id,
                    section_title=chunk_data.get("section"),
                    page=chunk_data.get("page"),
                    chunk_index=i,
                    text=chunk_data["text"],
                    char_count=len(chunk_data["text"]),
                    chroma_id=chroma_id,
                )
                chunk_id = insert_chunk(chunk)

                store.add(
                    ids=[chroma_id],
                    embeddings=[embedding.tolist()],
                    documents=[chunk_data["text"]],
                    metadatas=[{
                        "paper_id": paper.id,
                        "doi": paper.doi or "",
                        "authors": paper.authors,
                        "year": paper.year or 0,
                        "title": paper.title,
                        "section": chunk_data.get("section", ""),
                        "page": chunk_data.get("page", 0),
                        "sqlite_chunk_id": chunk_id,
                    }],
                )

            console.print(f"    [green]OK — {len(chunks)} chunks almacenados[/green]")
        except Exception as e:
            console.print(f"    [red]Error: {e}[/red]")


# ── write ───────────────────────────────────────────────────────────────

@cli.command()
@click.argument("chapter", type=int)
@click.argument("section")
@click.option("--outline", "-o", default="", help="Descripción del contenido de la sección")
def write(chapter, section, outline):
    """Escribir una sección con RAG + verificación + aprobación humana."""
    from pipeline.writing.retriever import retrieve_chunks
    from pipeline.writing.composer import compose_paragraph
    from pipeline.writing.verifier import verify_paragraph
    from pipeline.review.reviewer import review_paragraph
    from pipeline.db.operations import (
        create_session, insert_paragraph, link_paragraph_chunk,
        update_paragraph, update_session_status,
    )
    from pipeline.db.models import Paragraph

    session_id = create_session(chapter, section, outline)
    console.print(f"\n[bold]Sesión #{session_id} — Cap. {chapter}, Sección {section}[/bold]")
    if outline:
        console.print(f"[dim]Outline: {outline}[/dim]\n")

    paragraph_num = 0
    context_paragraphs = []

    while True:
        paragraph_num += 1
        console.print(f"\n[bold cyan]═══ Párrafo #{paragraph_num} ═══[/bold cyan]")

        # Pedir tema/foco del párrafo
        topic = console.input(
            "[bold]Tema/foco de este párrafo (o 'fin' para terminar):[/bold] "
        ).strip()
        if topic.lower() in ("fin", "end", "q", "quit"):
            break

        # RAG: buscar chunks relevantes
        query = f"{outline} {topic}" if outline else topic
        ranked_chunks = retrieve_chunks(query, top_k=15)

        if not ranked_chunks:
            console.print("[red]No se encontraron chunks relevantes.[/red]")
            continue

        # Mostrar chunks y pedir selección
        table = Table(title="Chunks relevantes", show_lines=True)
        table.add_column("#", width=4)
        table.add_column("Score", width=8)
        table.add_column("Cita", max_width=25)
        table.add_column("Sección", max_width=20)
        table.add_column("Texto", max_width=60)

        for i, rc in enumerate(ranked_chunks, 1):
            meta = rc["metadata"]
            cite = f"({meta.get('authors', '?').split(';')[0].split(',')[0]}, {meta.get('year', '?')})"
            table.add_row(
                str(i),
                f"{rc['score']:.3f}",
                cite[:25],
                str(meta.get("section", ""))[:20],
                rc["text"][:60].replace("\n", " "),
            )
        console.print(table)

        selection = console.input(
            "\n[bold]Selecciona chunks a usar (ej: 1,3,5 o Enter para todos los top 5):[/bold] "
        ).strip()

        if not selection:
            selected_indices = list(range(min(5, len(ranked_chunks))))
        else:
            try:
                selected_indices = [int(x.strip()) - 1 for x in selection.split(",")]
            except ValueError:
                console.print("[red]Entrada inválida, usando top 5.[/red]")
                selected_indices = list(range(min(5, len(ranked_chunks))))

        selected_chunks = [ranked_chunks[i] for i in selected_indices if 0 <= i < len(ranked_chunks)]

        # Componer párrafo
        console.print("\n[cyan]Componiendo párrafo con Gemini...[/cyan]")
        paragraph_text = compose_paragraph(
            selected_chunks, topic, outline,
            context_paragraphs=context_paragraphs,
        )

        # Verificar
        console.print("[cyan]Verificando...[/cyan]")
        verification = verify_paragraph(paragraph_text, selected_chunks)

        # Review loop
        while True:
            decision = review_paragraph(paragraph_text, selected_chunks, verification)

            if decision["action"] == "approve":
                para = Paragraph(
                    session_id=session_id,
                    paragraph_order=paragraph_num,
                    text=paragraph_text,
                    status="approved",
                )
                para_id = insert_paragraph(para)

                # Vincular chunks
                for i, rc in enumerate(ranked_chunks):
                    was_sel = i in [idx for idx in selected_indices]
                    link_paragraph_chunk(
                        para_id, rc["chunk_id"],
                        similarity_score=rc["score"],
                        was_selected=was_sel,
                    )

                # Registrar citas
                from pipeline.writing.citation_formatter import extract_and_register_citations
                extract_and_register_citations(para_id, paragraph_text)

                context_paragraphs.append(paragraph_text)
                console.print("[bold green]Párrafo aprobado.[/bold green]")
                break

            elif decision["action"] == "edit":
                paragraph_text = decision["text"]
                console.print("[yellow]Texto editado manualmente.[/yellow]")
                verification = verify_paragraph(paragraph_text, selected_chunks)

            elif decision["action"] == "rewrite":
                console.print("[cyan]Reescribiendo con Gemini...[/cyan]")
                extra_instruction = decision.get("instruction", "")
                paragraph_text = compose_paragraph(
                    selected_chunks, topic, outline,
                    context_paragraphs=context_paragraphs,
                    extra_instruction=extra_instruction,
                )
                verification = verify_paragraph(paragraph_text, selected_chunks)

            elif decision["action"] == "reject":
                para = Paragraph(
                    session_id=session_id,
                    paragraph_order=paragraph_num,
                    text=paragraph_text,
                    status="rejected",
                )
                insert_paragraph(para)
                console.print("[red]Párrafo rechazado.[/red]")
                break

    update_session_status(session_id, "completed")
    console.print(f"\n[bold green]Sesión #{session_id} completada.[/bold green]")


# ── review ──────────────────────────────────────────────────────────────

@cli.command()
@click.argument("session_id", type=int)
def review(session_id):
    """Revisar párrafos pendientes (draft) de una sesión."""
    from pipeline.db.operations import get_paragraphs_by_status, update_paragraph, get_session
    from pipeline.review.reviewer import review_paragraph
    from pipeline.writing.verifier import verify_paragraph

    session = get_session(session_id)
    if not session:
        console.print(f"[red]Sesión {session_id} no encontrada.[/red]")
        return

    console.print(f"\n[bold]Revisando sesión #{session_id} — Cap. {session['chapter']}, {session['section']}[/bold]\n")

    drafts = get_paragraphs_by_status(session_id, "draft")
    if not drafts:
        console.print("[yellow]No hay párrafos pendientes de revisión.[/yellow]")
        return

    for para in drafts:
        console.print(f"\n[bold]Párrafo #{para.paragraph_order}[/bold]")
        verification = verify_paragraph(para.text, [])
        decision = review_paragraph(para.text, [], verification)

        if decision["action"] == "approve":
            update_paragraph(para.id, status="approved")
            console.print("[green]Aprobado.[/green]")
        elif decision["action"] == "edit":
            update_paragraph(para.id, text=decision["text"], status="approved")
            console.print("[green]Editado y aprobado.[/green]")
        elif decision["action"] == "reject":
            update_paragraph(para.id, status="rejected")
            console.print("[red]Rechazado.[/red]")


# ── assemble ────────────────────────────────────────────────────────────

@cli.command()
@click.argument("chapter", type=int)
def assemble(chapter):
    """Ensamblar capítulo final desde párrafos aprobados."""
    from pipeline.review.assembler import assemble_chapter
    output_path = assemble_chapter(chapter)
    if output_path:
        console.print(f"\n[bold green]Capítulo ensamblado → {output_path}[/bold green]")
    else:
        console.print("[red]No se pudo ensamblar el capítulo.[/red]")


# ── add-manual ──────────────────────────────────────────────────────────

@cli.command("add-manual")
@click.argument("pdf_path")
@click.option("--doi", required=True, help="DOI del paper")
@click.option("--title", required=True, help="Título del paper")
@click.option("--authors", required=True, help="Autores (separados por ;)")
@click.option("--year", required=True, type=int, help="Año de publicación")
@click.option("--journal", default="", help="Nombre del journal")
def add_manual(pdf_path, doi, title, authors, year, journal):
    """Agregar un PDF manualmente con su metadata."""
    import shutil
    import hashlib
    from pathlib import Path
    from pipeline.config import PDFS_DIR
    from pipeline.db.operations import insert_paper
    from pipeline.db.models import Paper

    src = Path(pdf_path)
    if not src.exists():
        console.print(f"[red]No se encontró: {pdf_path}[/red]")
        return

    # Copiar a data/pdfs/
    dest = PDFS_DIR / src.name
    if not dest.exists():
        shutil.copy2(src, dest)

    # Hash
    file_hash = hashlib.sha256(dest.read_bytes()).hexdigest()

    paper = Paper(
        doi=doi, title=title, authors=authors, year=year,
        journal=journal, local_path=str(dest), file_hash=file_hash,
        download_status="manual",
    )
    pid = insert_paper(paper)
    console.print(f"[green]Paper agregado (id={pid}): {title}[/green]")


# ── import-existing ─────────────────────────────────────────────────────

@cli.command("import-existing")
def import_existing():
    """Importar los PDFs existentes de capitulo_6/referencias/."""
    import shutil
    import hashlib
    from pathlib import Path
    from pipeline.config import PROJECT_ROOT, PDFS_DIR
    from pipeline.db.operations import insert_paper, get_paper_by_doi
    from pipeline.db.models import Paper

    refs_dir = PROJECT_ROOT / "capitulo_6" / "referencias"
    if not refs_dir.exists():
        console.print(f"[red]No existe: {refs_dir}[/red]")
        return

    # Metadata conocida de los PDFs del capítulo 6
    known_papers = {
        "Bravo_et_al_2018.pdf": {
            "doi": "10.1016/j.jbusres.2017.12.006",
            "title": "The role of financial information in small enterprise management",
            "authors": "Bravo, F.; Rubio, J.; Calderón, L.",
            "year": 2018,
            "journal": "Journal of Business Research",
        },
        "Garcia-Moreno_et_al_2019.pdf": {
            "doi": "10.1108/IJEBR-11-2018-0726",
            "title": "Financial management practices in small enterprises: an empirical study",
            "authors": "García-Moreno, S.; Montoya-del-Corte, J.; Fernández-Laviada, A.",
            "year": 2019,
            "journal": "International Journal of Entrepreneurial Behaviour and Research",
        },
        "Govea_2021.pdf": {
            "doi": "10.33262/exploradordigital.v5i3.1770",
            "title": "Control interno en las microempresas: importancia para el desarrollo empresarial",
            "authors": "Govea, J.",
            "year": 2021,
            "journal": "Explorador Digital",
        },
        "Medina_Aguilar_2013.pdf": {
            "doi": "10.15174/au.2013.515",
            "title": "Sistemas de información financiera y su impacto en las PYMES",
            "authors": "Medina, J.; Aguilar, P.",
            "year": 2013,
            "journal": "Acta Universitaria",
        },
    }

    pdfs = list(refs_dir.glob("*.pdf"))
    if not pdfs:
        console.print("[yellow]No se encontraron PDFs.[/yellow]")
        return

    for pdf in pdfs:
        console.print(f"  Importando: {pdf.name}...")

        # Copiar a data/pdfs/
        dest = PDFS_DIR / pdf.name
        if not dest.exists():
            shutil.copy2(pdf, dest)

        file_hash = hashlib.sha256(dest.read_bytes()).hexdigest()

        meta = known_papers.get(pdf.name, {})
        doi = meta.get("doi", f"manual/{pdf.stem}")

        if get_paper_by_doi(doi):
            console.print(f"    [yellow]Ya existe.[/yellow]")
            continue

        paper = Paper(
            doi=doi,
            title=meta.get("title", pdf.stem.replace("_", " ")),
            authors=meta.get("authors", "Desconocido"),
            year=meta.get("year"),
            journal=meta.get("journal"),
            local_path=str(dest),
            file_hash=file_hash,
            download_status="manual",
        )
        pid = insert_paper(paper)
        console.print(f"    [green]Importado (id={pid})[/green]")

    console.print("[bold green]Importación completada.[/bold green]")


# ── __main__ ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    cli()
