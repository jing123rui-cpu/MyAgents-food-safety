#!/usr/bin/env python3
"""Sprint 40 — Executive Demonstration Console.

Interactive CLI demonstrating the food production enterprise intelligent
inspection agent.  Zero changes to core business logic — pure presentation layer.

Usage:
    python demo_console.py
"""

from __future__ import annotations

import datetime
import logging
import os
import sys
import webbrowser
from typing import Any, Dict, List, Optional, Tuple

from colorama import Fore, Back, Style, init as colorama_init
from colorama import Cursor  # fmt: skip

from script import FoodAuditAgent
from script.ai import AuditWritingEngine
from script.ai.report_exporter import ReportExporter
from script.models import Evidence, EvidenceType

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

# ── Constants ──────────────────────────────────────────────────────

ENTERPRISE_TYPES: Dict[str, Tuple[str, str]] = {
    "1": ("普通食品", "general_food"),
    "2": ("饮料", "beverage"),
    "3": ("包装饮用水", "packaged_water"),
}

SAMPLE_FINDINGS = [
    "供应商许可证过期",
    "生产记录填写不完整",
    "包装车间未设置防蝇设施",
]

BOX_WIDTH = 72

# ── Console Helpers ────────────────────────────────────────────────


def cprintln(text: str, color=Fore.WHITE, end="\n") -> None:
    print(color + text + Style.RESET_ALL, end=end)


def header(text: str, color=Fore.CYAN) -> None:
    print()
    cprintln("=" * BOX_WIDTH, color)
    cprintln(f"  {text}", color)
    cprintln("=" * BOX_WIDTH, color)
    print()


def step(n: int, title: str) -> None:
    line = f"-- Step {n}: {title} "
    pad = "-" * max(2, BOX_WIDTH - len(line))
    print()
    cprintln(line + pad, Fore.YELLOW)


def item(label: str, value: str, val_color=Fore.WHITE) -> None:
    print(f"  {Fore.GREEN}{label}{Style.RESET_ALL} {val_color}{value}{Style.RESET_ALL}")


CHECK = "+"
CROSS = "x"

def status_icon(ok: bool) -> str:
    return f"{Fore.GREEN}{CHECK}{Style.RESET_ALL}" if ok else f"{Fore.RED}{CROSS}{Style.RESET_ALL}"


def prompt(label: str, default: str = "") -> str:
    val = input(f"  {Fore.GREEN}{label}{Style.RESET_ALL}").strip()
    if not val and default:
        print(f"    (默认：{default})")
        return default
    return val


def info_box(label: str, value: str, color=Fore.YELLOW) -> None:
    print(f"  {Fore.CYAN}*{Style.RESET_ALL} {Fore.WHITE}{label}{Style.RESET_ALL}: {color}{value}{Style.RESET_ALL}")


# ── Finding-to-Checkpoint Matching ────────────────────────────────


def match_finding(agent: FoodAuditAgent, text: str) -> Optional[Any]:
    """Match a free-text finding to the most relevant checkpoint.

    Uses the search engine first; falls back to 2-char sliding-window
    substring search across checkpoint names and registry keywords.
    """
    # 1. Full-text search
    results = agent._search.search_keyword(text)
    if results:
        return results[0]

    # 2. Sliding 2-char window
    for i in range(len(text) - 1):
        seg = text[i : i + 2]
        results = agent._search.search_keyword(seg)
        if results:
            return results[0]

    return None


def get_risk_label(risk_level: str) -> Tuple[str, Any]:
    """Map checkpoint risk level to display label and color."""
    mapping = {
        "H": ("重点风险项", Fore.RED),
        "M": ("一般风险项", Fore.YELLOW),
    }
    return mapping.get(risk_level.upper(), ("一般风险项", Fore.YELLOW))


