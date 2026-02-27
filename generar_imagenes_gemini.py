"""
Generador de evidencias visuales para Rústico Pizza y Pan.
Usa Gemini 3 Pro Image (Nano Banana Pro) para crear imágenes fotorrealistas
con texto renderizado de alta calidad (~94% de precisión).

Nota: gemini-3-pro-image-preview es un modelo de paga (sin tier gratuito).
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key or api_key == "YOUR_API_KEY_HERE":
    print("ERROR: Configura tu API key en el archivo .env")
    print("  1. Ve a https://aistudio.google.com/apikey")
    print("  2. Copia tu clave")
    print("  3. Pégala en .env: GOOGLE_API_KEY=tu_clave_aqui")
    sys.exit(1)

client = genai.Client(api_key=api_key)

OUTPUT_DIR = Path(__file__).parent / "investigacion" / "evidencias"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gemini-3-pro-image-preview"

# Sufijo para todas las imágenes: aspecto de foto tomada con celular
CELLPHONE_SUFFIX = (
    " The image must look like a candid photograph taken with a smartphone camera — "
    "slight lens distortion, natural ambient lighting with subtle color cast, "
    "minor motion softness, shallow depth of field typical of a phone camera, "
    "visible noise/grain in shadow areas, slightly warm white balance. "
    "No studio lighting, no perfect framing. Ultra photorealistic, 12MP cellphone quality."
)

# --- Las 6 imágenes originales ---
PROMPTS_ORIGINALES = {
    "01_libreta_gastos": (
        "A top-down photograph of an open lined notebook (cuaderno rayado, Mexican school-style) "
        "resting on a rustic wooden table. The notebook is filled with handwritten expense entries "
        "in Spanish using a blue ballpoint pen, slightly messy but legible cursive-print hybrid "
        "handwriting. Each entry has a date in DD/MM format on the left margin, followed by a short "
        "concept description and an amount in Mexican pesos with the \"$\" sign. Visible entries "
        "include items like \"Gas LP — $380\", \"Harina (2 bultos) — $520\", \"Queso Oaxaca 5kg — $690\", "
        "\"Servilletas y desechables — $145\", \"Jitomate caja — $230\", \"Aceite de oliva — $310\". "
        "Two or three entries are crossed out with a single line and rewritten below. A faint brown "
        "coffee ring stain appears on the lower-right corner of the right page. The pen rests "
        "diagonally across the gutter. Warm, natural side lighting from a window creates soft shadows. "
        "The notebook spiral binding is visible at the top."
    ),
    "02_corte_caja": (
        "A photograph of a single sheet of grid paper (hoja cuadriculada) placed on a laminate "
        "countertop surface, showing a handwritten daily cash register closing form in Spanish. "
        "At the top, written in slightly larger letters with blue pen: \"Corte de Caja\" and a date "
        "\"Martes 14/Oct/2025\". Below, a hand-drawn table with four columns labeled \"Concepto\", "
        "\"Entrada\", \"Salida\", and \"Saldo\". Rows include entries like \"Fondo inicial — — $2,000\", "
        "\"Ventas mostrador — $4,850 — —\", \"Pago repartidor — — $350 —\", "
        "\"Compra refrescos — — $480 —\", \"Ventas Rappi — $1,200 — —\", and a final row \"TOTAL\" "
        "with amounts summed. Red pen is used for the totals and for circling one discrepancy. "
        "Arithmetic calculations are scribbled in the right margin with pencil. The paper is slightly "
        "wrinkled with one small fold at the corner. Overhead fluorescent lighting, typical of a small "
        "commercial kitchen. A calculator partially visible at the edge of the frame."
    ),
    "03_notas_proveedor": (
        "A photograph of three to four small pre-printed receipt papers (notas de remision mexicanas) "
        "spread casually on a dark wooden table surface, partially overlapping. Each receipt is the "
        "standard Mexican \"nota de remision\" format — small pre-printed pads with fields for date, "
        "client, concepts, quantities, unit prices, and totals, all filled in by hand with different "
        "pen colors. One receipt is from \"Cremeria Don Pancho\" showing dairy products (queso Oaxaca, "
        "crema, queso Chihuahua) totaling $1,480 MXN. Another from \"Abarrotes El Sol\" lists sundry "
        "items (aceite, sal, azucar, levadura) for $620 MXN. A third from \"Distribuidora de Harinas "
        "del Bajio\" shows bulk flour and semolina purchases for $1,950 MXN. One receipt has a purple "
        "\"PAGADO\" rubber stamp impression over it. Another has a handwritten \"P\" circled in the "
        "margin. The receipts show slight crumpling and one has a small tear at the edge. Natural "
        "daylight, top-down angle, shallow depth of field with the nearest receipt in sharp focus."
    ),
    "04_app_bancaria": (
        "A realistic screenshot of a generic Mexican mobile banking application displayed on a "
        "smartphone screen, showing a business checking account statement. The interface has a dark "
        "blue header bar with a white account name \"Rustico Pizza y Pan\" and account number partially "
        "masked. The main balance displayed prominently reads \"$45,230.17 MXN\". Below, a scrollable "
        "list of recent transactions from October 2025 dates, each with an icon, description, and "
        "amount. Transactions include: \"Transferencia recibida — Uber Eats — +$3,420.00\", "
        "\"Compra TPV — Distribuidora de Harinas — -$1,950.00\", \"Deposito efectivo — Sucursal Centro "
        "— +$8,500.00\", \"Pago de servicio — CFE Luz — -$2,180.00\", \"Transferencia enviada — Luis A. "
        "Hernandez — -$3,500.00\", \"Compra en linea — Amazon MX — -$459.00\". The UI follows typical "
        "Mexican banking app design with Spanish labels: \"Movimientos\", \"Saldo disponible\", "
        "\"Cuenta de cheques\". Two transactions are highlighted in yellow. Clean mobile interface, "
        "modern flat design. No real bank branding — use generic design elements."
    ),
    "05_inventario": (
        "A top-down photograph of a handwritten inventory list on a plain white letter-size sheet of "
        "paper clipped to a brown clipboard. The list is written primarily in pencil with some erased "
        "and rewritten sections visible as smudges. At the top of the page, underlined in pen, it "
        "reads \"Inventario — 15 Oct\". Below, a hand-drawn table with three columns: \"Producto\", "
        "\"Cantidad\", and \"Unidad\". Entries listed include: \"Harina de trigo — 8 — bultos 44kg\", "
        "\"Queso Oaxaca — 3.5 — kg\", \"Queso Chihuahua — 2 — kg\", \"Salsa de tomate — 12 — latas\", "
        "\"Pepperoni — 1.5 — kg\", \"Champiñones — 0.8 — kg\", \"Aceite de oliva — 4 — L\", "
        "\"Azucar — 3 — kg\", \"Mantequilla — 2.5 — kg\", \"Huevo — 2 — cartones (30)\", "
        "\"Levadura — 6 — sobres\". Some quantities have question marks next to them in pen. One item "
        "has an asterisk with a marginal note \"pedir el jueves\". The clipboard's metal clip is visible "
        "at the top. The setting is a stainless steel kitchen prep surface. Cool overhead lighting."
    ),
    "06_recibo_nomina": (
        "A photograph of a simple handwritten payment receipt on a half-sheet of white paper (media "
        "carta), placed on a dark surface. At the top center, written in slightly larger letters with "
        "blue pen: \"Rustico Pizza y Pan\" with a small hand-drawn wheat stalk or pizza slice doodle "
        "next to it. Below, the title \"RECIBO DE PAGO\" is written in block capitals and underlined. "
        "The body reads in neat handwriting: \"Nombre: Luis Angel Hernandez Martinez\", \"Periodo: 1 al "
        "15 de Octubre 2025\", \"Concepto: Sueldo quincenal\", \"Cantidad: $3,500.00 (Tres mil "
        "quinientos pesos 00/100 M.N.)\". At the bottom, two lines for signatures: the left one "
        "labeled \"Recibe\" has a cursive signature above it, while the right one labeled \"Entrega\" is "
        "signed with a different hand. A small rectangular area in the upper right has a faded purple "
        "rubber stamp impression reading \"Rustico Pizza y Pan — Morelia, Mich.\" The paper has a "
        "slight fold mark across the middle as if it had been folded in half. Warm ambient lighting, "
        "the pen used to write it rests nearby."
    ),
}

# --- Las 4 imágenes adicionales ---
PROMPTS_ADICIONALES = {
    "07_local_exterior": (
        "A street-level photograph of the exterior facade of a small artisan pizzeria and bakery "
        "named 'Rustico Pizza y Pan' located in a mixed residential-commercial neighborhood in "
        "Morelia, Michoacan, Mexico. The storefront is modest — a single-story building with a "
        "hand-painted wooden sign above the entrance displaying the name 'Rústico' in warm "
        "earth-toned lettering with a small stylized wheat stalk illustration next to it. The "
        "main door is a rustic wooden door with a glass panel in the upper half, through which "
        "the interior counter is faintly visible. The facade is painted in a warm terracotta or "
        "cream color with slight weathering. A small chalkboard menu stand sits beside the door "
        "on the sidewalk showing daily specials written in colored chalk in Spanish. The sidewalk "
        "is narrow concrete. The adjacent buildings are typical Mexican urban architecture — "
        "low-rise, painted in different colors. Natural afternoon sunlight hits the facade at an "
        "angle, creating warm tones and soft shadows. A couple of potted plants flank the entrance. "
        "The scene conveys a cozy, neighborhood bakery-pizzeria, handmade and unpretentious."
    ),
    "08_cocina_horno": (
        "An interior photograph of a small artisan pizzeria kitchen in Morelia, Mexico, showing the "
        "heart of the operation: a medium-sized commercial gas pizza oven (not wood-fired) with its "
        "door slightly ajar, revealing the glowing interior. The oven sits against a tiled wall. In "
        "front of the oven, a stainless steel prep table holds balls of pizza dough in various stages "
        "of preparation — some in metal trays, some being stretched. A wooden pizza peel leans against "
        "the table. To one side, metal shelving holds ingredient containers: large plastic tubs labeled "
        "in handwritten Spanish with masking tape labels ('Harina', 'Azucar', 'Sal'), squeeze bottles "
        "of olive oil and sauces, and stacked metal pans. A commercial upright refrigerator is partially "
        "visible in the background with its stainless steel door. The floor is utilitarian tile. "
        "Overhead fluorescent lighting mixes with the warm glow from the oven. A dusting of flour is "
        "visible on the prep surface. A cook's apron hangs on a wall hook. The kitchen is clean but "
        "clearly in active use — it feels like a working space, not a showroom. The overall impression "
        "is of a small, efficient, hands-on artisan kitchen."
    ),
    "09_mostrador_caja": (
        "A photograph of the front counter area of a small Mexican pizzeria-bakery. The counter is an "
        "L-shaped wooden surface with a laminate top showing some wear. On the counter, the following "
        "items are visible: a simple metal cash drawer (open, showing compartments with Mexican peso "
        "bills and coins), a small portable credit card payment terminal (POS terminal) next to it, "
        "a small open notebook (Sofia's sales log) with handwritten entries in blue pen listing "
        "individual sales like 'Pizza pepperoni $150', 'Pan concha x3 $45', 'Agua fresca $25'. Behind "
        "the counter, partially visible, is an older desktop computer with an LCD monitor showing a "
        "spreadsheet. A blue hard-cover lined notebook (Mariana's expense ledger) rests between the "
        "cash drawer and the wall. A ballpoint pen sits on top of it. A glass bakery display case on "
        "the counter shows conchas, cuernos, and cinnamon rolls on metal trays. A small hand-written "
        "chalkboard on the wall behind the counter shows pizza prices in Spanish. The lighting is a "
        "mix of natural light from the storefront and overhead fluorescent. The scene conveys a "
        "functional, informal, family-run business point of sale."
    ),
    "10_bolsa_notas": (
        "A top-down photograph of a transparent plastic bag (like a grocery store bag) that has been "
        "pulled out of a drawer and its contents emptied onto a dark wooden surface. The bag is "
        "crumpled and pushed to one side. Scattered across the surface are approximately 20 to 25 "
        "small pre-printed Mexican 'nota de remision' receipts in various states: some are neatly "
        "folded, some are crumpled, some are flat. Several receipts show visible wear — grease stains, "
        "a torn corner, slightly faded ink. A few have a purple 'PAGADO' rubber stamp impression. "
        "Others have a handwritten circled 'P' in pen in the corner. The receipts are from different "
        "suppliers, with different handwriting and pen colors (blue, black, some in pencil). Some "
        "receipts are partially stuck together. A couple of receipts are flipped showing the blank "
        "back side. One receipt near the edge has water damage with slightly run ink. The drawer from "
        "which the bag was pulled is partially visible at the edge of the frame — a simple wooden "
        "drawer with a metal handle, positioned below what appears to be a counter surface. The scene "
        "conveys informal, unorganized document storage typical of a small business. Natural overhead "
        "lighting, slight shadows."
    ),
}

ALL_PROMPTS = {**PROMPTS_ORIGINALES, **PROMPTS_ADICIONALES}


def generate_image(name: str, prompt: str) -> Path:
    """Genera una imagen con Gemini 3 Pro Image y la guarda en evidencias/."""
    full_prompt = prompt + CELLPHONE_SUFFIX
    print(f"  Generando: {name}...")

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=full_prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                image_config=types.ImageConfig(
                    aspect_ratio="4:3",
                ),
            ),
        )
    except Exception as e:
        print(f"  ERROR en {name}: {e}")
        return None

    # Extraer imagen de la respuesta
    if not response.candidates or not response.candidates[0].content.parts:
        print(f"  FILTRADA: {name} — No se generó imagen")
        return None

    for part in response.candidates[0].content.parts:
        if getattr(part, "thought", False):
            continue
        if part.inline_data is not None:
            out_path = OUTPUT_DIR / f"{name}.jpg"
            raw_bytes = part.inline_data.data
            # Convertir a JPEG si es necesario
            from PIL import Image as PILImage
            import io
            pil_img = PILImage.open(io.BytesIO(raw_bytes))
            if pil_img.mode in ("RGBA", "P"):
                pil_img = pil_img.convert("RGB")
            pil_img.save(str(out_path), format="JPEG", quality=95)
            print(f"  OK: {out_path}")
            return out_path

    print(f"  ERROR: {name} — Respuesta sin imagen")
    return None


def main():
    print("=" * 60)
    print("Generador de evidencias — Rústico Pizza y Pan")
    print(f"Modelo: {MODEL} (Nano Banana Pro)")
    print("=" * 60)
    print(f"Salida: {OUTPUT_DIR}\n")

    if len(sys.argv) > 1:
        if sys.argv[1] == "--originales":
            prompts = PROMPTS_ORIGINALES
        elif sys.argv[1] == "--adicionales":
            prompts = PROMPTS_ADICIONALES
        else:
            targets = sys.argv[1:]
            prompts = {k: v for k, v in ALL_PROMPTS.items() if k in targets}
            if not prompts:
                print(f"No se encontraron prompts para: {targets}")
                print(f"Disponibles: {list(ALL_PROMPTS.keys())}")
                print("  O usa: --originales | --adicionales")
                sys.exit(1)
    else:
        prompts = ALL_PROMPTS

    results = {"ok": [], "error": []}

    for name, prompt in prompts.items():
        path = generate_image(name, prompt)
        if path:
            results["ok"].append(name)
        else:
            results["error"].append(name)

    print("\n" + "=" * 60)
    print(f"Generadas: {len(results['ok'])}/{len(prompts)}")
    if results["error"]:
        print(f"Errores: {results['error']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
