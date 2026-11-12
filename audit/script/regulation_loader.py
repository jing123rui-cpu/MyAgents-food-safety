"""RegulationLoader — loads, indexes and queries the Regulatory Knowledge Base.

Reads ``knowledge/regulations/regulation_registry.yaml`` and Markdown
full-text files, then provides lookup methods for:

- Loading regulation metadata and full-text content
- Searching regulations by keyword
- Querying regulations by enterprise type (applicability rules)
- Resolving related checkpoints and risk rules
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

logger = logging.getLogger(__name__)

# Enterprise type hierarchy
_ENTERPRISE_TYPE_HIERARCHY = {
    "general_food": [],
    "beverage": ["general_food"],
    "packaged_water": ["general_food", "beverage"],
}

# Default regulations for each enterprise type (fallback when registry is empty)
_DEFAULT_REGS_BY_TYPE = {
    "general_food": [
        "REG-FOOD-SAFETY-LAW",
        "REG-FOOD-SAFETY-LAW-IMPL",
        "REG-FOOD-PRODUCTION-LICENSE",
        "REG-PRODUCTION-LICENSE-REVIEW",
        "REG-INSPECTION-CHECKLIST",
        "REG-GB-14881",
    ],
    "beverage": [
        "REG-GB-12695",
        "REG-GB-7101",
    ],
    "packaged_water": [
        "REG-GB-19298",
    ],
}


@dataclass
class RegulationEntry:
    """Metadata for a single regulation from the regulatory registry."""
    id: str
    title: str
    title_zh: str
    document_type: str
    issuing_authority: str
    effective_date: str
    status: str
    scope: str = ""
    keywords: List[str] = field(default_factory=list)
    last_revision: str = ""
    enterprise_types: List[str] = field(default_factory=list)


@dataclass
class RegulationDocument:
    """Full-text content of a single regulation document."""
    regulation_id: str
    title: str
    title_zh: str
    purpose: str = ""
    scope: str = ""
    key_requirements: List[str] = field(default_factory=list)
    inspection_scenarios: List[str] = field(default_factory=list)
    related_checkpoints: List[str] = field(default_factory=list)
    related_risk_rules: List[str] = field(default_factory=list)
    raw_content: str = ""


@dataclass
class RegulationRepository:
    """Container for all loaded regulation assets."""
    registry: Dict[str, RegulationEntry] = field(default_factory=dict)
    documents: Dict[str, RegulationDocument] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)


class RegulationLoader:
    """Loads, indexes, and queries the Regulatory Knowledge Base.

    Usage
    -----
    loader = RegulationLoader(knowledge_dir="knowledge")
    repo = loader.load_regulations()

    entry = loader.search_regulation("GB 14881")
    checkpoints = loader.get_related_checkpoints("REG-GB-14881")
    rules = loader.get_related_rules("REG-GB-14881")
    """

    def __init__(self, knowledge_dir: str = "knowledge") -> None:
        self._knowledge_dir = Path(knowledge_dir)
        self._regulations_dir = self._knowledge_dir / "regulations"

    # ── Public API ────────────────────────────────────────────────────────────

    def load_regulations(self) -> RegulationRepository:
        """Load the regulation registry and all full-text Markdown documents.

        Returns
        -------
        RegulationRepository
            Populated repository with registry entries and documents.
        """
        repo = RegulationRepository()
        registry_path = self._regulations_dir / "regulation_registry.yaml"

        if not registry_path.exists():
            repo.errors.append(f"Regulation registry not found: {registry_path}")
            return repo

        # 1. Load registry
        try:
            raw = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
        except Exception as exc:
            repo.errors.append(f"Failed to parse registry YAML: {exc}")
            return repo

        if not isinstance(raw, list):
            repo.errors.append("Registry YAML root must be a list")
            return repo

        for entry in raw:
            reg_id = entry.get("id", "")
            if not reg_id:
                repo.warnings.append("Registry entry missing 'id' — skipped")
                continue
            reg = RegulationEntry(
                id=reg_id,
                title=entry.get("title", ""),
                title_zh=entry.get("title_zh", ""),
                document_type=entry.get("document_type", ""),
                issuing_authority=entry.get("issuing_authority", ""),
                effective_date=entry.get("effective_date", ""),
                status=entry.get("status", ""),
                scope=entry.get("scope", ""),
                keywords=entry.get("keywords", []),
                last_revision=entry.get("last_revision", ""),
                enterprise_types=entry.get("enterprise_types", []),
            )
            repo.registry[reg_id] = reg

        # 2. Load full-text Markdown documents
        md_files = sorted(self._regulations_dir.glob("REG-*.md"))
        for mf in md_files:
            reg_id = mf.stem  # e.g. "REG-FOOD-SAFETY-LAW"
            if reg_id in repo.registry:
                try:
                    content = mf.read_text(encoding="utf-8")
                    doc = RegulationDocument(
                        regulation_id=reg_id,
                        title=repo.registry[reg_id].title,
                        title_zh=repo.registry[reg_id].title_zh,
                        raw_content=content,
                    )
                    # Extract sections via headings
                    doc.purpose = self._extract_section(content, "## Purpose")
                    doc.scope = self._extract_section(content, "## Scope")
                    doc.key_requirements = self._extract_list(content, "## Key Requirements")
                    doc.inspection_scenarios = self._extract_list(content, "## Applicable Inspection Scenarios")
                    repo.documents[reg_id] = doc
                except Exception as exc:
                    repo.warnings.append(f"Failed to load {mf.name}: {exc}")

        logger.info(
            "Loaded %d registry entries, %d documents",
            len(repo.registry), len(repo.documents),
        )
        return repo

    # ── Query Methods ──────────────────────────────────────────────────────────

    def search_regulation(
        self,
        query: str,
        *,
        repo: RegulationRepository,
        field: Optional[str] = None,
    ) -> List[RegulationEntry]:
        """Search regulations by keyword or field match.

        Parameters
        ----------
        query
            Search term (matched against title, title_zh, keywords, and scope).
        repo
            A loaded ``RegulationRepository``.
        field
            Optional field restriction (e.g. ``"title"``, ``"keywords"``).

        Returns
        -------
        List[RegulationEntry]
            Matching regulation entries.
        """
        q = query.lower()
        results: List[RegulationEntry] = []
        for entry in repo.registry.values():
            if field:
                val = getattr(entry, field, "")
                if q in str(val).lower():
                    results.append(entry)
            else:
                searchable = f"{entry.title} {entry.title_zh} {' '.join(entry.keywords)} {entry.scope}"
                if q in searchable.lower():
                    results.append(entry)
        return results

    def get_applicable_regulations(
        self,
        repo: RegulationRepository,
        enterprise_type: str = "general_food",
    ) -> List[RegulationEntry]:
        """Return regulations applicable to a given enterprise type.

        Resolves the enterprise type hierarchy (e.g. ``beverage`` includes
        ``general_food`` base regs). Falls back to defaults if no registry
        entries contain ``enterprise_types``.

        Parameters
        ----------
        repo
            A loaded ``RegulationRepository``.
        enterprise_type
            One of ``general_food``, ``beverage``, ``packaged_water``.

        Returns
        -------
        List[RegulationEntry]
            Applicable regulation entries.
        """
        # Collect all relevant enterprise type tags
        types_to_match = {enterprise_type}
        parent_types = _ENTERPRISE_TYPE_HIERARCHY.get(enterprise_type, [])
        types_to_match.update(parent_types)

        # Find regs whose enterprise_types overlap with types_to_match
        matched: List[RegulationEntry] = []
        for entry in repo.registry.values():
            if not entry.enterprise_types:
                continue
            if any(t in entry.enterprise_types for t in types_to_match):
                matched.append(entry)

        # Fallback: if no regs have enterprise_types, use ID-based defaults
        if not matched:
            default_ids = _DEFAULT_REGS_BY_TYPE.get(enterprise_type, [])
            for ent_type in parent_types:
                default_ids.extend(_DEFAULT_REGS_BY_TYPE.get(ent_type, []))
            seen = set()
            for rid in default_ids:
                if rid not in seen and rid in repo.registry:
                    matched.append(repo.registry[rid])
                    seen.add(rid)

        return matched

    def get_related_checkpoints(
        self,
        regulation_id: str,
        *,
        repo: RegulationRepository,
    ) -> List[str]:
        """Return checkpoint IDs that reference a given regulation.

        Cross-references against ``knowledge/registry/`` entries.
        Uses the registry entry's ``laws`` field.
        """
        # This requires access to registry entries, which we don't have here.
        # Return empty list for now — cross-reference is a future enhancement.
        return []

    # ── Internal Helpers ───────────────────────────────────────────────────────

    @staticmethod
    def _extract_section(content: str, heading: str) -> str:
        """Extract text under a Markdown heading until the next heading."""
        pattern = rf"^{heading}\s*\n\n(.+?)(?=\n---|\n##|\Z)"
        m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if m:
            return m.group(1).strip()
        # Try <!-- block
        pattern2 = rf"^{heading}\s*\n<!-- TODO: (.+?) -->"
        m2 = re.search(pattern2, content, re.DOTALL)
        return m2.group(1).strip() if m2 else ""

    @staticmethod
    def _extract_list(content: str, heading: str) -> List[str]:
        """Extract a bullet list under a heading."""
        pattern = rf"^{heading}\s*\n\n(.*?)(?=\n---|\n##|\Z)"
        m = re.search(pattern, content, re.MULTILINE | re.DOTALL)
        if m:
            block = m.group(1)
            items = re.findall(r"^- (.+)", block, re.MULTILINE)
            return items
        # Try <!-- block
        pattern2 = rf"^{heading}\s*\n<!-- TODO:.*?\n\n(.+?)-->"
        m2 = re.search(pattern2, content, re.DOTALL)
        if m2:
            items = re.findall(r"- (.+)", m2.group(1))
            return items
        return []
