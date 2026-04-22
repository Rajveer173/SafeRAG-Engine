from pathlib import Path
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
DATA_DIR: Path = PROJECT_ROOT / "data"
VECTOR_DB_DIR: Path = PROJECT_ROOT / "vector_db"
LOGS_DIR: Path = PROJECT_ROOT / "logs"

DATA_DIR.mkdir(exist_ok=True)
VECTOR_DB_DIR.mkdir(exist_ok=True)
LOGS_DIR.mkdir(exist_ok=True)

PDF_FILES: List[str] = os.getenv("PDF_FILES", "data.pdf").split(",")
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "50"))

EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
LLM_MODEL: str = os.getenv("LLM_MODEL", "llama3")
LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.7"))

VECTOR_DB_NAME: str = os.getenv("VECTOR_DB_NAME", "resume_db")
SIMILARITY_SEARCH_K: int = int(os.getenv("SIMILARITY_SEARCH_K", "3"))

LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE: Path = LOGS_DIR / "rag.log"

OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "http://localhost:11434")
