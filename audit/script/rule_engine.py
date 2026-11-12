"""Rule Engine — evaluate evidence against risk rules deterministically.

No AI reasoning, no LLM, no prompt generation.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .models import (
    Checkpoint,
    EvaluationResult,
    EvaluationStatus,
    Evidence,
    KnowledgeRepository,
    RiskRule,
)

logger = logging.getLogger(__name__)

# Severity thresholds for deterministic scoring
# Critical/High require attachments; Medium/Low also require them for compliance
_SEVERITY_REQUIRE_ATTACHMENT = {"Critical", "High", "Medium", "Moderate"}


class RuleEngine:
    """Deterministic rule evaluation engine.

    Evaluates inspection evidence against risk rules and produces
    structured ``EvaluationResult`` objects.
    """

    def __init__(
        self,
        repository: KnowledgeRepository,
        risk_rules: Optional[List[RiskRule]] = None,
    ) -> None:
        self._repo = repository
        self._risk_rules = risk_rules or []
        self._warnings: List[str] = []

        # Index: checkpoint_id -> RiskRule
        self._cp_to_rules: Dict[str, List[RiskRule]] = {}
        self._build_rule_index()

    # ── Public API ──────────────────────────────────────────────

    def evaluate(self, evidence: Evidence) -> EvaluationResult:
        """Evaluate a single evidence item against its matching risk rule.

        Pipeline
        --------
        1. Locate checkpoint (via evidence.checkpoint_id)
        2. Locate risk rule (via checkpoint ID index)
        3. Validate applicability
        4. Execute deterministic rule logic
        5. Return EvaluationResult
        """
        cp_id = evidence.checkpoint_id

        # 1. Locate checkpoint
        checkpoint = self._repo.checkpoints.get(cp_id)
        if checkpoint is None:
            self._warnings.append(f"Evidence '{evidence.id}' references unknown checkpoint '{cp_id}'")
            return EvaluationResult(
                checkpoint_id=cp_id,
                rule_id="",
                evidence_id=evidence.id,
                status=EvaluationStatus.NOT_APPLICABLE,
                score=0.0,
                reason=f"Unknown checkpoint '{cp_id}'",
            )

        # 2. Locate risk rule
        rules = self._cp_to_rules.get(cp_id, [])
        if not rules:
            self._warnings.append(f"No risk rule found for checkpoint '{cp_id}'")
            return EvaluationResult(
                checkpoint_id=cp_id,
                rule_id="",
                evidence_id=evidence.id,
                status=EvaluationStatus.NOT_APPLICABLE,
                score=0.0,
                reason=f"No risk rule for checkpoint '{cp_id}'",
            )

        # 3. Execute deterministic rule logic
        # Use the first matching rule (most specific)
        rule = rules[0]
        return self._apply_rule(rule, evidence, checkpoint)

    def evaluate_all(
        self,
        evidence_list: List[Evidence],
    ) -> List[EvaluationResult]:
        """Evaluate every evidence item and return one result per item.

        Also resets the internal warning list.
        """
        self._warnings.clear()
        return [self.evaluate(ev) for ev in evidence_list]

    @property
    def warnings(self) -> List[str]:
        """Warnings collected during the last ``evaluate_all`` call."""
        return list(self._warnings)

    # ── Deterministic Rule Logic ────────────────────────────────

    def _apply_rule(
        self,
        rule: RiskRule,
        evidence: Evidence,
        checkpoint: Checkpoint,
    ) -> EvaluationResult:
        """Execute deterministic evaluation logic for *evidence* against *rule*.

        Regulatory logic (aligned with food safety inspection practice)
        ----------------------------------------------------------------
        - If evidence has no description → NON_COMPLIANT
        - If evidence has no attachments and rule requires them → NON_COMPLIANT
        - If all requirements satisfied → COMPLIANT
        """
        severity = rule.risk_level

        # Collect violated laws from registry
        reg = self._repo.registry.get(checkpoint.checkpoint_id)
        violated_laws = list(reg.laws) if reg else []

        # Empty description → NON_COMPLIANT
        if not evidence.description.strip():
            return EvaluationResult(
                checkpoint_id=checkpoint.checkpoint_id,
                rule_id=rule.rule_id,
                evidence_id=evidence.id,
                status=EvaluationStatus.NON_COMPLIANT,
                score=0.0,
                reason=f"Checkpoint '{rule.rule_id}' — 证据描述为空 (evidence description is empty)",
                violated_laws=violated_laws,
                recommendation="提供详细的观察描述记录 (provide a detailed observation description)",
            )

        # Missing attachments when severity requires them → NON_COMPLIANT
        has_attachments = bool(evidence.attachments)
        if severity in _SEVERITY_REQUIRE_ATTACHMENT and not has_attachments:
            return EvaluationResult(
                checkpoint_id=checkpoint.checkpoint_id,
                rule_id=rule.rule_id,
                evidence_id=evidence.id,
                status=EvaluationStatus.NON_COMPLIANT,
                score=0.0,
                reason=f"检查点 '{rule.rule_id}' 需要附证材料但未提供",
                violated_laws=violated_laws,
                recommendation="上传相关照片或证明文件作为附件",
            )

        # COMPLIANT — all checks satisfied
        return EvaluationResult(
            checkpoint_id=checkpoint.checkpoint_id,
            rule_id=rule.rule_id,
            evidence_id=evidence.id,
            status=EvaluationStatus.COMPLIANT,
            score=1.0,
            reason=f"检查点 '{rule.rule_id}' — 证据完整，符合要求",
            violated_laws=violated_laws,
            recommendation=rule.description,
        )

    # ── Index Builders ──────────────────────────────────────────

    def _build_rule_index(self) -> None:
        """Build ``checkpoint_id -> [RiskRule, ...]`` from risk rules.

        Derives the mapping from the ``RR-{checkpoint_id}`` naming
        convention in the rule ID.
        """
        for rule in self._risk_rules:
            if rule.rule_id.startswith("RR-"):
                cp_id = rule.rule_id[3:]  # "RR-CP-..." -> "CP-..."
                self._cp_to_rules.setdefault(cp_id, []).append(rule)

        # Also match by exact rule_id pattern
        for cp_id in self._repo.checkpoints:
            expected_rid = f"RR-{cp_id}"
            for rule in self._risk_rules:
                if rule.rule_id == expected_rid:
                    if rule not in self._cp_to_rules.setdefault(cp_id, []):
                        self._cp_to_rules[cp_id].append(rule)
