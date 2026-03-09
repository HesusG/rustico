#!/usr/bin/env python3
"""
Genera las 10 imagenes de evidencia para Rustico Pizza y Pan
usando Gemini 3 Pro Image (gemini-3-pro-image-preview) a 4K
con prompts optimizados para texto manuscrito realista.

Uso:
    export GEMINI_API_KEY="tu-api-key"
    python generar_imagenes.py                  # Genera todas
    python generar_imagenes.py 03 09            # Solo las indicadas
    python generar_imagenes.py --compress-only   # Solo comprime las existentes
"""

import os
import sys
import time
from pathlib import Path
from io import BytesIO

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Configuracion
# ---------------------------------------------------------------------------
BASE_DIR = Path(__file__).parent
OUTPUT_DIR = BASE_DIR / "evidencias"
COMPRESSED_DIR = BASE_DIR / "evidencias_compressed"
MODEL = "gemini-3-pro-image-preview"
MAX_RETRIES = 3
RETRY_DELAY = 15  # segundos entre reintentos (mas conservador para 4K)

# ---------------------------------------------------------------------------
# Prefijo comun — semantic negative prompts + imperfecciones agresivas
# ---------------------------------------------------------------------------
PREFIJO = """Generate a hyperrealistic documentary-style photograph taken with a modern smartphone \
(iPhone 15 Pro) with natural lighting. This is photographic evidence for an academic \
investigation about internal controls in a small artisanal pizzeria called "Rustico Pizza y Pan" \
in Morelia, Michoacan, Mexico. October 2025.

CRITICAL RULES FOR HANDWRITTEN TEXT:
All visible text MUST be in Mexican Spanish. Never mix with English.

The handwriting must look AUTHENTICALLY HUMAN — like a real worker wrote it quickly between customers:
- Variable slant: some letters lean right, others are more upright, inconsistently
- Inconsistent letter SIZE: some letters in the same word are bigger than others
- Variable PEN PRESSURE: strokes get thicker and thinner naturally, ink pools slightly at curves
- Irregular SPACING between words and between letters within words
- BASELINE DRIFT: lines of text gently rise or fall, never perfectly straight on the page
- LETTERFORM VARIATION: the same letter (a, e, r, s) looks slightly different each time it appears
- Ink characteristics: slight feathering/bleed into paper fibres, occasional ink blob at stroke starts
- One or two NATURAL CORRECTIONS: a crossed-out word rewritten, or a letter written over another
- NOT calligraphy, NOT a computer font, NOT a child's writing, NOT trembling elderly writing
- Think: a 30-year-old Mexican employee writing quickly with a cheap BIC pen on real paper

SEMANTIC NEGATIVE CONSTRAINTS (describe what to AVOID by stating what IS desired):
- The handwriting looks naturally inconsistent and slightly messy, like an actual person wrote it quickly
- Edges are slightly soft like a phone photo; ink has tiny feathering into paper fibres
- Paper has natural texture, micro-wrinkles, and subtle grain — not a flat digital surface
- The photo has slight lens softness at edges, natural smartphone depth of field
- Lighting creates soft shadows showing paper texture and pen indentations

Avoid: typed fonts, calligraphy perfection, vector-clean strokes, perfectly uniform spacing, \
perfectly straight baselines, perfectly consistent letter shapes, printed textbook layout, \
over-sharpened edges, synthetic look, AI-perfect symmetry. No watermarks or UI overlays.

"""

