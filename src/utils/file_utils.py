from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Dict, List

from fastapi import UploadFile

from src.config.config import DEFAULT_WORK


async def save_file(session_id: str, file: UploadFile, storage_path: Path = DEFAULT_WORK) -> dict:
    """
    Save an uploaded file to the specified storage location.

    Args:
        session_id: Unique identifier for the session
        file: UploadFile object from FastAPI
        storage_path: Base directory for storage (default: DEFAULT_STORAGE)

    Returns:
        dict: Contains 'path' (relative to storage_path) and 'size' (file size in bytes)
    """
    # Create directory structure: {storage_path}/{session_id}/{task_id}
    session_dir = storage_path / session_id / "data"
    session_dir.mkdir(parents=True, exist_ok=True)

    file_path = session_dir / file.filename

    # Stream file contents to disk
    with file_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Get file size in bytes
    file_size = file_path.stat().st_size

    return {
        "path": str(file_path.relative_to(storage_path)),
        "size": file_size
    }

def get_file_path(session_id: str, task_id: str, filename: str, storage_path: Path = DEFAULT_WORK) -> Path | None:
    """
    Get the full path to a file based on session, task, and filename.

    Args:
        session_id: Session identifier
        task_id: Task identifier
        filename: Name of the file
        storage_path: Base storage directory

    Returns:
        Path: Full file path if exists, None otherwise
    """
    file_path = storage_path / session_id / task_id / filename
    if not file_path.exists():
        return None
    return file_path

async def delete_file_async(file_path: Path) -> bool:
    """
    Asynchronously delete a file.

    Args:
        file_path: Path to the file to delete

    Returns:
        bool: True if deletion succeeded, False otherwise
    """
    try:
        if file_path.exists():
            file_path.unlink()
        return True
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False

def get_language_from_extension(filename: str) -> str:
    """Determine language based on file extension"""
    extension_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.java': 'Java',
        '.kt': 'Kotlin',
        '.go': 'Go',
        '.rs': 'Rust',
        '.cpp': 'C++',
        '.c': 'C',
        '.h': 'C Header',
        '.cs': 'C#',
        '.swift': 'Swift',
        '.rb': 'Ruby',
        '.php': 'PHP',
        '.sh': 'Shell',
        '.pl': 'Perl',
        '.lua': 'Lua',
        '.r': 'R',
        '.m': 'Objective-C',
        '.sql': 'SQL',
        '.html': 'HTML',
        '.css': 'CSS',
        '.scss': 'SCSS',
        '.json': 'JSON',
        '.xml': 'XML',
        '.yaml': 'YAML',
        '.yml': 'YAML',
        '.md': 'Markdown',
        '.txt': 'Text',
        '.csv': 'CSV',
        '.tsv': 'TSV',
    }
    ext = os.path.splitext(filename)[1].lower()
    return extension_map.get(ext, 'Unknown')

def list_files_in_task(session_id: str, task_id: str, storage_path: Path = DEFAULT_WORK) -> Dict[str, List[Dict]]:
    """
    List files in a task directory with detailed information including name, language, size, and content.
    Files are categorized into codes, figures, and results.

    Args:
        session_id: Session identifier
        task_id: Task identifier
        storage_path: Base storage directory

    Returns:
        dict: Contains 'codes', 'figures', and 'results' lists with file details
    """
    task_dir = storage_path / session_id / task_id
    if not task_dir.exists():
        return {"codes": [], "figures": [], "results": [], "session_id": session_id, "task_id": task_id}

    figures_dir = task_dir / "figures"
    results_dir = task_dir / "results"

    def get_file_details(file_path: Path, show_content: bool = False) -> Dict:
        """Get file details including name, language, size, and content"""
        if show_content:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                # If UTF-8 fails, try reading as binary
                with open(file_path, 'rb') as f:
                    content = str(f.read())  # Convert bytes to string representation

            return {
                "name": file_path.name,
                "language": get_language_from_extension(file_path.name),
                "size": _human_readable_size(file_path.stat().st_size),
                "content": content
            }
        return {
            "name": file_path.name,
            "language": get_language_from_extension(file_path.name),
            "size_human": _human_readable_size(file_path.stat().st_size),
        }


    def _human_readable_size(size_bytes: int) -> str:
        """Convert size in bytes to human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    # Collect files in main task directory
    codes = [get_file_details(f, True) for f in task_dir.iterdir() if f.is_file()]

    # Collect figures (if figures directory exists)
    figures = [f.name for f in figures_dir.iterdir() if f.is_file()] if figures_dir.exists() else []

    # Collect results (if results directory exists)
    results = [f.name for f in results_dir.iterdir() if f.is_file()] if results_dir.exists() else []
    return {
        "session_id": session_id,
        "codes": codes,
        "figures": figures,
        "results": results,
        "task_id": task_id,
    }