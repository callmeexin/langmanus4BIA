"""Configure application storage directories"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR / "storage"
DEFAULT_STORAGE = STORAGE_DIR / "default"

DEFAULT_STORAGE.mkdir(parents=True, exist_ok=True)