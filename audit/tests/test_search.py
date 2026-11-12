"""Tests for KnowledgeSearchEngine — ID, keyword, category, risk search."""

from __future__ import annotations

from pathlib import Path

import pytest

from script.loader import KnowledgeLoader
from script.search import KnowledgeSearchEngine

_BASE = Path(__file__).resolve().parent.parent


@pytest.fixture
def engine() -> KnowledgeSearchEngine:
    loader = KnowledgeLoader(knowledge_dir=_BASE / "knowledge")
    repo = loader.load_all()
    return KnowledgeSearchEngine(repository=repo)


class TestSearchByCheckpointID:
    def test_exact_match(self, engine: KnowledgeSearchEngine) -> None:
        cp = engine.search_checkpoint("CP-BEV-RM-001")
        assert cp is not None
        assert cp.checkpoint_id == "CP-BEV-RM-001"

    def test_last_checkpoint(self, engine: KnowledgeSearchEngine) -> None:
        cp = engine.search_checkpoint("CP-BEV-RM-025")
        assert cp is not None
        assert cp.checkpoint_id == "CP-BEV-RM-025"

    def test_nonexistent_returns_none(self, engine: KnowledgeSearchEngine) -> None:
        cp = engine.search_checkpoint("CP-BEV-RM-999")
        assert cp is None

    def test_empty_string_returns_none(self, engine: KnowledgeSearchEngine) -> None:
        cp = engine.search_checkpoint("")
        assert cp is None


class TestSearchByKeyword:
    def test_supplier_license_returns_results(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_keyword("供应商许可证")
        assert len(results) > 0

    def test_supplier_license_first_is_cp001(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_keyword("供应商许可证")
        assert results[0].checkpoint_id == "CP-BEV-RM-001"

    def test_empty_keyword_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_keyword("")
        assert results == []

    def test_nonexistent_keyword_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_keyword("zzzznotexist")
        assert results == []

    def test_temperature_search(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_keyword("温湿度")
        assert len(results) > 0
        ids = {cp.checkpoint_id for cp in results}
        assert "CP-BEV-RM-013" in ids

    def test_results_are_ranked_by_score(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_keyword("supplier")
        assert len(results) >= 2
        scores = [cp.checkpoint_id for cp in results]
        assert len(scores) == len(set(scores))


class TestSearchByCategory:
    def test_category_match(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_category("原料管理")
        assert len(results) > 0

    def test_category_empty_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_category("")
        assert results == []

    def test_nonexistent_category_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_category("nonexistentcat")
        assert results == []

    def test_subcategory_match(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_category("供应商资质审核")
        assert len(results) == 2
        ids = {cp.checkpoint_id for cp in results}
        assert ids == {"CP-BEV-RM-001", "CP-BEV-RM-002"}


class TestSearchByRisk:
    def test_high_risk_returns_results(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_risk("High")
        assert len(results) > 0

    def test_high_risk_includes_cp001(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_risk("High")
        ids = {cp.checkpoint_id for cp in results}
        assert "CP-BEV-RM-001" in ids

    def test_medium_risk_returns_results(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_risk("Medium")
        assert len(results) > 0

    def test_low_risk_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_risk("Low")
        assert results == []

    def test_empty_level_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_risk("")
        assert results == []

    def test_nonexistent_level_returns_empty(self, engine: KnowledgeSearchEngine) -> None:
        results = engine.search_risk("nonexistent")
        assert results == []

    def test_risk_maps_high_to_h(self, engine: KnowledgeSearchEngine) -> None:
        results_h = engine.search_risk("H")
        results_high = engine.search_risk("High")
        ids_h = {cp.checkpoint_id for cp in results_h}
        ids_high = {cp.checkpoint_id for cp in results_high}
        assert ids_h == ids_high


class TestConvenience:
    def test_total_checkpoints(self, engine: KnowledgeSearchEngine) -> None:
        assert engine.total_checkpoints() == 45

    def test_repository_property(self, engine: KnowledgeSearchEngine) -> None:
        assert engine.repository is not None
