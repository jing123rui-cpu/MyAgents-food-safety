#!/usr/bin/env python3
"""DeepSeek Provider Validation — Sprint 27.

Usage:
    set DEEPSEEK_API_KEY=sk-...
    python demo_ai.py

Output:
    Terminal validation log + reports/deepseek_validation_report.md
"""

from __future__ import annotations

import logging
import sys
import time
from pathlib import Path

logging.basicConfig(level=logging.WARNING, format="%(levelname)s: %(message)s")

from script import FoodAuditAgent
from script.ai.exceptions import (
    AuthenticationError,
    ProviderUnavailable,
    RateLimitError,
)
from script.ai.schemas import AIRequest, AIMessage

REPORT_PATH = Path("reports/deepseek_validation_report.md")


def main() -> None:
    results: dict = {
        "configuration": {},
        "startup": {},
        "response": {},
        "latency": {},
        "error_handling": {},
        "validation_result": "FAIL",
    }

    print("=" * 60)
    print("  Sprint 27 — DeepSeek Provider Validation")
    print("=" * 60)

    # ── Configuration ────────────────────────────────────────────
    import os

    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    results["configuration"]["DEEPSEEK_API_KEY"] = "SET" if api_key else "NOT SET"
    results["configuration"]["DEEPSEEK_BASE_URL"] = base_url
    results["configuration"]["DEEPSEEK_MODEL"] = os.environ.get(
        "DEEPSEEK_MODEL", "deepseek-chat"
    )

    print(f"\n  DEEPSEEK_API_KEY : {results['configuration']['DEEPSEEK_API_KEY']}")
    print(f"  DEEPSEEK_BASE_URL: {base_url}")

    # ── Task 1: Create & initialise agent ───────────────────────
    print("\n[1] Initialising FoodAuditAgent...")
    agent = FoodAuditAgent("knowledge")

    start_ts = time.monotonic()
    summary = agent.initialize()
    init_elapsed = time.monotonic() - start_ts

    health = agent.health()
    results["startup"]["agent_status"] = health["status"]
    results["startup"]["checkpoints"] = health["checkpoints"]
    results["startup"]["risk_rules"] = health["risk_rules"]
    results["startup"]["ai_providers"] = str(health["ai_providers"])
    results["startup"]["ai_status"] = health["ai_status"]
    results["startup"]["init_time_s"] = round(init_elapsed, 2)

    print(f"  Agent Status  : {health['status']}")
    print(f"  Checkpoints   : {health['checkpoints']}")
    print(f"  Risk Rules    : {health['risk_rules']}")
    print(f"  AI Providers  : {health['ai_providers']}")
    print(f"  AI Status     : {health['ai_status']}")

    # ── Check provider availability ──────────────────────────────
    provider_statuses = health.get("ai_providers", {})
    if not provider_statuses or all(
        s in ("DISABLED", "ERROR") for s in provider_statuses.values()
    ):
        print("\n  No API key configured.")
        results["validation_result"] = "SKIP — No API key configured"
        _write_report(results)
        sys.exit(0)

    # ── Task 2 & 3: Send request, print response ────────────────
    print("\n[2] Sending validation request...")

    provider = agent._ai_manager.get_provider("deepseek")

    request = AIRequest(
        messages=[AIMessage(role="user", content="Hello.")],
        system_prompt=(
            "You are a validation assistant. "
            "Reply with exactly:\n"
            "Food Audit Agent Connected.\n\n"
            "No explanation."
        ),
        temperature=0.0,
        max_tokens=50,
    )

    try:
        send_start = time.monotonic()
        response = provider.chat(request)
        elapsed = time.monotonic() - send_start

        results["response"]["raw_content"] = response.content
        results["response"]["model"] = response.model or "N/A"
        results["response"]["finish_reason"] = response.finish_reason
        results["response"]["usage"] = dict(response.usage)
        results["latency"]["response_time_s"] = round(elapsed, 2)
        results["latency"]["total_tokens"] = response.usage.get("total_tokens", 0)

        print("\n[3] Response Details")
        print(f"  Raw Content    : {response.content!r}")
        print(f"  Response Time  : {elapsed:.2f}s")
        print(f"  Provider Name  : {provider.provider_name}")
        print(f"  Model Name     : {response.model or 'N/A'}")
        print(f"  Finish Reason  : {response.finish_reason}")
        print(f"  Token Usage    : {response.usage}")

        # Verify expected reply
        expected = "Food Audit Agent Connected."
        if expected in response.content:
            print(f"\n  ✓ Reply contains expected text: {expected!r}")
            results["validation_result"] = "PASS"
        else:
            print(f"\n  ⚠ Reply did not contain expected text: {expected!r}")
            results["validation_result"] = "PASS (content mismatch)"

    except AuthenticationError as exc:
        print(f"\n  ✗ AuthenticationError: {exc}")
        results["error_handling"]["type"] = "AuthenticationError"
        results["error_handling"]["message"] = str(exc)
        results["validation_result"] = "FAIL — AuthenticationError"
    except RateLimitError as exc:
        print(f"\n  ✗ RateLimitError: {exc}")
        results["error_handling"]["type"] = "RateLimitError"
        results["error_handling"]["message"] = str(exc)
        results["validation_result"] = "FAIL — RateLimitError"
    except ProviderUnavailable as exc:
        msg = str(exc)
        if "timed out" in msg.lower():
            print(f"\n  ✗ Timeout: {exc}")
            results["error_handling"]["type"] = "Timeout"
            results["error_handling"]["message"] = msg
            results["validation_result"] = "FAIL — Timeout"
        else:
            print(f"\n  ✗ ProviderUnavailable: {exc}")
            results["error_handling"]["type"] = "ProviderUnavailable"
            results["error_handling"]["message"] = msg
            results["validation_result"] = "FAIL — ProviderUnavailable"
    except Exception as exc:
        print(f"\n  ✗ Unexpected Exception [{type(exc).__name__}]: {exc}")
        results["error_handling"]["type"] = type(exc).__name__
        results["error_handling"]["message"] = str(exc)
        results["validation_result"] = f"FAIL — {type(exc).__name__}"

    # ── Write report ─────────────────────────────────────────────
    _write_report(results)

    print(f"\n{'=' * 60}")
    print(f"  Validation Result: {results['validation_result']}")
    print(f"{'=' * 60}")


