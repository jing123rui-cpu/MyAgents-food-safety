"""Tests for KnowledgeLoader — taxonomy, registry, checkpoint, risk rule loading."""

from __future__ import annotations

from pathlib import Path

import pytest

from script.loader import KnowledgeLoader
from script.models import Checkpoint, KnowledgeRepository, RegistryEntry, RiskRule, TaxonomyNode

_BASE = Path(__file__).resolve().parent.parent


@pytest.fixture
def loader() -> KnowledgeLoader:
    return KnowledgeLoader(knowledge_dir=_BASE / "knowledge")


class TestTaxonomyLoading:
    def test_returns_dict(self, loader: KnowledgeLoader) -> None:
        result = loader.load_taxonomy()
        assert isinstance(result, dict)

    def test_has_270_nodes(self, loader: KnowledgeLoader) -> None:
        result = loader.load_taxonomy()
        assert len(result) == 270

    def test_contains_raw_material_management(self, loader: KnowledgeLoader) -> None:
        result = loader.load_taxonomy()
        assert "raw_material_management" in result

    def test_nodes_are_taxonomynode(self, loader: KnowledgeLoader) -> None:
        result = loader.load_taxonomy()
        for node in result.values():
            assert isinstance(node, TaxonomyNode)

    def test_raw_material_has_children(self, loader: KnowledgeLoader) -> None:
        result = loader.load_taxonomy()
        node = result["raw_material_management"]
        assert len(node.children) == 5

    def test_no_errors(self, loader: KnowledgeLoader) -> None:
        loader.load_taxonomy()
        assert len(loader.errors) == 0, f"Errors: {loader.errors}"


