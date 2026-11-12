# Rule Engine Report

## Files Created / Modified

| File | Change |
|------|--------|
| `script/models.py` | Added `EvaluationStatus` enum, `EvaluationResult` dataclass |
| `script/rule_engine.py` | **Created** 鈥?`RuleEngine` class |
| `script/workflow.py` | Added `evaluation_results` field to `InspectionContext` |
| `script/__init__.py` | Exported `RuleEngine`, `EvaluationResult`, `EvaluationStatus` |

---

## Evaluation Statuses

```python
class EvaluationStatus(str, Enum):
    PASS            = "PASS"
    WARNING         = "WARNING"
    FAIL            = "FAIL"
    NOT_APPLICABLE  = "NOT_APPLICABLE"
```

---

## EvaluationResult Model

```python
@dataclass
class EvaluationResult:
    checkpoint_id: str
    rule_id: str
    evidence_id: str
    status: EvaluationStatus
    score: float        # 1.0 PASS, 0.5 WARNING, 0.0 FAIL
    reason: str
    violated_laws: List[str]
    recommendation: str
    metadata: Dict[str, Any]
```

---

## Rule Execution Flow

```
Evidence (checkpoint_id, description, attachments)
      鈹?      鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?1. Locate Checkpoint 鈹?鈹?   repository.checkpoints[id]           鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?found?
       鈹溾攢鈹€ No  鈫?NOT_APPLICABLE (unknown checkpoint)
       鈹?       鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?2. Locate Risk Rule  鈹?鈹?   Precomputed index 鈹?鈹?   checkpoint_id 鈫?List[RiskRule]        鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?found?
       鈹溾攢鈹€ No  鈫?NOT_APPLICABLE (no rule)
       鈹?       鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?3. Execute Deterministic     鈹?鈹?   Rule Logic                鈹?鈹?                             鈹?鈹? 鈹屸攢 Empty description? 鈹€鈹€鈫?WARNING (score 0.5)                    鈹?鈹? 鈹溾攢 Critical/High + no attachments? 鈹€鈹€鈫?FAIL (score 0.0)          鈹?鈹? 鈹溾攢 Medium + incomplete?    鈹€鈹€鈫?WARNING (score 0.5)               鈹?鈹? 鈹斺攢 All satisfied           鈹€鈹€鈫?PASS (score 1.0)                  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?       鈹?       鈻? EvaluationResult
```

---

## Evaluation Lifecycle

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?Evidence 鈹傗攢鈹€鈹€鈹€鈻垛攤  RuleEngine  鈹傗攢鈹€鈹€鈹€鈻垛攤  Evaluation   鈹?鈹?(single) 鈹?    鈹? evaluate()  鈹?    鈹?  Result     鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?Evidence     鈹傗攢鈹€鈹€鈹€鈻垛攤  RuleEngine  鈹傗攢鈹€鈹€鈹€鈻垛攤 List[Evaluation] 鈹?鈹?Collection   鈹?    鈹?evaluate_all 鈹?    鈹?    Result       鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?    鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                              鈹?                              鈻?                     InspectionContext
                     evaluation_results
```

---

## Severity Thresholds

| Risk Level | Logic | Default Status |
|-----------|-------|---------------|
| `Critical` | Attachments required | FAIL if missing |
| `High` | Attachments required | FAIL if missing |
| `Medium` / `Moderate` | Description + optional attachments | WARNING if incomplete |
| `Low` / `Info` | Soft check | PASS |

---

## Validation (warnings collected during `evaluate_all`)

| Check | Condition | Warning |
|-------|-----------|---------|
| Missing checkpoint | `evidence.checkpoint_id` not in repository | `"Evidence '{id}' references unknown checkpoint '{cp}'"` |
| Missing rule | No risk rule indexed for checkpoint | `"No risk rule found for checkpoint '{cp}'"` |

---

## Error Handling

| Scenario | Status | Score | Result |
|----------|--------|-------|--------|
| Unknown checkpoint | `NOT_APPLICABLE` | 0.0 | Graceful skip |
| No risk rule found | `NOT_APPLICABLE` | 0.0 | Graceful skip |
| Empty evidence description | `WARNING` | 0.5 | Deterministic |
| Critical/High + no attachments | `FAIL` | 0.0 | Deterministic |
| All valid | `PASS` | 1.0 | Deterministic |

---

## Workflow Integration

```python
from core.rule_engine import RuleEngine

# Create engine
engine = RuleEngine(repository=repo, risk_rules=risk_rules)

# Evaluate single evidence
result = engine.evaluate(evidence)

# Evaluate all evidence
results = engine.evaluate_all(context.evidence)

# Store in context
context.evaluation_results = results

# Check warnings
for w in engine.warnings:
    logger.warning(w)
```

---

## Future Extensibility

| Feature | Description |
|---------|-------------|
| **Custom rule logic** | Replace `_apply_rule` with pluggable strategy functions |
| **Weighted scoring** | Support per-rule score weights from `RiskRule` metadata |
| **Rule chaining** | Evaluate multiple rules per checkpoint and aggregate results |
| **Evidence sufficiency** | Check that all `required_evidence` from `RegistryEntry` are present |
| **AI-assisted evaluation** | Pass evidence + rule context to an LLM for natural-language reasoning |

