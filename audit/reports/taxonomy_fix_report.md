# Taxonomy Fix Report

## Root Cause

`demo.py` accesses `n.name_zh` on `TaxonomyNode` objects, but the `TaxonomyNode` dataclass in `script/models.py` only defined `id`, `name`, and `children` 鈥?no `name_zh` field.

The YAML taxonomy files (`beverage_knowledge_tree.yaml`) use `name_zh` extensively for Chinese display names. The loader (`script/loader.py`) read those values but collapsed them into the single `name` field via fallback logic (`domain.get("name", domain.get("name_zh", node_id))`), discarding the original `name_zh` value.

## Files Changed

| File | Change |
|------|--------|
| `script/models.py:75` | Added `name_zh: str = ""` to `TaxonomyNode` dataclass |
| `script/loader.py:66-85` | Updated `_build_taxonomy_node` to extract and pass `name_zh` from YAML to all 3 `TaxonomyNode(...)` constructor calls (domain, sub-domain, category levels) |

No other modules were modified.

## Compatibility Notes

- **`name` field** 鈥?unchanged. Still uses fallback: `node.get("name", node.get("name_zh", node_id))`. All existing consumers of `.name` are unaffected.
- **`name_zh` field** 鈥?defaults to `""` when a YAML node has no `name_zh`, ensuring backward compatibility with any future taxonomy files that omit it.
- **API** 鈥?`TaxonomyNodeResponse` in `api/schemas.py` only serializes `id` and `name`; `name_zh` is available for future API use without breaking existing endpoints.
- **Context Engine** 鈥?`_build_taxonomy_breadcrumb` uses `node.name`; unchanged.
- **Workflow** 鈥?uses only `node.id` for lookup; `name_zh` is transparent.

## Validation Result

| Check | Status |
|-------|--------|
| `demo.py` 鈥?Taxonomy Nodes section | 鉁?Prints `n.name_zh` without `AttributeError` |
| All 233 taxonomy nodes have `name_zh` populated | 鉁?Confirmed bytes decode to correct Chinese |
| `pytest tests/ -x -q` (118 tests) | 鉁?118 passed |

## Summary

Two-line model fix (add field + populate in loader). Zero behavioral change to any other module. The `AttributeError: TaxonomyNode has no attribute "name_zh"` is resolved at the model level, not by patching the consumer.

