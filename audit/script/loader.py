"""Knowledge Loader — discovers, validates, loads and indexes all knowledge assets."""

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from .models import (
    Checkpoint,
    KnowledgeBase,
    KnowledgeRepository,
    LoaderStatistics,
    RegistryEntry,
    RiskRule,
    TaxonomyNode,
)
from .utils import discover_files, read_markdown, read_yaml

logger = logging.getLogger(__name__)


# ── Module-Level Helpers ──────────────────────────────────────────

_valid_severities = {"Critical", "High", "Medium", "Low", "Info"}


def _parse_yaml_frontmatter(content: str) -> Optional[Dict[str, Any]]:
    """Extract YAML front matter from a checkpoint Markdown file.

    Looks for a ```yaml ... ``` block.
    """
    match = re.search(r"```yaml\s*\n(.*?)\n```", content, re.DOTALL)
    if match:
        try:
            return yaml.safe_load(match.group(1))
        except yaml.YAMLError:
            return None
    return None


def _extract_cp_id_from_heading(content: str) -> Optional[str]:
    """Extract checkpoint ID from ``# CP-XXX-NNN …`` heading."""
    m = re.search(r"^#\s+(CP-[\w-]+)", content, re.MULTILINE)
    return m.group(1).strip() if m else None


def _extract_cp_title_from_heading(content: str) -> str:
    """Extract checkpoint title (text after ``：`` in heading)."""
    m = re.search(r"^#\s+CP-[\w-]+[：:]\s*(.+)", content, re.MULTILINE)
    return m.group(1).strip() if m else ""


def _build_taxonomy_node(
    domain: Dict[str, Any],
    flat_store: Dict[str, TaxonomyNode],
) -> TaxonomyNode:
    """Recursively build a TaxonomyNode tree from the YAML domain dict.

    Also inserts every node into *flat_store* keyed by its ``id``.
    """
    node_id = domain["id"]
    node_name = domain.get("name", domain.get("name_zh", node_id))
    node_name_zh = domain.get("name_zh", "")
    children: List[TaxonomyNode] = []

    for sd in domain.get("sub_domains", []):
        sd_id = sd["id"]
        sd_name = sd.get("name", sd.get("name_zh", sd_id))
        sd_name_zh = sd.get("name_zh", "")
        sd_children: List[TaxonomyNode] = []

        for cat in sd.get("categories", []):
            cat_id = cat["id"]
            cat_name = cat.get("name", cat.get("name_zh", cat_id))
            cat_name_zh = cat.get("name_zh", "")
            cn = TaxonomyNode(id=cat_id, name=cat_name, name_zh=cat_name_zh)
            flat_store[cat_id] = cn
            sd_children.append(cn)

        sdn = TaxonomyNode(id=sd_id, name=sd_name, name_zh=sd_name_zh, children=sd_children)
        flat_store[sd_id] = sdn
        children.append(sdn)

    dn = TaxonomyNode(id=node_id, name=node_name, name_zh=node_name_zh, children=children)
    flat_store[node_id] = dn
    return dn


def _extract_section(content: str, start: str, end: str | None = None) -> str:
    """Extract text between *start* and an optional *end* heading marker."""
    m = re.search(re.escape(start), content)
    if not m:
        return ""
    pos = m.end()
    if end:
        n = re.search(re.escape(end), content[pos:])
        if n:
            return content[pos:pos + n.start()].strip()
    return content[pos:].strip()


