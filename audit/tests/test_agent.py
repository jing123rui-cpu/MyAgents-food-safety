"""Tests for FoodAuditAgent — initialize, health, inspect."""

from __future__ import annotations

from pathlib import Path

import pytest

from script.agent import FoodAuditAgent

_BASE = Path(__file__).resolve().parent.parent


@pytest.fixture
def agent() -> FoodAuditAgent:
    return FoodAuditAgent(knowledge_dir=str(_BASE / "knowledge"))


class TestInitialize:
    def test_initialize_returns_summary(self, agent: FoodAuditAgent) -> None:
        summary = agent.initialize()
        assert isinstance(summary, dict)

    def test_initialize_status_ready(self, agent: FoodAuditAgent) -> None:
        summary = agent.initialize()
        assert summary["status"] == "READY"

    def test_initialize_counts(self, agent: FoodAuditAgent) -> None:
        summary = agent.initialize()
        assert summary["registry"] == 45
        assert summary["checkpoints"] == 45
        assert summary["risk_rules"] == 45
        assert summary["taxonomy_nodes"] == 270
        assert summary["errors"] == 0

    def test_initialize_no_warnings(self, agent: FoodAuditAgent) -> None:
        summary = agent.initialize()
        assert summary["warnings"] == 0


class TestHealth:
    def test_health_returns_dict(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        status = agent.health()
        assert isinstance(status, dict)

    def test_health_ready(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        status = agent.health()
        assert status["status"] == "READY"

    def test_health_counts(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        status = agent.health()
        assert status["registry"] == 45
        assert status["checkpoints"] == 45
        assert status["risk_rules"] == 45
        assert status["taxonomy_nodes"] == 270
        assert status["errors"] == 0

    def test_health_before_init_returns_error(self, agent: FoodAuditAgent) -> None:
        status = agent.health()
        assert status["status"] == "ERROR"


class TestInspect:
    def test_inspect_by_id(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        ctx = agent.inspect(checkpoint_id="CP-BEV-RM-001")
        assert len(ctx.matched_checkpoints) == 1
        assert ctx.matched_checkpoints[0].checkpoint_id == "CP-BEV-RM-001"

    def test_inspect_by_query(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        ctx = agent.inspect(query="供应商许可证")
        assert len(ctx.matched_checkpoints) > 0

    def test_inspect_by_category(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        ctx = agent.inspect(category="原料管理")
        assert len(ctx.matched_checkpoints) > 0

    def test_inspect_by_risk(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        ctx = agent.inspect(risk_level="High")
        assert len(ctx.matched_checkpoints) > 0

    def test_inspect_with_evidence(self, agent: FoodAuditAgent) -> None:
        from script.models import Evidence, EvidenceType
        agent.initialize()
        ev = Evidence(
            id="EV-AGENT-01",
            evidence_type=EvidenceType.PHOTO,
            checkpoint_id="CP-BEV-RM-001",
            description="许可证齐全",
            attachments=["lic.pdf"],
        )
        ctx = agent.inspect(checkpoint_id="CP-BEV-RM-001", evidence=[ev])
        assert len(ctx.evidence) == 1
        assert len(ctx.evaluation_results) == 1

    def test_inspect_no_criteria_returns_empty(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        ctx = agent.inspect()
        assert len(ctx.matched_checkpoints) == 0

    def test_inspect_before_init_raises(self, agent: FoodAuditAgent) -> None:
        with pytest.raises(RuntimeError):
            agent.inspect(query="test")