def get_risk_level_from_rules(agent: FoodAuditAgent, checkpoint_id: str) -> str:
    """Look up a checkpoint's risk level from its matching risk rule."""
    expected_rid = f"RR-{checkpoint_id}"
    for rule in agent._loader.risk_rules:
        if rule.rule_id == expected_rid:
            return rule.risk_level
    # Fallback to checkpoint's own risk_level
    cp = agent._repo.checkpoints.get(checkpoint_id)
    if cp:
        level_map = {"H": "High", "M": "Medium"}
        return level_map.get(cp.risk_level, "Medium")
    return "Medium"


# ── Main ────────────────────────────────────────────────────────────


def main() -> None:
    colorama_init(autoreset=True)

    # ═══════════════════════════════════════════════════════════════
    # PART 1: 系统启动
    # ═══════════════════════════════════════════════════════════════
    header("食品生产企业智能监督检查 Agent v1.0", Fore.CYAN)

    print("  正在初始化系统...\n")

    agent = FoodAuditAgent("knowledge")
    summary = agent.initialize()

    ai_available = agent._ai_manager.get_provider() is not None
    ai_label = f"{Fore.GREEN}Online{Style.RESET_ALL}" if ai_available else f"{Fore.YELLOW}Offline{Style.RESET_ALL}"

    print(f"  {status_icon(True)} 系统启动成功")
    print(f"  {status_icon(True)} Knowledge Loaded（{summary.get('checkpoints', 0)} checkpoints, {summary.get('registry', 0)} registry entries）")
    print(f"  {status_icon(True)} Rule Engine Ready（{summary.get('risk_rules', 0)} risk rules）")
    print(f"  {status_icon(True)} Report Engine Ready")
    print(f"  {status_icon(ai_available)} AI Provider Status：{ai_label}")
    logger.warning = lambda *a, **kw: None  # suppress further warnings
    print()

    # ═══════════════════════════════════════════════════════════════
    # PART 2: 基本信息录入
    # ═══════════════════════════════════════════════════════════════
    header("信息录入 —— 被检查单位基本信息", Fore.CYAN)

    company_name = prompt("企业名称：", "XX食品饮料有限公司")

    print(f"\n  {Fore.GREEN}企业类型：{Style.RESET_ALL}")
    for key, (label, _) in ENTERPRISE_TYPES.items():
        print(f"    [{key}] {label}")
    type_choice = input("  请选择（1-3，默认1）：").strip() or "1"
    chinese_type, enterprise_type = ENTERPRISE_TYPES.get(type_choice, ENTERPRISE_TYPES["1"])
    info_box("企业类型", chinese_type)

    auditor = prompt("检查人员：", "王五、赵六")
    date_str = prompt("检查日期（YYYY-MM-DD，默认今天）：", datetime.date.today().strftime("%Y-%m-%d"))

    # ═══════════════════════════════════════════════════════════════
    # PART 3: 现场问题录入
    # ═══════════════════════════════════════════════════════════════
    header("现场检查 —— 请录入发现的问题", Fore.CYAN)

    print(f"  {Fore.YELLOW}提示：输入一行一条问题描述，输入 END 结束{Style.RESET_ALL}")
    print(f"  {Fore.YELLOW}示例：{Style.RESET_ALL}")
    for i, s in enumerate(SAMPLE_FINDINGS, 1):
        print(f"    [{i}] {s}")
    print()

    findings: List[str] = []
    while True:
        line = input(f"  {Fore.GREEN}> {Style.RESET_ALL}").strip()
        if line.upper() == "END":
            break
        if not line:
            continue
        findings.append(line)

    if not findings:
        print(f"\n  {Fore.YELLOW}未录入自定义问题，使用默认示例。{Style.RESET_ALL}")
        findings = SAMPLE_FINDINGS.copy()

    print(f"\n  {Fore.CYAN}> 共录入 {len(findings)} 条现场发现{Style.RESET_ALL}\n")

    # ═══════════════════════════════════════════════════════════════
    # PART 4: 智能检查分析
    # ═══════════════════════════════════════════════════════════════
    header("智能检查分析报告", Fore.CYAN)

    # ── Step 1：AI 识别的问题 ──
    step(1, "检查发现问题")
    for i, f in enumerate(findings, 1):
        print(f"    {Fore.RED}[问题 {i}]{Style.RESET_ALL}  {f}")
    print()

    # ── Match findings to checkpoints ──
    evidence_list: List[Evidence] = []
    matched_pairs: List[Tuple[str, Optional[Any]]] = []

    for i, f in enumerate(findings):
        cp = match_finding(agent, f)
        matched_pairs.append((f, cp))
        if cp:
            ev = Evidence(
                id=f"EVID-{i + 1:03d}",
                evidence_type=EvidenceType.OBSERVATION,
                checkpoint_id=cp.checkpoint_id,
                description=f,
                source="现场检查",
            )
            evidence_list.append(ev)

    # ── Run the inspection engine ──
    effective_type = ENTERPRISE_TYPES.get(type_choice, ENTERPRISE_TYPES["1"])[1]
    print(f"  {Fore.CYAN}正在执行智能分析...{Style.RESET_ALL}\n")
    ctx = agent.inspect(query=effective_type, evidence=evidence_list)

    # ── Step 2：匹配到的 Checkpoint ──
    step(2, "匹配 Checkpoint")
    for f, cp in matched_pairs:
        if cp:
            print(f"    {Fore.GREEN}{cp.checkpoint_id}{Style.RESET_ALL}  {cp.checkpoint_name}")
            rl, _ = get_risk_label(cp.risk_level)
            print(f"      └ 领域：{Fore.CYAN}{cp.domain}{Style.RESET_ALL}  风险等级：{Fore.YELLOW}{rl}{Style.RESET_ALL}")
        else:
            print(f"    {Fore.RED}未匹配到相关检查点{Style.RESET_ALL}  「{f}」")
    print()

    # ── Step 3：匹配到的 Risk Rule ──
    step(3, "匹配 Risk Rule")
    for f, cp in matched_pairs:
        if cp is None:
            continue
        expected_rid = f"RR-{cp.checkpoint_id}"
        matched_rules = [r for r in agent._loader.risk_rules if r.rule_id == expected_rid]
        if matched_rules:
            rule = matched_rules[0]
            print(f"    {Fore.GREEN}{rule.rule_id}{Style.RESET_ALL}  {rule.description}")
            rl, rl_color = get_risk_label(cp.risk_level)
            print(f"      └ 风险等级：{rl_color}{rule.risk_level}{Style.RESET_ALL}")
        else:
            print(f"    {Fore.YELLOW}未匹配到风险规则{Style.RESET_ALL}  ({cp.checkpoint_id})")
    print()

    # ── Step 4：引用法规 ──
    step(4, "自动引用法规依据")
    try:
        from script.regulation_loader import RegulationLoader
        reg_loader = RegulationLoader("knowledge")
        reg_repo = reg_loader.load_regulations()
        applicable = reg_loader.get_applicable_regulations(reg_repo, effective_type)
        if applicable:
            for i, reg in enumerate(applicable, 1):
                print(f"    {Fore.CYAN}[{i}]{Style.RESET_ALL}  {Fore.GREEN}{reg.id}{Style.RESET_ALL}  《{reg.title_zh}》")
                if reg.issuing_authority:
                    print(f"      └ 发布机关：{reg.issuing_authority}")
        else:
            print(f"    {Fore.YELLOW}（当前企业类型「{chinese_type}」无专项适用法规）{Style.RESET_ALL}")
    except Exception:
        print(f"    {Fore.YELLOW}（法规知识库加载中，请确认 knowledge 目录完整）{Style.RESET_ALL}")
    print()

    # ── Step 5：RuleEngine 判定 ──
    step(5, "RuleEngine 判定")
    print()
    print(f"    {'检查点':<28} {'判定结果':<12} {'风险分类':<12}")
    print(f"    {'─' * 28} {'─' * 12} {'─' * 12}")

    compliant = 0
    non_compliant = 0
    not_applicable = 0

    for result in ctx.evaluation_results:
        cp = agent._repo.checkpoints.get(result.checkpoint_id)
        cp_name = cp.checkpoint_name if cp else result.checkpoint_id[:20]
        status_zh = result.status.chinese

        if result.status.value == "COMPLIANT":
            compliant += 1
            sc = Fore.GREEN
            risk_display = f"{Fore.WHITE}-{Style.RESET_ALL}"
        elif result.status.value == "NON_COMPLIANT":
            non_compliant += 1
            sc = Fore.RED
            rl = get_risk_level_from_rules(agent, result.checkpoint_id)
            risk_label = "重点风险项" if rl.lower() in ("critical", "high") else "一般风险项"
            risk_color = Fore.RED if rl.lower() in ("critical", "high") else Fore.YELLOW
            risk_display = f"{risk_color}{risk_label}{Style.RESET_ALL}"
        else:
            not_applicable += 1
            sc = Fore.WHITE
            risk_display = f"{Fore.WHITE}-{Style.RESET_ALL}"

        print(f"    {cp_name[:28]:<28} {sc}{status_zh:<12}{Style.RESET_ALL} {risk_display:<12}")

    print()
    info_box("合格项", f"{compliant} 项", Fore.GREEN)
    info_box("不合格项", f"{non_compliant} 项", Fore.RED)
    info_box("不适用项", f"{not_applicable} 项", Fore.WHITE)
    print()

    # ── Step 6：企业综合判定 ──
    step(6, "企业综合判定")
    ent = ctx.metadata.get("enterprise_evaluation")
    if ent:
        is_pass = ent.overall_result == "企业通过检查"
        con_color = Fore.GREEN if is_pass else Fore.RED

        print(f"\n  {con_color}{'#' * 48}{Style.RESET_ALL}")
        print(f"  {con_color}  {ent.overall_result}{Style.RESET_ALL}")
        print(f"  {con_color}{'#' * 48}{Style.RESET_ALL}")
        print(f"\n  {Fore.CYAN}* {ent.summary}{Style.RESET_ALL}")
        print()

    # ═══════════════════════════════════════════════════════════════
    # PART 5: 报告生成
    # ═══════════════════════════════════════════════════════════════
    header("报告生成 —— 导出监督检查报告", Fore.CYAN)

    enterprise_info: Dict[str, str] = {
        "facility_name": company_name,
        "credit_code": "91440101MA5XXXXXXX",
        "license_number": "SC106440111XXXXX",
        "address": "XX省XX市XX区XX路XX号",
        "legal_representative": "张三",
        "food_safety_director": "李四",
        "audit_date": date_str,
        "audit_type": "日常监督",
        "auditor_name": auditor,
        "company_representative": "陈七",
    }

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
        enterprise_type=effective_type,
        knowledge_dir="knowledge",
    )
    if ent:
        writing_result.metadata["enterprise_evaluation"] = ent
    writing_result.metadata["facility_name"] = company_name

    exporter = ReportExporter()
    export_result = exporter.export_word(writing_result)

    if export_result.success:
        print(f"\n  {Fore.GREEN}{'=' * 20}{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}报告导出成功{Style.RESET_ALL}")
        print(f"  {Fore.GREEN}{'=' * 20}{Style.RESET_ALL}")
        print(f"\n  文件名：{Fore.CYAN}{export_result.filename}{Style.RESET_ALL}")
        print(f"  保存位置：{Fore.CYAN}reports/output/{Style.RESET_ALL}")
        print(f"  完整路径：{Fore.CYAN}{export_result.filepath}{Style.RESET_ALL}")

        print(f"\n  {Fore.CYAN}正在打开 Word 文档…{Style.RESET_ALL}")
        try:
            webbrowser.open(str(export_result.filepath))
        except Exception:
            print(f"  {Fore.YELLOW}报告已生成，请手动打开。{Style.RESET_ALL}")
    else:
        print(f"\n  {Fore.RED}{CROSS} 报告生成失败：{export_result.error}{Style.RESET_ALL}")

    # ── Footer ──
    print()
    header("演示结束，谢谢使用", Fore.GREEN)


if __name__ == "__main__":
    main()
