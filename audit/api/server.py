"""FastAPI server wrapping the FoodAuditAgent runtime.

Endpoints
---------
GET   /          — Root info
GET   /health    — Agent health status
POST  /search    — Search checkpoints
POST  /inspect   — Run full inspection with optional evidence evaluation
"""

from __future__ import annotations

import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import AsyncIterator

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from script import FoodAuditAgent
from script.models import Evidence, EvidenceType

from .schemas import (
    CheckpointResponse,
    EvaluationResultResponse,
    EvidenceItem,
    HealthResponse,
    InspectRequest,
    InspectResponse,
    RegistryEntryResponse,
    RiskRuleResponse,
    RootResponse,
    SearchRequest,
    SearchResponse,
    TaxonomyNodeResponse,
)

logger = logging.getLogger(__name__)

# ── Global agent instance (initialised during startup) ─────────────

_agent: FoodAuditAgent | None = None


def get_agent() -> FoodAuditAgent:
    if _agent is None:
        raise RuntimeError("Agent not initialised")
    return _agent


# ── Internal converters ────────────────────────────────────────────

def _to_checkpoint(cp) -> CheckpointResponse:
    return CheckpointResponse(
        checkpoint_id=cp.checkpoint_id,
        checkpoint_name=cp.checkpoint_name,
        domain=cp.domain,
        module=cp.module,
        unit=cp.unit,
        category=cp.category,
        applicable_products=list(cp.applicable_products),
        risk_level=cp.risk_level,
        priority=cp.priority,
        estimated_time=cp.estimated_time,
        objective=cp.objective,
    )


def _to_registry_entry(reg) -> RegistryEntryResponse:
    return RegistryEntryResponse(
        id=reg.id,
        title=reg.title,
        category=reg.category,
        subcategory=reg.subcategory,
        risk_level=reg.risk_level,
        laws=list(reg.laws),
        keywords=list(reg.keywords),
        evidence_required=list(reg.evidence_required),
    )


def _to_risk_rule(rule) -> RiskRuleResponse:
    return RiskRuleResponse(
        rule_id=rule.rule_id,
        risk_level=rule.risk_level,
        condition=rule.condition,
        description=rule.description,
    )


def _to_taxonomy_node(node) -> TaxonomyNodeResponse:
    return TaxonomyNodeResponse(id=node.id, name=node.name)


def _to_evaluation_result(er) -> EvaluationResultResponse:
    return EvaluationResultResponse(
        checkpoint_id=er.checkpoint_id,
        rule_id=er.rule_id,
        evidence_id=er.evidence_id,
        status=er.status.value if hasattr(er.status, "value") else str(er.status),
        score=er.score,
        reason=er.reason,
        violated_laws=list(er.violated_laws),
        recommendation=er.recommendation,
        metadata=dict(er.metadata),
    )


def _to_evidence_item(ev) -> EvidenceItem:
    return EvidenceItem(
        id=ev.id,
        evidence_type=ev.evidence_type.value if hasattr(ev.evidence_type, "value") else str(ev.evidence_type),
        checkpoint_id=ev.checkpoint_id,
        description=ev.description,
        source=ev.source,
        attachments=list(ev.attachments),
        metadata=dict(ev.metadata),
    )


def _evidence_from_schema(item: EvidenceItem) -> Evidence:
    return Evidence(
        id=item.id,
        evidence_type=EvidenceType(item.evidence_type),
        checkpoint_id=item.checkpoint_id,
        description=item.description,
        source=item.source,
        attachments=list(item.attachments),
        metadata=dict(item.metadata),
    )


# ── Lifespan ───────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    global _agent
    logger.info("Starting Food Audit Agent API server")
    agent = FoodAuditAgent("knowledge")
    summary = agent.initialize()
    if summary["errors"]:
        logger.error("Agent initialisation failed: %d error(s)", summary["errors"])
    else:
        logger.info("Agent initialised: status=%s", summary["status"])
    _agent = agent
    # Mount Web UI after agent is ready
    from web.routes import router as web_router, set_agent
    set_agent(agent)
    app.mount("/static", StaticFiles(directory="web/static"), name="static")
    app.include_router(web_router)
    yield
    logger.info("Shutting down Food Audit Agent API server")


