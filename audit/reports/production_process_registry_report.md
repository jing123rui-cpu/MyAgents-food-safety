# Production Process Registry Report

**Generated:** 2026-07-03
**Domain:** `production_process_management`
**Sub-domain:** `process_control`

---

## 1. Registry Overview

| Metric | Value |
|--------|-------|
| Total registry entries | 45 |
| New PP entries | 20 |
| Existing RM entries | 25 |
| Registry files | 2 |
| Duplicate IDs detected | 0 |
| Missing checkpoint files | 0 |

## 2. Category Distribution (PP)

| Subcategory (name_zh) | Checkpoint Count | Checkpoints |
|-----------------------|-----------------|-------------|
| 工艺参数监控 | 8 | PP-001 ~ PP-008 |
| 过程记录 | 4 | PP-009 ~ PP-012 |
| 过程偏差处理 | 3 | PP-013 ~ PP-015 |
| 过程验证 | 5 | PP-016 ~ PP-020 |

## 3. Risk Level Distribution (PP)

| Risk Level | Count | Checkpoints |
|------------|-------|-------------|
| High | 14 | PP-001..003, 005..007, 009, 011..013, 015..016, 018, 020 |
| Medium | 6 | PP-004, 008, 010, 014, 017, 019 |
| Low | 0 | — |

## 4. Validation Results

| Check | Status |
|-------|--------|
| PP checkpoint files exist (20/20) | ✅ |
| PP registry IDs unique (no duplicates) | ✅ |
| PP checkpoint_file paths valid | ✅ |
| PP taxonomy reference exists (IDs in taxonomy YAML) | ✅ |
| PP subcategory matches taxonomy category name_zh | ✅ |
| PP domain ID matches taxonomy domain | ✅ |
| PP sub_domain ID matches taxonomy sub-domain | ✅ |
| RM registry intact (unchanged) | ✅ |
| Loader errors | 0 |
| Loader warnings (all PP risk rules missing) | 20 |

## 5. Updated Totals

| Asset | Before | After |
|-------|--------|-------|
| Registry entries | 25 | **45** |
| Checkpoint files | 25 | **45** |
| Taxonomy nodes | 233 | **270** |
| Search coverage | 25/25 (100%) | **45/45 (100%)** |
| Risk rules | 25 | 25 (PP pending) |

## 6. File Structure

```
knowledge/registry/
├── beverage_raw_material_registry.yaml     (25 entries, unchanged)
└── beverage_production_process_registry.yaml  (20 entries, new)
```

## 7. Pending Items (Future Sprint)

- Risk rules for CP-BEV-PP-001 through CP-BEV-PP-020 (20 rules)
- Risk rule generation and validation
