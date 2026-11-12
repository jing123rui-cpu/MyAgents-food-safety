"""InspectionPipeline — orchestrates the full AI inspection workflow.

Wires together InspectionWorkflow, ContextEngine, PromptEngine,
and AIProvider into a single ``run()`` call.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from ..workflow import InspectionContext, InspectionRequest, InspectionWorkflow
from ..models import KnowledgeRepository
from .base import AIProvider
from .context_engine import AIContext, ContextEngine
from .prompt_engine import PromptEngine
from .schemas import AIRequest as AIRequestSchema, AIResponse, AIMessage

logger = logging.getLogger(__name__)


@dataclass
class AIInspectionResult:
    """Complete result of an AI-powered inspection run."""

    inspection_context: InspectionContext = field(default_factory=lambda: InspectionContext.__new__(InspectionContext))
    ai_context: AIContext = field(default_factory=AIContext)
    prompt: str = ""
    raw_response: Optional[AIResponse] = None
    provider: str = ""
    model: str = ""
    latency: float = 0.0
    timestamp: str = ""
    success: bool = False
    error_message: str = ""


class InspectionPipeline:
    """End-to-end AI inspection pipeline.

    Pipeline steps
    --------------
    1. ``InspectionWorkflow.build_context()``
    2. ``ContextEngine.build_context()``
    3. ``PromptEngine.build_inspection_prompt()``
    4. ``AIProvider.chat()``
    5. Return ``AIInspectionResult``
    """

    def __init__(
        self,
        workflow: InspectionWorkflow,
        repository: KnowledgeRepository,
        provider: Optional[AIProvider] = None,
    ) -> None:
        self._workflow = workflow
        self._repo = repository
        self._provider = provider
        self._context_engine = ContextEngine(repository)
        self._prompt_engine = PromptEngine()

    # ── Public API ───────────────────────────────────────────────

    def run(self, request: InspectionRequest) -> AIInspectionResult:
        """Execute the full inspection pipeline.

        Parameters
        ----------
        request
            Search / filter parameters.

        Returns
        -------
        AIInspectionResult
            The combined result of workflow, context, prompt, and AI response.
        """
        ts = time.strftime("%Y-%m-%dT%H:%M:%S")
        start = time.monotonic()
        result = AIInspectionResult(timestamp=ts, latency=0.0)

        try:
            # Step 1 — Workflow
            insp_ctx = self._workflow.build_context(request)
            result.inspection_context = insp_ctx

            # Step 2 — Context Engine
            ai_ctx = self._context_engine.build_context(insp_ctx)
            result.ai_context = ai_ctx

            # Step 3 — Prompt Engine
            prompt = self._build_prompt(ai_ctx)
            result.prompt = prompt

            # Step 4 — AI call
            if self._provider is None:
                raise RuntimeError("No AI provider available — cannot complete inspection")

            ai_request = AIRequestSchema(
                messages=[AIMessage(role="user", content=prompt)],
                system_prompt=(
                    "You are a food safety audit AI assistant for beverage manufacturing. "
                    "Respond based on the inspection data provided."
                ),
                temperature=0.3,
                max_tokens=2048,
            )

            response = self._provider.chat(ai_request)
            result.raw_response = response
            result.provider = self._provider.provider_name
            result.model = response.model or self._provider.model_name
            result.success = True

        except Exception as exc:
            result.success = False
            result.error_message = f"[{type(exc).__name__}] {exc}"
            logger.error("Inspection pipeline failed: %s", exc)

        elapsed = time.monotonic() - start
        result.latency = round(elapsed, 3)

        return result

    # ── Prompt assembly ──────────────────────────────────────────

    @staticmethod
    def _build_prompt(ai_ctx: AIContext) -> str:
        """Map ``AIContext`` fields to the inspection prompt template."""
        task = (
            f"Evaluate \"{ai_ctx.inspector_query}\" against regulatory requirements."
            if ai_ctx.inspector_query
            else "Evaluate the matched checkpoints against regulatory requirements."
        )

        return PromptEngine().build_inspection_prompt(
            task=task,
            checkpoint_details=ai_ctx.checkpoints,
            risk_rules=ai_ctx.risk_rules,
            evidence=ai_ctx.evidence_summary,
            regulations=ai_ctx.applicable_laws,
            expected_output=(
                "Return a structured JSON object with:\n"
                '  "status": "合格" | "不合格" | "不适用",\n'
                '  "findings": [list of non-conformities],\n'
                '  "recommendations": [list of corrective actions],\n'
                '  "confidence": 0.0-1.0'
            ),
        )
