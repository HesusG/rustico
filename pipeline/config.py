"""Configuración central del pipeline."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Rutas
PROJECT_ROOT = Path(__file__).parent.parent
PIPELINE_ROOT = Path(__file__).parent
DATA_DIR = PIPELINE_ROOT / "data"
PDFS_DIR = DATA_DIR / "pdfs"
SQLITE_DB = DATA_DIR / "rustico_papers.db"
CHROMA_DIR = DATA_DIR / "chroma_db"

# Crear directorios si no existen
DATA_DIR.mkdir(exist_ok=True)
PDFS_DIR.mkdir(exist_ok=True)
CHROMA_DIR.mkdir(exist_ok=True)

# Cargar variables de entorno
load_dotenv(PROJECT_ROOT / ".env")

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
UNPAYWALL_EMAIL = os.getenv("UNPAYWALL_EMAIL", "")

# ChromaDB
CHROMA_COLLECTION = "rustico_academic_chunks"
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
EMBEDDING_DIM = 384

# Chunking
CHUNK_TARGET_SIZE = 800
CHUNK_OVERLAP = 100
CHUNK_MIN_SIZE = 200

# Verificación
MIN_SIMILARITY_THRESHOLD = 0.45

# Gemini model
GEMINI_MODEL = "gemini-2.5-flash"