class TestRegistryLoading:
    def test_returns_dict(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        assert isinstance(result, dict)

    def test_has_45_entries(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        assert len(result) == 45

    def test_all_ids_start_with_valid_prefix(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        for cp_id in result:
            valid = cp_id.startswith("CP-BEV-RM-") or cp_id.startswith("CP-BEV-PP-")
            assert valid, f"Unexpected ID: {cp_id}"

    def test_entries_are_registryentry(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        for entry in result.values():
            assert isinstance(entry, RegistryEntry)

    def test_required_fields(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        for entry in result.values():
            assert entry.id
            assert entry.title
            assert entry.domain
            assert entry.category

    def test_first_and_last(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        assert result["CP-BEV-RM-001"].title == "供应商生产许可证审查"
        assert result["CP-BEV-RM-025"].title == "添加剂GB2760符合性抽查"

    def test_no_duplicates(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        assert len(result) == len(set(result))

    def test_cp001_risk_high(self, loader: KnowledgeLoader) -> None:
        result = loader.load_registry()
        assert result["CP-BEV-RM-001"].risk_level == "High"

    def test_no_errors(self, loader: KnowledgeLoader) -> None:
        loader.load_registry()
        assert len(loader.errors) == 0, f"Errors: {loader.errors}"


class TestCheckpointLoading:
    def test_returns_dict(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        assert isinstance(result, dict)

    def test_has_45_checkpoints(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        assert len(result) == 45

    def test_checkpoints_are_checkpoint(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        for cp in result.values():
            assert isinstance(cp, Checkpoint)

    def test_cp001_metadata(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        cp = result["CP-BEV-RM-001"]
        assert cp.checkpoint_name == "供应商生产许可证审查"
        assert cp.risk_level == "H"
        assert cp.priority == "P0"

    def test_cp025_metadata(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        cp = result["CP-BEV-RM-025"]
        assert cp.checkpoint_name == "添加剂GB2760符合性抽查"
        assert cp.risk_level == "H"

    def test_every_checkpoint_has_title(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        for cp in result.values():
            assert cp.checkpoint_name, f"Missing title for {cp.checkpoint_id}"

    def test_every_checkpoint_has_content(self, loader: KnowledgeLoader) -> None:
        result = loader.load_checkpoints()
        for cp in result.values():
            assert cp.raw_content, f"Empty content for {cp.checkpoint_id}"

    def test_no_errors(self, loader: KnowledgeLoader) -> None:
        loader.load_checkpoints()
        assert len(loader.errors) == 0, f"Errors: {loader.errors}"


class TestRiskRuleLoading:
    def test_returns_list(self, loader: KnowledgeLoader) -> None:
        result = loader.load_risk_rules()
        assert isinstance(result, list)

    def test_has_45_rules(self, loader: KnowledgeLoader) -> None:
        result = loader.load_risk_rules()
        assert len(result) == 45

    def test_rules_are_riskrule(self, loader: KnowledgeLoader) -> None:
        result = loader.load_risk_rules()
        for rule in result:
            assert isinstance(rule, RiskRule)

    def test_rule_ids(self, loader: KnowledgeLoader) -> None:
        result = loader.load_risk_rules()
        ids = {r.rule_id for r in result}
        assert "RR-CP-BEV-RM-001" in ids
        assert "RR-CP-BEV-RM-025" in ids
        assert "RR-CP-BEV-PP-001" in ids
        assert "RR-CP-BEV-PP-020" in ids

    def test_no_duplicate_ids(self, loader: KnowledgeLoader) -> None:
        result = loader.load_risk_rules()
        ids = [r.rule_id for r in result]
        assert len(ids) == len(set(ids))

    def test_no_errors(self, loader: KnowledgeLoader) -> None:
        loader.load_risk_rules()
        assert len(loader.errors) == 0, f"Errors: {loader.errors}"


class TestCrossValidation:
    def test_cross_validate_no_warnings(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        assert len(loader.warnings) == 0, f"Warnings: {loader.warnings}"

    def test_cross_validate_no_errors(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        assert len(loader.errors) == 0, f"Errors: {loader.errors}"


class TestLoadAll:
    def test_returns_knowledge_repository(self, loader: KnowledgeLoader) -> None:
        repo = loader.load_all()
        assert isinstance(repo, KnowledgeRepository)

    def test_has_45_checkpoints(self, loader: KnowledgeLoader) -> None:
        repo = loader.load_all()
        assert len(repo.checkpoints) == 45

    def test_has_45_registry_entries(self, loader: KnowledgeLoader) -> None:
        repo = loader.load_all()
        assert len(repo.registry) == 45

    def test_has_270_taxonomy_nodes(self, loader: KnowledgeLoader) -> None:
        repo = loader.load_all()
        assert len(repo.taxonomy) == 270

    def test_every_checkpoint_in_registry(self, loader: KnowledgeLoader) -> None:
        repo = loader.load_all()
        for cp_id in repo.checkpoints:
            assert cp_id in repo.registry, f"{cp_id} not in registry"

    def test_every_registry_has_checkpoint(self, loader: KnowledgeLoader) -> None:
        repo = loader.load_all()
        for cp_id in repo.registry:
            assert cp_id in repo.checkpoints, f"{cp_id} not loaded as checkpoint"

    def test_no_errors(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        assert len(loader.errors) == 0, f"Errors: {loader.errors}"


class TestLookups:
    def test_get_checkpoint_by_id(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        cp = loader.get_checkpoint("CP-BEV-RM-003")
        assert cp is not None
        assert cp.checkpoint_id == "CP-BEV-RM-003"

    def test_get_checkpoint_nonexistent(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        cp = loader.get_checkpoint("CP-BEV-RM-999")
        assert cp is None

    def test_get_checkpoints_by_domain_returns_all(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        cps = loader.get_checkpoints_by_domain("raw_material_management")
        assert len(cps) == 25

    def test_get_checkpoints_by_subdomain(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        cps = loader.get_checkpoints_by_subdomain("supplier_management")
        assert len(cps) == 5

    def test_get_checkpoints_by_subdomain_nonexistent(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        cps = loader.get_checkpoints_by_subdomain("nonexistent")
        assert cps == []


class TestStatistics:
    def test_statistics(self, loader: KnowledgeLoader) -> None:
        loader.load_all()
        stats = loader.statistics()
        assert stats.registry_files == 1
        assert stats.taxonomy_files == 1
        assert stats.checkpoint_files == 45
        assert stats.domains == 17
        assert stats.sub_domains == 68
        assert stats.categories == 185
        assert stats.total_nodes == 270
        assert stats.errors == 0


class TestErrorHandling:
    def test_nonexistent_directory(self) -> None:
        ldr = KnowledgeLoader(knowledge_dir=Path("/nonexistent/knowledge"))
        ldr.initialize()
        assert len(ldr.errors) > 0