# ---------------------------------------------------------------------------
# Instruccion de refinamiento para segunda pasada (chat turn 2)
# ---------------------------------------------------------------------------
REFINE_INSTRUCTION = """Using the image you just generated, make the following changes while keeping \
paper texture, lighting, shadows, composition, and all other elements IDENTICAL:

Make the handwriting MORE humanly imperfect:
1. INCREASE baseline drift — lines should gently wave, not stay straight
2. VARY letter sizes more — some letters noticeably bigger or smaller than neighbors
3. Make pen PRESSURE more variable — thicker strokes at beginning of words, thinner at ends
4. Add slight INK FEATHERING — tiny bleeding into paper fibres, especially at curves
5. Make the same letter look DIFFERENT each time (e.g., each 'a' slightly unique)
6. Add ONE ink smudge or fingerprint somewhere subtle
7. Make spacing between words IRREGULAR — some words closer, some further apart

Keep all text content EXACTLY the same. Keep it in Spanish. Keep it READABLE but imperfect.
The goal is: if someone saw this photo, they would believe a real person wrote this by hand."""

# ---------------------------------------------------------------------------
# Prompts individuales
# ---------------------------------------------------------------------------
PROMPTS = {
    "01": """Top-down smartphone photo of a hardcover notebook open on a dark rustic wooden table with \
visible wood grain. The notebook has cream-colored lined pages, yellowed from use. A blue BIC pen \
with cap rests on the right page. On the right page there is a circular coffee ring stain.

On the left page, handwritten text in blue ballpoint ink, informal cursive but legible, recording \
business expenses. Format: date — item — amount. Each line on a ruled line:

12/10  Gas LP — $380
14/10  Harina (2 bultos) — $790
15/10  Queso Oaxaca 5kg — $650
17/10  Servilletas y desechables — $145
19/10  Jitomate caja — $230
22/10  Aceite de oliva — $310
24/10  Huevo carton — $95  [this line crossed out with a single horizontal strike]
24/10  Huevo carton — $110
26/10  Verdura variada — $150  [this line crossed out with a single horizontal strike]
26/10  Verdura surtida — $165

The crossed-out lines show natural corrections (single strike, original text still readable beneath).
The handwriting has personality: "g" with long descenders, numbers clear but not identical.
Ink intensity varies — darker at start of each line, lighter toward the end as the pen moves faster.
The "$" signs are each slightly different from each other.
Some lines drift slightly above or below the printed ruling.""",

    "02": """Smartphone photo at 30-degree angle of a sheet of graph paper (letter size) on a stainless \
steel counter. The paper is slightly crumpled with one corner bent. A basic black Casio calculator \
is partially visible in the upper right corner.

Handwritten text in blue and red ballpoint pen. At the top:

"Corte de Caja          Martes 14/Oct/2025"

Below, a hand-drawn table (lines drawn with ruler but not perfectly aligned):

| Concepto          | Entrada  | Salida | Saldo   |
| Fondo inicial     |    —     |   —    | $2,000  |
| Ventas mostrador  | $4,850   |   —    |   —     |
| Pago repartidor   |    —     |  $350  |   —     |
| Compra refrescos  |    —     |  $480  |   —     |
| Ventas Rappi      | $1,200   |   —    |   —     |
| TOTAL             | $8,050   |  $830  | $7,220  |

The TOTAL row is written in red ink, slightly larger and less careful than the blue text.
"$7,220" is circled in red (an imperfect oval, not a circle) with a "?" next to it.
In the right margin, quick arithmetic: $2,000 + $4,850 - $350 + $480 = $7,220 \
(note: +$480 should be -$480, showing the calculation error).
The margin arithmetic is smaller and more cramped, written quickly as a side note.
Table lines are slightly uneven where the ruler slipped.""",

    "03": """Top-down smartphone photo of three paper delivery receipts (half-letter size) on a stainless \
steel kitchen surface. The receipts are slightly crumpled with bent edges; one has a translucent \
grease stain. They are placed side by side, slightly overlapping.

LEFT RECEIPT — Cremeria Don Pancho:
Printed header: "Cremeria Don Pancho"
Subtitle: "Morelia, Mich. Tel: (443) 315-0779"
Text: "nota de remision"
Handwritten table in blue pen (TIGHT CURSIVE, fast, barely legible):
| Descripcion        | Precio   |
| Queso Oaxaca 1kg   | $1,480   |
| Crema              |   $140   |
| Queso Chihuahua    | $2,140   |
TOTAL: $1,480 MXN
Purple rubber stamp: "PAGADO" in rectangle
Line: "Proveedor: ___________"

CENTER RECEIPT — Abarrotes El Sol:
Printed header: "Abarrotes El Sol"
Subtitle: "Morelia, Mich."
Text: "nota de remision"
Handwritten table (LARGE BLOCK LETTERS, clear but irregular):
| Descripcion  | Precio |
| Aceite       |  $620  |
| Sal          |  $460  |
| Azucar       |  $230  |
| Levadura     |  $320  |
TOTAL: $620 MXN

RIGHT RECEIPT — Distribuidora de Harinas del Bajio:
Printed header: "Distribuidora de Harinas del Bajio"
Subtitle: "Morelia, Mich. Tel: (443) 312-9738"
Text: "nota de remision"
Handwritten table (MEDIUM handwriting, some numbers corrected/overwritten):
| Descripcion           | Precio   |
| Bulto Harina 1o       | $1,950   |
| Bulto Harina 2o       | $1,050   |
| Bulto Harina 3o       |   $850   |
| Bulto Harina 4o       |   $350   |
| Bulto Harina 5o       |   $350   |
TOTAL: $1,950 MXN
Purple circular stamp: "P"

CRITICAL: All text in Spanish. "Bulto Harina" NOT "Bulk Flour" or "Bulck Floura".
Each receipt was filled by a DIFFERENT person — three distinctly different handwriting styles.
The receipts look like real pre-printed Mexican stationery forms (white bond paper, dark blue printed text).
Ink varies in each — one pen is running low (lighter strokes), another is fresh (dark and bold).""",

    "04": """Smartphone photo of a brown-skinned male hand holding a black smartphone (6.5" screen) over \
a wooden table. A takeout coffee cup is blurred in the background. The screen shows a modern \
Mexican banking app:

Dark blue top bar:
"Rustico Pizza y Pan"
"Cuenta: 60-**-***-**78"

White balance section:
"Saldo disponible"
"$45,230.17 MXN"  (large, black, bold typography)

"Movimientos" section — "OCTUBRE 2025":

1. Transferencia recibida — Uber Eats        +$3,420.00  (green)
2. Compra TPV — Distribuidora de Harinas      -$1,950.00  (red, yellow highlight)
3. Deposito efectivo — Sucursal Centro        +$8,500.00  (green)
4. Pago de servicio — CFE Luz                 -$2,180.00  (black)
5. Transferencia enviada — Luis A. Hernandez  -$3,500.00  (red)
6. Compra en linea — Amazon MX                  -$459.00  (black)

Bottom navigation bar: Inicio | Transferir | Pagos | Tarjetas | Mas

All UI text in Spanish. Interface should look like a real Mexican banking app (BBVA/Banorte style).
Yellow-highlighted transactions indicate mixed personal/business spending.""",

    "05": """Front-facing smartphone photo of a wooden clipboard hanging on a stainless steel kitchen wall. \
The sheet is white letter-size bond paper.

Title centered, handwritten with thick black marker (UNEVEN strokes, not calligraphy):
"Inventario — 15 Oct"

Table handwritten with black pen (smaller, irregular writing):

| Producto         | Cantidad | Unidad        |
| Harina de trigo  |  8 ?     | bultos 44kg   |
| Queso Oaxaca     |  3.5     | kg            |
| Queso Chihuahua  |  2 ?     | kg            |
| Salsa de tomate  | 12       | latas         |
| Pepperoni        |  1.5     | kg            |
| Champinones      |  0.8 *   | kg            |   * pedir el jueves
| Aceite de oliva  |  4       | L             |
| Azucar           |  3 ?     | kg            |
| Mantequilla      |  2.5     | kg            |
| Huevo            |  2       | cartones (30) |
| Levadura         |  6       | sobres        |

"?" marks next to quantities indicate uncertainty/estimation.
Asterisk on champinones has a margin note: "* pedir el jueves".
White flour/dust smudge on the lower part of the paper.
Table lines drawn BY HAND without ruler — visibly wobbly.
The "8?" was written over a "6" that was crossed out (correction visible).
"bultos 44kg" is written smaller because the writer ran out of space on the line.
The "Unidad" column text is cramped — the writer misjudged column widths.""",

    "06": """Angled smartphone photo of a half-letter sheet on a dark wooden table. A blue BIC pen beside it. \
The paper has fold creases (was folded in thirds). Warm interior lighting.

Centered printed header:
"Rustico Pizza y Pan"
[Small pizza slice icon with wheat sprig]

Rubber stamp rectangle in upper right corner:
"Rustico Pizza y Pan — Morelia, Mich."

Bold printed text:
"RECIBO DE PAGO"

Printed fields with data FILLED IN BY HAND (blue ballpoint, right-leaning slant, slightly hurried):
Nombre: Luis Angel Hernandez Martinez
Periodo: 1 al 15 de Octubre 2025
Concepto: Sueldo quincenal
Cantidad: $3,500.00 (Tres mil quinientos pesos 00/100 M.N.)

Two signature lines at the bottom:
Left: illegible cursive signature scrawl — below it "Recibe"
Right: different illegible cursive signature scrawl — below it "Entrega"

The handwritten fields lean right, written slightly hurried.
"Hernandez" is more cramped because the writer was running out of space on the line.
"$3,500.00" is written more carefully than the rest (slower, more legible).
Signatures are asymmetric quick scribbles, clearly different from each other — NOT readable text.""",

    "07": """Exterior smartphone photo of a colonial facade on a cobblestone street in Morelia, Michoacan. \
Golden hour (sunset). Pink-terracotta cantera stone building with an antique wooden door, open. \
Above the door, a carved wooden sign:

"Rustico"  (with accent: Rustico, rustic serif typography with carved wheat sprig)

To the left of the door, a black A-frame chalkboard with chalk text:

"Especiales de Hoy:
Pizza Margarita — $120
Pan de Masa Madre — $50"

CHALK IMPERFECTIONS (mandatory):
- Chalk leaves irregular porous strokes, not clean lines
- Chalk dust accumulated at base of the board
- Letters have variable thickness as the chalk wears and changes angle
- One letter has been erased and rewritten (ghost of previous chalk visible)
- "$120" and "$50" written larger to be visible from the street
- Some letters have small gaps where the chalk skipped on the rough surface

Two clay pots with plants: one with pink bougainvillea, one with herbs.
The street shows colorful colonial facades (yellow, terracotta) on both sides.
Window with black wrought iron grill.""",

    "08": """Interior smartphone photo of an artisanal pizzeria kitchen. Stainless steel industrial oven \
built into a wall covered with Puebla-style talavera tiles (floral pattern: blue, yellow, orange). \
The oven is on (orange glow visible through the glass window).

Stainless steel work table with flour dusted on it and 6-8 dough balls in various stages of shaping. \
A male arm (brown skin) kneading a dough ball on the right.

Metal shelving in the back with translucent plastic containers with red lids.
Handwritten labels on yellow masking tape stuck to the front:
"Harina"   "Azucar"   "Sal"
(written with thick black Sharpie marker, large block letters, irregular and quick strokes, \
tape cut by hand with uneven edges, labels stuck slightly crooked on the containers)

Wooden pizza peel leaning against the wall. Squeeze bottles with sauces.
Industrial stainless steel refrigerator in the background. Fluorescent ceiling light.""",

    "09": """Interior smartphone photo of the counter/register area of a small Mexican artisanal pizzeria. \
Natural light from a side window. Worn rustic wooden counter.

CHALKBOARD MENU (left wall, wooden frame, black background):
Chalk text, informal lettering:

Pizza Margarita    $120
Pizza Pepperoni    $150
Pizza Hawaiana     $140
Pizza Especial     $150
Pizza 4 Quesos     $145
Pan de masa madre   $50
Concha              $15
Rol de canela       $25
Agua fresca         $25

CHALK: thick irregular strokes, dust at bottom, variable letter sizes, prices bigger than names, \
some lines slightly crooked, chalk skipping on rough surface.

OPEN SPIRAL NOTEBOOK (on the counter, foreground):
Handwritten in blue pen, underlined title:

"Registro de ventas — Sofia"

Pizza pepperoni     $150
Pan concha x3        $45
Agua fresca          $25

NOTEBOOK HANDWRITING: young person's writing (Sofia is the young employee), informal block letters, \
some rounded numbers, title underlined with a wavy line not a straight one.
The chalkboard and notebook must have CLEARLY DIFFERENT handwriting (different people wrote them).

OTHER ELEMENTS:
- Open metal cash register with Mexican bills ($20, $50, $100, $200) and coins in compartments
- Small payment terminal (datafono) next to the register
- Glass display case with artisanal bread (conchas, cuernos, cinnamon rolls)
- Blue folder with pen on the counter (expense ledger)
- Old computer monitor in background showing a blurry spreadsheet

CRITICAL: All text in Mexican Spanish. "Rol de canela" (NOT "Cinnamon roll"). \
"Registro de ventas" (NOT "Sales log"). "Pizza Hawaiana" (NOT "Pizza ya morando").""",

    "10": """Top-down smartphone photo of a dark wooden desk with approximately 20-25 delivery receipts \
scattered messily. A crumpled black plastic bag in the upper left corner (where the receipts were stored).

The receipts are pre-printed Mexican stationery forms, half-letter size, white bond paper. \
Printed header on each: "NOTA DE REMISION" (dark blue serif typography).

Variations among receipts:
- Some filled in with blue pen, others with black pen
- 3-4 receipts with purple "PAGADO" stamp (rectangular or circular)
- 2-3 receipts with translucent grease stains
- Some folded, others crumpled, worn edges
- Handwritten text partially legible (the intent is to show volume and disorder, \
not to read each individual receipt)

The image should convey documentary disorder: evidence that supplier receipts are stored \
in a plastic bag without organization. Some receipts overlap each other.""",
}

