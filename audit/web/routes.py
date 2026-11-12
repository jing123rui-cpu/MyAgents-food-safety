"""Web UI routes for the Food Audit Agent demo interface.

Adds government-style inspection UI pages and analysis endpoints.
No modifications to core business logic.
"""

from __future__ import annotations

import datetime
import logging
import os
import time
import uuid
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from script.ai import AuditWritingEngine
from script.ai.report_exporter import ReportExporter
from script.models import Evidence, EvidenceType

logger = logging.getLogger(__name__)

# ── Template & static config ──────────────────────────────────────

templates = Jinja2Templates(directory="web/templates")

# ── In-memory session store ───────────────────────────────────────

_sessions: Dict[str, Dict[str, Any]] = {}
_agent_ref: Any = None  # set by mount_web_ui()


def set_agent(agent: Any) -> None:
    global _agent_ref
    _agent_ref = agent


def _get_agent():
    if _agent_ref is None:
        raise RuntimeError("Agent not initialised")
    return _agent_ref


# ── Helpers ────────────────────────────────────────────────────────

_ENTERPRISE_TYPE_LABELS = {
    "general_food": "其他食品生产企业",
    "beverage": "饮料生产企业",
    "packaged_water": "包装饮用水企业",
}


def _match_finding(agent, text: str):
    """Match a free-text finding to the most relevant checkpoint."""
    results = agent._search.search_keyword(text)
    if results:
        return results[0]
    for i in range(len(text) - 1):
        seg = text[i: i + 2]
        results = agent._search.search_keyword(seg)
        if results:
            return results[0]
    return None


def _get_risk_label(risk_level: str) -> str:
    return "重点风险项" if risk_level.upper() == "H" else "一般风险项"


# ── Router ─────────────────────────────────────────────────────────

router = APIRouter(prefix="/ui")


# ── Page routes ────────────────────────────────────────────────────


@router.get("", response_class=HTMLResponse)
async def ui_home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(request, "index.html")


@router.get("/enterprise", response_class=HTMLResponse)
async def ui_enterprise(request: Request) -> HTMLResponse:
    today = datetime.date.today().strftime("%Y-%m-%d")
    return templates.TemplateResponse(request, "enterprise.html", {"today": today})


@router.get("/problems", response_class=HTMLResponse)
async def ui_problems(
    request: Request,
    name: str = "",
    type: str = "beverage",
    auditor: str = "",
    date: str = "",
) -> HTMLResponse:
    return templates.TemplateResponse(request, "problems.html", {
        "name": name,
        "ent_type": type,
        "auditor": auditor,
        "date": date,
    })


@router.post("/analyze")
async def ui_analyze(request: Request, name: str = Form(""), type: str = Form("beverage"),
                     auditor: str = Form(""), date: str = Form(""),
                     problems: str = Form("")) -> HTMLResponse:
    agent = _get_agent()
    findings = [p.strip() for p in problems.strip().split("\n") if p.strip()]

    if not name:
        name = "食品生产企业"
    if not auditor:
        auditor = "系统管理员"
    if not date:
        date = datetime.date.today().strftime("%Y-%m-%d")

    session_id = uuid.uuid4().hex[:12]
    _sessions[session_id] = {
        "name": name,
        "enterprise_type": type,
        "auditor": auditor,
        "date": date,
        "findings": findings,
        "step": 0,
        "complete": False,
        "results": None,
        "start_time": time.time(),
    }

    # Run analysis
    try:
        _run_analysis(session_id, agent, findings, type)
    except Exception as exc:
        logger.error("Analysis failed: %s", exc)
        _sessions[session_id]["error"] = str(exc)
        _sessions[session_id]["complete"] = True
        _sessions[session_id]["step"] = 6

    return templates.TemplateResponse(request, "analyzing.html", {
        "name": name,
        "analysis_id": session_id,
    })


@router.get("/analyze/status/{session_id}")
async def ui_analyze_status(session_id: str) -> JSONResponse:
    sess = _sessions.get(session_id)
    if not sess:
        return JSONResponse({"error": "Session not found", "step": 0, "complete": False})

    elapsed = time.time() - sess["start_time"]
    # Simulate progressive step completion over ~5 seconds
    step_progress = min(int(elapsed / 0.8) + 1, 6)

    # Actual analysis is already done; just animate the step display
    actual_step = sess.get("step", 0)
    current_step = min(step_progress, actual_step)
    complete = sess["complete"] or current_step >= 6

    if complete:
        current_step = 6

    return JSONResponse({
        "step": current_step,
        "complete": complete,
        "error": sess.get("error", ""),
    })


