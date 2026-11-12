# Food Audit Agent

AI-powered food safety audit system for beverage manufacturing facilities.

Version **2.0.0** — Regulatory Report v2.0.

---

## Overview

The Food Audit Agent automates on-site food safety audits by guiding auditors through structured checkpoints, collecting evidence, evaluating against risk rules, and generating professional audit reports. The initial domain is beverage raw material management with 25 checkpoints across 16 taxonomy domains.

The system connects to the **DeepSeek API** for AI-powered analysis and writing, but all core inspection logic (search, workflow, rule engine) works fully offline.

---

## Architecture

```
┌───────────────────────────────────────────────────────────────┐
│                  Application Layer                             │
│  CLI (main.py)   FastAPI (api/)   Demo Scripts (demo*.py)     │
└──────────────────────────┬────────────────────────────────────┘
                           │
┌──────────────────────────▼────────────────────────────────────┐
│                    FoodAuditAgent                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐ │
│  │ Loader   │  │ Search   │  │ Workflow │  │ Rule Engine  │ │
│  │ loader.py│  │ search.py│  │workflow. │  │ rule_engine  │ │
│  └──────────┘  └──────────┘  │ py       │  └──────────────┘ │
│                              └──────────┘                     │
│  ┌─────────────────────────────────────────────────────────┐  │
│  │              AI Provider Layer                           │  │
│  │  ContextEngine → PromptEngine → DeepSeekProvider         │  │
│  │  InspectionPipeline → AuditWritingEngine                 │  │
│  └─────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

See `docs/system_architecture_v1.md` for the full architecture.

---

## Installation

```bash
# Clone the repository
git clone <repo-url>
cd Food-Audit-Agent

# Create a virtual environment (Python 3.10+)
python -m venv venv
venv\Scripts\activate    # Windows
source venv/bin/activate # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Set the DeepSeek API key (required for AI features)
set DEEPSEEK_API_KEY=sk-your-key-here
```

---

## Quick Start

### Health Check

```bash
python main.py health
```

### Manual Inspection

```bash
python main.py inspect --query "supplier"
python main.py inspect --id CP-BEV-RM-001
python main.py inspect --risk High
```

### AI-Powered Inspection

```bash
python demo_inspection_ai.py
```

### Audit Writing Demo

```bash
python demo_writing.py
```

### Semantic Search (RAG)

Local vector index over `knowledge/` and `skills/`, embedded with paratera `GLM-Embedding-2` (1024-d) and stored in SQLite. Requires `PARATERA_API_KEY` (or a provider entry in `~/.local/share/opencode/auth.json`).

```bash
python main.py index                  # incremental build (--force to rebuild)
python main.py search "supplier license expired" -k 5
python main.py rag-status
```

The index lives in `audit/.index/rag.db` and is git-ignored. Retrieval is hybrid: `0.65 × cosine + 0.35 × keyword coverage`, max 2 chunks per file. It only recalls candidates — always verify the original clause.

### CLI Usage

```
usage: main.py [-h] {health,inspect,index,search,rag-status} ...

Food Audit Agent CLI

positional arguments:
  {health,inspect,index,search,rag-status}
    health          Show agent health status
    inspect         Inspect checkpoints
    index           Build or update the semantic index
    search          Semantic search over knowledge and skills
    rag-status      Show semantic index status

options:
  -h, --help        Show help message

inspect options:
  --id CHECKPOINT_ID     Search by checkpoint ID
  --query QUERY          Keyword search
  --category CATEGORY    Category filter
  --risk RISK_LEVEL      Risk level filter

search options:
  query                  Natural-language question
  -k N                   Number of results (default 5)
  --scope {all,knowledge,skills}
  --json                 JSON output
```

### API Usage

Start the FastAPI server:

```bash
uvicorn api.server:app --host 0.0.0.0 --port 8000
```

Endpoints:

```bash
# Health
curl http://localhost:8000/health

# Search checkpoints
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"query": "supplier", "risk_level": "high"}'

# Full inspection
curl -X POST http://localhost:8000/inspect \
  -H "Content-Type: application/json" \
  -d '{"query": "supplier", "evidence": []}'
```

---

## AI Workflow

The system implements a 5-step AI pipeline:

```
InspectionRequest
       │
       ▼
1. InspectionWorkflow.build_context()    — search + enrich
2. ContextEngine.build_context()         — summarise + format
3. PromptEngine.build_inspection_prompt() — template → prompt
4. DeepSeekProvider.chat()               — LLM call
5. AIInspectionResult                    — structured result
       │
       ▼
AuditWritingEngine.generate_all()        — 6 writing generators
       │
       ▼
AuditWritingResult                       — professional report
```

All AI features require `DEEPSEEK_API_KEY` to be set. The core inspection engine (search, workflow, rules) works offline without AI.

### Word Report Export (v2.0 — Regulatory Format)

Generate a formal 12-section regulatory inspection report:

```bash
# Online (requires DeepSeek API key)
set DEEPSEEK_API_KEY=sk-... && python demo_export.py

