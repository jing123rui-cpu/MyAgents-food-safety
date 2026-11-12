# Writing Engine Report

**Date:** 2026-07-03

---

## Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                    AuditWritingEngine                        鈹?鈹?                  (script/ai/writing_engine.py)                 鈹?鈹?                                                             鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹? 鈹?Nonconformity鈹傗啋鈹?Risk Analysis鈹傗啋鈹?Corrective Action  鈹?鈹?鈹? 鈹?             鈹? 鈹?             鈹? 鈹?                   鈹?鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹?                                                             鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹? 鈹俁egulation Ref    鈹傗啋鈹?Audit Conclusion鈹傗啋鈹?Full Report  鈹?鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?                       鈻?              鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?              鈹?  PromptEngine   鈹?              鈹?  (template +    鈹?              鈹?  placeholders)  鈹?              鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?                       鈻?              鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?              鈹?DeepSeekProvider 鈹?              鈹?  .chat()       鈹?              鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?                       鈻?              鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?              鈹?AuditWritingRes 鈹?              鈹?  (dataclass)   鈹?              鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

## Workflow

```
                     鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                     鈹?FoodAuditAgent  鈹?                     鈹?.inspect_ai()   鈹?                     鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?AIInspectionResult
                              鈻?                     鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                     鈹?AuditWritingEng 鈹?                     鈹?.generate_all() 鈹?                     鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?          鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?          鈻?                  鈻?                  鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?build_       鈹?  鈹?build_       鈹?  鈹?build_       鈹?  鈹?question_    鈹?  鈹?report_      鈹?  鈹?question_    鈹?  鈹?prompt()     鈹?  鈹?prompt()     鈹?  鈹?prompt()     鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈻?                 鈻?                 鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?  AI.chat()  鈹?  鈹?  AI.chat()  鈹?  鈹?  AI.chat()  鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?         鈻?                 鈻?                 鈻?  Nonconformity      Full Report         Risk Analysis
```

## Prompt Strategy

Each writing method uses a purpose-built question prompt via `PromptEngine.build_question_prompt()`:

| Method | Template | Question Focus |
|--------|----------|----------------|
| `generate_nonconformity()` | `question.md` | Violated requirement, observed condition, gap analysis |
| `generate_risk_analysis()` | `question.md` | Likelihood, severity, existing controls, risk rating |
| `generate_corrective_action()` | `question.md` | Root cause, immediate correction, preventive measure, owner, deadline |
| `generate_regulation_reference()` | `question.md` | Regulation name, article clause, relation to finding |
| `generate_audit_conclusion()` | `question.md` | Overall compliance, critical findings, pass/fail decision |
| `generate_full_report()` | `report.md` | Executive summary, scope, findings, non-conformities, recommendations, conclusion |

**System prompt** (shared across all calls):

> "You are a professional food safety audit report writer for beverage manufacturing. Write in precise, regulatory-compliant language. Be specific and actionable."

The context for each prompt is the consolidated `AIContext` (checkpoints, registry entries, risk rules, evidence, laws, taxonomy).

## Output Format

Each method returns raw text (markdown). The `AuditWritingResult` dataclass aggregates them:

```python
@dataclass
class AuditWritingResult:
    nonconformity: str        # Detailed nonconformity statement
    risk_analysis: str        # Risk likelihood/severity/rating
    regulation_reference: str # Specific regulation articles
    corrective_action: str    # Root cause + corrective actions
    audit_conclusion: str     # Overall audit verdict
    risk_level: str           # e.g. "H", "Medium", "Critical"
    score: float               # 0.0鈥?.0 confidence/severity
    metadata: dict             # timestamps, counts
```

### Example section (nonconformity)

```markdown
**Nonconformity NC-001 鈥?Supplier Qualification**

**Requirement:** GB 14881-2013 Section 7.2 requires that all food material
suppliers hold a valid Food Production License (椋熷搧鐢熶骇璁稿彲璇?.

**Observed Condition:** Supplier "ABC Ingredients Co." listed on the approved
supplier list does not have a valid production license on file. The most recent
license expired on 2025-06-30 and no renewal documentation was provided.

**Gap:** The facility failed to verify license validity before procurement.
Two purchase orders (PO-2026-0189, PO-2026-0214) were placed with this
supplier after the license expiry date.

**Evidence:** PO records, approved supplier list, expired license copy.
```

## Future Extensions

| Feature | Description |
|---------|-------------|
| **Multilingual output** | Prompt templates in `zh/`, `en/` for Chinese/English report generation |
| **Structured JSON output** | Instruct the model to return JSON instead of markdown for programmatic consumption |
| **Score aggregation** | Compute weighted audit score from multiple checkpoint results |
| **Corrective action tracking** | Assign CAPA numbers, track deadlines, link to evidence |
| **Regulation database lookup** | Cross-reference findings against a structured regulation database |
| **Report versioning** | Generate incremental reports for re-audits with delta highlighting |

## File Inventory

| File | Purpose |
|------|---------|
| `script/ai/writing_engine.py` | `AuditWritingEngine` (6 generators) + `AuditWritingResult` dataclass |
| `script/ai/__init__.py` | Re-exports `AuditWritingEngine`, `AuditWritingResult` |
| `demo_writing.py` | Standalone demo script |
| `reports/writing_engine_report.md` | This report |

