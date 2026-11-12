# Risk Rule Design Standard 鈥?Production Process

**Version:** 1.0
**Date:** 2026-07-03
**Domain:** Production Process Management (`production_process_management`)

---

## 1. Risk Rule Purpose

Risk rules provide deterministic evaluation logic for audit evidence. Each rule:

- Maps inspection evidence to a **PASS / WARNING / FAIL** status
- Assigns a **risk level** that drives scoring and recommendations
- References **regulatory basis** for compliance traceability
- Enables the `RuleEngine` to operate without AI or LLM inference

Rules are stored as individual YAML files under:
```
knowledge/risk_rules/beverage/production_process/
```

Named following the convention:
```
RR-CP-BEV-PP-NNN.yaml
```

---

## 2. Risk Level Definition

All Production Process risk rules use one of four risk levels, consistent with Raw Material rules:

| Code | Level | Rule Engine Severity | Score Impact | Meaning |
|------|-------|---------------------|--------------|---------|
| RISK-01 | **Critical** | `_SEVERITY_FAIL` | 0.0 | Product safety or legal non-compliance |
| RISK-02 | **High** | `_SEVERITY_FAIL` | 0.0 | Systemic process failure |
| RISK-03 | **Medium** | `_SEVERITY_WARN` | 0.5 | Isolated or procedural gap |
| RISK-04 | **Low** | `_SEVERITY_PASS` | 1.0 | Minor observation, no material risk |

### 2.1 Assignment Rules

| Checkpoint Risk Level | Rule Risk Level | Condition |
|-----------------------|-----------------|-----------|
| H (High) | 鈫?Critical or High | H checkpoints map to RISK-01 or RISK-02 |
| M (Medium) | 鈫?Medium or Low | M checkpoints map to RISK-03 or RISK-04 |

### 2.2 Severity Thresholds (RuleEngine)

```python
_SEVERITY_FAIL = {"Critical", "High"}    # No attachments 鈫?FAIL
_SEVERITY_WARN = {"Medium", "Moderate"}  # No attachments 鈫?WARNING
_SEVERITY_PASS = {"Low", "Info"}         # Always PASS with caveat
```

---

## 3. YAML Schema

Every Production Process risk rule file must follow this structure:

```yaml
id: RR-CP-BEV-PP-NNN
checkpoint_id: CP-BEV-PP-NNN
title: <checkpoint_name from metadata>
version: "1.0"
domain: <sub-domain name_zh from taxonomy>
category: <category name_zh from taxonomy>
risk_level: Critical | High | Medium | Low
purpose: <inspection objective>

decision_logic:
  - condition: <deterministic condition 1>
    result: PASS
  - condition: <deterministic condition 2>
    result: WARNING
    severity: Low | Medium | High
  - condition: <deterministic condition 3>
    result: FAIL
    severity: Critical | High

required_evidence:
  - <mandatory evidence item 1>
  - <mandatory evidence item 2>

pass_condition: <single sentence describing PASS>
fail_condition: <single sentence describing FAIL>
warning_condition: <single sentence describing WARNING>

legal_basis:
  - REG-GB-14881
  - REG-FOOD-SAFETY-LAW

risk_description: <short description of the risk scenario>

typical_nonconformities:
  - <common finding 1>
  - <common finding 2>

recommended_actions:
  - 鏌ヨ瘉: <finding description> 鈥?<recommended action>

output_template:
  status: PASS / WARNING / FAIL
  reason: ""
  risk_level: <risk_level>
  laws:
    - REG-GB-14881
    - REG-FOOD-SAFETY-LAW
  recommendation: ""
```

### 3.1 Field Descriptions

