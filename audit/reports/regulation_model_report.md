# Regulation Knowledge Model Report

**Generated:** 2026-07-03
**Sprint:** 38
**Module:** `script/regulation_models.py`

---

## 1. Model Overview

The Regulation Knowledge Model defines a 6-level hierarchy that traces from law text through to enterprise audit conclusion.

```
Regulation (娉曞緥/鏍囧噯)
    鈹?    鈻?Chapter (绔?鑺?
    鈹?    鈻?Article (鏉℃)
    鈹?    鈻?Requirement (妫€鏌ヨ姹?
    鈹?    鈻?Checkpoint (妫€鏌ョ偣)
    鈹?    鈻?Risk Rule (椋庨櫓瑙勫垯)
    鈹?    鈻?Inspection Result (妫€鏌ョ粨鏋?
    鈹?    鈻?Enterprise Conclusion (浼佷笟缁撹)
```

---

## 2. Traceability Chain (Detail)

### Level 1 鈥?Regulation

```
Model:      Regulation
ID prefix:  REG-
Examples:   REG-GB-14881, REG-FOOD-SAFETY-LAW
Content:    Bilingual title, document type, issuing authority,
            effective date, scope, purpose
Storage:    knowledge/regulations/{REG-ID}.md (future)
            knowledge/regulations/regulation_registry.yaml (metadata)
```

The top-level container. Each regulation is identified by its `REG-*` code and carries metadata for search, citation, and lifecycle management.

### Level 2 鈥?Chapter

```
Model:      RegulationChapter
ID prefix:  CH-
Examples:   CH-GB-14881-09 (Chapter 9: Production Process Control)
Content:    Chapter number, bilingual title, parent chapter (for nesting)
Storage:    Embedded within Regulation YAML
```

Chapters group related articles. The model supports nesting (chapters within chapters) via the `parent_chapter_id` field.

### Level 3 鈥?Article

```
Model:      RegulationArticle
ID prefix:  ART-
Examples:   ART-GB-14881-09-03 (Article 9.3: CCP Monitoring)
Content:    Full legal text, one-sentence summary, keywords,
            inspection topics, risk tags, severity
Relations:  related_checkpoint_ids 鈫?Checkpoint
            related_rule_ids 鈫?RiskRule
```

The finest independently citable legal unit. Each article carries metadata that enables:
- Legal traceability (citation in reports)
- AI reasoning (inspection_topics, risk_tags)
- Checkpoint mapping (related_checkpoint_ids)
- Rule mapping (related_rule_ids)

### Level 4 鈥?Requirement

```
Model:      RegulationRequirement
ID prefix:  REQ-
Examples:   REQ-GB-14881-09-03-01
Content:    Description, inspection method, required evidence,
            decision logic, common nonconformities,
            recommended actions
Relations:  related_checkpoint_ids 鈫?Checkpoint
            related_rule_ids 鈫?RiskRule
```

The inspectable criterion. One article may decompose into multiple requirements. Each requirement carries everything needed for an auditor to evaluate compliance.

### Level 5 鈥?Checkpoint + RiskRule

```
Checkpoint: CP-BEV-*-NNN  (knowledge/checkpoints/)
    Defines: inspection objective, methods, required evidence
    Links to: REG-* via legal_basis

Risk Rule:  RR-CP-BEV-*-NNN  (knowledge/risk_rules/)
    Defines: deterministic PASS/FAIL logic
    Links to: REG-* via legal_basis
```

These are the existing audit system components. The requirement model links to them bidirectionally:
- `RegulationRequirement.related_checkpoint_ids` 鈫?which checkpoints verify this requirement
- `RegulationRequirement.related_rule_ids` 鈫?which risk rules evaluate this requirement

### Level 6 鈥?Inspection Result + Enterprise Conclusion

```
Inspection Result: COMPLIANT / NON_COMPLIANT / NOT_APPLICABLE
    Produced by: RuleEngine._apply_rule()
    Outputs: status, score, reason, violated_laws (RegulationCitation[])

Enterprise Conclusion:
    non_compliant_count == 0 鈫?浼佷笟閫氳繃妫€鏌?    non_compliant_count > 0  鈫?浼佷笟闇€瑕佹暣鏀?```

The final output. The `violated_laws` field in `EvaluationResult` uses the `RegulationCitation` model to cite which regulations and articles were violated.

---

## 3. Model Statistics

