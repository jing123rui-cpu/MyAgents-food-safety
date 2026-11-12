# Context Engine Report

**Date:** 2026-07-03

---

## Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?InspectionWorkflow鈹?     鈹? ContextEngine    鈹?     鈹? PromptEngine     鈹?鈹? (script/workflow)  鈹?鈹€鈹€鈫? 鈹? (script/ai/        鈹?鈹€鈹€鈫? 鈹? (script/ai/        鈹?鈹?                  鈹?     鈹?  context_engine) 鈹?     鈹?  prompt_engine)  鈹?鈹?build_context()   鈹?     鈹? build_context()  鈹?     鈹? build_*_prompt() 鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?     鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈹?                        鈹?                        鈹?         鈻?                        鈻?                        鈻?  InspectionContext          AIContext                  Prompt string
  (raw domain objects)       (formatted strings)         (ready for LLM)
```

**Layers:**

| Layer | Responsibility | Input | Output |
|-------|---------------|-------|--------|
| Workflow | Search, match, validate | `InspectionRequest` | `InspectionContext` (objects) |
| **ContextEngine** | Format, summarise, aggregate | `InspectionContext` | `AIContext` (strings) |
| PromptEngine | Template render | `AIContext` fields | Prompt string |

The ContextEngine is the bridge 鈥?it converts domain objects (`Checkpoint`, `RegistryEntry`, `RiskRule`, `TaxonomyNode`, `Evidence`, `EvaluationResult`) into human-readable strings that the PromptEngine can slot into templates.

---

## Data Flow

### Input: `InspectionContext`

```python
@dataclass
class InspectionContext:
    request: InspectionRequest
    matched_checkpoints: List[Checkpoint]
    matched_risk_rules: List[RiskRule]
    matched_registry_entries: List[RegistryEntry]
    matched_taxonomy_nodes: List[TaxonomyNode]
    evidence: List[Evidence]
    evaluation_results: List[EvaluationResult]
    warnings: List[str]
    metadata: Dict[str, Any]
```

### Processing

The `build_context()` method runs the following pipeline:

1. **Checkpoints** 鈥?format ID, name, risk level, objective
2. **Registry entries** 鈥?format ID, title, risk level, keywords
3. **Risk rules** 鈥?format rule ID, condition, risk level, description
4. **Taxonomy breadcrumb** 鈥?resolve domain/sub_domain IDs to node names, append category/subcategory
5. **Applicable laws** 鈥?collect all laws from registry entries, de-duplicate, preserve order
6. **Evidence summary** 鈥?count evidence items grouped by `EvidenceType`
7. **Risk level** 鈥?first checkpoint's risk level
8. **Inspector query** 鈥?from the original `InspectionRequest`

### Output: `AIContext`

```python
@dataclass
class AIContext:
    checkpoints: str          # formatted block
    registry_entries: str     # formatted block
    risk_rules: str           # formatted block
    taxonomy_path: str        # breadcrumb e.g. "A > B > C"
    applicable_laws: str      # bullet list, de-duplicated
    evidence_summary: str     # human-readable counts
    risk_level: str           # e.g. "H" or "High"
    inspector_query: str      # original search query
    metadata: Dict[str, Any]  # counts for introspection
```

---

## Sample Output

With real knowledge data (query="supplier"):

```
=== Inspector Query ===
supplier

=== Checkpoints ===
- CP-BEV-RM-001: 渚涘簲鍟嗙敓浜ц鍙瘉瀹℃煡 [H]
  Objective: 纭浼佷笟閲囪喘鐨勬墍鏈夐鍝佸師鏂欎緵搴斿晢鎸佹湁鏈夋晥鐨勯鍝佺敓浜ц鍙瘉...
- CP-BEV-RM-002: 渚涘簲鍟嗕骇鍝佹楠屾姤鍛婂鏌?[H]
  Objective: 纭渚涘簲鍟嗘彁渚涚殑姣忔壒鍘熸枡鍧囧叿鏈夊悎鏍肩殑浜у搧妫€楠屾姤鍛?..
- CP-BEV-RM-003: 渚涘簲鍟嗗噯鍏ヨ瘎浠疯褰曟鏌?[M]
  Objective: 纭浼佷笟鍦ㄥ紩鍏ユ柊渚涘簲鍟嗗墠宸叉寜鍒跺害瑙勫畾瀹屾垚鍑嗗叆璇勪环...
- CP-BEV-RM-004: 渚涘簲鍟嗗勾搴﹁瘎浠疯褰曟鏌?[M]
  Objective: 纭浼佷笟宸叉寜鍒跺害瑕佹眰瀵瑰悎鏍间緵搴斿晢杩涜瀹氭湡锛堝勾搴︼級璇勪环...
- CP-BEV-RM-005: 鍚堟牸渚涘簲鍟嗗悕褰曟牳鏌?[H]
  Objective: 纭浼佷笟鍏峰瀹屾暣鐨勫悎鏍间緵搴斿晢鍚嶅綍...

=== Registry Entries ===
- CP-BEV-RM-001: 渚涘簲鍟嗙敓浜ц鍙瘉瀹℃煡 (High)
  Keywords: supplier, license, SC, permit, qualification
- CP-BEV-RM-002: 渚涘簲鍟嗕骇鍝佹楠屾姤鍛婂鏌?(High)
  Keywords: supplier, COA, inspection report, test report, certificate
...

=== Taxonomy Breadcrumb ===
Raw Material Management > Supplier Management > 鍘熸枡绠＄悊 > 渚涘簲鍟嗚祫璐ㄥ鏍?
=== Applicable Laws ===
- 椋熷搧鐢熶骇璁稿彲绠＄悊鍔炴硶
- 椋熷搧瀹夊叏娉?- GB 14881

=== Evidence Summary ===
No evidence collected.

=== Risk Rules ===
- RR-CP-BEV-RM-001: 璁稿彲璇佸鍗颁欢涓庡師浠朵竴鑷翠笖鍦ㄦ湁鏁堟湡鍐?鈫?Critical
- RR-CP-BEV-RM-002: 妫€楠屾姤鍛婂畬鏁翠笖鍧囧悎鏍?鈫?Critical
...

=== Risk Level ===
H

=== Metadata ===
{
  "checkpoint_count": 5,
  "registry_count": 5,
  "risk_rule_count": 5,
  "taxonomy_node_count": 2,
  "evidence_count": 0,
  "evaluation_count": 0
}
```

### Evidence Summary (synthetic example)

```
Observations:
5

Documents:
3

Photos:
2

Measurements:
1
```

### Law Merging

Input registry entries:
- Entry A: `["Law A", "Law B", "Law C"]`
- Entry B: `["Law B", "Law D", "Law C"]`

Output:
```
- Law A
- Law B
- Law C
- Law D
```

Duplicates are removed; order of first appearance is preserved.

---

## Future Extensions

| Feature | How |
|---------|-----|
| **Multilingual breadcrumbs** | Use taxonomy `name_zh` / `name_en` fields when available |
| **Evaluation-aware context** | Surface `evaluation_results` alongside evidence in the summary |
| **Checkpoint details** | Include `inspection_methods` and `required_evidence` as structured text |
| **Cross-checkpoint aggregation** | Merge laws and risk rules across ALL matched checkpoints (already done) |
| **Scoring summary** | Calculate pass/fail rates from evaluation results |
| **Evidence attachment listing** | List attachment filenames from each evidence item |

---

## File Inventory

| File | Purpose |
|------|---------|
| `script/ai/context_engine.py` | `AIContext` dataclass + `ContextEngine` class |
| `reports/context_engine_report.md` | This report |

