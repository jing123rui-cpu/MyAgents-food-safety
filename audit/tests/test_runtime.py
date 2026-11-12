"""Integration test — full pipeline: Agent → Loader → Search → Workflow → Evidence → RuleEngine."""

from __future__ import annotations

from pathlib import Path

import pytest

from script import FoodAuditAgent
from script.models import Evidence, EvidenceType, EvaluationStatus

_BASE = Path(__file__).resolve().parent.parent


@pytest.fixture
def agent() -> FoodAuditAgent:
    return FoodAuditAgent(knowledge_dir=str(_BASE / "knowledge"))


class TestFullPipeline:
    def test_full_pipeline_passes(self, agent: FoodAuditAgent) -> None:
        summary = agent.initialize()
        assert summary["status"] == "READY"

        ctx = agent.inspect(query="供应商许可证")
        assert len(ctx.matched_checkpoints) >= 1
        assert len(ctx.matched_registry_entries) >= 1
        assert len(ctx.matched_taxonomy_nodes) >= 1
        assert len(ctx.matched_risk_rules) >= 1

        ev = Evidence(
            id="EV-INT-001",
            evidence_type=EvidenceType.OBSERVATION,
            checkpoint_id="CP-BEV-RM-001",
            description="供应商许可证齐全有效，品种范围覆盖",
            attachments=["许可证复印件.pdf"],
        )
        ctx2 = agent.inspect(query="供应商许可证", evidence=[ev])
        assert len(ctx2.evidence) == 1
        assert len(ctx2.evaluation_results) == 1
        assert ctx2.evaluation_results[0].status == EvaluationStatus.COMPLIANT
        assert ctx2.evaluation_results[0].score == 1.0

    def test_full_pipeline_with_non_compliant(self, agent: FoodAuditAgent) -> None:
        agent.initialize()

        ev = Evidence(
            id="EV-INT-010",
            evidence_type=EvidenceType.DOCUMENT,
            checkpoint_id="CP-BEV-RM-008",
            description="",
            attachments=[],
        )
        ctx = agent.inspect(query="感官验收", evidence=[ev])

        assert len(ctx.evidence) == 1
        assert len(ctx.evaluation_results) == 1
        result = ctx.evaluation_results[0]
        assert result.status == EvaluationStatus.NON_COMPLIANT
        assert result.score == 0.0

    def test_full_pipeline_with_non_compliant_attachments(self, agent: FoodAuditAgent) -> None:
        agent.initialize()

        ev = Evidence(
            id="EV-INT-020",
            evidence_type=EvidenceType.PHOTO,
            checkpoint_id="CP-BEV-RM-001",
            description="供应商许可证已过期",
            attachments=[],
        )
        ctx = agent.inspect(query="供应商许可证", evidence=[ev])

        assert len(ctx.evaluation_results) == 1
        result = ctx.evaluation_results[0]
        assert result.status == EvaluationStatus.NON_COMPLIANT
        assert result.score == 0.0

    def test_full_pipeline_multiple_evidence(self, agent: FoodAuditAgent) -> None:
        agent.initialize()

        evs = [
            Evidence(
                id="EV-M-01", evidence_type=EvidenceType.PHOTO,
                checkpoint_id="CP-BEV-RM-001",
                description="许可证复印件", attachments=["lic.pdf"],
            ),
            Evidence(
                id="EV-M-02", evidence_type=EvidenceType.DOCUMENT,
                checkpoint_id="CP-BEV-RM-006",
                description="进货查验记录完整", attachments=["rec.pdf"],
            ),
            Evidence(
                id="EV-M-03", evidence_type=EvidenceType.DOCUMENT,
                checkpoint_id="CP-BEV-RM-013",
                description="", attachments=[],
            ),
        ]
        ctx = agent.inspect(query="原料", evidence=evs)

        assert len(ctx.evidence) == 3
        assert len(ctx.evaluation_results) == 3

        statuses = {r.status for r in ctx.evaluation_results}
        assert EvaluationStatus.COMPLIANT in statuses
        assert EvaluationStatus.NON_COMPLIANT in statuses

    def test_full_pipeline_no_matches(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        ctx = agent.inspect(query="zzzznotexist")
        assert len(ctx.matched_checkpoints) == 0

    def test_full_pipeline_health_check(self, agent: FoodAuditAgent) -> None:
        agent.initialize()
        h = agent.health()
        assert h["status"] == "READY"
        assert h["registry"] == 45
        assert h["checkpoints"] == 45
        assert h["risk_rules"] == 45
