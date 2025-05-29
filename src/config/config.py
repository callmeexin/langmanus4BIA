"""Configure application storage directories"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_WORK = BASE_DIR / "work"

DEFAULT_WORK.mkdir(parents=True, exist_ok=True)