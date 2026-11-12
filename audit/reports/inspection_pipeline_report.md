# Inspection Pipeline Report

**Date:** 2026-07-03

---

## Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                   InspectionPipeline                         鈹?鈹?               (script/ai/inspection_pipeline.py)               鈹?鈹?                                                             鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹愨攤
鈹? 鈹?Workflow 鈹傗啋鈫掆攤 ContextEngine鈹傗啋鈫掆攤 PromptEngine鈹傗啋鈫掆攤AI Prov鈹傗攤
鈹? 鈹?build_   鈹?  鈹?build_       鈹?  鈹?build_      鈹?  鈹?chat 鈹傗攤
鈹? 鈹?context()鈹?  鈹?context()    鈹?  鈹?inspect_    鈹?  鈹?     鈹傗攤
鈹? 鈹?         鈹?  鈹?             鈹?  鈹?prompt()    鈹?  鈹?     鈹傗攤
鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹攢鈹€鈹€鈹樷攤
鈹?      鈹?               鈹?                 鈹?            鈹?   鈹?鈹?      鈻?               鈻?                 鈻?            鈻?   鈹?鈹? Inspection      AIContext           Prompt          AIResp 鈹?鈹? Context         (strings)           (markdown)      (json) 鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                               鈹?                               鈻?                      AIInspectionResult
```

## Sequence Diagram

```
Agent               Pipeline              Workflow     ContextEng    PromptEng    AIProv
  鈹?                    鈹?                   鈹?            鈹?           鈹?          鈹?  鈹傗攢鈹€ inspect_ai() 鈹€鈹€鈫? 鈹?                   鈹?            鈹?           鈹?          鈹?  鈹?                    鈹傗攢鈹€ build_context()鈫? 鈹?            鈹?           鈹?          鈹?  鈹?                    鈹傗啇鈹€鈹€ InspectionCtx 鈹€鈹€ 鈹?            鈹?           鈹?          鈹?  鈹?                    鈹傗攢鈹€ build_context()鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈫?鈹?           鈹?          鈹?  鈹?                    鈹傗啇鈹€鈹€鈹€鈹€鈹€ AIContext 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ 鈹?           鈹?          鈹?  鈹?                    鈹傗攢鈹€ build_inspection_prompt()鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈫?鈹?           鈹?  鈹?                    鈹傗啇鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ Prompt 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ 鈹?           鈹?  鈹?                    鈹傗攢鈹€ chat(request)鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈫?鈹?  鈹?                    鈹傗啇鈹€鈹€鈹€鈹€鈹€鈹€ AIResponse 鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€ 鈹?  鈹?                    鈹?                   鈹?            鈹?           鈹?          鈹?  鈹傗啇鈹€鈹€ AIInspectionRes 鈹€鈹?                   鈹?            鈹?           鈹?          鈹?```

---

## Pipeline Description

### Step 1 鈥?`InspectionWorkflow.build_context(request)`

Accepts an `InspectionRequest` (query, checkpoint_id, category, risk_level). Uses the `KnowledgeSearchEngine` to retrieve matching checkpoints, then enriches them with registry entries, risk rules, and taxonomy nodes.

**Output:** `InspectionContext` with domain objects.

### Step 2 鈥?`ContextEngine.build_context(inspection_ctx)`

Converts domain objects into human-readable `AIContext` strings:
- Checkpoints formatted as a bullet list with ID, name, objective
- Registry entries with title, risk level, keywords
- Risk rules with condition and severity
- Taxonomy breadcrumb (domain > sub-domain > category > subcategory)
- Merged, de-duplicated applicable laws
- Evidence counts grouped by type
- Risk level and inspector query

### Step 3 鈥?`PromptEngine.build_inspection_prompt()`

Maps `AIContext` fields to the `inspection.md` template placeholders and renders a structured markdown prompt with sections: Role, Task, Checkpoint, Risk Rule, Evidence, Regulations, Expected Output.

### Step 4 鈥?`DeepSeekProvider.chat(request)`

Wraps the rendered prompt into an `AIRequest` and sends it to the DeepSeek API via `httpx`. Returns an `AIResponse` with content, model, usage, and finish reason.

### Step 5 鈥?Return

Wraps everything into an `AIInspectionResult` dataclass with all intermediate outputs plus latency, timestamp, and success status.

---

## Example Request

```python
from core import FoodAuditAgent

agent = FoodAuditAgent("knowledge")
agent.initialize()

result = agent.inspect_ai(query="supplier")
```

| Parameter | Value |
|-----------|-------|
| `query` | `"supplier"` |
| `checkpoint_id` | `""` |
| `category` | `""` |
| `risk_level` | `""` |

## Example Response

```python
AIInspectionResult(
    success=False,  # True if AI provider responds
    provider="deepseek",
    model="deepseek-chat",
    latency=0.001,   # seconds
    timestamp="2026-07-03T15:06:48",
    error_message="[RuntimeError] No AI provider available ...",
    prompt="# Role\nYou are a food safety audit AI assistant...",
    ai_context=AIContext(
        checkpoints="- CP-BEV-RM-001: 渚涘簲鍟嗙敓浜ц鍙瘉瀹℃煡 [H]\n...",
        taxonomy_path="Raw Material Management > Supplier Management > 鍘熸枡绠＄悊 > 渚涘簲鍟嗚祫璐ㄥ鏍?,
        applicable_laws="- 椋熷搧鐢熶骇璁稿彲绠＄悊鍔炴硶\n- 椋熷搧瀹夊叏娉昞n- GB 14881",
        risk_level="H",
        ...
    ),
)
```

### InspectionContext summary
| Field | Count |
|-------|-------|
| Matched checkpoints | 5 |
| Matched registry entries | 5 |
| Matched risk rules | 5 |
| Matched taxonomy nodes | 2 |

---

## Error Handling

The pipeline catches all exceptions at the top level and records them in `AIInspectionResult.error_message` rather than crashing.

| Scenario | `success` | `error_message` |
|----------|-----------|-----------------|
| No API key | `False` | `[RuntimeError] No AI provider available ...` |
| Invalid API key | `False` | `[AuthenticationError] DeepSeek API key ...` |
| Rate limited | `False` | `[RateLimitError] DeepSeek rate limit ...` |
| Network error | `False` | `[ProviderUnavailable] DeepSeek network error ...` |
| Successful call | `True` | `""` |

---

## File Inventory

| File | Purpose |
|------|---------|
| `script/ai/inspection_pipeline.py` | `InspectionPipeline` (166 lines) + `AIInspectionResult` dataclass |
| `script/agent.py` | `inspect_ai()` method on `FoodAuditAgent` |
| `demo_inspection_ai.py` | Standalone demo script |
| `reports/inspection_pipeline_report.md` | This report |

