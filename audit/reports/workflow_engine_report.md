# Workflow Engine Report

## Created File

| File | Contents |
|------|----------|
| `script/workflow.py` | `InspectionRequest`, `InspectionContext`, `InspectionWorkflow` |

## Exported Classes (added to `script/__init__.py`)

- `InspectionRequest`
- `InspectionContext`
- `InspectionWorkflow`

---

## Workflow Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                    InspectionWorkflow                        鈹?鈹?                                                              鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?鈹? 鈹?Repository鈹?  鈹?SearchEngine 鈹?  鈹?   Risk Rules /      鈹? 鈹?鈹? 鈹?(loaded)  鈹傗攢鈹€鈻垛攤  (indexed)   鈹傗攢鈹€鈻垛攤  Taxonomy Indexes    鈹? 鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?鈹?                                                              鈹?鈹? build_context(request)                                       鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## Pipeline Stages

```
InspectionRequest
      鈹?      鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 1. Search Checkpoints               鈹?鈹?    鈹溾攢 checkpoint_id 鈫?exact lookup  鈹?鈹?    鈹溾攢 category      鈫?category scan 鈹?鈹?    鈹溾攢 risk_level    鈫?risk filter   鈹?鈹?    鈹斺攢 query         鈫?keyword scan  鈹?鈹?    (dimensions are intersected)     鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?List[Checkpoint]
               鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 2. Look Up Registry Entries         鈹?鈹?    Map checkpoint IDs 鈫?Registry    鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?List[RegistryEntry]
               鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 3. Locate Risk Rules                鈹?鈹?    Precomputed index:               鈹?鈹?    cp_id 鈫?List[RiskRule]           鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?List[RiskRule]
               鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 4. Locate Taxonomy Nodes            鈹?鈹?    Registry fields matched against  鈹?鈹?    taxonomy node IDs / names        鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?List[TaxonomyNode]
               鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 5. Assemble Context                 鈹?鈹?    Build InspectionContext with     鈹?鈹?    all matched assets + metadata    鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?               鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹? 6. Validate                         鈹?鈹?    Missing checkpoint               鈹?鈹?    Missing risk rule                鈹?鈹?    Missing taxonomy                 鈹?鈹?    Empty search result              鈹?鈹?    Duplicate results                鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?               鈻?       InspectionContext
```

---

## Context Structure

```python
@dataclass
class InspectionContext:
    request: InspectionRequest
    matched_checkpoints: List[Checkpoint]
    matched_risk_rules: List[RiskRule]
    matched_registry_entries: List[RegistryEntry]
    matched_taxonomy_nodes: List[TaxonomyNode]
    warnings: List[str]
    metadata: Dict[str, Any]
```

### Metadata fields

| Key | Type | Description |
|-----|------|-------------|
| `total_checkpoints` | int | Number of matched checkpoints |
| `total_registry_entries` | int | Number of matched registry entries |
| `total_risk_rules` | int | Number of matched risk rules |
| `total_taxonomy_nodes` | int | Number of matched taxonomy nodes |
| `warnings_count` | int | Total validation warnings |

---

## Search Strategy

When multiple request fields are provided, results are **intersected**:

| `checkpoint_id` | `query` | `category` | `risk_level` | Strategy |
|:---:|:---:|:---:|:---:|---------|
| 鉁?| 鈥?| 鈥?| 鈥?| Exact lookup, single result |
| 鈥?| 鉁?| 鈥?| 鈥?| Keyword search (ranked) |
| 鈥?| 鈥?| 鉁?| 鈥?| Category search |
| 鈥?| 鈥?| 鈥?| 鉁?| Risk search |
| 鈥?| 鉁?| 鉁?| 鉁?| Intersection of all three |
| 鉁?| 鉁?| 鈥?| 鈥?| Exact lookup only (id wins) |

---

## Precomputed Indexes

Built once at `InspectionWorkflow.__init__`:

| Index | Key | Value | Build method |
|-------|-----|-------|-------------|
| `_cp_to_rules` | checkpoint_id | `List[RiskRule]` | Derived from `RR-{cp_id}` rule ID convention |
| `_cp_to_taxonomy` | checkpoint_id | `List[TaxonomyNode]` | Matched via registry field 鈫?node ID/name alignment |

No file I/O during pipeline execution.

---

## Validation Logic

| Check | Condition | Warning message |
|-------|-----------|-----------------|
| Missing checkpoint | Registry entry has no matched checkpoint | `"Registry entry '{id}' has no matched checkpoint"` |
| Missing risk rule | Checkpoint has no risk rule in index | `"Checkpoint '{id}' has no risk rule"` |
| Missing taxonomy | Checkpoint has no taxonomy mapping | `"Checkpoint '{id}' has no taxonomy mapping"` |
| Empty result | No checkpoints matched the request | `"Search produced no matching checkpoints"` |
| Duplicate results | Same checkpoint ID appears multiple times | `"Duplicate checkpoint '{id}' in results"` |

---

## Future Integration with AI Agent

The `InspectionContext` is designed to be consumed by an AI Agent:

```python
# After building context
context = workflow.build_context(request)

# AI Agent consumes:
context.matched_checkpoints     # what to inspect
context.matched_risk_rules      # how to evaluate
context.matched_registry_entries  # metadata & laws
context.matched_taxonomy_nodes  # hierarchical classification
context.warnings                # known issues to handle

# Agent would produce AuditResult per checkpoint
```

The context contains everything needed for an LLM to reason about
an inspection 鈥?without the LLM needing to search the knowledge
base itself.