@router.get("/results/{session_id}", response_class=HTMLResponse)
async def ui_results(request: Request, session_id: str) -> HTMLResponse:
    sess = _sessions.get(session_id)
    if not sess or not sess.get("results"):
        return templates.TemplateResponse(request, "index.html")

    r = sess["results"]
    ent = r.get("enterprise_evaluation", {})
    total = ent.get("total_checkpoints", 0)
    compliant = ent.get("compliant_count", 0)
    non_compliant = ent.get("non_compliant_count", 0)
    key_risks = ent.get("key_risks", 0)
    general_risks = ent.get("general_risks", 0)
    conclusion = ent.get("overall_result", "")
    is_pass = conclusion == "企业通过检查"

    regulations = r.get("regulations", [])
    findings = r.get("findings", [])

    return templates.TemplateResponse(request, "results.html", {
        "analysis_id": session_id,
        "name": sess["name"],
        "total": total,
        "compliant": compliant,
        "non_compliant": non_compliant,
        "key_risks": key_risks,
        "general_risks": general_risks,
        "conclusion": conclusion,
        "is_pass": is_pass,
        "regulations": regulations,
        "findings": findings,
    })


@router.post("/export")
async def ui_export(analysis_id: str = Form("")) -> JSONResponse:
    sess = _sessions.get(analysis_id)
    if not sess:
        return JSONResponse({"success": False, "error": "Session not found"})

    results = sess.get("results")
    if not results:
        return JSONResponse({"success": False, "error": "No analysis results"})

    agent = _get_agent()
    ctx = results.get("inspection_context")
    if not ctx:
        return JSONResponse({"success": False, "error": "No inspection context"})

    ent_eval = results.get("enterprise_evaluation")
    enterprise_info = {
        "facility_name": sess["name"],
        "credit_code": "91440101MA5XXXXXXX",
        "license_number": "SC106440111XXXXX",
        "address": "XX省XX市XX区XX路XX号",
        "legal_representative": "（待填写）",
        "food_safety_director": "（待填写）",
        "audit_date": sess["date"],
        "audit_type": "日常监督",
        "auditor_name": sess["auditor"],
        "company_representative": "（待填写）",
    }

    try:
        engine = AuditWritingEngine()
        writing_result = engine.generate_all_offline(
            ctx,
            facility_name=enterprise_info["facility_name"],
            credit_code=enterprise_info["credit_code"],
            license_number=enterprise_info["license_number"],
            address=enterprise_info["address"],
            legal_representative=enterprise_info["legal_representative"],
            food_safety_director=enterprise_info["food_safety_director"],
            audit_date=enterprise_info["audit_date"],
            audit_type=enterprise_info["audit_type"],
            auditor_name=enterprise_info["auditor_name"],
            company_representative=enterprise_info["company_representative"],
            enterprise_type=sess["enterprise_type"],
            knowledge_dir="knowledge",
        )
        if ent_eval:
            writing_result.metadata["enterprise_evaluation"] = ent_eval
        writing_result.metadata["facility_name"] = sess["name"]

        exporter = ReportExporter()
        export_result = exporter.export_word(writing_result)

        if export_result.success:
            download_url = f"/download/{export_result.filename}"
            return JSONResponse({
                "success": True,
                "filename": export_result.filename,
                "filepath": str(export_result.filepath),
                "download_url": download_url,
            })
        else:
            return JSONResponse({"success": False, "error": export_result.error})

    except Exception as exc:
        logger.exception("Export failed")
        return JSONResponse({"success": False, "error": str(exc)})


# ── Analysis Engine ────────────────────────────────────────────────