| Model | Fields | Key Relationships |
|-------|--------|-------------------|
| Regulation | 12 + chapters[] | Parent of all |
| RegulationChapter | 7 + articles[] + sub_chapters[] | Groups articles |
| RegulationArticle | 17 + requirements[] | Links to CP + RR |
| RegulationRequirement | 12 | Full inspection spec |
| RegulationCitation | 7 | Lightweight for reports |
| RegulationKnowledgeBase | 6 + 4 lookup methods | Container + queries |

---

## 4. Data Flow for a Typical Audit

```
1. Auditor inspects Checkpoint CP-BEV-PP-007 (鏃堕棿娓╁害鎺у埗)
       鈹?2. Checkpoint references REG-GB-14881 (legal_basis)
       鈹?3. Regulation model shows which articles apply:
       ART-GB-14881-09-03 (CCP Monitoring)
       ART-GB-14881-09-04 (Temperature Recording)
       鈹?4. Each article decomposes into requirements:
       REQ-GB-14881-09-03-01: CCP records must be complete
       REQ-GB-14881-09-03-02: Critical limits must not be breached
       鈹?5. Risk Rule RR-CP-BEV-PP-007 evaluates evidence:
       PASS  鈫?娓╁害鏃堕棿绗﹀悎CCP鍏抽敭闄愬€?       FAIL  鈫?鏉€鑿屾俯搴︿綆浜庡叧閿檺鍊?       鈹?6. RuleEngine returns EvaluationResult:
       status: COMPLIANT / NON_COMPLIANT
       violated_laws: [REG-GB-14881 搂9.3]
       鈹?7. Enterprise evaluation aggregates:
       浼佷笟閫氳繃妫€鏌?/ 浼佷笟闇€瑕佹暣鏀?```

---

## 5. Compliance Traceability Matrix

| Level | What | ID Format | Example |
|-------|------|-----------|---------|
| 1 | Law | `REG-*` | REG-GB-14881 |
| 2 | Chapter | `CH-{REG}-{N}` | CH-GB-14881-09 |
| 3 | Article | `ART-{REG}-{CN}-{AN}` | ART-GB-14881-09-03 |
| 4 | Requirement | `REQ-{REG}-{CN}-{AN}-{S}` | REQ-GB-14881-09-03-01 |
| 5 | Checkpoint | `CP-{DOM}-{CAT}-{N}` | CP-BEV-PP-007 |
| 5 | Risk Rule | `RR-{CHECKPOINT_ID}` | RR-CP-BEV-PP-007 |
| 6 | Result | EvaluationStatus | COMPLIANT |
| 6 | Enterprise | String | 浼佷笟闇€瑕佹暣鏀?|

---

## 6. Forward and Reverse Traceability

### Forward: Law 鈫?Enterprise

```
REG-GB-14881
  鈫?CH-GB-14881-09 (Production Process Control)
    鈫?ART-GB-14881-09-03 (CCP Monitoring)
      鈫?REQ-GB-14881-09-03-01 (CCP records)
        鈫?CP-BEV-PP-007 (鏃堕棿娓╁害鎺у埗)
          鈫?RR-CP-BEV-PP-007
            鈫?COMPLIANT / NON_COMPLIANT
              鈫?浼佷笟閫氳繃妫€鏌?/ 浼佷笟闇€瑕佹暣鏀?```

### Reverse: Enterprise 鈫?Law

```
浼佷笟闇€瑕佹暣鏀?  鈫?CP-BEV-PP-007: NON_COMPLIANT
    鈫?RR-CP-BEV-PP-007: 鏉€鑿屾俯搴︿綆浜庡叧閿檺鍊?      鈫?CP-BEV-PP-007 inspection objective
        鈫?REQ-GB-14881-09-03-01
          鈫?ART-GB-14881-09-03
            鈫?CH-GB-14881-09
              鈫?REG-GB-14881
```

---

## 7. Citation in Reports

When a non-compliance is identified, the audit report cites:

```
Violated: REG-GB-14881 搂9.3
Title:    椋熷搧瀹夊叏鍥藉鏍囧噯 椋熷搧鐢熶骇閫氱敤鍗敓瑙勮寖
Severity: HIGH
Reason:   鏉€鑿屾俯搴︿綆浜嶤CP鍏抽敭闄愬€?```

This is represented by the `RegulationCitation` model in `EvaluationResult.violated_laws`.

---

## 8. File Manifest

| File | Size | Description |
|------|------|-------------|
| `script/regulation_models.py` | ~8KB | All dataclass definitions |
| `docs/regulation_schema.md` | ~10KB | Field reference + UML diagram |
| `knowledge/regulations/examples/REG-DEMO.yaml` | ~5KB | 3-article demonstration |
| `reports/regulation_model_report.md` | This file | Model report |