| Field | Required | Type | Rules |
|-------|----------|------|-------|
| `id` | Yes | string | Format: `RR-CP-BEV-PP-NNN`. Must be unique. |
| `checkpoint_id` | Yes | string | Must match an existing CP-BEV-PP-NNN |
| `title` | Yes | string | Must match `checkpoint_name` from the checkpoint metadata |
| `version` | Yes | string | Semantic version, start at "1.0" |
| `domain` | Yes | string | Use Chinese name_zh from taxonomy sub-domain |
| `category` | Yes | string | Use Chinese name_zh from taxonomy category |
| `risk_level` | Yes | enum | One of: Critical, High, Medium, Low |
| `purpose` | Yes | string | Copied from checkpoint Inspection Objective |
| `decision_logic` | Yes | list | At least 2 entries, at most 6. Each must have `condition` + `result`. WARNING/FAIL results must have `severity`. |
| `required_evidence` | Yes | list | Must reference mandatory evidence items from the checkpoint |
| `pass_condition` | Yes | string | Deterministic condition for PASS |
| `fail_condition` | Yes | string | Deterministic condition for FAIL |
| `warning_condition` | Yes | string | Deterministic condition for WARNING |
| `legal_basis` | Yes | list | At least 1 REG- reference from the checkpoint |
| `risk_description` | Yes | string | Short summary of the risk scenario |
| `typical_nonconformities` | Yes | list | At least 2 common findings |
| `recommended_actions` | Yes | list | At least 2 recommended actions |
| `output_template` | Yes | dict | Standard output structure |

---

## 4. Evaluation Logic

### 4.1 RuleEngine Pipeline

```
Evidence
  鈫?Locate Checkpoint (via evidence.checkpoint_id)
  鈫?Locate Risk Rule (via RR-{checkpoint_id} naming)
  鈫?Check description (empty 鈫?WARNING)
  鈫?Check attachments:
      - Critical/High + no attachments 鈫?FAIL
      - Medium + no attachments + has description 鈫?WARNING
      - Low/Info 鈫?PASS
  鈫?Return EvaluationResult with status + score + violated laws
```

### 4.2 Decision Logic Conditions

Each `decision_logic` entry defines a scenario that maps to a result:

| Result | Meaning | Condition Examples |
|--------|---------|-------------------|
| PASS | Evidence satisfies the requirement | "鍙傛暟璁板綍瀹屾暣涓斿潎鍦ㄦ爣鍑嗚寖鍥村唴" |
| WARNING | Evidence partially meets requirements | "鍙傛暟璁板綍瀹屾暣浣嗘湁杞诲井涓嶈鑼? |
| FAIL | Evidence fails to meet requirements | "鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿涓旀棤绾犳鎺柦" |

**WARNING and FAIL** entries must include a `severity` field.

### 4.3 PASS / WARNING / FAIL Rules

| Category | PASS Condition | WARNING Condition | FAIL Condition |
|----------|---------------|-------------------|----------------|
| Process Control | All parameters within spec | Parameters recorded but minor deviations exist | Parameter out of spec with no corrective action |
| Equipment | Equipment verified and calibrated | Verification done but incomplete or overdue | No verification performed; safety devices disabled |
| Online Inspection | Detector working, sensitivity verified | Sensitivity verification frequency insufficient | Detector bypassed or sensitivity failed |
| Material Transfer | All containers labeled, records match | Labels present but incomplete | Unlabeled containers; cross-contamination risk |
| Semi-finished | Hold times within limit, conditions met | Hold time exceeded but product segregated | Hold time exceeded, product used without evaluation |
| Process Monitoring | All monitoring performed per plan | Frequency gaps but data available | No monitoring performed; data falsified |
| Time/Temperature | All values within spec, recorders calibrated | Minor deviation documented with corrective action | Critical deviation (e.g., under-sterilization) |
| Changeover | Clearance complete, first article passed | Clearance done but undocumented | Cross-contamination risk from incomplete clearance |
| Batch Records | Records complete, logical, accurate | Records complete but with minor errors | Missing records or logical inconsistencies |
| Product ID | All materials labeled with status | Labels present but incomplete | Unlabeled materials in production |
| Batch Control | Unique batch numbers, full traceability | Coding rule exists but traceability incomplete | Duplicate batches or broken traceability |
| Critical Records | All critical steps recorded and reviewed | Records exist but missing reviewer signature | Key process steps not recorded |
| Deviation | All deviations recorded and investigated | Deviation recorded but root cause incomplete | Deviation hidden or product disposition unknown |
| Line Clearance | Clearance complete, verified by second person | Clearance recorded but not verified | Residual material found; clearance record falsified |
| Shutdown Recovery | Full recovery checklist completed and verified | Recovery done but checklist incomplete | Production restarted without recovery check |
| Process Validation | Validation current, parameters match | Validation exists but expired or parameter drift | No validation or production outside validated range |
| Sampling | Sampling per plan, samples identified and stored | Sampling done but storage condition deviation | Sampling not performed or samples unidentifiable |
| In-Process Inspection | All inspections performed per plan | Inspection done but frequency insufficient | No inspection performed; failed results ignored |
| Process Review | All critical operations independently reviewed | Review done but reviewer is same as operator | No review performed for critical operations |
| Production Compliance | All operations match approved documentation | Minor undocumented process optimizations | Unauthorized process changes or outdated documents |

