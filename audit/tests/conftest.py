"""pytest configuration — ensures project root is on sys.path."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path so that "from script import ..." works
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))