# Offline (no API key required)
python demo_export.py
```

The exporter generates a formal Chinese government-style food safety inspection report:

- **文件**: `reports/output/{企业名称}_监督检查报告_{YYYYMMDD}_{HHMMSS}.docx`
- **格式**: A4, 宋体/黑体, 12 sections, tables with borders, page numbers
- **文件名**: Unique per export (timestamped, never overwrites existing files)
- **内容**: 企业基本信息、检查基本情况、检查项目统计、现场检查情况、发现问题及不符合项、风险分析、法规依据、整改要求、企业综合判定、检查结论、附件目录、检查人员签字
- **模式**: Online (AI-generated) or Offline (deterministic Chinese text)
- **依赖**: `python-docx` (no Office required)

---

## Agent Skill Library

The system adopts a **Modular Skill Architecture**. The inspection workflow is decomposed into 8 professional Skills, each mapped to a specific engine module:

| Skill | Status | Engine |
|-------|--------|--------|
| Checkpoint Match | implemented | InspectionPipeline, taxonomy, registry |
| Regulation Lookup | implemented | RegulationLoader, knowledge/regulations |
| Risk Assessment | implemented | RuleEngine, RiskRule |
| Inspection Review | implemented | InspectionPipeline, InspectionWorkflow |
| Report Generation | implemented | AuditWritingEngine, ReportExporter |
| Corrective Action | implemented | AuditWritingEngine |
| Enterprise Evaluation | implemented | EnterpriseEvaluation |
| Image Recognition | planning | (none) |

See `skills/` for full skill definitions, YAML configurations, and workflow documentation.

---

## Repository Structure

```
Food-Audit-Agent/
├── script/                    # Core engine
│   ├── ai/                 # AI provider framework
│   │   ├── base.py         # AIProvider ABC
│   │   ├── deepseek.py     # DeepSeek API implementation
│   │   ├── prompt_engine.py # Template-driven prompt builder
│   │   ├── context_engine.py # Inspection → AIContext converter
│   │   ├── inspection_pipeline.py # AI pipeline orchestrator
│   │   ├── writing_engine.py # Professional report writer
│   │   ├── report_exporter.py # Word document export engine
│   │   ├── provider.py     # ProviderManager lifecycle
│   │   ├── registry.py     # Provider name → class mapping
│   │   ├── schemas.py      # AI dataclasses
│   │   ├── exceptions.py   # Error hierarchy
│   │   ├── prompts.py      # Prompt builders (placeholders)
│   │   └── templates/      # Markdown prompt templates
│   ├── agent.py            # FoodAuditAgent orchestrator
│   ├── loader.py           # Knowledge loading pipeline
│   ├── models.py           # Data models & enums
│   ├── search.py           # Knowledge search engine
│   ├── workflow.py         # Inspection workflow engine
│   ├── rule_engine.py      # Evidence evaluation engine
│   ├── evidence.py         # Evidence management
│   ├── regulation_loader.py # Regulation knowledge base
│   ├── regulation_models.py # Regulation data models
│   └── utils.py            # Shared utilities
├── api/                    # FastAPI REST API
│   ├── server.py           # API server (4 endpoints)
│   └── schemas.py          # Pydantic request/response models
├── knowledge/              # Knowledge base (read-only)
│   ├── checkpoints/        # 25 checkpoint markdown files
│   ├── registry/           # Registry YAML files
│   ├── risk_rules/         # 25 risk rule YAML files
│   └── taxonomy/           # Taxonomy tree YAML
├── tests/                  # Pytest test suite (118 tests)
├── docs/                   # Architecture documentation
│   ├── system_architecture_v1.md
│   ├── developer_guidelines.md
│   ├── version_history.md
│   ├── ai_architecture.md
│   └── runtime_architecture.md
├── reports/                # Sprint reports (19 reports)
│   └── output/             # Generated Word documents (gitignored)
├── main.py                 # CLI entry point
├── demo*.py                # Demo scripts
├── requirements.txt        # Dependencies (5 packages)
└── pyproject.toml          # Project metadata
```

---

## Roadmap

### v1.0 — Current (2026-07-03)
- ✅ 25 beverage raw material checkpoints
- ✅ Knowledge loading, search, workflow, rule evaluation
- ✅ DeepSeek AI provider integration
- ✅ Prompt engine with 4 templates
- ✅ Context engine → AI context assembly
- ✅ AI inspection pipeline (5-step)
- ✅ Audit writing engine (6 generators)
- ✅ REST API (FastAPI, 4 endpoints)
- ✅ CLI (health / inspect / semantic search / index)
- ✅ 118 passing tests
- ✅ Word report export engine (.docx)

### v2.0 — Current
- ✅ Formal 12-section regulatory inspection report (市场监督管理局 format)
- ✅ Word export with tables, page numbers, color-coded conclusions
- ✅ Completely offline report generation (no AI required)
- ✅ Old fields preserved, backward-compatible with AI path

### v3.0 — Planned
- 🔲 Additional knowledge domains (production, facility, personnel, HACCP)
- 🔲 Multilingual prompt templates (Chinese report generation)
- 🔲 OCR and image analysis skills
- 🔲 Document parsing (PDF, DOCX)
- 🔲 Regulation database with version tracking
- 🔲 CAPA tracking and audit trail
- 🔲 Provider switching (Qwen, GLM, Doubao)
- 🔲 Web UI dashboard

---

## License

MIT
