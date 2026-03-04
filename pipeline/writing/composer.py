"""Composición de párrafos académicos usando Gemini con chunks seleccionados."""

from google import genai
from pipeline.config import GOOGLE_API_KEY, GEMINI_MODEL


def compose_paragraph(
    selected_chunks: list[dict],
    topic: str,
    outline: str = "",
    context_paragraphs: list[str] = None,
    extra_instruction: str = "",
) -> str:
    """Compone un párrafo académico usando SOLO los chunks proporcionados.

    Retorna el texto del párrafo con citas inline APA 7.
    """
    # Preparar fuentes
    sources_text = ""
    for i, chunk in enumerate(selected_chunks, 1):
        meta = chunk.get("metadata", {})
        authors = meta.get("authors", "Desconocido")
        year = meta.get("year", "s.f.")
        title = meta.get("title", "")
        sources_text += f"\n--- FUENTE {i} ---\n"
        sources_text += f"Autores: {authors}\n"
        sources_text += f"Año: {year}\n"
        sources_text += f"Título: {title}\n"
        sources_text += f"Texto:\n{chunk['text']}\n"

    # Contexto previo
    context = ""
    if context_paragraphs:
        context = "\n\nPárrafos anteriores de esta sección:\n"
        for p in context_paragraphs[-3:]:  # solo últimos 3 para contexto
            context += f"\n{p}\n"

    prompt = f"""Eres un redactor académico experto en formato APA 7 en español.

TAREA: Escribe UN solo párrafo académico sobre el tema indicado.

REGLAS ESTRICTAS:
1. SOLO usa información de las fuentes proporcionadas abajo. NO inventes datos ni cites fuentes no listadas.
2. Cada afirmación debe estar respaldada por al menos una fuente.
3. Usa citas inline APA 7: (Apellido, Año) o (Apellido1 y Apellido2, Año) o (Apellido1 et al., Año).
4. Escribe en español formal académico, tercera persona.
5. El párrafo debe tener entre 4 y 8 oraciones.
6. NO incluyas la sección de referencias, solo citas inline.
7. Conecta las ideas de forma coherente con el párrafo anterior si existe contexto.

TEMA DEL PÁRRAFO: {topic}
{"OUTLINE DE LA SECCIÓN: " + outline if outline else ""}
{extra_instruction and f"INSTRUCCIÓN ADICIONAL: {extra_instruction}" or ""}

FUENTES DISPONIBLES (SOLO puedes citar estas):
{sources_text}
{context}

Escribe el párrafo:"""

    client = genai.Client(api_key=GOOGLE_API_KEY)
    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return response.text.strip()
