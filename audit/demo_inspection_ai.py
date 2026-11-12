#!/usr/bin/env python3
"""AI Inspection Demo — Sprint 30.

Runs the full AI inspection pipeline end-to-end.

Usage:
    set DEEPSEEK_API_KEY=sk-...
    python demo_inspection_ai.py
"""

from __future__ import annotations

import logging
import os
import sys

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

from script import FoodAuditAgent
from script.ai.exceptions import AIProviderError
from script.workflow import InspectionRequest


def main() -> None:
    # ── 1. Check API key early ──────────────────────────────────
    if not os.environ.get("DEEPSEEK_API_KEY", ""):
        print("No DEEPSEEK_API_KEY configured. Run with:")
        print("  set DEEPSEEK_API_KEY=sk-... && python demo_inspection_ai.py")
        sys.exit(1)

    print("=" * 60)
    print("  Sprint 30 — AI Inspection Pipeline Demo")
    print("=" * 60)

    # ── 2. Initialise Agent ─────────────────────────────────────
    print("\n[1] Initialising FoodAuditAgent...")
    agent = FoodAuditAgent("knowledge")
    summary = agent.initialize()
    print(f"  Status      : {summary['status']}")
    print(f"  Checkpoints : {summary['checkpoints']}")
    print(f"  Risk Rules  : {summary['risk_rules']}")

    health = agent.health()
    print(f"  AI Status   : {health['ai_status']}")
    if health["ai_status"] != "AVAILABLE":
        print("  AI provider is not available. Exiting.")
        sys.exit(1)

    # ── 3. Run AI Inspection ────────────────────────────────────
    print("\n[2] Running AI inspection (query='supplier')...")
    try:
        result = agent.inspect_ai(query="supplier")
    except Exception as exc:
        print(f"  ✗ Pipeline error: [{type(exc).__name__}] {exc}")
        sys.exit(1)

    # ── 4. Print Results ────────────────────────────────────────
    print("\n[3] Results")

    # Matched checkpoint
    ic = result.inspection_context
    first_cp = ic.matched_checkpoints[0] if ic.matched_checkpoints else None
    if first_cp:
        print(f"\n  Matched Checkpoint:")
        print(f"    ID       : {first_cp.checkpoint_id}")
        print(f"    Name     : {first_cp.checkpoint_name}")
        print(f"    Domain   : {first_cp.domain}")

    # Risk level
    print(f"\n  Risk Level          : {result.ai_context.risk_level}")

    # Evidence summary
    print(f"\n  Evidence Summary:")
    print(f"    {result.ai_context.evidence_summary.replace(chr(10), chr(10) + '    ')}")

    # Taxonomy path
    print(f"  Taxonomy Path       : {result.ai_context.taxonomy_path}")

    # Generated prompt
    print(f"\n  Generated Prompt (first 600 chars):")
    print(f"    {result.prompt[:600].replace(chr(10), chr(10) + '    ')}")

    # AI response
    if result.raw_response:
        print(f"\n  AI Response:")
        print(f"    Content       : {result.raw_response.content[:300]}")
        print(f"    Finish Reason : {result.raw_response.finish_reason}")
        print(f"    Usage         : {result.raw_response.usage}")
    else:
        print(f"\n  AI Response        : N/A (no API response captured)")

    # Latency
    print(f"\n  Latency             : {result.latency}s")

    # Provider & model
    print(f"  Provider            : {result.provider or 'N/A'}")
    print(f"  Model               : {result.model or 'N/A'}")

    # Overall
    status = "PASS" if result.success else "FAIL"
    print(f"\n  Pipeline Status     : {status}")
    if result.error_message:
        print(f"  Error               : {result.error_message}")

    print(f"\n{'=' * 60}")


if __name__ == "__main__":
    main()
