"""Food Audit Agent — CLI entry point."""

from __future__ import annotations

import argparse
import logging
import sys

from script import FoodAuditAgent
from script.models import RegistryEntry, RiskRule

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s %(message)s",
)

_SEP = "=" * 53


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="food-audit-agent",
        description="Food safety audit inspection system",
    )
    parser.add_argument(
        "--knowledge-dir",
        default="knowledge",
        help="Path to the knowledge directory (default: knowledge)",
    )

    sub = parser.add_subparsers(dest="command", required=True)

    # ── health ───────────────────────────────────────────────────
    sub.add_parser("health", help="Show agent health status")

    # ── inspect ──────────────────────────────────────────────────
    insp = sub.add_parser("inspect", help="Run an inspection")
    insp.add_argument("--id", dest="checkpoint_id", help="Checkpoint ID (e.g. CP-BEV-RM-001)")
    insp.add_argument("--query", help="Keyword search")
    insp.add_argument("--category", help="Category name")
    insp.add_argument("--risk", dest="risk_level", help="Risk level (High, Medium, Low)")

    # ── RAG：本地语义检索 ────────────────────────────────────────
    rag_index = sub.add_parser("index", help="Build or update the semantic index")
    rag_index.add_argument("--force", action="store_true", help="Rebuild every chunk")
    rag_index.add_argument(
        "--scope", nargs="+", default=["knowledge", "skills"],
        choices=["knowledge", "skills", "repo"],
    )

    rag_search = sub.add_parser("search", help="Semantic search over knowledge and skills")
    rag_search.add_argument("query")
    rag_search.add_argument("-k", type=int, default=5, help="Number of results")
    rag_search.add_argument("--scope", default="all", choices=["all", "knowledge", "skills"])
    rag_search.add_argument("--json", action="store_true")

    sub.add_parser("rag-status", help="Show semantic index status")

    args = parser.parse_args()

    if args.command in ("index", "search", "rag-status"):
        from script import rag
        return rag.main(_rag_argv(args))

    # ── Agent initialisation ─────────────────────────────────────
    try:
        agent = FoodAuditAgent(args.knowledge_dir)
        summary = agent.initialize()
    except Exception as exc:
        print(_SEP)
        print("  Food Audit Agent")
        print(_SEP)
        print(f"  Initialisation failed: {exc}", file=sys.stderr)
        sys.exit(1)

    if summary["errors"]:
        print(_SEP)
        print("  Food Audit Agent")
        print(_SEP)
        print(f"  Errors during loading: {summary['errors']}")
        print(_SEP)
        sys.exit(1)

    # ── Dispatch ─────────────────────────────────────────────────
    if args.command == "health":
        _cmd_health(agent)
    elif args.command == "inspect":
        _cmd_inspect(agent, args)
    else:
        print(f"Unknown command: {args.command}")
        sys.exit(1)


# ── Health Command ───────────────────────────────────────────────

def _cmd_health(agent: FoodAuditAgent) -> None:
    status = agent.health()
    print(_SEP)
    print("  Food Audit Agent")
    print(_SEP)
    print(f"  Status:        {status['status']}")
    print()
    print("  Knowledge Loaded")
    print(f"    Registry:    {status['registry']}")
    print(f"    Checkpoints: {status['checkpoints']}")
    print(f"    Risk Rules:  {status['risk_rules']}")
    print(f"    Taxonomy:    {status['taxonomy_nodes']}")
    if status["warnings"]:
        print(f"    Warnings:    {status['warnings']}")
    if status["errors"]:
        print(f"    Errors:      {status['errors']}")
    print(_SEP)


# ── Inspect Command ──────────────────────────────────────────────

def _cmd_inspect(agent: FoodAuditAgent, args: argparse.Namespace) -> None:
    kwargs = {}
    for key in ("checkpoint_id", "query", "category", "risk_level"):
        val = getattr(args, key, None)
        if val:
            kwargs[key] = val

    if not kwargs:
        print("Error: provide at least one search criterion (--id, --query, --category, --risk)")
        sys.exit(1)

    try:
        ctx = agent.inspect(**kwargs)
    except Exception as exc:
        print(f"  Inspection failed: {exc}", file=sys.stderr)
        sys.exit(1)

    checkpoints = ctx.matched_checkpoints
    registry = ctx.matched_registry_entries
    rules = ctx.matched_risk_rules
    warnings = ctx.warnings

    if not checkpoints:
        print(_SEP)
        print("  Food Audit Agent — Inspection")
        print(_SEP)
        print("  No matching checkpoints found.")
        if warnings:
            print()
            for w in warnings:
                print(f"  Warning: {w}")
        print(_SEP)
        return

    print(_SEP)
    print("  Food Audit Agent — Inspection")
    print(_SEP)

    for cp in checkpoints:
        reg = _find_registry(registry, cp.checkpoint_id)
        rule = _find_rule(rules, cp.checkpoint_id)

        print(f"  Checkpoint:   {cp.checkpoint_id}")
        print(f"  Title:        {cp.checkpoint_name}")
        if cp.domain:
            print(f"  Domain:       {cp.domain}")
        if cp.module:
            print(f"  Module:       {cp.module}")
        if cp.objective:
            print(f"  Objective:    {cp.objective[:80]}{'...' if len(cp.objective) > 80 else ''}")

        if reg:
            print(f"  Category:     {reg.category or ''}")
            if reg.subcategory:
                print(f"  Subcategory:  {reg.subcategory}")
            print(f"  Risk Level:   {reg.risk_level or ''}")
            if reg.evidence_required:
                print(f"  Evidence Req: {', '.join(reg.evidence_required)}")
            if reg.laws:
                print(f"  Laws:         {', '.join(reg.laws)}")
        else:
            print(f"  Risk Level:   {cp.risk_level or ''}")

        if rule:
            print(f"  Risk Rule:    {rule.rule_id} ({rule.risk_level})")
            if rule.condition:
                print(f"  Condition:    {rule.condition[:80]}")

        print(f"  ---")

    if warnings:
        print()
        print("  Warnings:")
        for w in warnings:
            print(f"    - {w}")

    print(_SEP)


# ── Helpers ──────────────────────────────────────────────────────

def _rag_argv(args: argparse.Namespace) -> list[str]:
    if args.command == "index":
        argv = ["index", "--scope", *args.scope]
        if args.force:
            argv.append("--force")
        return argv
    if args.command == "search":
        argv = ["search", args.query, "-k", str(args.k), "--scope", args.scope]
        if args.json:
            argv.append("--json")
        return argv
    return ["status"]


def _find_registry(entries: list[RegistryEntry], cp_id: str) -> RegistryEntry | None:
    for e in entries:
        if e.id == cp_id:
            return e
    return None


def _find_rule(rules: list[RiskRule], cp_id: str) -> RiskRule | None:
    expected = f"RR-{cp_id}"
    for r in rules:
        if r.rule_id == expected:
            return r
    return None


if __name__ == "__main__":
    raise SystemExit(main() or 0)
