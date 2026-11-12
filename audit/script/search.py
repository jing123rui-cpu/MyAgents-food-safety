"""Knowledge Search Engine — deterministic retrieval of knowledge objects."""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .models import Checkpoint, KnowledgeRepository

logger = logging.getLogger(__name__)

# Score weights for keyword search ranking
_TITLE_WEIGHT = 3
_KEYWORD_WEIGHT = 2
_BODY_WEIGHT = 1

# Mapping from user-facing risk levels to internal representations
_RISK_MAP: Dict[str, List[str]] = {
    "critical": ["critical", "RISK-01", "c"],
    "high": ["high", "h", "RISK-02"],
    "medium": ["medium", "m", "RISK-03", "moderate"],
    "moderate": ["medium", "m", "RISK-03", "moderate"],
    "low": ["low", "l", "RISK-04"],
}


class KnowledgeSearchEngine:
    """Deterministic search engine over a loaded KnowledgeRepository.

    Supports lookups by checkpoint ID, keyword (full-text across
    titles, keywords, and markdown bodies), category, and risk level.
    """

    def __init__(self, repository: KnowledgeRepository) -> None:
        self._repo = repository

    # ── Search by ID ────────────────────────────────────────────

    def search_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Return the checkpoint with the given ID, or ``None``."""
        return self._repo.checkpoints.get(checkpoint_id)

    # ── Keyword Search ──────────────────────────────────────────

    def search_keyword(self, keyword: str) -> List[Checkpoint]:
        """Return checkpoints matching *keyword*, ranked by relevance.

        Searches across:
        - Registry entry keywords (stored in :attr:`RegistryEntry.keywords`)
        - Checkpoint title (:attr:`Checkpoint.checkpoint_name`)
        - Checkpoint markdown body (:attr:`Checkpoint.raw_content`)

        Results are sorted descending by a relevance score:
        - Title match:    3 points
        - Keyword match:  2 points
        - Body match:     1 point
        """
        if not keyword:
            return []

        q = keyword.lower()
        scored: List[tuple[int, str]] = []  # (score, checkpoint_id)

        for cp_id, cp in self._repo.checkpoints.items():
            score = 0

            # Title
            if q in cp.checkpoint_name.lower():
                score += _TITLE_WEIGHT

            # Markdown body
            if q in cp.raw_content.lower():
                score += _BODY_WEIGHT

            # Registry keywords
            reg = self._repo.registry.get(cp_id)
            if reg:
                for kw in reg.keywords:
                    if q in kw.lower():
                        score += _KEYWORD_WEIGHT
                        break

            if score > 0:
                scored.append((score, cp_id))

        # Sort descending by score, then by ID for determinism
        scored.sort(key=lambda x: (-x[0], x[1]))

        return [self._repo.checkpoints[cid] for _, cid in scored]

    # ── Category Search ─────────────────────────────────────────

    def search_category(self, category: str) -> List[Checkpoint]:
        """Return all checkpoints belonging to a registry category.

        Matches against :attr:`RegistryEntry.category` and
        :attr:`RegistryEntry.subcategory` (case-insensitive).
        """
        if not category:
            return []

        q = category.lower()
        matched_ids: set[str] = set()

        for cid, reg in self._repo.registry.items():
            if q in reg.category.lower() or q in reg.subcategory.lower():
                matched_ids.add(cid)

        return [
            self._repo.checkpoints[cid]
            for cid in sorted(matched_ids)
            if cid in self._repo.checkpoints
        ]

    # ── Risk Search ─────────────────────────────────────────────

    def search_risk(self, level: str) -> List[Checkpoint]:
        """Return all checkpoints whose risk level matches *level*.

        Accepts common names (``"High"``, ``"Medium"``, ``"Low"``) as
        well as internal codes (``"RISK-01"``, ``"H"``, etc.).
        Matching is case-insensitive.

        Matches are drawn from:
        - :attr:`Checkpoint.risk_level`
        - :attr:`RegistryEntry.risk_level`
        """
        if not level:
            return []

        q = level.lower()
        candidates: set[str] = set()

        # Resolve the query to a set of known aliases
        aliases = _RISK_MAP.get(q, [q])

        for cid, cp in self._repo.checkpoints.items():
            if cp.risk_level.lower() in aliases:
                candidates.add(cid)

        for cid, reg in self._repo.registry.items():
            if reg.risk_level.lower() in aliases:
                candidates.add(cid)

        return [
            self._repo.checkpoints[cid]
            for cid in sorted(candidates)
            if cid in self._repo.checkpoints
        ]

    # ── Convenience / Introspection ─────────────────────────────

    @property
    def repository(self) -> KnowledgeRepository:
        """The underlying knowledge repository."""
        return self._repo

    def total_checkpoints(self) -> int:
        """Number of checkpoints indexed by the engine."""
        return len(self._repo.checkpoints)
