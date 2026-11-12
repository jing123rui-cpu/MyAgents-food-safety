"""Utility functions for the Food Audit Agent."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)


def validate_path(path: Path) -> bool:
    """Verify that *path* exists and is readable.

    Raises
    ------
    FileNotFoundError
        If the path does not exist.
    PermissionError
        If the path is not readable.
    """
    if not path.exists():
        raise FileNotFoundError(f"Path not found: {path}")
    if not path.is_file():
        raise FileNotFoundError(f"Not a file: {path}")
    return True


def read_yaml(path: Path) -> Any:
    """Load and parse a YAML file.

    Parameters
    ----------
    path : Path
        Path to the YAML file.

    Returns
    -------
    Any
        Parsed YAML content (typically ``list`` or ``dict``).

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If the file is empty or contains invalid YAML.
    """
    validate_path(path)

    raw = path.read_text(encoding="utf-8")
    if not raw.strip():
        raise ValueError(f"YAML file is empty: {path}")

    try:
        data = yaml.safe_load(raw)
    except yaml.YAMLError as exc:
        raise ValueError(f"Invalid YAML in {path}: {exc}") from exc

    if data is None:
        raise ValueError(f"YAML file is empty (null document): {path}")

    return data


def ensure_dir(path: Path) -> Path:
    """Ensure a directory exists, creating it if necessary."""
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_report_id() -> str:
    """Generate a unique report identifier."""
    # TODO: Produce a timestamp-based unique report ID.
    raise NotImplementedError


def read_markdown(path: Path) -> str:
    """Read a Markdown file and return its content as a string.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    """
    validate_path(path)
    return path.read_text(encoding="utf-8")


def discover_files(directory: Path, pattern: str) -> List[Path]:
    """Recursively discover files matching a glob pattern.

    Returns a sorted list of matching file paths.
    """
    if not directory.is_dir():
        return []
    return sorted(directory.rglob(pattern))
