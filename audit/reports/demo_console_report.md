# Sprint 40 — Executive Demonstration Console

## Overview

An interactive CLI for live demonstration of the food production enterprise
intelligent inspection agent.  Zero changes to core business logic — pure
presentation layer using `colorama` for terminal styling.

## File

| File | Purpose |
|---|---|
| `demo_console.py` | Main interactive console entry point |

## Dependencies

- `colorama >= 0.4.6` (added to `requirements.txt`)

## Console Structure (6 Parts)

### Part 1 — System Startup

```
============================================
  食品生产企业智能监督检查 Agent v1.0
============================================
```

Displays component readiness:
- System status
- Knowledge Loaded (checkpoint / registry count)
- Rule Engine Ready (risk rule count)
- Report Engine Ready
- AI Provider Status (Online / Offline)

### Part 2 — Enterprise Information Input

Prompts for:
- Enterprise name (default: XX食品饮料有限公司)
- Enterprise type (1: 普通食品 / 2: 饮料 / 3: 包装饮用水)
- Inspector name
- Inspection date (default: today)

Types map to internal tags:
- `1` → `general_food`
- `2` → `beverage`
- `3` → `packaged_water`

### Part 3 — On-Site Finding Input

Continuously accepts finding descriptions (one per line).
Enter `END` to finish.  Sample defaults if input is empty:

1. 供应商许可证过期
2. 生产记录填写不完整
3. 包装车间未设置防蝇设施

### Part 4 — Step-by-step Pipeline Display

| Step | Title | Implementation |
|---|---|---|
| Step 1 | 检查发现问题 | Lists all user-entered findings verbatim |
| Step 2 | 匹配 Checkpoint | Keyword search via `KnowledgeSearchEngine.search_keyword()`, fallback to sliding 2-char window |
| Step 3 | 匹配 Risk Rule | `RR-{checkpoint_id}` lookup in loaded risk rules |
| Step 4 | 自动引用法规依据 | `RegulationLoader.get_applicable_regulations()` for the selected enterprise type |
| Step 5 | RuleEngine 判定 | Per-evidence `EvaluationResult` with status + risk category (重点风险项 / 一般风险项) |
| Step 6 | 企业综合判定 | `EnterpriseEvaluation.overall_result` with visual block (green `#` for pass, red for rectification) |

### Part 5 — Report Generation

- Creates `AuditWritingEngine` (offline) → `generate_all_offline()`
- Exports via `ReportExporter.export_word()` to `reports/output/食品生产企业监督检查报告.docx`
- Auto-opens the generated file via `webbrowser.open()`

### Part 6 — Console Styling

- All output in Chinese
- `colorama` ANSI colours (green for success, red for failure, cyan for headers, yellow for steps)
- ASCII-only decorative characters for cross-platform compatibility (`=`, `-`, `#`, `*`)
- Government-information-system visual style with bordered headers and block highlights

## Architecture Notes

- Uses only public / internal APIs of `FoodAuditAgent`, `AuditWritingEngine`, `ReportExporter`
- No changes to `knowledge/`, `risk_rules/`, `registry/`, `RuleEngine`, `InspectionPipeline`, `WritingEngine`, `PromptEngine`, `ContextEngine`
- Finding-to-checkpoint matching: primary via `_search.search_keyword()`, fallback via 2-char sliding window
- Findings without a matching checkpoint are displayed as "未匹配到相关检查点" and skipped in evidence creation
- Risk level display: checkpoint `risk_level` "H" → 重点风险项, "M" → 一般风险项
- Rule risk level determines risk category for NON_COMPLIANT evaluations (Critical/High → 重点风险项, Medium → 一般风险项)
