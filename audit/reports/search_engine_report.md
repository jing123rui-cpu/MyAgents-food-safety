# Knowledge Search Engine Report

## Overview

The `KnowledgeSearchEngine` provides deterministic retrieval over a loaded
`KnowledgeRepository`. It is a pure-Python, zero-dependency search layer
designed for offline audit workflows.

## Created File

| File | Purpose |
|------|---------|
| `script/search.py` | `KnowledgeSearchEngine` class with four search methods |

---

## Search Methods

| Method | Signature | Description |
|--------|-----------|-------------|
| `search_checkpoint` | `(checkpoint_id: str) -> Optional[Checkpoint]` | Exact ID lookup |
| `search_keyword` | `(keyword: str) -> List[Checkpoint]` | Full-text search across titles, keywords, and markdown body |
| `search_category` | `(category: str) -> List[Checkpoint]` | Match against registry category / subcategory |
| `search_risk` | `(level: str) -> List[Checkpoint]` | Match risk level by name or internal code |

---

## Index Strategy

No external index is maintained. All searches are computed at query time
against the in-memory `KnowledgeRepository`:

```
KnowledgeRepository
 鈹溾攢鈹€ checkpoints  Dict[str, Checkpoint]   鈫?direct ID lookup
 鈹溾攢鈹€ registry     Dict[str, RegistryEntry] 鈫?keyword / category / risk
 鈹斺攢鈹€ taxonomy     Dict[str, TaxonomyNode]  鈫?(not yet indexed)
```

**Keyword search** builds a relevance score per checkpoint:

| Match location | Points |
|----------------|--------|
| Checkpoint title | 3 |
| Registry keywords list | 2 |
| Markdown body (`raw_content`) | 1 |

Results are sorted descending by score, then alphabetically by ID.

**Risk search** normalises user input through an alias map:

| User input | Matched aliases |
|------------|-----------------|
| `critical` | critical, RISK-01, c |
| `high` | high, h, RISK-02 |
| `medium` / `moderate` | medium, m, RISK-03, moderate |
| `low` | low, l, RISK-04 |

---

## Supported Queries

| Query type | Example |
|------------|---------|
| Checkpoint ID | `search_checkpoint("CP-BEV-RM-013")` |
| Keyword (title) | `search_keyword("supplier")` |
| Keyword (registry) | `search_keyword("license")` |
| Keyword (body) | `search_keyword("娓╂箍搴?)` |
| Category | `search_category("鍘熸枡璐瓨")` |
| Category | `search_category("supplier_qualification")` |
| Risk level (name) | `search_risk("High")` |
| Risk level (code) | `search_risk("RISK-02")` |
| Risk level (short) | `search_risk("H")` |

---

## Time Complexity

| Operation | Complexity | Notes |
|-----------|------------|-------|
| `search_checkpoint(id)` | O(1) | dict lookup |
| `search_keyword(kw)` | O(N 脳 B) | N = checkpoints, B = body length |
| `search_category(cat)` | O(R) | R = registry entries |
| `search_risk(level)` | O(N + R) | linear scan of checkpoints + registry |

All queries operate in O(N) or better with respect to repository size.

---

## Future Improvements

- **Inverted index** 鈥?pre-build a term 鈫?checkpoint map for O(1) keyword
  lookups (trade-off: memory for speed).
- **Full-text indexing** 鈥?use `whoosh` or `tantivy` for tokenised search
  with stemming and fuzzy matching.
- **Taxonomy-aware search** 鈥?expand queries to include all checkpoints
  under a domain / sub-domain tree.
- **Faceted search** 鈥?combine filters (risk + category + keyword) in a
  single query.
- **Pagination** 鈥?return sliced, cursor-based results for large result
  sets.

---

## Integration

```python
from core.loader import KnowledgeLoader
from core.search import KnowledgeSearchEngine

loader = KnowledgeLoader("knowledge")
repo = loader.load_all()
engine = KnowledgeSearchEngine(repo)

# Exact ID lookup
cp = engine.search_checkpoint("CP-BEV-RM-013")

# Keyword search (ranked)
results = engine.search_keyword("supplier")

# Category lookup
results = engine.search_category("鍘熸枡璐瓨")

# Risk filter
results = engine.search_risk("High")
```

