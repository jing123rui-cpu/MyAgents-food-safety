"""Tests for InspectionWorkflow — context assembly pipeline."""

from __future__ import annotations

from pathlib import Path

import pytest

from script.loader import KnowledgeLoader
from script.search import KnowledgeSearchEngine
from script.workflow import InspectionRequest, InspectionWorkflow

_BASE = Path(__file__).resolve().parent.parent


@pytest.fixture
def workflow() -> InspectionWorkflow:
    loader = KnowledgeLoader(knowledge_dir=_BASE / "knowledge")
    repo = loader.load_all()
    search = KnowledgeSearchEngine(repository=repo)
    return InspectionWorkflow(repository=repo, search_engine=search, risk_rules=loader.risk_rules)


class TestContextByCheckpointID:
    def test_exact_id_returns_context(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-001")
        ctx = workflow.build_context(req)
        assert ctx is not None

    def test_exact_id_has_one_checkpoint(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-001")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) == 1

    def test_exact_id_has_registry(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-001")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_registry_entries) == 1
        assert ctx.matched_registry_entries[0].id == "CP-BEV-RM-001"

    def test_exact_id_has_taxonomy_nodes(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-001")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_taxonomy_nodes) >= 1

    def test_exact_id_has_risk_rule(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-001")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_risk_rules) >= 1

    def test_nonexistent_id_returns_no_results(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-999")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) == 0


class TestContextByKeyword:
    def test_keyword_returns_results(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(query="供应商许可证")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) > 0

    def test_keyword_has_registry_and_rules(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(query="供应商许可证")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_registry_entries) > 0
        assert len(ctx.matched_risk_rules) > 0

    def test_empty_query_no_results(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(query="")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) == 0


class TestContextByCategory:
    def test_category_returns_results(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(category="原料管理")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) > 0

    def test_nonexistent_category_returns_empty(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(category="nonexistent")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) == 0


class TestContextByRiskLevel:
    def test_high_risk_returns_results(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(risk_level="High")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) > 0

    def test_nonexistent_risk_returns_empty(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(risk_level="nonexistent")
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) == 0


class TestContextMetadata:
    def test_metadata_has_counts(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(query="供应商")
        ctx = workflow.build_context(req)
        assert "total_checkpoints" in ctx.metadata
        assert "total_registry_entries" in ctx.metadata
        assert "total_risk_rules" in ctx.metadata
        assert "total_taxonomy_nodes" in ctx.metadata

    def test_metadata_counts_match(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest(checkpoint_id="CP-BEV-RM-001")
        ctx = workflow.build_context(req)
        assert ctx.metadata["total_checkpoints"] == len(ctx.matched_checkpoints)
        assert ctx.metadata["total_registry_entries"] == len(ctx.matched_registry_entries)


class TestEmptyRequest:
    def test_empty_request_returns_empty(self, workflow: InspectionWorkflow) -> None:
        req = InspectionRequest()
        ctx = workflow.build_context(req)
        assert len(ctx.matched_checkpoints) == 0