def _write_report(results: dict) -> None:
    """Write the validation report markdown file."""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    cfg = results["configuration"]
    startup = results["startup"]
    resp = results["response"]
    lat = results["latency"]
    err = results["error_handling"]

    lines = [
        "# DeepSeek Provider Validation Report",
        "",
        f"**Validation Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Python Version:** {sys.version.split()[0]}",
        "",
        "---",
        "",
        "## Configuration",
        "",
        f"| Variable | Value |",
        f"|----------|-------|",
        f"| `DEEPSEEK_API_KEY` | {cfg['DEEPSEEK_API_KEY']} |",
        f"| `DEEPSEEK_BASE_URL` | {cfg['DEEPSEEK_BASE_URL']} |",
        f"| `DEEPSEEK_MODEL` | {cfg.get('DEEPSEEK_MODEL', 'deepseek-chat')} |",
        "",
        "---",
        "",
        "## Startup",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Agent Status | `{startup['agent_status']}` |",
        f"| Checkpoints | `{startup['checkpoints']}` |",
        f"| Risk Rules | `{startup['risk_rules']}` |",
        f"| AI Providers | `{startup['ai_providers']}` |",
        f"| AI Status | `{startup['ai_status']}` |",
        f"| Init Time | `{startup['init_time_s']}s` |",
        "",
        "---",
        "",
        "## Response",
        "",
        "**Raw Content:**",
        "",
        "```",
        resp.get("raw_content", "N/A"),
        "```",
        "",
        "| Field | Value |",
        "|-------|-------|",
        f"| Model | `{resp.get('model', 'N/A')}` |",
        f"| Finish Reason | `{resp.get('finish_reason', 'N/A')}` |",
        f"| Usage | `{resp.get('usage', {})}` |",
        "",
        "## Latency",
        "",
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Response Time | `{lat.get('response_time_s', 'N/A')}s` |",
        f"| Total Tokens | `{lat.get('total_tokens', 'N/A')}` |",
        "",
        "---",
        "",
        "## Error Handling",
        "",
    ]
    if err:
        lines.extend(
            [
                f"| Exception | Message |",
                f"|-----------|---------|",
                f"| `{err.get('type', 'N/A')}` | `{err.get('message', 'N/A')}` |",
            ]
        )
    else:
        lines.append("No errors encountered during validation.")

    lines.extend(
        [
            "",
            "---",
            "",
            "## Validation Result",
            "",
            f"**{results['validation_result']}**",
            "",
        ]
    )

    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"\n  Report written → {REPORT_PATH}")


if __name__ == "__main__":
    main()
