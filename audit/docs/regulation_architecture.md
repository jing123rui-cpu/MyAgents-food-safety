# Regulatory Knowledge Base Architecture

**Version:** 1.0
**Date:** 2026-07-03
**Sprint:** 37

---

## 1. Overview

The Regulatory Knowledge Base provides a structured, traceable legal foundation for all inspection decisions. Every checkpoint and risk rule references one or more regulations, forming a clear chain from law to enterprise conclusion.

---

## 2. Architecture Diagram

```
                   鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                   鈺?    Regulatory Knowledge      鈺?                   鈺?           Base               鈺?                   鈺犫晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                   鈺?  regulation_registry.yaml    鈺?                   鈺?  REG-*.md (full text)        鈺?                   鈺氣晲鈺愨晲鈺愨晲鈺愨暒鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                          鈹?                          鈹?references (legal_basis)
                          鈻?            鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺?        Registry              鈺?            鈺? (knowledge/registry/*.yaml)   鈺?            鈺犫晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺? Maps: Checkpoint 鈫?Law(s)    鈺?            鈺? Fields: id, risk_level,      鈺?            鈺?          laws[], keywords[]   鈺?            鈺氣晲鈺愨晲鈺愨晲鈺愨暒鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                   鈹?                   鈹?defines
                   鈻?            鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺?        Checkpoint            鈺?            鈺? (knowledge/checkpoints/*.md)  鈺?            鈺犫晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺? Inspection objective         鈺?            鈺? Inspection methods           鈺?            鈺? Required evidence            鈺?            鈺? Regulatory references        鈺?            鈺氣晲鈺愨晲鈺愨晲鈺愨暒鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                   鈹?                   鈹?evaluated by
                   鈻?            鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺?        Risk Rule             鈺?            鈺? (knowledge/risk_rules/*.yaml) 鈺?            鈺犫晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺? Deterministic logic          鈺?            鈺? PASS / FAIL conditions       鈺?            鈺? legal_basis: [REG-*]         鈺?            鈺氣晲鈺愨晲鈺愨晲鈺愨暒鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                   鈹?                   鈹?processed by
                   鈻?            鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺?        RuleEngine            鈺?            鈺?     (script/rule_engine.py)     鈺?            鈺犫晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺? Evidence 鈫?COMPLIANT         鈺?            鈺?         鈫?NON_COMPLIANT      鈺?            鈺?         鈫?NOT_APPLICABLE     鈺?            鈺氣晲鈺愨晲鈺愨晲鈺愨暒鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?                   鈹?                   鈹?aggregated by
                   鈻?            鈺斺晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺?   Enterprise Evaluation      鈺?            鈺?  (script/agent.py)             鈺?            鈺犫晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?            鈺? 闈瀇compliant_count == 0      鈺?            鈺?   鈫?浼佷笟閫氳繃妫€鏌?             鈺?            鈺? 闈瀇compliant_count > 0       鈺?            鈺?   鈫?浼佷笟闇€瑕佹暣鏀?             鈺?            鈺氣晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺愨晲鈺?```

---

## 3. Data Flow

### 3.1 Forward Traceability (Law 鈫?Enterprise)

```
Law (REG-*)
  鈫? referenced in legal_basis
Checkpoint (CP-BEV-*-NNN)
  鈫? evaluated by
Risk Rule (RR-CP-BEV-*-NNN)
  鈫? processed by
RuleEngine
  鈫? aggregates to
Enterprise Evaluation
  鈫? outputs
浼佷笟閫氳繃妫€鏌?/ 浼佷笟闇€瑕佹暣鏀?```

### 3.2 Reverse Traceability (Enterprise 鈫?Law)

```
Enterprise Conclusion
  鈫? composed from
Evaluation Results (COMPLIANT / NON_COMPLIANT)
  鈫? produced by
RuleEngine._apply_rule()
  鈫? uses
RiskRule.risk_level + Evidence fields
  鈫? derived from
Checkpoint inspection criteria
  鈫? references
Regulation (REG-*) in legal_basis
```

---

## 4. Regulation Types

| Type Code | Type | Examples |
|-----------|------|----------|
| `national_law` | National law enacted by the NPC Standing Committee | REG-FOOD-SAFETY-LAW |
| `national_standard` | National food safety standard (GB series) | REG-GB-14881, REG-GB-2760 |
| `administrative_regulation` | Administrative regulation issued by SAMR | REG-FOOD-PRODUCTION-LICENSE, REG-FOOD-ADDITIVE |

---

## 5. Directory Structure

```
knowledge/
鈹溾攢鈹€ regulations/                           鈫?NEW (Sprint 37)
鈹?  鈹溾攢鈹€ regulation_registry.yaml           鈫?6 entries
鈹?  鈹溾攢鈹€ REG-FOOD-SAFETY-LAW.md
鈹?  鈹溾攢鈹€ REG-GB-14881.md
鈹?  鈹溾攢鈹€ REG-FOOD-PRODUCTION-LICENSE.md
鈹?  鈹斺攢鈹€ REG-HACCP.md
鈹?鈹溾攢鈹€ registry/
鈹?  鈹溾攢鈹€ beverage_raw_material_registry.yaml      鈫?25 entries
鈹?  鈹斺攢鈹€ beverage_production_process_registry.yaml 鈫?20 entries
鈹?鈹溾攢鈹€ checkpoints/
鈹?  鈹溾攢鈹€ beverage/raw_material/          鈫?25 checkpoints
鈹?  鈹斺攢鈹€ beverage/production_process/    鈫?20 checkpoints
鈹?鈹斺攢鈹€ risk_rules/
    鈹溾攢鈹€ beverage/raw_material/          鈫?25 rules
    鈹斺攢鈹€ beverage/production_process/    鈫?20 rules
```

---

## 6. RegulationLoader Framework

```
script/regulation_loader.py
鈹溾攢鈹€ RegulationEntry          鈥?metadata dataclass
鈹溾攢鈹€ RegulationDocument       鈥?full-text dataclass
鈹溾攢鈹€ RegulationRepository     鈥?container (registry + documents)
鈹斺攢鈹€ RegulationLoader         鈥?framework with 4 methods:
    鈹溾攢鈹€ load_regulations()
    鈹溾攢鈹€ search_regulation()
    鈹溾攢鈹€ get_related_checkpoints()
    鈹斺攢鈹€ get_related_rules()
```

All methods are **NotImplementedError** 鈥?framework only. Implementation planned for Sprint 38+.

---

## 7. Cross-Reference Rules

| Relationship | Source | Target | Join Key |
|-------------|--------|--------|----------|
| Checkpoint 鈫?Law | `registry/*.yaml` 鈫?`laws[]` | `REG-*` | `laws[i]` matches regulation ID |
| Risk Rule 鈫?Law | `risk_rules/*.yaml` 鈫?`legal_basis[]` | `REG-*` | `legal_basis[i]` matches regulation ID |
| Checkpoint 鈫?Risk Rule | Naming convention | `CP-BEV-*-NNN` 鈫?`RR-CP-BEV-*-NNN` | `RR-{checkpoint_id}` |

---

## 8. Document Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-07-03 | Initial release 鈥?Regulatory Knowledge Base architecture |
