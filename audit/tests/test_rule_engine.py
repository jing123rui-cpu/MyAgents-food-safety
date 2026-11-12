"""Tests for RuleEngine — COMPLIANT, NON_COMPLIANT, NOT_APPLICABLE."""

from __future__ import annotations

from pathlib import Path

import pytest

from script.loader import KnowledgeLoader
from script.models import Evidence, EvidenceType, EvaluationStatus
from script.rule_engine import RuleEngine
from script.search import KnowledgeSearchEngine

_BASE = Path(__file__).resolve().parent.parent


@pytest.fixture
def rule_engine() -> RuleEngine:
    loader = KnowledgeLoader(knowledge_dir=_BASE / "knowledge")
    repo = loader.load_all()
    return RuleEngine(repository=repo, risk_rules=loader.risk_rules)


class TestEvaluateCompliant:
    def test_complete_evidence_returns_compliant(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-001",
            evidence_type=EvidenceType.OBSERVATION,
            checkpoint_id="CP-BEV-RM-001",
            description="供应商许可证齐全有效，品种范围覆盖",
            attachments=["许可证复印件.pdf"],
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.COMPLIANT
        assert result.score == 1.0

    def test_compliant_has_reason(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-002",
            evidence_type=EvidenceType.PHOTO,
            checkpoint_id="CP-BEV-RM-002",
            description="产品检验报告已提供，数据达标",
            attachments=["COA报告.pdf"],
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.COMPLIANT
        assert result.reason is not None


class TestEvaluateNonCompliant:
    def test_empty_description_returns_non_compliant(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-010",
            evidence_type=EvidenceType.DOCUMENT,
            checkpoint_id="CP-BEV-RM-003",
            description="",
            attachments=[],
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.NON_COMPLIANT
        assert result.score == 0.0

    def test_non_compliant_has_recommendation(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-011",
            evidence_type=EvidenceType.DOCUMENT,
            checkpoint_id="CP-BEV-RM-003",
            description="",
            attachments=[],
        )
        result = rule_engine.evaluate(ev)
        assert result.recommendation
        assert "为空" in result.reason or "empty" in result.reason.lower()


class TestEvaluateNonCompliantAttachments:
    def test_high_no_attachments_returns_non_compliant(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-020",
            evidence_type=EvidenceType.OBSERVATION,
            checkpoint_id="CP-BEV-RM-001",
            description="供应商许可证待补充",
            attachments=[],
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.NON_COMPLIANT
        assert result.score == 0.0

    def test_critical_no_attachments_returns_non_compliant(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-021",
            evidence_type=EvidenceType.PHOTO,
            checkpoint_id="CP-BEV-RM-014",
            description="挡鼠板已安装",
            attachments=[],
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.NON_COMPLIANT
        assert result.score == 0.0

    def test_non_compliant_lists_violated_laws(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-022",
            evidence_type=EvidenceType.DOCUMENT,
            checkpoint_id="CP-BEV-RM-001",
            description="缺少许可证",
            attachments=[],
        )
        result = rule_engine.evaluate(ev)
        assert len(result.violated_laws) > 0


class TestEvaluateNotApplicable:
    def test_unknown_checkpoint_returns_na(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-030",
            evidence_type=EvidenceType.OBSERVATION,
            checkpoint_id="CP-BEV-RM-999",
            description="不存在",
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.NOT_APPLICABLE
        assert result.score == 0.0

    def test_na_with_no_rule_returns_na(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(
            id="EV-TEST-031",
            evidence_type=EvidenceType.DOCUMENT,
            checkpoint_id="",
            description="empty checkpoint",
        )
        result = rule_engine.evaluate(ev)
        assert result.status == EvaluationStatus.NOT_APPLICABLE


class TestEvaluateAll:
    def test_all_returns_list(self, rule_engine: RuleEngine) -> None:
        ev_list = [
            Evidence(id="EV-A", evidence_type=EvidenceType.PHOTO, checkpoint_id="CP-BEV-RM-001",
                     description="OK", attachments=["a.jpg"]),
            Evidence(id="EV-B", evidence_type=EvidenceType.DOCUMENT, checkpoint_id="CP-BEV-RM-003",
                     description="", attachments=[]),
        ]
        results = rule_engine.evaluate_all(ev_list)
        assert len(results) == 2

    def test_all_clears_warnings(self, rule_engine: RuleEngine) -> None:
        ev_list = [
            Evidence(id="EV-C", evidence_type=EvidenceType.PHOTO, checkpoint_id="CP-BEV-RM-001",
                     description="OK", attachments=["a.jpg"]),
        ]
        rule_engine.evaluate_all(ev_list)
        assert len(rule_engine.warnings) == 0


class TestScoring:
    def test_compliant_scores_1(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(id="EV-SCORE-01", evidence_type=EvidenceType.OBSERVATION,
                      checkpoint_id="CP-BEV-RM-005",
                      description="合格供应商名录已更新",
                      attachments=["名录.pdf"])
        result = rule_engine.evaluate(ev)
        assert result.score == 1.0

    def test_non_compliant_scores_0(self, rule_engine: RuleEngine) -> None:
        ev = Evidence(id="EV-SCORE-02", evidence_type=EvidenceType.OBSERVATION,
                      checkpoint_id="CP-BEV-RM-001",
                      description="缺少许可证附件",
                      attachments=[])
        result = rule_engine.evaluate(ev)
        assert result.score == 0.0
