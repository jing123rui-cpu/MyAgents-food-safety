# Runtime Loader Report

## Load Order

```
initialize()
    ↓
load_taxonomy()
    ↓
load_registry()
    ↓
load_checkpoints()
    ↓
load_risk_rules()
    ↓
cross_validate()
    ↓
return KnowledgeRepository
```

---

## Registry Loaded

| Metric | Value |
|--------|-------|
| Files found | 1 |
| Total entries | 25 |
| First ID | CP-BEV-RM-001 |
| Last ID | CP-BEV-RM-025 |
| Duplicate IDs | 0 |

---

## Taxonomy Loaded

| Metric | Value |
|--------|-------|
| Files found | 1 |
| Domains | 1 (active) + 15 (placeholder) |
| Sub-domains | 6 (active domain) |
| Categories | 16 (active domain) |
| Total nodes | 23 |

---

## Checkpoint Count

| Metric | Value |
|--------|-------|
| Files found | 25 |
| Total loaded | 25 |
| First ID | CP-BEV-RM-001 |
| Last ID | CP-BEV-RM-025 |
| Empty files | 0 |
| Missing titles | 0 |
| Duplicate IDs | 0 |

---

## Risk Rule Count

| Metric | Value |
|--------|-------|
| Files found | 25 |
| Total loaded | 25 |
| First ID | RR-CP-BEV-RM-001 |
| Last ID | RR-CP-BEV-RM-025 |
| Duplicate IDs | 0 |

---

## Warnings

None.

---

## Errors

None.

---

## Memory Summary

| Dataset | Approximate size |
|---------|-----------------|
| Registry | 25 entries |
| Taxonomy | 23 nodes |
| Checkpoints | 25 files |
| Risk Rules | 25 rules |

---

## Validation Summary

| Check | Result |
|-------|--------|
| Registry entry has checkpoint | 25/25 OK |
| Registry entry has risk rule | 25/25 OK |
| Checkpoint exists in taxonomy | 25/25 OK |
| Orphan checkpoints | 0 |
| Orphan risk rules | 0 |
| Orphan taxonomy references | 0 |

---

## Repository Structure

```
KnowledgeRepository
 ├── registry:   Dict[str, RegistryEntry]    (25)
 ├── taxonomy:   Dict[str, TaxonomyNode]     (23)
 ├── checkpoints: Dict[str, Checkpoint]      (25)
 ├── warnings:   List[str]                   (0)
 └── errors:     List[str]                   (0)
```