def _run_analysis(session_id: str, agent, findings: List[str], enterprise_type: str) -> None:
    """Run the full inspection pipeline and store results."""
    sess = _sessions[session_id]
    sess["step"] = 1  # Step 1: identifying problems

    # Build evidence from findings
    evidence_list: List[Evidence] = []
    finding_details: List[Dict] = []
    for i, f in enumerate(findings):
        cp = _match_finding(agent, f)
        if cp:
            ev = Evidence(
                id=f"EVID-{i + 1:03d}",
                evidence_type=EvidenceType.OBSERVATION,
                checkpoint_id=cp.checkpoint_id,
                description=f,
                source="现场检查",
            )
            evidence_list.append(ev)
            finding_details.append({
                "problem": f,
                "checkpoint_id": cp.checkpoint_id,
                "checkpoint_name": cp.checkpoint_name,
            })
        else:
            finding_details.append({
                "problem": f,
                "checkpoint_id": "（未匹配）",
                "checkpoint_name": "（未匹配到相关检查点）",
            })

    sess["step"] = 2  # Step 2: matching checkpoints

    # Map enterprise type to search query
    type_to_query = {
        "general_food": "食品生产",
        "beverage": "beverage",
        "packaged_water": "beverage",
    }
    query = type_to_query.get(enterprise_type, "食品生产")

    # Run inspection
    ctx = agent.inspect(query=query, evidence=evidence_list)

    sess["step"] = 3  # Step 3: matching risk rules
    # (same as inspect step)

    # Load regulations
    reg_list: List[str] = []
    try:
        from script.regulation_loader import RegulationLoader
        reg_loader = RegulationLoader("knowledge")
        reg_repo = reg_loader.load_regulations()
        applicable = reg_loader.get_applicable_regulations(reg_repo, enterprise_type)
        reg_list = [f"《{r.title_zh}》" for r in applicable]
    except Exception:
        reg_list = ["《中华人民共和国食品安全法》", "《食品生产经营监督检查管理办法》"]

    sess["step"] = 4  # Step 4: referencing regulations

    # Build finding display with risk + status
    # Build rule-level mapping
    cp_risk_map: Dict[str, str] = {}
    for rule in agent._loader.risk_rules:
        if rule.rule_id.startswith("RR-"):
            cp_risk_map[rule.rule_id[3:]] = rule.risk_level

    compliant = 0
    non_compliant = 0
    key_risks = 0
    general_risks = 0

    result_findings: List[Dict] = []
    for er in ctx.evaluation_results:
        cp = agent._repo.checkpoints.get(er.checkpoint_id)
        cp_name = cp.checkpoint_name if cp else er.checkpoint_id
        risk_lvl = cp_risk_map.get(er.checkpoint_id, "Medium")
        is_key = risk_lvl.lower() in ("critical", "high")
        risk_label = "重点风险项" if is_key else "一般风险项"
        status_zh = er.status.chinese if hasattr(er.status, "chinese") else str(er.status)

        if er.status.value == "COMPLIANT":
            compliant += 1
        elif er.status.value == "NON_COMPLIANT":
            non_compliant += 1
            if is_key:
                key_risks += 1
            else:
                general_risks += 1

        violated_law = er.violated_laws[0] if er.violated_laws else ""
        # Find the original problem text
        problem_text = ""
        for fd in finding_details:
            if fd["checkpoint_id"] == er.checkpoint_id:
                problem_text = fd["problem"]
                break

        result_findings.append({
            "problem": problem_text or f"（检查点 {er.checkpoint_id} 相关）",
            "checkpoint_id": er.checkpoint_id,
            "checkpoint_name": cp_name,
            "risk_label": risk_label,
            "status": status_zh,
            "law": violated_law,
        })

    sess["step"] = 5  # Step 5: rule engine evaluation (done)

    # Enterprise evaluation
    ent = ctx.metadata.get("enterprise_evaluation")
    ent_dict = {}
    if ent:
        ent_dict = {
            "total_checkpoints": getattr(ent, "total_checkpoints", 0),
            "compliant_count": getattr(ent, "compliant_count", compliant),
            "non_compliant_count": getattr(ent, "non_compliant_count", non_compliant),
            "overall_result": getattr(ent, "overall_result", ""),
            "key_risks": key_risks,
            "general_risks": general_risks,
            "summary": getattr(ent, "summary", ""),
        }

    if not result_findings:
        result_findings = finding_details

    sess["results"] = {
        "enterprise_evaluation": ent_dict,
        "regulations": reg_list,
        "findings": result_findings,
        "inspection_context": ctx,
    }

    sess["step"] = 6  # Step 6: enterprise evaluation (complete)
    sess["complete"] = True
