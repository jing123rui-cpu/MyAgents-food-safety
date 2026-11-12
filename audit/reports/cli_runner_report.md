# CLI Runner Report

## Files Created

| File | Purpose |
|------|---------|
| `main.py` | CLI entry point — parses args, dispatches to `FoodAuditAgent` |
| `reports/cli_runner_report.md` | This documentation |

---

## Supported Commands

### `python main.py health`

Show agent health and knowledge counts.

```
=====================================================
  Food Audit Agent
=====================================================
  Status:        READY

  Knowledge Loaded
    Registry:    25
    Checkpoints: 25
    Risk Rules:  25
    Taxonomy:    23
=====================================================
```

### `python main.py inspect --id CP-BEV-RM-001`

Inspect a single checkpoint by its ID.

```
=====================================================
  Food Audit Agent — Inspection
=====================================================
  Checkpoint:   CP-BEV-RM-001
  Title:        供应商生产许可证审查
  Domain:       原料管理
  Module:       供应商管理
  Objective:    确认企业采购的所有食品原料供应商持有有效的食品...
  Category:     原料管理
  Subcategory:  供应商资质审核
  Risk Level:   High
  Evidence Req: 供应商生产许可证复印件
  Laws:         食品生产许可管理办法, 食品安全法
  Risk Rule:    RR-CP-BEV-RM-001 (Critical)
  Condition:    许可证复印件与原件一致且在有效期内
  ---
=====================================================
```

### `python main.py inspect --query "供应商许可证"`

Keyword search across titles, registry keywords, and markdown body.
Results sorted by relevance.

```
=====================================================
  Food Audit Agent — Inspection
=====================================================
  Checkpoint:   CP-BEV-RM-001
  Title:        供应商生产许可证审查
  ...
  ---
  Checkpoint:   CP-BEV-RM-005
  Title:        合格供应商名录核查
  ...
  ---
=====================================================
```

### `python main.py inspect --category "原料贮存"`

Return all checkpoints in a registry category or subcategory.

### `python main.py inspect --risk High`

Return all checkpoints whose risk level is High (or Critical).

---

## Error Handling

| Scenario | Behaviour |
|----------|-----------|
| Unknown command | `food-audit-agent: error: argument command: invalid choice` |
| Unknown checkpoint | `"No matching checkpoints found."` + warnings |
| No search results | `"No matching checkpoints found."` |
| Missing knowledge dir | `"Initialisation failed: ..."` |
| No search criteria | `"Error: provide at least one search criterion"` |
| Loading errors | Prints error count and exits |

---

## Architecture

```
main.py  (CLI)
   │
   ├── argparse  (parse args)
   │
   ├── FoodAuditAgent(knowledge_dir)
   │   └── .initialize()
   │
   ├── dispatch:
   │   ├── health  → agent.health() → print counts
   │   └── inspect → agent.inspect(...) → print checkpoints
   │
   └── no business logic — only orchestrates core components
```

---

## Execution Flow

```
User
 │
 ├── python main.py health
 │       │
 │       └── FoodAuditAgent.initialize()
 │               │
 │               ├── KnowledgeLoader.load_all()
 │               ├── KnowledgeSearchEngine(repo)
 │               ├── InspectionWorkflow(repo, search, rules)
 │               └── RuleEngine(repo, rules)
 │
 ├── python main.py inspect --id CP-BEV-RM-001
 │       │
 │       └── FoodAuditAgent.inspect(checkpoint_id="CP-BEV-RM-001")
 │               │
 │               └── InspectionWorkflow.build_context(request)
 │                       │
 │                       ├── search_checkpoints (exact ID)
 │                       ├── lookup_registry
 │                       ├── lookup_risk_rules
 │                       └── lookup_taxonomy
 │
 └── python main.py inspect --query "supplier"
         │
         └── FoodAuditAgent.inspect(query="supplier")
                 │
                 └── InspectionWorkflow.build_context(request)
                         │
                         ├── search_keyword("supplier")
                         ├── lookup_registry
                         ├── lookup_risk_rules
                         └── lookup_taxonomy
```

---

## CLI Examples

```bash
# Health check
python main.py health

# Inspect by checkpoint ID
python main.py inspect --id CP-BEV-RM-013

# Keyword search
python main.py inspect --query "温湿度"

# Category search
python main.py inspect --category "原料贮存"

# Risk filter
python main.py inspect --risk High

# Custom knowledge directory
python main.py --knowledge-dir /path/to/knowledge health
```
