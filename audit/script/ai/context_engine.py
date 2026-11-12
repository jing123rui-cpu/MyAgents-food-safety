"""ContextEngine — bridges InspectionWorkflow and PromptEngine.

Assembles structured ``AIContext`` from an ``InspectionContext``.
Performs NO AI calls and NO prompt rendering — only data aggregation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..models import (
    Checkpoint,
    Evidence,
    EvidenceType,
    EvaluationResult,
    KnowledgeRepository,
    RegistryEntry,
    RiskRule,
    TaxonomyNode,
)
from ..workflow import InspectionContext

logger = logging.getLogger(__name__)


@dataclass
class AIContext:
    """Structured context ready for PromptEngine.

    All fields are human-readable strings (or simple containers)
    built from the raw ``InspectionContext``.
    """

    checkpoints: str = ""
    registry_entries: str = ""
    risk_rules: str = ""
    taxonomy_path: str = ""
    applicable_laws: str = ""
    evidence_summary: str = ""
    risk_level: str = ""
    inspector_query: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


class ContextEngine:
    """Aggregates inspection data into ``AIContext``.

    Usage
    -----
    engine = ContextEngine(repository)
    ctx = engine.build_context(inspection_context)
    """

    def __init__(self, repository: KnowledgeRepository) -> None:
        self._repo = repository

    # ── Public API ───────────────────────────────────────────────

    def build_context(self, inspection_ctx: InspectionContext) -> AIContext:
        """Convert an ``InspectionContext`` into a populated ``AIContext``.

        Parameters
        ----------
        inspection_ctx
            The assembled context from ``InspectionWorkflow.build_context()``.

        Returns
        -------
        AIContext
            Strings and summaries ready for prompt rendering.
        """
        ctx = AIContext()
        ctx.inspector_query = inspection_ctx.request.query

        # 1. Checkpoints
        ctx.checkpoints = self._format_checkpoints(
            inspection_ctx.matched_checkpoints
        )

        # 2. Registry entries
        ctx.registry_entries = self._format_registry_entries(
            inspection_ctx.matched_registry_entries
        )

        # 3. Risk rules
        ctx.risk_rules = self._format_risk_rules(
            inspection_ctx.matched_risk_rules
        )

        # 4. Taxonomy breadcrumb (first checkpoint / registry pair)
        first_reg = (
            inspection_ctx.matched_registry_entries[0]
            if inspection_ctx.matched_registry_entries
            else None
        )
        if first_reg:
            ctx.taxonomy_path = self._build_taxonomy_breadcrumb(first_reg)

        # 5. Applicable laws (merged, de-duplicated, order preserved)
        ctx.applicable_laws = self._build_applicable_laws(
            inspection_ctx.matched_registry_entries
        )

        # 6. Evidence summary
        ctx.evidence_summary = self._build_evidence_summary(
            inspection_ctx.evidence
        )

        # 7. Risk level from the first checkpoint
        first_cp = (
            inspection_ctx.matched_checkpoints[0]
            if inspection_ctx.matched_checkpoints
            else None
        )
        ctx.risk_level = first_cp.risk_level if first_cp else ""

        # 8. Metadata
        ctx.metadata = {
            "checkpoint_count": len(inspection_ctx.matched_checkpoints),
            "registry_count": len(inspection_ctx.matched_registry_entries),
            "risk_rule_count": len(inspection_ctx.matched_risk_rules),
            "taxonomy_node_count": len(inspection_ctx.matched_taxonomy_nodes),
            "evidence_count": len(inspection_ctx.evidence),
            "evaluation_count": len(inspection_ctx.evaluation_results),
        }

        logger.info(
            "AIContext built: %d checkpoints, %d evidence, %d rules",
            len(inspection_ctx.matched_checkpoints),
            len(inspection_ctx.evidence),
            len(inspection_ctx.matched_risk_rules),
        )
        return ctx

    # ── Formatting helpers ───────────────────────────────────────

    @staticmethod
    def _format_checkpoints(checkpoints: List[Checkpoint]) -> str:
        """Format checkpoints as a readable block."""
        if not checkpoints:
            return "No checkpoints matched."
        lines: List[str] = []
        for cp in checkpoints:
            lines.append(
                f"- {cp.checkpoint_id}: {cp.checkpoint_name} "
                f"[{cp.risk_level or 'N/A'}]"
            )
            if cp.objective:
                lines.append(f"  Objective: {cp.objective}")
        return "\n".join(lines)

    @staticmethod
    def _format_registry_entries(entries: List[RegistryEntry]) -> str:
        """Format registry entries as a readable block."""
        if not entries:
            return "No registry entries matched."
        lines: List[str] = []
        for reg in entries:
            lines.append(f"- {reg.id}: {reg.title} ({reg.risk_level})")
            if reg.keywords:
                lines.append(f"  Keywords: {', '.join(reg.keywords)}")
        return "\n".join(lines)

    @staticmethod
    def _format_risk_rules(rules: List[RiskRule]) -> str:
        """Format risk rules as a readable block."""
        if not rules:
            return "No risk rules matched."
        lines: List[str] = []
        for rule in rules:
            lines.append(
                f"- {rule.rule_id}: {rule.condition} → {rule.risk_level}"
            )
            if rule.description:
                lines.append(f"  {rule.description}")
        return "\n".join(lines)

    # ── Evidence summary ─────────────────────────────────────────

    @staticmethod
    def _build_evidence_summary(evidence: List[Evidence]) -> str:
        """Generate a human-readable evidence count by type.

        Example
        -------
        Photo:
        2

        Documents:
        3

        Measurements:
        1

        Observations:
        5
        """
        if not evidence:
            return "No evidence collected."

        counts: Dict[str, int] = {}
        for ev in evidence:
            key = ev.evidence_type.value if isinstance(
                ev.evidence_type, EvidenceType
            ) else str(ev.evidence_type)
            # Normalise display labels
            label = _EVIDENCE_LABELS.get(key, key.title())
            counts[label] = counts.get(label, 0) + 1

        lines: List[str] = []
        for label in sorted(counts, key=lambda x: -counts[x]):
            lines.append(f"{label}:\n{counts[label]}\n")
        return "\n".join(lines).rstrip()

    # ── Laws ─────────────────────────────────────────────────────

    @staticmethod
    def _build_applicable_laws(entries: List[RegistryEntry]) -> str:
        """Merge duplicate laws across registry entries.

        Preserves the original order of first appearance.

        Returns
        -------
        str
            Bulleted list of unique laws.
        """
        seen: set[str] = set()
        ordered: List[str] = []
        for reg in entries:
            for law in reg.laws:
                if law not in seen:
                    seen.add(law)
                    ordered.append(law)
        if not ordered:
            return "No applicable laws referenced."
        return "\n".join(f"- {law}" for law in ordered)

    # ── Taxonomy breadcrumb ──────────────────────────────────────

    def _build_taxonomy_breadcrumb(self, reg: RegistryEntry) -> str:
        """Build a breadcrumb path from the taxonomy hierarchy.

        Builds the path by resolving registry entry fields
        (``domain``, ``sub_domain``, ``category``) against
        taxonomy node names.

        Returns
        -------
        str
            e.g. ``"Raw Material Management > Supplier Management > "
                  "原料管理 > 供应商资质审核"``
        or simply ``"N/A"`` if no taxonomy is available.
        """
        parts: List[str] = []

        # Resolve domain
        if reg.domain:
            node = self._repo.taxonomy.get(reg.domain)
            parts.append(node.name if node else reg.domain)

        # Resolve sub-domain
        if reg.sub_domain:
            node = self._repo.taxonomy.get(reg.sub_domain)
            parts.append(node.name if node else reg.sub_domain)

        # category / subcategory are direct display names in the registry
        if reg.category:
            parts.append(reg.category)
        if reg.subcategory:
            parts.append(str(reg.subcategory))  # ensure str

        return " > ".join(parts) if parts else "N/A"


# Display labels for evidence type values
_EVIDENCE_LABELS: Dict[str, str] = {
    "OBSERVATION": "Observations",
    "PHOTO": "Photos",
    "DOCUMENT": "Documents",
    "MEASUREMENT": "Measurements",
    "LAB_REPORT": "Lab Reports",
    "VIDEO": "Videos",
    "SYSTEM_RECORD": "System Records",
}