---

## 5. Evidence Dependency Rules

| Rule | Logic |
|------|-------|
| **Mandatory evidence missing** | If a required evidence item is not collected, the rule engine cannot PASS. Result: PENDING until evidence is provided. |
| **Empty description** | Any evidence with empty `description` field 鈫?WARNING (score 0.5). |
| **No attachments (Critical/High)** | If risk_level is Critical or High and evidence has no attachments 鈫?FAIL (score 0.0). |
| **No attachments (Medium)** | If risk_level is Medium, evidence has a description but no attachments 鈫?WARNING (score 0.5). |
| **All requirements satisfied** | Evidence has description + attachments (if required) 鈫?PASS (score 1.0). |

### 5.1 Evidence-to-Rule Mapping

Each risk rule's `required_evidence` field must reference the **蹇呴』** (mandatory) evidence items from the checkpoint's Required Evidence table (Section 鈶?. Optional evidence items (鏄惁蹇呴』 = 鍙€? may be referenced but are not required for a PASS.

---

## 6. Regulatory Mapping Rules

### 6.1 Law Codes

| Code | Full Name |
|------|-----------|
| `REG-GB-14881` | GB 14881 鈥?椋熷搧瀹夊叏鍥藉鏍囧噯 椋熷搧鐢熶骇閫氱敤鍗敓瑙勮寖 |
| `REG-FOOD-SAFETY-LAW` | 涓崕浜烘皯鍏卞拰鍥介鍝佸畨鍏ㄦ硶 |
| `REG-PRODUCE-MEASURE` | 椋熷搧鐢熶骇璁稿彲绠＄悊鍔炴硶 |

### 6.2 Mapping Convention

- Every Production Process checkpoint references `REG-GB-14881` and `REG-FOOD-SAFETY-LAW`
- These two laws are the **minimum** `legal_basis` for every PP risk rule
- No PP rule should deviate from this baseline unless the checkpoint explicitly references additional laws
- The `legal_basis` field in the rule file maps directly to `REG-` codes from the checkpoint's Regulatory Reference section

---

## 7. Risk Pattern Matrix

| Checkpoint Category | Risk Pattern | Typical Trigger | Default Risk Level |
|---------------------|-------------|-----------------|-------------------|
| 宸ヨ壓鍙傛暟鐩戞帶 (Process Control) | Parameter deviation risk | Temperature/pressure/flow outside spec | Critical / High |
| 杩囩▼璁板綍 (Records) | Compliance risk | Missing data, logical errors, unauthorized changes | High |
| 杩囩▼鍋忓樊澶勭悊 (Deviation) | Contamination / systemic failure | Product disposition unknown, root cause missing | Critical |
| 杩囩▼楠岃瘉 (Verification) | Validation failure / sampling gap | No validation, expired validation, insufficient sampling | High |

### 7.1 Per-Checkpoint Risk Mapping

| Checkpoints | Risk Pattern | Evaluation Focus |
|-------------|-------------|-----------------|
| PP-001 ~ PP-008 | Parameter deviation | Process control integrity, parameter record accuracy |
| PP-009 ~ PP-012 | Compliance / records | Data integrity, traceability, record completeness |
| PP-013 ~ PP-015 | Deviation / contamination | Corrective action effectiveness, product safety |
| PP-016 ~ PP-020 | Verification gap | Process validation, sampling control, regulatory compliance |

---

## 8. Rule Generation Guidelines

### 8.1 Determinism Rules

1. **Every condition must be objectively verifiable.** No subjective terms like "reasonable", "sufficient", "adequate" without definition.
2. **Every condition must be mappable to boolean logic.** The RuleEngine must be able to evaluate PASS/WARNING/FAIL without human judgment.
3. **No LLM or AI inference.** Rules must produce identical results given identical input.

### 8.2 Vague Terms 鈥?Prohibited

| 鉂?Prohibited | 鉁?Replacement |
|---------------|----------------|
| "adequate documentation" | "at least 3 batch records per quarter" |
| "reasonable evidence" | "evidence with non-empty description and at least 1 attachment" |
| "sufficient inspection" | "inspection performed at minimum frequency defined in monitoring plan" |
| "appropriate action" | "deviation report completed with root cause analysis and corrective action plan" |

### 8.3 Inspection Behavior Alignment

Each `decision_logic` condition in the rule must map to at least one inspection step from the checkpoint's Section 鈶?(Inspection Method). For example:

| Decision Logic Condition | Corresponding Inspection Step |
|-------------------------|-------------------------------|
| "鍙傛暟璁板綍瀹屾暣涓斿潎鍦ㄦ爣鍑嗚寖鍥村唴" | Step 3: 璁板綍鏍告煡 鈥?鏍稿宸ヨ壓鍙傛暟璁板綍 |
| "鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿涓旀棤绾犳鎺柦" | Step 4: 璁板綍鏍告煡 鈥?妫€鏌ュ弬鏁板紓甯告椂鏄惁鏈夊亸宸褰?|

### 8.4 Naming Convention

```
Rule ID:   RR-CP-BEV-PP-NNN
Directory: knowledge/risk_rules/beverage/production_process/RR-CP-BEV-PP-NNN.yaml
```

### 8.5 Validation Checklist

Before a rule can be committed, verify:

- [ ] `id` matches `RR-{checkpoint_id}` format
- [ ] `checkpoint_id` exists in registry
- [ ] `risk_level` is consistent with checkpoint's registry risk_level
- [ ] `decision_logic` contains at least 1 PASS, 1 WARNING, and 1 FAIL condition
- [ ] WARNING/FAIL entries have `severity` field
- [ ] `required_evidence` items exist in checkpoint's Section 鈶?- [ ] `legal_basis` contains at least `REG-GB-14881` and `REG-FOOD-SAFETY-LAW`
- [ ] File exists at `knowledge/risk_rules/beverage/production_process/RR-CP-BEV-PP-NNN.yaml`
- [ ] Loader loads the rule without errors
- [ ] RuleEngine evaluates sample evidence against the rule

---

## 9. Example Risk Rule 鈥?CP-BEV-PP-001

```yaml
id: RR-CP-BEV-PP-001
checkpoint_id: CP-BEV-PP-001
title: 宸ヨ壓鍙傛暟鎺у埗
version: "1.0"
domain: 鐢熶骇杩囩▼鎺у埗
category: 宸ヨ壓鍙傛暟鐩戞帶
risk_level: Critical
purpose: 纭鐢熶骇杩囩▼涓叧閿伐鑹哄弬鏁帮紙娓╁害銆佸帇鍔涖€佹椂闂淬€佹祦閲忋€乸H鍊肩瓑锛?         琚湁鏁堢洃鎺у拰璁板綍锛屽弬鏁版帶鍒跺湪宸ヨ壓鏍囧噯鑼冨洿鍐咃紝纭繚浜у搧璐ㄩ噺绋冲畾銆?
decision_logic:
  - condition: 鍙傛暟璁板綍瀹屾暣涓斿潎鍦ㄦ爣鍑嗚寖鍥村唴
    result: PASS
  - condition: 鍙傛暟璁板綍瀹屾暣浣嗘湁杞诲井涓嶈鑼冿紙濡備釜鍒瑪璇級
    result: WARNING
    severity: Low
  - condition: 鍙傛暟璁板綍缂哄け鎴栦笌浠〃鏄剧ず涓嶄竴鑷?    result: WARNING
    severity: High
  - condition: 鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿涓斿凡閲囧彇绾犳鎺柦
    result: WARNING
    severity: Medium
  - condition: 鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿涓旀棤绾犳鎺柦
    result: FAIL
    severity: Critical

required_evidence:
  - 宸ヨ壓鏍囧噯鏂囦欢
  - 鐢熶骇鍙傛暟璁板綍锛?鎵规锛?
pass_condition: 鍙傛暟鍏ㄧ▼鍙楁帶銆佽褰曞畬鏁村噯纭?fail_condition: 鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿涓旀棤绾犳鎺柦
warning_condition: 鍙傛暟璁板綍缂哄け鎴栦笌浠〃涓嶄竴鑷?
legal_basis:
  - REG-GB-14881
  - REG-FOOD-SAFETY-LAW

risk_description: 浠讳竴渚涘簲鍟嗘棤璇佹垨浣跨敤杩囨湡璁稿彲璇侀噰璐師鏂?
typical_nonconformities:
  - 鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿
  - 鍙傛暟璁板綍缂哄け鎴栨柇妗?  - 鍙傛暟璁板綍涓庝华琛ㄦ樉绀轰笉涓€鑷?  - 鎿嶄綔浜哄憳涓嶆帉鎻″弬鏁拌姹?  - 璁板綍琛ㄤ腑鍙傛暟濉啓涓嶅畬鏁?
recommended_actions:
  - 鏌ヨ瘉: 鍏抽敭鍙傛暟瓒呭嚭鎺у埗鑼冨洿 鈥?杩芥函璇ユ壒娆′骇鍝佸幓鍚戯紝鍗囩骇涓洪噸澶ч闄?  - 鏌ヨ瘉: 鍙傛暟璁板綍缂哄け 鈥?鎶芥煡鏇村鎵规鍒ゆ柇鏄惁涓虹郴缁熸€ч棶棰?  - 鏌ヨ瘉: 鎿嶄綔浜哄憳涓嶆帉鎻″弬鏁拌姹?鈥?妫€鏌ュ煿璁褰?
output_template:
  status: PASS / WARNING / FAIL
  reason: ""
  risk_level: Critical
  laws:
    - REG-GB-14881
    - REG-FOOD-SAFETY-LAW
  recommendation: ""
```

---

## 10. Sprint 35 Preparation

For Sprint 35, the following rules must be generated:

| ID Range | Count | Category |
|----------|-------|----------|
| RR-CP-BEV-PP-001 ~ 008 | 8 | 宸ヨ壓鍙傛暟鐩戞帶 |
| RR-CP-BEV-PP-009 ~ 012 | 4 | 杩囩▼璁板綍 |
| RR-CP-BEV-PP-013 ~ 015 | 3 | 杩囩▼鍋忓樊澶勭悊 |
| RR-CP-BEV-PP-016 ~ 020 | 5 | 杩囩▼楠岃瘉 |

Each rule follows the standard schema and the example above.

---

## 11. Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-03 | Initial release 鈥?Production Process risk rule design standard |
