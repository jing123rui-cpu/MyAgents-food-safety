# Runtime Architecture

## Overview

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                    CLI Entry                    鈹?鈹?            (cli/main.py / __init__.py)          鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?                       鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?              Knowledge Loader                   鈹?鈹?               script/loader.py                    鈹?鈹?                                                 鈹?鈹? KnowledgeLoader                                 鈹?鈹?  鈹溾攢鈹€ initialize()                               鈹?鈹?  鈹溾攢鈹€ load_registry()                            鈹?鈹?  鈹溾攢鈹€ load_taxonomy()                            鈹?鈹?  鈹溾攢鈹€ discover_checkpoints()                     鈹?鈹?  鈹溾攢鈹€ load_checkpoint(path)                      鈹?鈹?  鈹溾攢鈹€ load_all() -> KnowledgeRepository          鈹?鈹?  鈹溾攢鈹€ get_checkpoint(id)                         鈹?鈹?  鈹溾攢鈹€ get_checkpoints_by_domain(domain)          鈹?鈹?  鈹溾攢鈹€ get_checkpoints_by_subdomain(subdomain)    鈹?鈹?  鈹溾攢鈹€ statistics() -> LoaderStatistics           鈹?鈹?  鈹斺攢鈹€ to_knowledge_base() -> KnowledgeBase       鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?                       鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                  Data Models                    鈹?鈹?               script/models.py                    鈹?鈹?                                                 鈹?鈹? Checkpoint       RegistryEntry   TaxonomyNode   鈹?鈹? RiskRule         KnowledgeBase                  鈹?鈹? KnowledgeRepository  LoaderStatistics           鈹?鈹? Finding          AuditResult     AuditReport    鈹?鈹? RiskLevel (enum) AuditStatus (enum)             鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                       鈹?                       鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                Utility Layer                    鈹?鈹?               script/utils.py                     鈹?鈹?                                                 鈹?鈹? ensure_dir()     generate_report_id()           鈹?鈹? read_yaml()      read_markdown()                鈹?鈹? validate_path()  discover_files()               鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

## Component Responsibilities

### Knowledge Loader (`script/loader.py`)

The `KnowledgeLoader` class is the central orchestrator for all knowledge
ingestion. It follows a sequential loading pipeline:

1. **initialize()** 鈥?Validate the knowledge base path and reset caches.
2. **load_registry()** 鈥?Read all registry YAML files and produce a
   `dict[str, RegistryEntry]`.
3. **load_taxonomy()** 鈥?Read all taxonomy YAML files and merge them into
   a single dictionary.
4. **discover_checkpoints()** 鈥?Walk the checkpoints directory tree to
   find `.md` files.
5. **load_checkpoint()** 鈥?Parse a single Markdown checkpoint file,
   extract YAML frontmatter and section content, return a `Checkpoint`.
6. **load_all()** 鈥?Chain the above steps in order.
7. **Lookup methods** 鈥?`get_checkpoint`, `get_checkpoints_by_domain`,
   `get_checkpoints_by_subdomain` 鈥?query the in-memory repository.
8. **statistics()** 鈥?Report file counts and taxonomy node counts.
9. **to_knowledge_base()** 鈥?Export the repository as a `KnowledgeBase`.

### Data Models (`script/models.py`)

All data is defined as Python `@dataclass` classes with no business logic.

| Class               | Purpose                                    |
|---------------------|--------------------------------------------|
| `Checkpoint`        | One audit checkpoint (CP-XXX-NNN).        |
| `RegistryEntry`     | Links a checkpoint ID to taxonomy info.    |
| `TaxonomyNode`      | A node in the domain/sub-domain/category tree. |
| `RiskRule`          | A condition-to-risk-level mapping rule.    |
| `KnowledgeBase`     | Top-level container for all knowledge.     |
| `KnowledgeRepository` | Runtime container (with lookup helpers). |
| `LoaderStatistics`  | Aggregate counts from the loading phase.   |
| `Finding`           | A non-conformance finding.                 |
| `AuditResult`       | Result of auditing one checkpoint.         |
| `AuditReport`       | Full audit report aggregating results.     |
| `RiskLevel` (enum)  | CRITICAL, MAJOR, MODERATE, LOW.            |
| `AuditStatus` (enum)| OK, NOK, PENDING, NA.                      |

### Utilities (`script/utils.py`)

Stateless helper functions used by the loader and other modules:

| Function             | Purpose                              |
|----------------------|--------------------------------------|
| `ensure_dir`         | Create a directory if missing.       |
| `generate_report_id` | Produce a unique report ID string.   |
| `read_yaml`          | Safely load a YAML file.             |
| `read_markdown`      | Read a Markdown file to string.      |
| `validate_path`      | Check path existence and access.     |
| `discover_files`     | Glob for files recursively.          |

## Data Flow

```
 CLI / Entry Point
      鈹?      鈻? KnowledgeLoader.load_all()
      鈹?      鈹溾攢鈹€ initialize()
      鈹?      鈹斺攢鈹€ validate knowledge_dir
      鈹?      鈹溾攢鈹€ load_registry()
      鈹?      鈹斺攢鈹€ read_yaml() 鈫?knowledge/registry/*.yaml
      鈹?      鈹溾攢鈹€ load_taxonomy()
      鈹?      鈹斺攢鈹€ read_yaml() 鈫?knowledge/taxonomy/*.yaml
      鈹?      鈹溾攢鈹€ discover_checkpoints()
      鈹?      鈹斺攢鈹€ discover_files() 鈫?knowledge/checkpoints/**/*.md
      鈹?      鈹斺攢鈹€ For each *.md:
              鈹斺攢鈹€ load_checkpoint()
                      鈹溾攢鈹€ read_markdown()
                      鈹溾攢鈹€ parse YAML frontmatter
                      鈹斺攢鈹€ extract markdown sections
                              鈹斺攢鈹€ returns Checkpoint
      鈹?      鈻? KnowledgeRepository
      鈹?      鈹溾攢鈹€ .registry    鈫?dict[str, RegistryEntry]
      鈹溾攢鈹€ .taxonomy    鈫?dict[str, Any]
      鈹溾攢鈹€ .checkpoints 鈫?dict[str, Checkpoint]
      鈹斺攢鈹€ .errors / .warnings
```

## Extension Points

- **New file formats**: Add a `read_*` function in `utils.py` and handle
  it in the relevant loader method.
- **New model types**: Add a `@dataclass` in `models.py` and reference it
  from `KnowledgeBase` or `KnowledgeRepository`.
- **Custom discovery logic**: Override `discover_checkpoints()` or add
  a new method to `KnowledgeLoader`.
