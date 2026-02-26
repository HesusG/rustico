"""
Generador de evidencias visuales para Rústico Pizza y Pan.
Usa Google Generative AI (Imagen 3) para crear imágenes fotorrealistas
que simulan documentos financieros informales tomados con celular.
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

# Sufijo para todas las imágenes: aspecto de foto tomada con celular
CELLPHONE_SUFFIX = (
    " The image must look like a candid photograph taken with a smartphone camera — "
    "slight lens distortion, natural ambient lighting with subtle color cast, "
    "minor motion softness, shallow depth of field typical of a phone camera, "
    "visible noise/grain in shadow areas, slightly warm white balance. "
    "No studio lighting, no perfect framing. Ultra photorealistic, 12MP cellphone quality."
)

PROMPTS = {
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


def generate_image(name: str, prompt: str) -> Path:
    """Genera una imagen con Imagen 3 y la guarda en evidencias/."""
    full_prompt = prompt + CELLPHONE_SUFFIX
    print(f"  Generando: {name}...")

    try:
        response = client.models.generate_images(
            model="imagen-3.0-generate-002",
            prompt=full_prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="4:3",
                output_mime_type="image/jpeg",
            ),
        )
    except Exception as e:
        print(f"  ERROR en {name}: {e}")
        return None

    if not response.generated_images:
        reason = getattr(response, "filtered_reason", "Desconocida")
        print(f"  FILTRADA: {name} — Razón: {reason}")
        return None

    img = response.generated_images[0]
    out_path = OUTPUT_DIR / f"{name}.jpg"
    img.image.save(str(out_path))
    print(f"  OK: {out_path}")
    return out_path


def main():
    print("=" * 60)
    print("Generador de evidencias — Rústico Pizza y Pan")
    print("=" * 60)
    print(f"Salida: {OUTPUT_DIR}\n")

    if len(sys.argv) > 1:
        # Generar solo las especificadas
        targets = sys.argv[1:]
        prompts = {k: v for k, v in PROMPTS.items() if k in targets}
        if not prompts:
            print(f"No se encontraron prompts para: {targets}")
            print(f"Disponibles: {list(PROMPTS.keys())}")
            sys.exit(1)
    else:
        prompts = PROMPTS

    results = {"ok": [], "error": [], "filtrada": []}

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
