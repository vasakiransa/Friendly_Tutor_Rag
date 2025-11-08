from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
VECTOR_DIR = PROJECT_ROOT / "vector_store"
for d in [DATA_DIR, VECTOR_DIR]:
    d.mkdir(parents=True, exist_ok=True)
LOCAL_MODEL = os.getenv("LOCAL_MODEL", "distilgpt2")
EMBED_MODEL = os.getenv("EMBED_MODEL","sentence-transformers/all-MiniLM-L6-v2")
SCRAPE_LIMIT = int(os.getenv("SCRAPE_LIMIT","2"))
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE","400"))
CHUNK_LIMIT = int(os.getenv("CHUNK_LIMIT","60"))
TOP_RETRIEVE = int(os.getenv("TOP_RETRIEVE","6"))
