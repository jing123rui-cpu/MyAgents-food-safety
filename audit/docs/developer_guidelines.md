# Developer Guidelines v1.0.0

**Date:** 2026-07-03

---

## Coding Conventions

### Python

- Target **Python 3.10+** (uses `from __future__ import annotations`, `str | None` syntax).
- Use **4-space indentation** (no tabs).
- Maximum line length: **88 characters** (PEP 8 + Black default).
- Use **double quotes** for strings (`"text"`), single quotes only for nested cases.

### Imports

Order imports in three groups separated by a blank line:

```python
from __future__ import annotations  # always first

import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx
import yaml

from .base import AIProvider
from ..models import Checkpoint
```

1. Standard library
2. Third-party packages
3. Application modules

Avoid `from module import *`. Prefer explicit imports.

### Type Annotations

- Add type annotations to all function signatures and dataclass fields.
- Use `Optional[T]` instead of `T | None` for consistency (legacy Python 3.10 compatibility).
- Use `List[T]`, `Dict[K, V]` from `typing` (not built-in `list[T]`).

### Docstrings

- One-line docstrings for trivial methods: `"""Brief description."""`
- Multi-line docstrings with Parameters / Returns / Raises sections for complex methods.
- Docstrings use double-triple-quotes (`"""`).
- No comments inside function bodies unless the logic is non-obvious.

---

## Folder Responsibilities

| Directory | Purpose |
|-----------|---------|
| `script/` | All business logic. No I/O except through loader. |
| `script/ai/` | AI provider abstraction, prompt engine, context engine, writing engine, pipeline. |
| `api/` | FastAPI server. Thin layer 鈥?delegates to `core`. |
| `knowledge/` | Read-only data: checkpoints, registry, taxonomy, risk rules. |
| `tests/` | Pytest suite. One file per module under `script/`. |
| `docs/` | Architecture documentation and developer guides. |
| `reports/` | Sprint reports and validation documents. |
| `demo*.py` | Root-level demo scripts (not part of the installable package). |
| `main.py` | CLI entry point. |

---

## Naming Conventions

### Classes

```python
class FoodAuditAgent:         # PascalCase for public classes
class DeepSeekProvider:       # PascalCase for providers
class _InferenceHelper:       # _prefix for private/internal classes
```

### Functions & Methods

```python
def build_context():          # snake_case
def _private_helper():        # _prefix for private
```

### Variables

```python
checkpoint_id: str            # snake_case
matched_checkpoints: List     # descriptive, not cp_list
```

### Constants

```python
_DEFAULT_MODEL = "deepseek-chat"    # UPPER_CASE with _prefix for module-private
_CHAT_ENDPOINT = "/chat/completions"
```

### Files

- Match the class name: `FoodAuditAgent` 鈫?`agent.py`
- One primary class per file.
- Module `__init__.py` re-exports the public API.

---

## Dataclass Standards

### Rules

1. All data models use `@dataclass` from the standard library (not Pydantic, not namedtuple).
2. Always add `from __future__ import annotations` at the top.
3. Always specify `field(default_factory=...)` for mutable defaults.
4. Use `Optional[T]` for nullable fields.
5. One dataclass per logical concept.

### Template

```python
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class ExampleModel:
    """One-line description of what this model represents."""
    id: str
    name: str = ""
    items: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    parent: Optional[ExampleModel] = None
```

---

## Exception Standards

### Hierarchy

```
AIProviderError (base)
鈹溾攢鈹€ ProviderUnavailable     鈫?provider unreachable / not initialised
鈹溾攢鈹€ PromptError              鈫?malformed prompt / exceeds limits
鈹溾攢鈹€ AuthenticationError      鈫?invalid / missing credentials
鈹溾攢鈹€ RateLimitError           鈫?rate limit exceeded
鈹斺攢鈹€ ModelError               鈫?unexpected model response
```

### Rules

- All AI exceptions inherit from `AIProviderError`.
- Catch specific exceptions at the call site; avoid bare `except:`.
- Convert third-party exceptions (httpx, json) into framework exceptions in the provider implementation.

---

## Module Dependency Rules

### Dependency Direction

```
models.py  鈫? (no dependencies on other modules)
    鈫?loader.py  search.py  rule_engine.py  workflow.py  evidence.py
    鈫?agent.py
    鈫?ai/ (provider, context_engine, prompt_engine, pipeline, writing_engine)
    鈫?api/ (server.py)
```

### Prohibited Patterns

- 鉂?`loader.py` imports from `agent.py` 鈥?loader must not depend on the agent.
- 鉂?`models.py` imports from any other module 鈥?models must stand alone.
- 鉂?Circular imports between `script/` modules.

### Allowed Patterns

- 鉁?Any module can import from `models.py`.
- 鉁?`agent.py` can import from any `script/` module (it's the orchestrator).
- 鉁?`ai/` modules can import from `script/` modules (models, workflow).

---

## Future Extension Rules

### Adding a New Provider

1. Create `script/ai/<name>.py` with a class that inherits from `AIProvider`.
2. Implement all abstract methods.
3. Register in `ProviderRegistry` (called from `agent.py` initialisation).
4. No changes needed to `PromptEngine`, `ContextEngine`, `Pipeline`, or `WritingEngine`.

### Adding a New Knowledge Domain

1. Create `knowledge/checkpoints/<domain>/` with markdown files.
2. Create entries in `knowledge/registry/<domain>.yaml`.
3. Create taxonoy nodes in `knowledge/taxonomy/` (optional).
4. Create risk rules in `knowledge/risk_rules/<domain>/`.
5. No code changes needed 鈥?the loader auto-discovers new files.

### Adding a New Prompt Template

1. Create `script/ai/templates/<name>.md` with `{{placeholder}}` markers.
2. Add a `build_<name>_prompt()` method to `PromptEngine`.
3. Expose the new method in `PromptEngine.__all__`.

### Adding a New API Endpoint

1. Add a Pydantic schema in `api/schemas.py`.
2. Add a route handler in `api/server.py`.
3. The handler receives the request, delegates to `FoodAuditAgent`, and returns the response.

---

## Testing Standards

- Write tests using **pytest** (no unittest).
- One test file per module: `test_<module>.py`.
- Use `conftest.py` for shared fixtures.
- Test function names: `test_<method>_<scenario>`.
- No mocking of AI providers in unit tests (integration tests are separate).
- Coverage target: 鈮?0% for `script/` modules.