FILENAMES = {
    "01": "01_libreta_gastos.jpg",
    "02": "02_corte_caja.jpg",
    "03": "03_notas_proveedor.jpg",
    "04": "04_app_bancaria.jpg",
    "05": "05_inventario.jpg",
    "06": "06_recibo_nomina.jpg",
    "07": "07_local_exterior.jpg",
    "08": "08_cocina_horno.jpg",
    "09": "09_mostrador_caja.jpg",
    "10": "10_bolsa_notas.jpg",
}

# Imagenes que requieren refinamiento iterativo (tienen texto manuscrito critico)
NEEDS_REFINEMENT = {"01", "02", "03", "05", "06", "09"}

# Aspect ratios por imagen
ASPECT_RATIOS = {
    "01": "3:2",   # libreta horizontal
    "02": "4:3",   # hoja en angulo
    "03": "3:2",   # tres notas horizontal
    "04": "3:4",   # celular vertical
    "05": "3:4",   # clipboard vertical
    "06": "4:3",   # recibo en angulo
    "07": "3:2",   # fachada horizontal
    "08": "3:2",   # cocina horizontal
    "09": "3:2",   # mostrador horizontal
    "10": "3:2",   # escritorio horizontal
}


# ---------------------------------------------------------------------------
# Compresion JPEG
# ---------------------------------------------------------------------------
def compress_jpeg(src: Path, dst: Path, quality: int = 60):
    """Comprime un JPEG a menor calidad/tamano."""
    try:
        from PIL import Image
        img = Image.open(src)
        img = img.convert("RGB")
        max_side = 1600
        if max(img.size) > max_side:
            ratio = max_side / max(img.size)
            new_size = (int(img.size[0] * ratio), int(img.size[1] * ratio))
            img = img.resize(new_size, Image.LANCZOS)
        img.save(dst, "JPEG", quality=quality, optimize=True)
        return True
    except ImportError:
        pass
    import subprocess
    try:
        subprocess.run(
            ["cjpeg", "-quality", str(quality), "-outfile", str(dst), str(src)],
            check=True, capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        import shutil
        shutil.copy2(src, dst)
        return False


# ---------------------------------------------------------------------------
# Generacion con Gemini — single shot
# ---------------------------------------------------------------------------
def generate_image(client, prompt_key: str) -> bytes | None:
    """Genera una imagen con Gemini y retorna los bytes."""
    full_prompt = PREFIJO + PROMPTS[prompt_key]
    aspect = ASPECT_RATIOS.get(prompt_key, "3:2")

    gen_cfg = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(
            aspect_ratio=aspect,
            image_size="2K",
        ),
        temperature=0.5,
        top_p=0.95,
        top_k=64,
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  Intento {attempt}/{MAX_RETRIES} (single-shot, 2K, aspect={aspect})...")
            response = client.models.generate_content(
                model=MODEL,
                contents=full_prompt,
                config=gen_cfg,
            )

            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        print(f"  Imagen generada ({len(part.inline_data.data)} bytes)")
                        return part.inline_data.data

            print(f"  No se genero imagen.")
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.text:
                        print(f"    Texto: {part.text[:200]}")

        except Exception as e:
            print(f"  Error: {e}")

        if attempt < MAX_RETRIES:
            print(f"  Reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    return None


# ---------------------------------------------------------------------------
# Generacion con Gemini — chat iterativo (2 turnos: generar + refinar)
# ---------------------------------------------------------------------------
def generate_image_with_refinement(client, prompt_key: str) -> bytes | None:
    """Genera imagen y luego la refina en un segundo turno de chat."""
    full_prompt = PREFIJO + PROMPTS[prompt_key]
    aspect = ASPECT_RATIOS.get(prompt_key, "3:2")

    gen_cfg = types.GenerateContentConfig(
        response_modalities=["IMAGE", "TEXT"],
        image_config=types.ImageConfig(
            aspect_ratio=aspect,
            image_size="2K",
        ),
        temperature=0.6,
        top_p=0.95,
        top_k=64,
    )

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            print(f"  Intento {attempt}/{MAX_RETRIES} (chat 2-turnos, 2K, aspect={aspect})...")

            # Turno 1: generar
            chat = client.chats.create(model=MODEL, config=gen_cfg)
            resp1 = chat.send_message(full_prompt)

            image_data_1 = None
            if resp1.candidates:
                for part in resp1.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        image_data_1 = part.inline_data.data
                        break

            if not image_data_1:
                print(f"  Turno 1 no genero imagen.")
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_DELAY)
                continue

            print(f"  Turno 1: imagen base ({len(image_data_1)} bytes)")
            time.sleep(5)  # breve pausa entre turnos

            # Turno 2: refinar escritura
            print(f"  Turno 2: refinando escritura...")
            resp2 = chat.send_message(REFINE_INSTRUCTION)

            image_data_2 = None
            if resp2.candidates:
                for part in resp2.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        image_data_2 = part.inline_data.data
                        break

            if image_data_2:
                print(f"  Turno 2: imagen refinada ({len(image_data_2)} bytes)")
                return image_data_2
            else:
                print(f"  Turno 2 no genero imagen, usando turno 1.")
                return image_data_1

        except Exception as e:
            print(f"  Error: {e}")

        if attempt < MAX_RETRIES:
            print(f"  Reintentando en {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

    return None


def main():
    # Determinar modo
    compress_only = "--compress-only" in sys.argv
    no_refine = "--no-refine" in sys.argv
    requested = [a for a in sys.argv[1:] if not a.startswith("--")]

    if compress_only:
        keys = requested if requested else sorted(PROMPTS.keys())
        print(f"Modo compresion: procesando {len(keys)} imagenes...")
        COMPRESSED_DIR.mkdir(exist_ok=True)
        for key in keys:
            src = OUTPUT_DIR / FILENAMES[key]
            dst = COMPRESSED_DIR / FILENAMES[key]
            if src.exists():
                compress_jpeg(src, dst)
                src_kb = src.stat().st_size / 1024
                dst_kb = dst.stat().st_size / 1024
                print(f"  {FILENAMES[key]}: {src_kb:.0f}KB -> {dst_kb:.0f}KB")
            else:
                print(f"  {FILENAMES[key]}: no existe, saltando")
        print("Compresion completada.")
        return

    # Validar API key
    api_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Define GEMINI_API_KEY o GOOGLE_API_KEY como variable de entorno.")
        sys.exit(1)

    # Imagenes a generar
    if requested:
        keys = [k.zfill(2) for k in requested]
        invalid = [k for k in keys if k not in PROMPTS]
        if invalid:
            print(f"Error: Imagenes no validas: {invalid}")
            sys.exit(1)
    else:
        keys = sorted(PROMPTS.keys())

    print(f"Generando {len(keys)} imagenes con {MODEL} a 2K...")
    print(f"  Destino: {OUTPUT_DIR}")
    print(f"  Comprimidas: {COMPRESSED_DIR}")
    print(f"  Refinamiento iterativo: {'OFF' if no_refine else 'ON para ' + str(NEEDS_REFINEMENT)}")
    print()

    client = genai.Client(api_key=api_key)
    OUTPUT_DIR.mkdir(exist_ok=True)
    COMPRESSED_DIR.mkdir(exist_ok=True)

    resultados = {"ok": [], "error": []}

    for i, key in enumerate(keys, 1):
        filename = FILENAMES[key]
        use_refinement = (key in NEEDS_REFINEMENT) and not no_refine

        print(f"[{i}/{len(keys)}] Generando {filename} {'(con refinamiento)' if use_refinement else '(single-shot)'}...")

        if use_refinement:
            image_data = generate_image_with_refinement(client, key)
        else:
            image_data = generate_image(client, key)

        if image_data:
            out_path = OUTPUT_DIR / filename
            out_path.write_bytes(image_data)
            print(f"  Guardada: {out_path} ({len(image_data) / 1024:.0f}KB)")

            comp_path = COMPRESSED_DIR / filename
            compress_jpeg(out_path, comp_path)
            comp_kb = comp_path.stat().st_size / 1024
            print(f"  Comprimida: {comp_path} ({comp_kb:.0f}KB)")

            resultados["ok"].append(key)
        else:
            print(f"  FALLO: No se pudo generar {filename}")
            resultados["error"].append(key)

        if i < len(keys):
            print(f"  Esperando {RETRY_DELAY}s...")
            time.sleep(RETRY_DELAY)

        print()

    # Resumen
    print("=" * 50)
    print("RESUMEN")
    print(f"  Exitosas: {len(resultados['ok'])}/{len(keys)}")
    if resultados["ok"]:
        print(f"    {', '.join(FILENAMES[k] for k in resultados['ok'])}")
    if resultados["error"]:
        print(f"  Fallidas: {len(resultados['error'])}/{len(keys)}")
        print(f"    {', '.join(FILENAMES[k] for k in resultados['error'])}")
        print(f"\n  Reintentar: python {sys.argv[0]} {' '.join(resultados['error'])}")


if __name__ == "__main__":
    main()