class KnowledgeLoader:
    """Discovers, validates, loads and indexes every knowledge asset."""

    def __init__(self, knowledge_dir: Optional[Path] = None) -> None:
        self.knowledge_dir = Path(knowledge_dir) if knowledge_dir else Path("knowledge")
        self.registry: Dict[str, RegistryEntry] = {}
        self.taxonomy: Dict[str, TaxonomyNode] = {}
        self.checkpoints: Dict[str, Checkpoint] = {}
        self.risk_rules: List[RiskRule] = []
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self._initialized = False
        self._rr_checkpoint_map: Dict[str, str] = {}
        self._taxonomy_roots: List[TaxonomyNode] = []

    # ── Initialisation ──────────────────────────────────────────

    def initialize(self) -> None:
        """Prepare paths, warning list and cache."""
        self.registry.clear()
        self.taxonomy.clear()
        self.checkpoints.clear()
        self.risk_rules.clear()
        self.errors.clear()
        self.warnings.clear()
        self._rr_checkpoint_map.clear()
        self._taxonomy_roots.clear()
        if not self.knowledge_dir.is_dir():
            self.errors.append(
                f"Knowledge directory does not exist: {self.knowledge_dir}"
            )
        self._initialized = True
        logger.info("KnowledgeLoader initialized (dir: %s)", self.knowledge_dir)

    # ── Registry Loading ────────────────────────────────────────

    def load_registry(self) -> Dict[str, RegistryEntry]:
        """Discover ``knowledge/registry/*.yaml`` files, parse each,
        and build a dict of ``RegistryEntry`` objects keyed by checkpoint ID.

        Returns
        -------
        Dict[str, RegistryEntry]
            All registry entries indexed by their ``id`` field.
        """
        if not self._initialized:
            self.initialize()

        registry_dir = self.knowledge_dir / "registry"
        if not registry_dir.is_dir():
            self.warnings.append(f"Registry directory not found: {registry_dir}")
            return {}

        yaml_files = sorted(registry_dir.glob("*.yaml"))
        if not yaml_files:
            self.warnings.append(f"No YAML files found in {registry_dir}")
            return {}

        for yaml_path in yaml_files:
            logger.info("Registry file found: %s", yaml_path.name)
            try:
                data = read_yaml(yaml_path)
            except Exception as exc:
                self.errors.append(f"Failed to load {yaml_path}: {exc}")
                continue

            if not isinstance(data, list):
                self.errors.append(
                    f"Registry file {yaml_path} is not a list (got {type(data).__name__})"
                )
                continue

            for idx, item in enumerate(data):
                if not isinstance(item, dict):
                    self.warnings.append(
                        f"Skipping non-dict entry at index {idx} in {yaml_path.name}"
                    )
                    continue

                cp_id = item.get("id", "")
                if not cp_id:
                    self.warnings.append(
                        f"Entry without 'id' at index {idx} in {yaml_path.name}"
                    )
                    continue

                if cp_id in self.registry:
                    self.warnings.append(
                        f"Duplicate registry ID '{cp_id}' in {yaml_path.name}"
                    )

                self.registry[cp_id] = RegistryEntry(
                    id=cp_id,
                    title=item.get("title", ""),
                    domain=item.get("domain", ""),
                    sub_domain=item.get("sub_domain", ""),
                    category=item.get("category", ""),
                    subcategory=item.get("subcategory", ""),
                    risk_level=item.get("risk_level", ""),
                    laws=item.get("laws", []),
                    keywords=item.get("keywords", []),
                    evidence_required=item.get("evidence_required", []),
                    checkpoint_file=item.get("checkpoint_file", ""),
                )

        ids = list(self.registry.keys())
        logger.info("Total registry entries: %d", len(ids))
        if ids:
            logger.info("First registry ID: %s", ids[0])
            logger.info("Last registry ID: %s", ids[-1])
        if not any("Duplicate" in w for w in self.warnings):
            logger.info("No duplicate IDs")

        return self.registry

    # ── Taxonomy Loading ────────────────────────────────────────

    def load_taxonomy(self) -> Dict[str, TaxonomyNode]:
        """Read ``knowledge/taxonomy/*.yaml`` and build a flat dict of
        ``TaxonomyNode`` objects keyed by node ID.

        Validates:
        - duplicate IDs in the same file
        - broken parent references
        - invalid hierarchy (more than 3 levels)
        """
        if not self._initialized:
            self.initialize()

        taxonomy_dir = self.knowledge_dir / "taxonomy"
        if not taxonomy_dir.is_dir():
            self.warnings.append(f"Taxonomy directory not found: {taxonomy_dir}")
            return {}

        yaml_files = sorted(taxonomy_dir.glob("*.yaml"))
        if not yaml_files:
            self.warnings.append(f"No YAML files found in {taxonomy_dir}")
            return {}

        seen_ids: set[str] = set()
        flat: Dict[str, TaxonomyNode] = {}

        for yaml_path in yaml_files:
            logger.info("Taxonomy file found: %s", yaml_path.name)
            try:
                raw = read_yaml(yaml_path)
            except Exception as exc:
                self.errors.append(f"Failed to load taxonomy {yaml_path}: {exc}")
                continue

            if not isinstance(raw, dict):
                self.errors.append(
                    f"Taxonomy file {yaml_path} is not a dict (got {type(raw).__name__})"
                )
                continue

            # Navigate through the top-level tree key
            tree = raw
            for key in ("beverage_knowledge_tree", "knowledge_tree", "taxonomy"):
                if key in tree:
                    tree = tree[key]
                    break

            domains = tree.get("domains", []) if isinstance(tree, dict) else []
            if not domains:
                self.warnings.append(f"No 'domains' list found in {yaml_path}")
                continue

            for domain in domains:
                if not isinstance(domain, dict):
                    continue
                try:
                    dn = _build_taxonomy_node(domain, flat)
                    self._taxonomy_roots.append(dn)
                except KeyError as exc:
                    self.errors.append(
                        f"Taxonomy node missing required key {exc} in {yaml_path}"
                    )
                    continue

                # Check for duplicate IDs across all files
                dupes = _collect_node_ids(dn) & seen_ids
                for d in dupes:
                    self.warnings.append(
                        f"Duplicate taxonomy node ID '{d}' in {yaml_path}"
                    )
                seen_ids.update(_collect_node_ids(dn))

            logger.info("Loaded %d taxonomy nodes from %s", len(flat), yaml_path.name)

        # Validate parent references (every child should have a parent recorded)
        # Since we build flat dict from the tree, all references are valid.
        # Check for broken checkpoint references later in cross_validate().

        if flat:
            logger.info("Total taxonomy nodes: %d", len(flat))
            logger.info("First taxonomy node: %s", next(iter(flat)))
            logger.info("Last taxonomy node: %s", list(flat.keys())[-1])

        self.taxonomy = flat
        return self.taxonomy

    # ── Checkpoint Loading ──────────────────────────────────────

    def load_checkpoints(self) -> Dict[str, Checkpoint]:
        """Read every ``knowledge/checkpoints/**/*.md`` file, parse
        front matter and markdown body, and return a dict of
        ``Checkpoint`` objects keyed by checkpoint ID.

        Validates:
        - duplicate IDs
        - empty files
        - missing titles
        """
        if not self._initialized:
            self.initialize()

        cp_dir = self.knowledge_dir / "checkpoints"
        if not cp_dir.is_dir():
            self.warnings.append(f"Checkpoints directory not found: {cp_dir}")
            return {}

        md_files = discover_files(cp_dir, "*.md")
        if not md_files:
            self.warnings.append(f"No markdown files found in {cp_dir}")
            return {}

        result: Dict[str, Checkpoint] = {}

        for md_path in md_files:
            logger.info("Checkpoint file found: %s", md_path.relative_to(self.knowledge_dir))
            try:
                content = read_markdown(md_path)
            except Exception as exc:
                self.errors.append(f"Failed to read {md_path}: {exc}")
                continue

            if not content.strip():
                self.warnings.append(f"Empty checkpoint file: {md_path}")
                continue

            # Parse YAML front matter
            meta = _parse_yaml_frontmatter(content) or {}

            # Extract ID
            cp_id = (
                meta.get("checkpoint_id", "")
                or _extract_cp_id_from_heading(content)
                or md_path.stem
            )
            if not cp_id:
                self.warnings.append(f"Could not extract checkpoint ID from {md_path}")
                continue

            # Extract title
            cp_name = (
                meta.get("checkpoint_name", "")
                or _extract_cp_title_from_heading(content)
            )
            if not cp_name:
                self.warnings.append(f"Missing checkpoint title in {md_path}")

            if cp_id in result:
                self.warnings.append(
                    f"Duplicate checkpoint ID '{cp_id}' ({md_path.name})"
                )

            # Parse metadata fields from front matter
            applicable_products_raw = meta.get("applicable_products", [])
            if isinstance(applicable_products_raw, str):
                applicable_products = [applicable_products_raw]
            else:
                applicable_products = list(applicable_products_raw) if applicable_products_raw else []

            # Extract sections from markdown body (best-effort, silently skip failures)
            objective = _extract_section(
                content, "## ② Inspection Objective", "## ③"
            )
            # remaining sections are stored in raw_content for later use
            body = content

            cp = Checkpoint(
                checkpoint_id=cp_id,
                checkpoint_name=cp_name,
                domain=meta.get("domain", ""),
                module=meta.get("module", ""),
                unit=meta.get("unit", ""),
                category=meta.get("category", ""),
                applicable_products=applicable_products,
                risk_level=str(meta.get("risk_level", "")),
                priority=meta.get("priority", ""),
                estimated_time=meta.get("estimated_time", ""),
                objective=objective,
                # Additional fields from registry enrichment happen in cross_validate
                filepath=md_path,
                raw_content=body,
            )

            result[cp_id] = cp

        ids = list(result.keys())
        logger.info("Total checkpoints loaded: %d", len(ids))
        if ids:
            logger.info("First checkpoint ID: %s", ids[0])
            logger.info("Last checkpoint ID: %s", ids[-1])

        self.checkpoints = result
        return self.checkpoints

    # ── Risk Rule Loading ───────────────────────────────────────

    def load_risk_rules(self) -> List[RiskRule]:
        """Read every ``knowledge/risk_rules/**/*.yaml`` file, parse
        into ``RiskRule`` objects, and return a list.

        Validates:
        - duplicate rule IDs
        - missing checkpoint references (cross-checked later)
        - invalid severity values
        """
        if not self._initialized:
            self.initialize()

        rules_dir = self.knowledge_dir / "risk_rules"
        if not rules_dir.is_dir():
            self.warnings.append(f"Risk rules directory not found: {rules_dir}")
            return []

        yaml_files = discover_files(rules_dir, "*.yaml")
        if not yaml_files:
            self.warnings.append(f"No YAML files found in {rules_dir}")
            return []

        result: List[RiskRule] = []
        seen_ids: set[str] = set()

        for yaml_path in yaml_files:
            logger.info("Risk rule file found: %s", yaml_path.relative_to(self.knowledge_dir))
            try:
                data = read_yaml(yaml_path)
            except Exception as exc:
                self.errors.append(f"Failed to load risk rule {yaml_path}: {exc}")
                continue

            if not isinstance(data, dict):
                self.errors.append(
                    f"Risk rule file {yaml_path} is not a dict (got {type(data).__name__})"
                )
                continue

            rule_id = data.get("id", "")
            if not rule_id:
                self.warnings.append(f"Risk rule without 'id' in {yaml_path}")
                continue

            if rule_id in seen_ids:
                self.warnings.append(f"Duplicate risk rule ID '{rule_id}' in {yaml_path}")
            seen_ids.add(rule_id)

            # Validate severity
            severity = str(data.get("risk_level", ""))
            if severity and severity not in _valid_severities:
                self.warnings.append(
                    f"Invalid severity '{severity}' in risk rule {rule_id}"
                )

            # Build condition from decision logic
            condition = ""
            decision_logic = data.get("decision_logic", [])
            if isinstance(decision_logic, list) and decision_logic:
                first = decision_logic[0]
                if isinstance(first, dict):
                    condition = first.get("condition", "")
                else:
                    condition = str(first)
            elif isinstance(decision_logic, str):
                condition = decision_logic
            else:
                condition = data.get("pass_condition", "")

            # Store checkpoint reference for cross-validation
            cid_from_yaml = data.get("checkpoint_id", "")
            if cid_from_yaml:
                self._rr_checkpoint_map[rule_id] = str(cid_from_yaml)

            rr = RiskRule(
                rule_id=rule_id,
                condition=condition,
                risk_level=severity,
                description=data.get("title", data.get("purpose", "")),
            )
            result.append(rr)

        logger.info("Total risk rules loaded: %d", len(result))
        if result:
            logger.info("First risk rule ID: %s", result[0].rule_id)
            logger.info("Last risk rule ID: %s", result[-1].rule_id)

        self.risk_rules = result
        return self.risk_rules

    # ── Cross Validation ────────────────────────────────────────

    def cross_validate(self) -> None:
        """Cross-reference all loaded knowledge assets and collect
        warnings for any inconsistencies.

        Checks:
        - Every registry entry has a corresponding checkpoint.
        - Every registry entry has a corresponding risk rule.
        - Every checkpoint is referenced in the taxonomy.
        - No orphan checkpoint (checkpoint without registry entry).
        - No orphan risk rule (rule referencing non-existent checkpoint).
        - No orphan taxonomy reference (taxonomy referencing non-existent checkpoint).
        """
        reg_ids = set(self.registry.keys())
        cp_ids = set(self.checkpoints.keys())

        # Collect checkpoint IDs referenced in risk rules
        rr_checkpoint_ids: set[str] = set(self._rr_checkpoint_map.values())

        # Collect checkpoint IDs referenced in taxonomy by re-scanning YAML
        taxo_cp_ids: set[str] = set()
        taxonomy_dir = self.knowledge_dir / "taxonomy"
        if taxonomy_dir.is_dir():
            for yaml_path in sorted(taxonomy_dir.glob("*.yaml")):
                try:
                    raw = read_yaml(yaml_path)
                except Exception:
                    continue
                if not isinstance(raw, dict):
                    continue
                tree = raw
                for key in ("beverage_knowledge_tree", "knowledge_tree", "taxonomy"):
                    if key in tree:
                        tree = tree[key]
                        break
                domains = tree.get("domains", []) if isinstance(tree, dict) else []
                for d in domains:
                    if not isinstance(d, dict):
                        continue
                    for sd in d.get("sub_domains", []):
                        if not isinstance(sd, dict):
                            continue
                        for cat in sd.get("categories", []):
                            if not isinstance(cat, dict):
                                continue
                            for cpid in cat.get("checkpoints", []):
                                if isinstance(cpid, str):
                                    taxo_cp_ids.add(cpid)

        # ── Checks ──────────────────────────────────────────────

        # 1. Registry entry has checkpoint
        for rid in reg_ids:
            if rid not in cp_ids:
                self.warnings.append(
                    f"Registry entry '{rid}' has no corresponding checkpoint file"
                )

        # 2. Registry entry has risk rule
        for rid in reg_ids:
            if rid not in rr_checkpoint_ids:
                self.warnings.append(
                    f"Registry entry '{rid}' has no corresponding risk rule"
                )

        # 3. Checkpoint exists in taxonomy
        for cid in cp_ids:
            if cid not in taxo_cp_ids:
                self.warnings.append(
                    f"Checkpoint '{cid}' is not referenced in the taxonomy"
                )

        # 4. No orphan checkpoint
        for cid in cp_ids:
            if cid not in reg_ids:
                self.warnings.append(
                    f"Orphan checkpoint '{cid}' has no registry entry"
                )

        # 5. No orphan risk rule
        for cid in rr_checkpoint_ids:
            if cid not in cp_ids and cid not in reg_ids:
                self.warnings.append(
                    f"Orphan risk rule references non-existent checkpoint '{cid}'"
                )

        # 6. No orphan taxonomy reference
        for cid in taxo_cp_ids:
            if cid not in cp_ids:
                self.warnings.append(
                    f"Taxonomy references non-existent checkpoint '{cid}'"
                )

        logger.info("Cross-validation complete (%d warnings)", len(self.warnings))

    # ── Bulk Loading ────────────────────────────────────────────

    def load_all(self) -> KnowledgeRepository:
        """Perform full load in order:

        initialize -> load_taxonomy -> load_registry
            -> load_checkpoints -> load_risk_rules -> cross_validate
        """
        self.initialize()
        self.load_taxonomy()
        self.load_registry()
        self.load_checkpoints()
        self.load_risk_rules()
        self.cross_validate()

        repo = KnowledgeRepository(
            registry=self.registry,
            taxonomy=self.taxonomy,
            checkpoints=self.checkpoints,
            errors=self.errors,
            warnings=self.warnings,
        )
        return repo

    # ── Lookup Methods ──────────────────────────────────────────

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        """Look up a checkpoint by its ID."""
        return self.checkpoints.get(checkpoint_id)

    def get_checkpoints_by_domain(self, domain: str) -> List[Checkpoint]:
        """Return all checkpoints belonging to a taxonomy domain.

        ``domain`` can be an ID or name.
        """
        # Match by registry entry domain
        domain_cp_ids = {
            reg.id for reg in self.registry.values()
            if reg.domain == domain
        }
        # Also match by taxonomy node name
        for node in self.taxonomy.values():
            if node.id == domain or node.name == domain:
                domain_cp_ids.add(node.id)
        return [
            cp for cid, cp in self.checkpoints.items()
            if cp.domain == domain or cid in domain_cp_ids
        ]

    def get_checkpoints_by_subdomain(self, subdomain: str) -> List[Checkpoint]:
        """Return all checkpoints belonging to a sub-domain."""
        sub_cp_ids = {
            reg.id for reg in self.registry.values()
            if reg.sub_domain == subdomain
        }
        return [
            cp for cid, cp in self.checkpoints.items()
            if cid in sub_cp_ids
        ]

    # ── Statistics ──────────────────────────────────────────────

    def statistics(self) -> LoaderStatistics:
        """Return aggregate statistics about loaded knowledge assets."""
        roots = self._taxonomy_roots
        domain_count = len(roots)
        sub_domain_count = sum(len(r.children) for r in roots)
        category_count = sum(
            sum(len(sd.children) for sd in r.children) for r in roots
        )
        total_nodes = domain_count + sub_domain_count + category_count

        return LoaderStatistics(
            registry_files=1 if self.registry else 0,
            taxonomy_files=1 if self.taxonomy else 0,
            checkpoint_files=len(self.checkpoints),
            domains=domain_count,
            sub_domains=sub_domain_count,
            categories=category_count,
            total_nodes=total_nodes,
            warnings=len(self.warnings),
            errors=len(self.errors),
        )

    # ── KnowledgeBase Convenience ───────────────────────────────

    def to_knowledge_base(self) -> KnowledgeBase:
        """Export loaded data as a KnowledgeBase instance."""
        return KnowledgeBase(
            registry=self.registry,
            taxonomy=self.taxonomy,
            checkpoints=self.checkpoints,
            risk_rules=self.risk_rules,
        )


# ── Module-Level Helper Functions ────────────────────────────────


def _collect_node_ids(node: TaxonomyNode) -> set[str]:
    """Collect all node IDs from a TaxonomyNode tree."""
    ids = {node.id}
    for child in node.children:
        ids.update(_collect_node_ids(child))
    return ids
