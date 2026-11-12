#!/usr/bin/env python3
"""Audit Writing Engine Demo — Sprint 31.

Demonstrates the full writing pipeline: inspection → AI → professional report.

Usage:
    set DEEPSEEK_API_KEY=sk-...
    python demo_writing.py
"""

from __future__ import annotations

import logging
import os
import sys

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

from script import FoodAuditAgent
from script.ai import AuditWritingEngine, PromptEngine


def main() -> None:
    # ── 1. Check API key ────────────────────────────────────────
    if not os.environ.get("DEEPSEEK_API_KEY", ""):
        print("No DEEPSEEK_API_KEY configured. Run with:")
        print("  set DEEPSEEK_API_KEY=sk-... && python demo_writing.py")
        sys.exit(1)

    print("=" * 60)
    print("  Sprint 31 — Audit Writing Engine Demo")
    print("=" * 60)

    # ── 2. Initialise agent ─────────────────────────────────────
    print("\n[1] Initialising FoodAuditAgent...")
    agent = FoodAuditAgent("knowledge")
    agent.initialize()

    health = agent.health()
    if health["ai_status"] != "AVAILABLE":
        print("  AI provider not available. Exiting.")
        sys.exit(1)

    # ── 3. Run AI inspection ────────────────────────────────────
    print("\n[2] Running AI inspection (query='supplier')...")
    insp_result = agent.inspect_ai(query="supplier")
    if not insp_result.success:
        print(f"  Inspection failed: {insp_result.error_message}")
        sys.exit(1)

    print(f"  Matched {insp_result.ai_context.metadata['checkpoint_count']} checkpoints")
    print(f"  Taxonomy: {insp_result.ai_context.taxonomy_path}")
    print(f"  AI Response: {insp_result.raw_response.content[:100] if insp_result.raw_response else 'N/A'}")

    # ── 4. Generate audit writing ───────────────────────────────
    print("\n[3] Generating professional audit writing...")
    provider = agent._ai_manager.get_provider("deepseek")
    engine = AuditWritingEngine(provider=provider)

    # Run all writing methods individually for demo clarity
    print("\n  --- Nonconformity / 不合格项描述 ---")
    nc = engine.generate_nonconformity(insp_result)
    print(f"  {nc[:500]}")
    print()

    print("  --- Risk Analysis / 风险分析 ---")
    ra = engine.generate_risk_analysis(insp_result)
    print(f"  {ra[:500]}")
    print()

    print("  --- Corrective Action / 纠正措施 ---")
    ca = engine.generate_corrective_action(insp_result)
    print(f"  {ca[:500]}")
    print()

    print("  --- Regulation Reference / 法规依据 ---")
    rr = engine.generate_regulation_reference(insp_result)
    print(f"  {rr[:500]}")
    print()

    print("  --- Audit Conclusion / 审计结论 ---")
    ac = engine.generate_audit_conclusion(insp_result)
    print(f"  {ac[:500]}")
    print()

    # ── 5. Full report (combined) ───────────────────────────────
    print("\n[4] Generating full audit report...")
    report = engine.generate_full_report(insp_result)
    print(f"\n  Full Report ({len(report)} chars):")
    print(f"  {report[:800]}")

    print(f"\n{'=' * 60}")
    print("  Demo complete / 演示完成")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
