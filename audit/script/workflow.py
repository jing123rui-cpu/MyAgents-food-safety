"""Workflow Engine — inspection pipeline that assembles structured audit context.

No AI reasoning, no LLM, no prompt generation.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .models import (
    Checkpoint,
    EvaluationResult,
    Evidence,
    KnowledgeRepository,
    RegistryEntry,
    RiskRule,
    TaxonomyNode,
)
from .search import KnowledgeSearchEngine

logger = logging.getLogger(__name__)


@dataclass
class InspectionRequest:
    """Parameters describing what to audit."""

    query: str = ""
    category: str = ""
    risk_level: str = ""
    checkpoint_id: str = ""

    @property
    def is_empty(self) -> bool:
        """``True`` when no search dimension is set."""
        return not (self.query or self.category or self.risk_level or self.checkpoint_id)


@dataclass
class InspectionContext:
    """Structured context assembled by the inspection pipeline."""

    request: InspectionRequest
    matched_checkpoints: List[Checkpoint] = field(default_factory=list)
    matched_risk_rules: List[RiskRule] = field(default_factory=list)
    matched_registry_entries: List[RegistryEntry] = field(default_factory=list)
    matched_taxonomy_nodes: List[TaxonomyNode] = field(default_factory=list)
    evidence: List[Evidence] = field(default_factory=list)
    evaluation_results: List[EvaluationResult] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class InspectionWorkflow:
    """Orchestrates the inspection pipeline.

    Uses the search engine for checkpoint retrieval, then enriches
    results with registry entries, risk rules, and taxonomy nodes.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
        search_engine: KnowledgeSearchEngine,
        risk_rules: Optional[List[RiskRule]] = None,
    ) -> None:
        self._repo = repository
        self._search = search_engine
        self._risk_rules = risk_rules or []

        # Precomputed index: checkpoint_id -> list of RiskRule
        self._cp_to_rules: Dict[str, List[RiskRule]] = {}
        self._build_risk_index()

        # Precomputed index: checkpoint_id -> list of TaxonomyNode
        self._cp_to_taxonomy: Dict[str, List[TaxonomyNode]] = {}
        self._build_taxonomy_index()

    # ── Public API ──────────────────────────────────────────────

    def build_context(self, request: InspectionRequest) -> InspectionContext:
        """Execute the full inspection pipeline for *request*.

        Pipeline
        --------
        1. Search checkpoints
        2. Look up registry entries
        3. Locate risk rules
        4. Locate taxonomy nodes
        5. Assemble context
        6. Validate
        """
        ctx = InspectionContext(request=request)

        # 1. Search checkpoints
        checkpoints = self._search_checkpoints(request)
        cp_ids = {cp.checkpoint_id for cp in checkpoints}
        ctx.matched_checkpoints = checkpoints

        # 2. Registry entries
        entries = self._lookup_registry(cp_ids)
        ctx.matched_registry_entries = entries

        # 3. Risk rules
        rules = self._lookup_risk_rules(cp_ids)
        ctx.matched_risk_rules = rules

        # 4. Taxonomy nodes
        nodes = self._lookup_taxonomy(cp_ids)
        ctx.matched_taxonomy_nodes = nodes

        # 5. Validate
        self._validate(ctx)

        # 6. Metadata
        ctx.metadata = {
            "total_checkpoints": len(checkpoints),
            "total_registry_entries": len(entries),
            "total_risk_rules": len(rules),
            "total_taxonomy_nodes": len(nodes),
            "total_evidence": len(ctx.evidence),
            "total_evaluation_results": len(ctx.evaluation_results),
            "warnings_count": len(ctx.warnings),
        }

        logger.info(
            "Inspection context built: %d checkpoints, %d rules, %d taxonomy nodes",
            len(checkpoints), len(rules), len(nodes),
        )
        return ctx

    # ── Pipeline Stages ─────────────────────────────────────────

    def _search_checkpoints(self, request: InspectionRequest) -> List[Checkpoint]:
        """Stage 1 — retrieve checkpoints based on request fields."""
        if request.checkpoint_id:
            cp = self._search.search_checkpoint(request.checkpoint_id)
            return [cp] if cp else []

        # Collect IDs from each provided search dimension
        sets: List[set[str]] = []

        if request.query:
            cps = self._search.search_keyword(request.query)
            sets.append({cp.checkpoint_id for cp in cps})

        if request.category:
            cps = self._search.search_category(request.category)
            sets.append({cp.checkpoint_id for cp in cps})

        if request.risk_level:
            cps = self._search.search_risk(request.risk_level)
            sets.append({cp.checkpoint_id for cp in cps})

        if not sets:
            return []

        # Intersect when multiple dimensions are specified
        ids = set.intersection(*sets) if len(sets) > 1 else sets[0]
        return [self._repo.checkpoints[cid] for cid in sorted(ids)]

    def _lookup_registry(self, cp_ids: set[str]) -> List[RegistryEntry]:
        """Stage 2 — resolve registry entries for the matched checkpoints."""
        return [
            reg for cid, reg in self._repo.registry.items()
            if cid in cp_ids
        ]

    def _lookup_risk_rules(self, cp_ids: set[str]) -> List[RiskRule]:
        """Stage 3 — collect risk rules that apply to the matched checkpoints."""
        seen: set[str] = set()
        result: List[RiskRule] = []
        for cid in cp_ids:
            for rule in self._cp_to_rules.get(cid, []):
                if rule.rule_id not in seen:
                    seen.add(rule.rule_id)
                    result.append(rule)
        return result

    def _lookup_taxonomy(self, cp_ids: set[str]) -> List[TaxonomyNode]:
        """Stage 4 — collect taxonomy nodes associated with the matched checkpoints."""
        seen: set[str] = set()
        result: List[TaxonomyNode] = []
        for cid in cp_ids:
            for node in self._cp_to_taxonomy.get(cid, []):
                if node.id not in seen:
                    seen.add(node.id)
                    result.append(node)
        return result

    # ── Validation ──────────────────────────────────────────────

    def _validate(self, ctx: InspectionContext) -> None:
        """Stage 5 — run validation checks and collect warnings."""
        cp_ids = {cp.checkpoint_id for cp in ctx.matched_checkpoints}
        reg_ids = {reg.id for reg in ctx.matched_registry_entries}

        # Missing checkpoint
        for rid in reg_ids:
            if rid not in cp_ids:
                ctx.warnings.append(f"Registry entry '{rid}' has no matched checkpoint")

        # Missing risk rule
        for cid in cp_ids:
            if cid not in self._cp_to_rules:
                ctx.warnings.append(f"Checkpoint '{cid}' has no risk rule")

        # Missing taxonomy
        for cid in cp_ids:
            if cid not in self._cp_to_taxonomy:
                ctx.warnings.append(f"Checkpoint '{cid}' has no taxonomy mapping")

        # Empty search result
        if not cp_ids:
            ctx.warnings.append("Search produced no matching checkpoints")

        # Duplicate results (checkpoint IDs should already be unique,
        # but warn if the same ID appears in the results list multiple times)
        seen = set()
        for cp in ctx.matched_checkpoints:
            if cp.checkpoint_id in seen:
                ctx.warnings.append(f"Duplicate checkpoint '{cp.checkpoint_id}' in results")
            seen.add(cp.checkpoint_id)

    # ── Internal Index Builders ─────────────────────────────────

    def _build_risk_index(self) -> None:
        """Build ``checkpoint_id -> [RiskRule, ...]`` from rule IDs.

        Risk rule IDs follow the convention ``RR-{checkpoint_id}``,
        e.g. ``RR-CP-BEV-RM-001``, and many also carry an explicit
        ``checkpoint_id`` field extracted during loading.
        """
        for rule in self._risk_rules:
            # Derive checkpoint ID from the rule_id convention
            candidates = set()
            if rule.rule_id.startswith("RR-"):
                candidates.add(rule.rule_id[3:])  # "RR-CP-..." -> "CP-..."

            for cid in candidates:
                self._cp_to_rules.setdefault(cid, []).append(rule)

        # Additionally check the loader's internal map (checkpoint_id
        # field stored during loading).  The loader exposed this via
        # the risk_rules list itself, but we also have the convention
        # above.  We store it on the loader's KnowledgeBase.
        # Re-scan the repo for checkpoints that match via file naming.
        for cp_id in self._repo.checkpoints:
            expected_rule_id = f"RR-{cp_id}"
            for rule in self._risk_rules:
                if rule.rule_id == expected_rule_id:
                    if rule not in self._cp_to_rules.setdefault(cp_id, []):
                        self._cp_to_rules[cp_id].append(rule)

    def _build_taxonomy_index(self) -> None:
        """Build ``checkpoint_id -> [TaxonomyNode, ...]`` by matching
        registry fields against taxonomy node IDs and names.

        For each registry entry, taxonomy nodes whose ``id`` or
        ``name`` matches the entry's ``domain``, ``sub_domain``,
        ``category``, or ``subcategory`` are linked.
        """
        # Searchable fields in RegistryEntry that may align with taxonomy node IDs
        reg_fields = ["domain", "sub_domain", "category", "subcategory"]

        for reg_id, reg in self._repo.registry.items():
            # Collect all possible taxonomy reference values from this entry
            refs = set()
            for f in reg_fields:
                val = getattr(reg, f, "")
                if val:
                    refs.add(val)

            # Match against taxonomy node ids and names
            for node in self._repo.taxonomy.values():
                node_key = node.id  # e.g. "raw_material_management"
                node_name_lower = node.name.lower()

                for ref in refs:
                    if node_key == ref or node_name_lower == ref.lower():
                        self._cp_to_taxonomy.setdefault(reg_id, []).append(node)
                        break  # one node per match is enough
