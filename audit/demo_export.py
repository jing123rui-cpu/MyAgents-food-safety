#!/usr/bin/env python3
"""Sprint 39 — Regulatory Inspection Report v2.0 Demo (Online + Offline).

Demonstrates the full pipeline in two modes:
  - Online (AI):   inspect_ai() → generate_all() → export_word()
  - Offline (no AI): inspect()   → generate_all_offline() → export_word()

Both modes produce a formal 12-section regulatory inspection report with
enterprise-type-specific regulation references.

Usage:
    set DEEPSEEK_API_KEY=sk-... && python demo_export.py                         (online)
    python demo_export.py                                                          (offline, general_food)
    python demo_export.py --enterprise-type beverage                                (beverage enterprise)
    python demo_export.py --enterprise-type packaged_water                         (packaged water enterprise)
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

from script import FoodAuditAgent
from script.ai import AuditWritingEngine, PromptEngine
from script.ai.report_exporter import ReportExporter


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Food Audit Agent — Regulatory Inspection Report v2.0 Demo"
    )
    parser.add_argument(
        "--enterprise-type",
        default="general_food",
        choices=["general_food", "beverage", "packaged_water"],
        help="Enterprise type for regulation applicability matching",
    )
    parser.add_argument(
        "--knowledge-dir",
        default="knowledge",
        help="Path to the knowledge base directory",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("  Sprint 39 — Regulatory Inspection Report v2.0")
    print(f"  Enterprise type: {args.enterprise_type}")
    print("=" * 60)

    # ── 1. Initialise agent ─────────────────────────────────────
    print("\n[1] Initialising FoodAuditAgent...")
    agent = FoodAuditAgent(args.knowledge_dir)
    agent.initialize()

    health = agent.health()
    print(f"  Status: {health['status']}")
    print(f"  AI: {health['ai_status']}")

    # ── 2. Enterprise info ──────────────────────────────────────
    enterprise_info = {
        "facility_name": "XX食品饮料有限公司",
        "credit_code": "91440101MA5XXXXXXX",
        "license_number": "SC106440111XXXXX",
        "address": "XX省XX市XX区XX路XX号",
        "legal_representative": "张三",
        "food_safety_director": "李四",
        "audit_date": "2026-07-06",
        "audit_type": "日常监督",
        "auditor_name": "王五、赵六",
        "company_representative": "陈七",
    }

    # ── 3. Detect mode and run inspection ───────────────────────
    ai_available = health["ai_status"] == "AVAILABLE" and bool(os.environ.get("DEEPSEEK_API_KEY", ""))

    if ai_available:
        print("\n[2] AI available. Running online inspection...")
        insp_result = agent.inspect_ai(query="production process")
        if not insp_result.success:
            print(f"  AI inspection failed: {insp_result.error_message}")
            print("  Falling back to offline mode.")
            ai_available = False

    if not ai_available:
        print("\nAI unavailable. Using offline report generator.")
        print("\n[2] Running offline inspection...")
        inspection_ctx = agent.inspect(query="production process")
        print(f"  Matched {len(inspection_ctx.matched_checkpoints)} checkpoints")
        print(f"  Evaluation results: {len(inspection_ctx.evaluation_results)}")

    # ── 4. Generate audit writing ───────────────────────────────
    print("\n[3] Generating audit writing content...")

    if ai_available:
        provider = agent._ai_manager.get_provider("deepseek")
        engine = AuditWritingEngine(provider=provider)
        writing_result = engine.generate_all(insp_result)
        ctx = insp_result.inspection_context
        # Fill enterprise info into metadata
        writing_result.metadata.update(enterprise_info)
    else:
        engine = AuditWritingEngine()
        writing_result = engine.generate_all_offline(
            inspection_ctx,
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
            enterprise_type=args.enterprise_type,
            knowledge_dir=args.knowledge_dir,
        )
        ctx = inspection_ctx

    # Attach enterprise evaluation to writing result metadata
    ent = ctx.metadata.get("enterprise_evaluation")
    if ent:
        writing_result.metadata["enterprise_evaluation"] = ent
        print(f"  Enterprise conclusion: {ent.overall_result}")
    writing_result.metadata["facility_name"] = enterprise_info["facility_name"]

    # ── 5. Export to Word ───────────────────────────────────────
    print("\n[4] Exporting to Word document...")
    exporter = ReportExporter()

    export_result = exporter.export_word(writing_result)

    if export_result.success:
        print(f"  Report generated successfully.")
        print(f"  Filename: {export_result.filename}")
        print(f"  Path: {export_result.filepath}")
        print(f"\n  Opening Word document...")
        try:
            import webbrowser
            webbrowser.open(str(export_result.filepath))
        except Exception:
            print(f"  Report saved. Please open manually.")
    else:
        print(f"  Export failed: {export_result.error}")
        sys.exit(1)

    print(f"\n{'=' * 60}")
    print("  Demo complete.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
