"""FoodAuditAgent — runtime orchestrator for the food safety audit system.

Coordinates KnowledgeLoader, KnowledgeSearchEngine, InspectionWorkflow,
and RuleEngine into a single executable agent.
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any, Dict, List, Optional

from .ai import DeepSeekProvider, ProviderManager
from .ai.inspection_pipeline import AIInspectionResult, InspectionPipeline
from .evidence import validate_evidence
from .loader import KnowledgeLoader
from .models import EnterpriseEvaluation, Evidence, EvaluationStatus, KnowledgeRepository
from .rule_engine import RuleEngine
from .search import KnowledgeSearchEngine
from .workflow import InspectionContext, InspectionRequest, InspectionWorkflow

logger = logging.getLogger(__name__)


class FoodAuditAgent:
    """Main runtime agent that coordinates all subsystems.

    Usage
    -----
    agent = FoodAuditAgent("knowledge")
    agent.initialize()
    ctx = agent.inspect(query="supplier", evidence=[...])
    status = agent.health()
    """

    def __init__(self, knowledge_dir: str = "knowledge", provider_manager: Optional[ProviderManager] = None) -> None:
        self._knowledge_dir = Path(knowledge_dir)
        self._loader: Optional[KnowledgeLoader] = None
        self._repo: Optional[KnowledgeRepository] = None
        self._search: Optional[KnowledgeSearchEngine] = None
        self._workflow: Optional[InspectionWorkflow] = None
        self._rule_engine: Optional[RuleEngine] = None
        self._ai_manager: ProviderManager = provider_manager or ProviderManager()
        self._ready = False

    # ── Startup ─────────────────────────────────────────────────

    def initialize(self) -> Dict[str, Any]:
        """Load all knowledge, build search index, initialise workflow and rule engine.

        Returns a startup summary dict.
        """
        logger.info("FoodAuditAgent initialising from %s", self._knowledge_dir)

        # 1. Load all knowledge
        self._loader = KnowledgeLoader(self._knowledge_dir)
        self._repo = self._loader.load_all()

        if self._repo.errors:
            logger.error("Loader reported %d error(s)", len(self._repo.errors))
            for err in self._repo.errors:
                logger.error("  %s", err)

        # 2. Build search engine
        self._search = KnowledgeSearchEngine(self._repo)

        # 3. Build workflow engine
        self._workflow = InspectionWorkflow(
            repository=self._repo,
            search_engine=self._search,
            risk_rules=self._loader.risk_rules,
        )

        # 4. Build rule engine
        self._rule_engine = RuleEngine(
            repository=self._repo,
            risk_rules=self._loader.risk_rules,
        )

        # 5. Initialise AI Provider (optional — does not block startup)
        try:
            self._ai_manager.register("deepseek", DeepSeekProvider)
            self._ai_manager.initialize_provider("deepseek")
            logger.info("DeepSeek AI provider initialised successfully")
        except Exception as exc:
            logger.warning("DeepSeek AI provider not available: %s", exc)

        self._ready = True

        # Startup summary
        registry_count = len(self._repo.registry)
        checkpoint_count = len(self._repo.checkpoints)
        taxonomy_count = len(self._repo.taxonomy)
        rule_count = len(self._loader.risk_rules)
        warn_count = len(self._repo.warnings)
        err_count = len(self._repo.errors)
        status = "READY" if self._ready and not err_count else "ERROR"

        summary = {
            "status": status,
            "registry": registry_count,
            "checkpoints": checkpoint_count,
            "risk_rules": rule_count,
            "taxonomy_nodes": taxonomy_count,
            "warnings": warn_count,
            "errors": err_count,
        }

        logger.info(
            "Agent status: %s | Registry: %d | Checkpoints: %d | "
            "Risk Rules: %d | Taxonomy: %d | Warnings: %d | Errors: %d",
            status, registry_count, checkpoint_count, rule_count,
            taxonomy_count, warn_count, err_count,
        )
        return summary

    # ── Inspection ──────────────────────────────────────────────

    def inspect(
        self,
        query: str = "",
        checkpoint_id: str = "",
        category: str = "",
        risk_level: str = "",
        evidence: Optional[List[Evidence]] = None,
    ) -> InspectionContext:
        """Run a full inspection pipeline.

        Parameters
        ----------
        query
            Keyword search across titles, keywords, and markdown body.
        checkpoint_id
            Exact checkpoint ID lookup.
        category
            Category or subcategory name.
        risk_level
            Risk level filter (High, Medium, Low, etc.).
        evidence
            Optional list of evidence items to validate and evaluate.

        Returns
        -------
        InspectionContext
            Assembled context with matched knowledge, evidence, and
            evaluation results.
        """
        self._require_ready()

        # 1. Build the workflow context
        request = InspectionRequest(
            query=query,
            checkpoint_id=checkpoint_id,
            category=category,
            risk_level=risk_level,
        )
        ctx = self._workflow.build_context(request)

        # 2. Attach and validate evidence
        evidence = evidence or []
        if evidence:
            ctx.evidence = evidence
            ev_warnings = validate_evidence(evidence, repository=self._repo)
            ctx.warnings.extend(ev_warnings)

            # 3. Evaluate evidence against risk rules
            results = self._rule_engine.evaluate_all(evidence)
            ctx.evaluation_results = results
            ctx.warnings.extend(self._rule_engine.warnings)

            # Update metadata
            ctx.metadata["total_evidence"] = len(evidence)
            ctx.metadata["total_evaluation_results"] = len(results)
            ctx.metadata["warnings_count"] = len(ctx.warnings)

        # 4. Compute enterprise-level evaluation
        enterprise = self._compute_enterprise_evaluation(ctx)
        ctx.metadata["enterprise_evaluation"] = enterprise

        logger.info(
            "Inspect complete: %d checkpoints, %d evidence, %d evaluations | %s",
            len(ctx.matched_checkpoints),
            len(ctx.evidence),
            len(ctx.evaluation_results),
            enterprise.overall_result,
        )
        return ctx

    # ── AI Inspection ──────────────────────────────────────────

    def inspect_ai(
        self,
        query: str = "",
        checkpoint_id: str = "",
        category: str = "",
        risk_level: str = "",
    ) -> AIInspectionResult:
        """Run the full AI inspection pipeline.

        Internally calls ``InspectionPipeline.run()`` which orchestrates
        workflow, context engine, prompt engine, and the AI provider.

        Parameters
        ----------
        query
            Keyword search query.
        checkpoint_id
            Exact checkpoint ID lookup.
        category
            Category or subcategory name.
        risk_level
            Risk level filter.

        Returns
        -------
        AIInspectionResult
            Combined result with context, prompt, and AI response.
        """
        self._require_ready()

        provider = self._ai_manager.get_provider("deepseek")
        pipeline = InspectionPipeline(
            workflow=self._workflow,
            repository=self._repo,
            provider=provider,
        )
        request = InspectionRequest(
            query=query,
            checkpoint_id=checkpoint_id,
            category=category,
            risk_level=risk_level,
        )
        return pipeline.run(request)

    # ── Health ──────────────────────────────────────────────────

    def health(self) -> Dict[str, Any]:
        """Return agent health status with component counts."""
        if not self._ready or self._repo is None:
            return {"status": "ERROR", "message": "Agent not initialised"}

        registry_count = len(self._repo.registry)
        checkpoint_count = len(self._repo.checkpoints)
        taxonomy_count = len(self._repo.taxonomy)
        rule_count = len(self._loader.risk_rules) if self._loader else 0
        warn_count = len(self._repo.warnings)
        err_count = len(self._repo.errors)

        overall = "READY" if self._ready and not err_count else "ERROR"

        ai_providers = self._ai_manager.list_providers()
        ai_status = "AVAILABLE" if self._ai_manager.get_provider() else "UNAVAILABLE"

        return {
            "status": overall,
            "registry": registry_count,
            "checkpoints": checkpoint_count,
            "risk_rules": rule_count,
            "taxonomy_nodes": taxonomy_count,
            "warnings": warn_count,
            "errors": err_count,
            "ai_providers": ai_providers,
            "ai_status": ai_status,
        }

    # ── Enterprise Evaluation ────────────────────────────────────

    @staticmethod
    def _compute_enterprise_evaluation(ctx: InspectionContext) -> EnterpriseEvaluation:
        """Aggregate evaluation results into an enterprise-level decision.

        Decision logic
        --------------
        If non_compliant_count == 0:
            overall_result = "企业通过检查"
        Else:
            overall_result = "企业需要整改"
        """
        total = len(ctx.evaluation_results)
        compliant = sum(1 for r in ctx.evaluation_results if r.status == EvaluationStatus.COMPLIANT)
        non_compliant = sum(1 for r in ctx.evaluation_results if r.status == EvaluationStatus.NON_COMPLIANT)
        na = sum(1 for r in ctx.evaluation_results if r.status == EvaluationStatus.NOT_APPLICABLE)

        overall = "企业通过检查" if non_compliant == 0 else "企业需要整改"

        summary_parts = [
            f"本次检查共评估 {total} 个检查项。",
            f"合格项：{compliant} 项",
        ]
        if non_compliant:
            summary_parts.append(f"不合格项：{non_compliant} 项")
        if na:
            summary_parts.append(f"不适用项：{na} 项")
        summary_parts.append(f"综合结论：{overall}")

        return EnterpriseEvaluation(
            total_checkpoints=total,
            compliant_count=compliant,
            non_compliant_count=non_compliant,
            not_applicable_count=na,
            overall_result=overall,
            summary="；".join(summary_parts),
        )

    # ── Internals ───────────────────────────────────────────────

    def _require_ready(self) -> None:
        """Raise ``RuntimeError`` if the agent has not been initialised."""
        if not self._ready:
            raise RuntimeError(
                "FoodAuditAgent not initialised. Call .initialize() first."
            )
