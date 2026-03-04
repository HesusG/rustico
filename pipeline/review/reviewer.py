"""UI terminal (rich): párrafo + chunks lado a lado, aprobar/rechazar."""

from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.table import Table

console = Console()


def review_paragraph(
    paragraph_text: str,
    selected_chunks: list[dict],
    verification: dict,
) -> dict:
    """Muestra párrafo + chunks + verificación, pide decisión al usuario.

    Retorna: {action: "approve"|"edit"|"rewrite"|"reject", text?: str, instruction?: str}
    """
    # Panel del párrafo
    para_panel = Panel(
        paragraph_text,
        title="[bold cyan]Párrafo propuesto[/bold cyan]",
        border_style="cyan",
        padding=(1, 2),
    )
    console.print(para_panel)

    # Chunks fuente
    if selected_chunks:
        console.print("\n[bold]Chunks fuente utilizados:[/bold]")
        for i, chunk in enumerate(selected_chunks, 1):
            meta = chunk.get("metadata", {})
            authors = meta.get("authors", "?")
            year = meta.get("year", "?")
            section = meta.get("section", "")
            header = f"[{i}] ({authors.split(';')[0].split(',')[0]}, {year})"
            if section:
                header += f" — {section}"

            chunk_panel = Panel(
                chunk["text"][:500],
                title=header,
                border_style="dim",
                padding=(0, 1),
            )
            console.print(chunk_panel)

    # Verificación
    console.print()
    if verification.get("all_passed"):
        console.print("[bold green]✓ Verificación: TODAS las pruebas pasaron[/bold green]")
    else:
        console.print("[bold yellow]⚠ Verificación: hay advertencias[/bold yellow]")
        for w in verification.get("warnings", []):
            console.print(f"  [yellow]• {w}[/yellow]")

    # Detalle
    cit_check = verification.get("citation_exists", {})
    sim_check = verification.get("claim_similarity", {})
    console.print(f"  Citas encontradas: {cit_check.get('count', 0)}")
    if sim_check.get("avg_similarity"):
        console.print(f"  Similitud promedio: {sim_check['avg_similarity']:.3f}")

    # Decisión
    console.print(
        "\n[bold]Decisión:[/bold] [a]probar  [e]ditar  re[w]rite  [r]echazar"
    )
    choice = console.input("[bold]> [/bold]").strip().lower()

    if choice in ("a", "aprobar"):
        return {"action": "approve"}

    elif choice in ("e", "editar"):
        console.print("[dim]Pega el texto editado (línea vacía + Enter para terminar):[/dim]")
        lines = []
        while True:
            line = input()
            if line == "":
                break
            lines.append(line)
        edited_text = "\n".join(lines) if lines else paragraph_text
        return {"action": "edit", "text": edited_text}

    elif choice in ("w", "rewrite"):
        instruction = console.input(
            "[bold]Instrucción para reescritura (o Enter):[/bold] "
        ).strip()
        return {"action": "rewrite", "instruction": instruction}

    elif choice in ("r", "rechazar"):
        return {"action": "reject"}

    else:
        console.print("[yellow]Opción no reconocida, tratando como rewrite.[/yellow]")
        return {"action": "rewrite", "instruction": ""}
