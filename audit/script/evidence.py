"""Evidence Engine — collect, validate, and manage inspection evidence.

No AI reasoning, no risk judgement, no LLM.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Dict, List, Optional

from .models import Evidence, EvidenceType, KnowledgeRepository

logger = logging.getLogger(__name__)


class EvidenceCollection:
    """An ordered collection of :class:`Evidence` objects.

    Supports add, remove, get, list, and count operations.
    Evidence IDs must be unique within the collection.
    """

    def __init__(self) -> None:
        self._items: Dict[str, Evidence] = {}

    # ── Mutators ────────────────────────────────────────────────

    def add(self, evidence: Evidence) -> None:
        """Add an evidence item.

        Raises
        ------
        ValueError
            If an item with the same ``id`` already exists.
        """
        if evidence.id in self._items:
            raise ValueError(f"Duplicate evidence ID '{evidence.id}'")
        self._items[evidence.id] = evidence

    def remove(self, evidence_id: str) -> None:
        """Remove an evidence item by ID.

        Raises
        ------
        KeyError
            If no item with *evidence_id* exists.
        """
        del self._items[evidence_id]

    # ── Accessors ───────────────────────────────────────────────

    def get(self, evidence_id: str) -> Optional[Evidence]:
        """Return the evidence item with *evidence_id*, or ``None``."""
        return self._items.get(evidence_id)

    def list(self) -> List[Evidence]:
        """Return all evidence items in insertion order."""
        return list(self._items.values())

    def count(self) -> int:
        """Return the number of evidence items."""
        return len(self._items)

    # ── Bulk ────────────────────────────────────────────────────

    def add_all(self, items: List[Evidence]) -> List[str]:
        """Add multiple evidence items.

        Returns a list of IDs that were skipped (duplicates).
        """
        skipped: List[str] = []
        for ev in items:
            try:
                self.add(ev)
            except ValueError:
                skipped.append(ev.id)
        return skipped


def validate_evidence(
    evidence_list: List[Evidence],
    repository: Optional[KnowledgeRepository] = None,
) -> List[str]:
    """Validate a list of evidence items and return a list of warnings.

    Checks
    ------
    - Missing checkpoint (checkpoint_id exists in repository)
    - Duplicate evidence ID
    - Empty description
    - Invalid evidence type
    - Broken attachment path (only for file-based attachment paths)

    Parameters
    ----------
    evidence_list
        Evidence items to validate.
    repository
        Optional. When provided, validates that ``checkpoint_id``
        values reference existing checkpoints in the repository.

    Returns
    -------
    List[str]
        Descriptive warning messages.
    """
    warnings: List[str] = []
    seen_ids: set[str] = set()
    valid_types = {t.value for t in EvidenceType}

    for ev in evidence_list:
        # Duplicate ID
        if ev.id in seen_ids:
            warnings.append(f"Duplicate evidence ID '{ev.id}'")
        seen_ids.add(ev.id)

        # Empty description
        if not ev.description.strip():
            warnings.append(f"Evidence '{ev.id}' has an empty description")

        # Invalid type
        if ev.evidence_type.value not in valid_types:
            warnings.append(
                f"Evidence '{ev.id}' has invalid type '{ev.evidence_type.value}'"
            )

        # Missing checkpoint
        if repository is not None and ev.checkpoint_id:
            if ev.checkpoint_id not in repository.checkpoints:
                warnings.append(
                    f"Evidence '{ev.id}' references unknown checkpoint '{ev.checkpoint_id}'"
                )

        # Broken attachment paths
        for att in ev.attachments:
            if att.startswith("/") or att.startswith("\\") or ":" in att:
                # Looks like an absolute path — verify
                p = Path(att)
                if not p.exists():
                    warnings.append(
                        f"Evidence '{ev.id}' attachment not found: {att}"
                    )

    return warnings
