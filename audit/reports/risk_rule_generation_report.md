# Risk Rule Generation Report

**Generated:** 2026-07-03
**Version:** 1.0
**Project:** Food Audit Agent

---

## 1. Generation Summary

| Metric | Value |
|--------|-------|
| Total risk rule files created | 25 |
| Total checkpoint files | 25 |
| Total registry entries | 25 |
| Decision rules (total) | 106 |
| Average decision rules per file | ~4.2 |
| Minimum rules per file | 3 |
| Schema version | 1.0 |

**File format:** YAML
**Directory:** `knowledge/risk_rules/beverage/raw_material/`
**Naming convention:** `RR-CP-BEV-RM-NNN.yaml`

---

## 2. Risk Level Distribution

| Risk Level | Count | Percentage |
|------------|-------|------------|
| Critical | 15 | 60% |
| High | 10 | 40% |
| Medium | 0 | 0% |
| Low | 0 | 0% |

**Note:** Risk levels map from checkpoint risk levels: H → Critical, M → High. No checkpoints currently have Medium or Low risk levels.

---

## 3. Validation Results

| Check | Result |
|-------|--------|
| Risk rule files match checkpoint files | ✅ 25 / 25 |
| Registry entries match checkpoints | ✅ 25 / 25 |
| Missing risk rules (checkpoint without rule) | ❌ 0 |
| Orphan risk rules (rule without checkpoint) | ❌ 0 |
| Duplicate risk rule IDs | ❌ 0 |
| Rules with at least 1 PASS decision | ✅ 25 / 25 |
| Rules with at least 1 WARNING decision | ✅ 25 / 25 |
| Rules with at least 1 FAIL decision | ✅ 25 / 25 |
| All IDs match exactly across systems | ✅ |
| **Overall coverage** | **100%** |

---

## 4. File Inventory

| # | Risk Rule File | Linked Checkpoint |
|---|----------------|-------------------|
| 1 | `RR-CP-BEV-RM-001.yaml` | CP-BEV-RM-001 |
| 2 | `RR-CP-BEV-RM-002.yaml` | CP-BEV-RM-002 |
| 3 | `RR-CP-BEV-RM-003.yaml` | CP-BEV-RM-003 |
| 4 | `RR-CP-BEV-RM-004.yaml` | CP-BEV-RM-004 |
| 5 | `RR-CP-BEV-RM-005.yaml` | CP-BEV-RM-005 |
| 6 | `RR-CP-BEV-RM-006.yaml` | CP-BEV-RM-006 |
| 7 | `RR-CP-BEV-RM-007.yaml` | CP-BEV-RM-007 |
| 8 | `RR-CP-BEV-RM-008.yaml` | CP-BEV-RM-008 |
| 9 | `RR-CP-BEV-RM-009.yaml` | CP-BEV-RM-009 |
| 10 | `RR-CP-BEV-RM-010.yaml` | CP-BEV-RM-010 |
| 11 | `RR-CP-BEV-RM-011.yaml` | CP-BEV-RM-011 |
| 12 | `RR-CP-BEV-RM-012.yaml` | CP-BEV-RM-012 |
| 13 | `RR-CP-BEV-RM-013.yaml` | CP-BEV-RM-013 |
| 14 | `RR-CP-BEV-RM-014.yaml` | CP-BEV-RM-014 |
| 15 | `RR-CP-BEV-RM-015.yaml` | CP-BEV-RM-015 |
| 16 | `RR-CP-BEV-RM-016.yaml` | CP-BEV-RM-016 |
| 17 | `RR-CP-BEV-RM-017.yaml` | CP-BEV-RM-017 |
| 18 | `RR-CP-BEV-RM-018.yaml` | CP-BEV-RM-018 |
| 19 | `RR-CP-BEV-RM-019.yaml` | CP-BEV-RM-019 |
| 20 | `RR-CP-BEV-RM-020.yaml` | CP-BEV-RM-020 |
| 21 | `RR-CP-BEV-RM-021.yaml` | CP-BEV-RM-021 |
| 22 | `RR-CP-BEV-RM-022.yaml` | CP-BEV-RM-022 |
| 23 | `RR-CP-BEV-RM-023.yaml` | CP-BEV-RM-023 |
| 24 | `RR-CP-BEV-RM-024.yaml` | CP-BEV-RM-024 |
| 25 | `RR-CP-BEV-RM-025.yaml` | CP-BEV-RM-025 |

---

## 5. Risk Rule Schema (v1.0)

Each rule file contains the following fields:

| Field | Type | Description |
|-------|------|-------------|
| `id` | string | Unique rule ID (RR-CP-BEV-RM-NNN) |
| `checkpoint_id` | string | Linked checkpoint ID |
| `title` | string | Chinese title from checkpoint |
| `version` | string | Schema version (1.0) |
| `domain` | string | Audit domain (module from checkpoint) |
| `category` | string | Audit category (unit from checkpoint) |
| `risk_level` | string | Critical / High / Medium / Low |
| `purpose` | string | Audit objective |
| `decision_logic` | list | Condition → result rules |
| `required_evidence` | list | Mandatory evidence items |
| `pass_condition` | string | Condition for PASS |
| `fail_condition` | string | Condition for FAIL |
| `warning_condition` | string | Condition for WARNING |
| `legal_basis` | list | Applicable regulations |
| `risk_description` | string | Risk condition description |
| `typical_nonconformities` | list | Common findings |
| `recommended_actions` | list | Suggested corrective actions |
| `output_template` | dict | Standardized output structure |

---

## 6. Files Modified

**No existing files were modified.**

**New files created:**
- `knowledge/risk_rules/beverage/raw_material/RR-CP-BEV-RM-001.yaml` through `025.yaml` (25 files)
- `reports/risk_rule_generation_report.md` (this file)
