"""
Editor de evidencias visuales — Rústico Pizza y Pan.
Envía las imágenes existentes a Gemini con instrucciones de edición mínima.
Mantiene la composición original, solo cambia lo solicitado.
"""

import os
import sys
import io
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
from PIL import Image as PILImage

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key or api_key == "YOUR_API_KEY_HERE":
    print("ERROR: Configura tu API key en el archivo .env")
    sys.exit(1)

client = genai.Client(api_key=api_key)

EVIDENCIAS = Path(__file__).parent / "investigacion" / "evidencias"
MODEL = "gemini-3-pro-image-preview"

# Instrucción base para todas las ediciones
BASE_INSTRUCTION = (
    "Edit this photograph. Keep EVERYTHING exactly the same — same composition, "
    "same lighting, same objects, same style, same handwriting style, same colors, "
    "same paper, same background. ONLY change what I specifically ask you to change. "
    "The result must look like the same photograph with minimal modifications."
)

EDITS = {
    "01_libreta_gastos": {
        "file": "01_libreta_gastos.jpg",
        "instruction": (
            f"{BASE_INSTRUCTION}\n\n"
            "CHANGE ONLY THE FOLLOWING TEXT:\n"
            "1. Change 'October 2025' to 'Febrero 2026' (in Spanish)\n"
            "2. Change ALL dates from October (10) to February (02):\n"
            "   - '12/10' → '03/02'\n"
            "   - '14/10' → '05/02'\n"
            "   - '15/10' → '06/02'\n"
            "   - '17/10' → '09/02'\n"
            "   - '19/10' → '11/02'\n"
            "   - '22/10' → '13/02'\n"
            "   - '24/10' → '16/02' (both lines)\n"
            "   - '26/10' → '18/02' (both lines)\n"
            "3. Keep ALL prices, product names, and everything else EXACTLY the same.\n"
            "4. Keep the same handwriting style, pen color, coffee stain, notebook appearance.\n"
            "CRITICAL: The month must say 'Febrero 2026' in SPANISH, not English."
        ),
    },
    "02_corte_caja": {
        "file": "02_corte_caja.jpg",
        "instruction": (
            f"{BASE_INSTRUCTION}\n\n"
            "CHANGE ONLY THE FOLLOWING:\n"
            "1. Change 'Martes 14/Oct/2025' to 'Miércoles 18/Feb/2026'\n"
            "2. Keep ALL numbers, table structure, red circles, margin calculations, "
            "calculator, and paper appearance EXACTLY the same.\n"
            "CRITICAL: Date must read '18/Feb/2026'. All text in Spanish."
        ),
    },
    "05_inventario": {
        "file": "05_inventario.jpg",
        "instruction": (
            f"{BASE_INSTRUCTION}\n\n"
            "CHANGE ONLY THE FOLLOWING:\n"
            "1. Change the title from 'Inventario — 15 Oct' to 'Inventario — 18 Feb'\n"
            "2. Keep ALL product names, quantities, units, question marks, asterisks, "
            "marginal notes, clipboard, and kitchen background EXACTLY the same.\n"
            "CRITICAL: Must say '18 Feb', not '15 Oct'. All text in Spanish."
        ),
    },
    "06_recibo_nomina": {
        "file": "06_recibo_nomina.jpg",
        "instruction": (
            f"{BASE_INSTRUCTION}\n\n"
            "CHANGE ONLY THE FOLLOWING:\n"
            "1. Change 'Periodo: 1 al 15 de Octubre 2025' to 'Periodo: 1 al 15 de Febrero 2026'\n"
            "2. Change '$3,500.00 (Tres mil quinientos pesos' to '$3,750.00 (Tres mil setecientos cincuenta pesos'\n"
            "3. Keep the name 'Luis Angel Hernández Martínez', header 'Rustico Pizza y Pan', "
            "stamps, signatures, pen, paper folds, and everything else EXACTLY the same.\n"
            "CRITICAL: Must say 'Febrero 2026'. Amount must be '$3,750.00'. All text in Spanish."
        ),
    },
    "08_cocina_horno": {
        "file": "08_cocina_horno.jpg",
        "instruction": (
            f"{BASE_INSTRUCTION}\n\n"
            "CHANGE ONLY THE FOLLOWING:\n"
            "1. Replace the current commercial gas/electric oven with a STONE PIZZA OVEN "
            "(horno de piedra). The stone oven should have a visible stone/brick interior "
            "and a rounded stone opening. It should look like an artisanal stone pizza oven, "
            "not a modern commercial one. The oven should still be glowing warm inside.\n"
            "2. Keep the prep table with dough balls, the ingredient containers with masking "
            "tape labels ('Harina', 'Azúcar', 'Sal'), the talavera tile wall, the wooden "
            "pizza peel, the man's arm kneading dough, and ALL other elements EXACTLY the same.\n"
            "The stone oven should fit naturally in the same position as the current oven."
        ),
    },
}


def edit_image(name: str, config: dict) -> Path:
    """Edita una imagen existente con Gemini."""
    input_path = EVIDENCIAS / config["file"]

    if not input_path.exists():
        print(f"  ERROR: No existe {input_path}")
        return None

    print(f"  Editando: {name}...")

    # Cargar imagen existente
    img = PILImage.open(input_path)

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=[
                config["instruction"],
                img,
            ],
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

    if not response.candidates or not response.candidates[0].content.parts:
        print(f"  FILTRADA: {name} — No se generó imagen")
        return None

    for part in response.candidates[0].content.parts:
        if getattr(part, "thought", False):
            continue
        if part.inline_data is not None:
            out_path = EVIDENCIAS / config["file"]
            raw_bytes = part.inline_data.data
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
    print("Editor de evidencias — Rústico Pizza y Pan")
    print(f"Modelo: {MODEL}")
    print("=" * 60)
    print(f"Directorio: {EVIDENCIAS}\n")

    if len(sys.argv) > 1:
        targets = sys.argv[1:]
        edits = {k: v for k, v in EDITS.items() if k in targets}
        if not edits:
            print(f"No se encontraron ediciones para: {targets}")
            print(f"Disponibles: {list(EDITS.keys())}")
            sys.exit(1)
    else:
        edits = EDITS

    print(f"Imágenes a editar: {list(edits.keys())}\n")

    results = {"ok": [], "error": []}
    for name, config in edits.items():
        path = edit_image(name, config)
        if path:
            results["ok"].append(name)
        else:
            results["error"].append(name)

    print("\n" + "=" * 60)
    print(f"Editadas: {len(results['ok'])}/{len(edits)}")
    if results["error"]:
        print(f"Errores: {results['error']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
