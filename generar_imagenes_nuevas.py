"""
Generador de evidencias visuales adicionales para Rústico Pizza y Pan.
Complementa las 6 imágenes originales (generar_imagenes.py) con 4 nuevas:
fachada del local, cocina/horno, mostrador/caja y bolsa de notas.
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


def generate_image(name: str, prompt: str) -> Path:
    """Genera una imagen con Imagen 3 y la guarda en evidencias/."""
    full_prompt = prompt + CELLPHONE_SUFFIX
    print(f"  Generando: {name}...")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
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
    print("Generador de evidencias ADICIONALES — Rústico Pizza y Pan")
    print("=" * 60)
    print(f"Salida: {OUTPUT_DIR}\n")

    if len(sys.argv) > 1:
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
