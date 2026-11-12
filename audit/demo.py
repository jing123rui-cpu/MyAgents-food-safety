"""Sprint 23 — End-to-End Runtime Demonstration.

Exercises the full inspection pipeline: initialize, search, load knowledge,
build inspection context, validate evidence, and evaluate risk.
"""

from __future__ import annotations

import time

from script import FoodAuditAgent
from script.models import Evidence, EvidenceType

_SEP = "=" * 60
_DASH = "-" * 60


def fmt_time(secs: float) -> str:
    m, s = divmod(round(secs, 3), 60)
    return f"{int(m):02d}:{s:05.3f}"


def main() -> None:
    t0 = time.perf_counter()

    # ═══════════════════════════════════════════════════════════════
    # Task 2 — Startup
    # ═══════════════════════════════════════════════════════════════
    print(_SEP)
    print("  Food Audit Agent — Runtime Demonstration")
    print(_SEP)
    print()

    agent = FoodAuditAgent("knowledge")
    t_start = time.perf_counter()
    summary = agent.initialize()
    t_init = time.perf_counter() - t_start

    print("  [STARTUP] Agent initialised")
    print()
    print(f"  Knowledge Loaded")
    print(f"    Registry:    {summary['registry']}")
    print(f"    Checkpoints: {summary['checkpoints']}")
    print(f"    Risk Rules:  {summary['risk_rules']}")
    print(f"    Taxonomy:    {summary['taxonomy_nodes']}")
    if summary["warnings"]:
        print(f"    Warnings:    {summary['warnings']}")
    if summary["errors"]:
        print(f"    Errors:      {summary['errors']}")
    print(f"    Init Time:   {fmt_time(t_init)}")
    print(f"    Status:      {summary['status']}")
    print()

    # ═══════════════════════════════════════════════════════════════
    # Task 3 — Inspection Demo
    # ═══════════════════════════════════════════════════════════════
    print(_DASH)
    print("  Task 3 — Inspection Demo")
    print(_DASH)
    print()

    t_start = time.perf_counter()
    ctx = agent.inspect(query="供应商许可证")
    t_search = time.perf_counter() - t_start

    print(f'  Query: "供应商许可证"')
    print(f"  Search Time: {fmt_time(t_search)}")
    print()

    if not ctx.matched_checkpoints:
        print("  No matching checkpoints found.")
        return

    for cp in ctx.matched_checkpoints:
        reg = _find_reg(ctx.matched_registry_entries, cp.checkpoint_id)
        rule = _find_rule(ctx.matched_risk_rules, cp.checkpoint_id)
        tax_nodes = [n for n in ctx.matched_taxonomy_nodes]

        print(f"  Matched Checkpoint:")
        print(f"    ID:     {cp.checkpoint_id}")
        print(f"    Title:  {cp.checkpoint_name}")
        print(f"    Domain: {cp.domain}")
        print(f"    Module: {cp.module}")
        print()

        if reg:
            print(f"  Registry Entry:")
            print(f"    ID:          {reg.id}")
            print(f"    Category:    {reg.category}")
            print(f"    Subcategory: {reg.subcategory}")
            print(f"    Risk Level:  {reg.risk_level}")
            print(f"    Laws:        {', '.join(reg.laws)}")
            if reg.evidence_required:
                print(f"    Evidence Req:")
                for ev_req in reg.evidence_required:
                    print(f"      - {ev_req}")
            print()

        if tax_nodes:
            print(f"  Taxonomy Nodes ({len(tax_nodes)}):")
            for n in tax_nodes:
                print(f"    - {n.id}  ({n.name_zh})")
            print()

        if rule:
            print(f"  Risk Rule:")
            print(f"    ID:          {rule.rule_id}")
            print(f"    Risk Level:  {rule.risk_level}")
            print(f"    Description: {rule.description}")
            print()

    # ═══════════════════════════════════════════════════════════════
    # Task 4 — Evidence Demo
    # ═══════════════════════════════════════════════════════════════
    print(_DASH)
    print("  Task 4 — Evidence Demo")
    print(_DASH)
    print()

    evidence_list = [
        Evidence(
            id="EVID-001",
            evidence_type=EvidenceType.OBSERVATION,
            checkpoint_id="CP-BEV-RM-001",
            description="现场观察：供应商许可证已在有效期内，品种范围覆盖采购原料",
            source="auditor_site_visit",
            attachments=["现场观察记录表_2026Q2.pdf"],
        ),
        Evidence(
            id="EVID-002",
            evidence_type=EvidenceType.PHOTO,
            checkpoint_id="CP-BEV-RM-001",
            description="供应商生产许可证复印件照片，清晰显示编号、有效期",
            source="auditor_photo_log",
            attachments=["supplier_license_001.jpg"],
        ),
        Evidence(
            id="EVID-003",
            evidence_type=EvidenceType.DOCUMENT,
            checkpoint_id="CP-BEV-RM-013",
            description="",
            source="warehouse_log",
            attachments=[],
        ),
    ]

    print(f"  Evidence Items ({len(evidence_list)}):")
    for ev in evidence_list:
        print(f"    {ev.id}")
        print(f"      Type:        {ev.evidence_type.value}")
        print(f"      Checkpoint:  {ev.checkpoint_id}")
        print(f"      Description: {ev.description}")
        print(f"      Attachments: {ev.attachments}")
    print()

    # Run validation
    t_start = time.perf_counter()
    ctx2 = agent.inspect(query="供应商许可证", evidence=evidence_list)
    t_eval = time.perf_counter() - t_start

    print(f"  Validation Time: {fmt_time(t_eval)}")
    print()

    if ctx2.warnings:
        print(f"  Evidence Warnings:")
        for w in ctx2.warnings:
            print(f"    - {w}")
        print()

    # ═══════════════════════════════════════════════════════════════
    # Task 5 — Rule Evaluation Demo
    # ═══════════════════════════════════════════════════════════════
    print(_DASH)
    print("  Task 5 — Rule Evaluation Demo")
    print(_DASH)
    print()

    if ctx2.evaluation_results:
        print(f"  Evaluation Results ({len(ctx2.evaluation_results)}):")
        print()
        for result in ctx2.evaluation_results:
            print(f"  {'=' * 56}")
            print(f"  Checkpoint:  {result.checkpoint_id}")
            print(f"  Rule:        {result.rule_id}")
            print(f"  Evidence:    {result.evidence_id}")
            print(f"  Status:      {result.status.value} ({result.status.chinese})")
            print(f"  Score:       {result.score}")
            print(f"  Reason:      {result.reason}")
            if result.violated_laws:
                print(f"  Violated Laws:")
                for law in result.violated_laws:
                    print(f"    - {law}")
            print(f"  Recommendation:")
            print(f"    {result.recommendation}")
            print()
    else:
        print("  No evaluation results (no evidence attached).")
        print()

    # ═══════════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════════
    t_total = time.perf_counter() - t0
    print(_SEP)
    print("  Demo Complete")
    print(_SEP)
    print(f"  Execution Sequence:")
    print(f"    1. Agent Initialisation      {fmt_time(t_init)}")
    print(f"    2. Keyword Search            {fmt_time(t_search)}")
    print(f"    3. Evidence Validation       {fmt_time(t_eval)}")
    print(f"    4. Rule Engine Evaluation    {fmt_time(t_eval)}")
    print(f"  Total Runtime:                {fmt_time(t_total)}")
    print()

    compliant = sum(1 for r in ctx2.evaluation_results if r.status.value == "COMPLIANT")
    non_compliant = sum(1 for r in ctx2.evaluation_results if r.status.value == "NON_COMPLIANT")
    na = sum(1 for r in ctx2.evaluation_results if r.status.value == "NOT_APPLICABLE")

    print(f"  Evaluation Results:")
    print(f"    合格 (COMPLIANT):      {compliant}")
    print(f"    不合格 (NON_COMPLIANT): {non_compliant}")
    print(f"    不适用 (NOT_APPLICABLE): {na}")
    print()

    # Enterprise evaluation
    ent = ctx2.metadata.get("enterprise_evaluation")
    if ent:
        print(f"  Enterprise Conclusion:")
        print(f"    {ent.overall_result}")
        print(f"    {ent.summary}")
        print()

    if ctx2.warnings:
        print("  System Warnings:")
        for w in ctx2.warnings:
            print(f"    - {w}")
    print(_SEP)


def _find_reg(entries, cp_id):
    for e in entries:
        if e.id == cp_id:
            return e
    return None


def _find_rule(rules, cp_id):
    expected = f"RR-{cp_id}"
    for r in rules:
        if r.rule_id == expected:
            return r
    return None


if __name__ == "__main__":
    main()