# ── App instance ───────────────────────────────────────────────────

app = FastAPI(
    title="Food Audit Agent API",
    description="REST API for the food safety audit inspection system",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)


# ── Exception handlers ─────────────────────────────────────────────

@app.exception_handler(RuntimeError)
async def runtime_error_handler(request: Request, exc: RuntimeError) -> JSONResponse:
    return JSONResponse(
        status_code=500,
        content={"detail": str(exc)},
    )


@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={"detail": str(exc)},
    )


@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception("Unhandled exception")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


# ── Endpoints ──────────────────────────────────────────────────────

@app.get("/", response_model=RootResponse)
async def root() -> RootResponse:
    return RootResponse(
        name="Food Audit Agent",
        version="1.0.0",
        status="running",
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    agent = get_agent()
    try:
        status = agent.health()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
    return HealthResponse(
        status=status["status"],
        registry=status["registry"],
        checkpoints=status["checkpoints"],
        risk_rules=status["risk_rules"],
        taxonomy_nodes=status["taxonomy_nodes"],
        warnings=status["warnings"],
        errors=status["errors"],
    )


@app.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest) -> SearchResponse:
    agent = get_agent()

    if not req.query and not req.checkpoint_id and not req.category and not req.risk_level:
        raise HTTPException(
            status_code=422,
            detail="At least one search criterion is required (query, checkpoint_id, category, risk_level)",
        )

    try:
        ctx = agent.inspect(
            query=req.query,
            checkpoint_id=req.checkpoint_id,
            category=req.category,
            risk_level=req.risk_level,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    if not ctx.matched_checkpoints:
        return SearchResponse(total=0)

    return SearchResponse(
        total=len(ctx.matched_checkpoints),
        checkpoints=[_to_checkpoint(cp) for cp in ctx.matched_checkpoints],
        registry_entries=[_to_registry_entry(reg) for reg in ctx.matched_registry_entries],
        risk_rules=[_to_risk_rule(rule) for rule in ctx.matched_risk_rules],
        taxonomy_nodes=[_to_taxonomy_node(n) for n in ctx.matched_taxonomy_nodes],
    )


@app.post("/inspect", response_model=InspectResponse)
async def inspect(req: InspectRequest) -> InspectResponse:
    agent = get_agent()

    if not req.query and not req.checkpoint_id and not req.category and not req.risk_level:
        raise HTTPException(
            status_code=422,
            detail="At least one search criterion is required",
        )

    evidence = [_evidence_from_schema(ev) for ev in req.evidence] if req.evidence else None

    try:
        ctx = agent.inspect(
            query=req.query,
            checkpoint_id=req.checkpoint_id,
            category=req.category,
            risk_level=req.risk_level,
            evidence=evidence,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))

    inspect_req = SearchRequest(
        query=req.query,
        checkpoint_id=req.checkpoint_id,
        category=req.category,
        risk_level=req.risk_level,
    )

    return InspectResponse(
        request=inspect_req,
        matched_checkpoints=[_to_checkpoint(cp) for cp in ctx.matched_checkpoints],
        matched_registry_entries=[_to_registry_entry(reg) for reg in ctx.matched_registry_entries],
        matched_risk_rules=[_to_risk_rule(rule) for rule in ctx.matched_risk_rules],
        matched_taxonomy_nodes=[_to_taxonomy_node(n) for n in ctx.matched_taxonomy_nodes],
        evidence=[_to_evidence_item(ev) for ev in ctx.evidence],
        evaluation_results=[_to_evaluation_result(er) for er in ctx.evaluation_results],
        warnings=list(ctx.warnings),
        metadata=dict(ctx.metadata),
    )


# ── Download endpoint for generated Word files ────────────────────


@app.get("/download/{filename:path}")
async def download_report(filename: str) -> FileResponse:
    """Serve a generated Word document for download."""
    base = Path("reports") / "output"
    filepath = base / filename
    if not filepath.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(
        path=str(filepath),
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        filename=filename,
    )
