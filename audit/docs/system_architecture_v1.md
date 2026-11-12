# System Architecture v1.0.0

**Date:** 2026-07-03

---

## Overall Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                        Application Layer                            鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹? 鈹?CLI      鈹? 鈹?FastAPI  鈹? 鈹?Demo     鈹? 鈹?Demo_ai  鈹? 鈹俉riting鈹?鈹?鈹? 鈹?main.py  鈹? 鈹?api/     鈹? 鈹?demo.py  鈹? 鈹?demo_... 鈹? 鈹俤emo   鈹?鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹攢鈹€鈹€鈹?鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹尖攢鈹€鈹€鈹€鈹€鈹?        鈹?            鈹?            鈹?            鈹?             鈹?        鈻?            鈻?            鈻?            鈻?             鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                      FoodAuditAgent                                 鈹?鈹?                      (script/agent.py)                                鈹?鈹?                                                                     鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?鈹? 鈹?Knowledge   鈹? 鈹?SearchEngine 鈹? 鈹?Workflow   鈹? 鈹?RuleEngine 鈹?鈹?鈹? 鈹?Loader      鈹? 鈹?(search)     鈹? 鈹?(workflow) 鈹? 鈹?(rule_eng) 鈹?鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹?鈹?鈹?        鈹?               鈹?                鈹?               鈹?       鈹?鈹?        鈻?               鈻?                鈻?               鈻?       鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?鈹? 鈹?                   AI Provider Layer                          鈹?  鈹?鈹? 鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?  鈹?鈹? 鈹? 鈹?Context  鈹? 鈹?Prompt   鈹? 鈹侷nspection鈹? 鈹?  Writing   鈹? 鈹?  鈹?鈹? 鈹? 鈹?Engine   鈹? 鈹?Engine   鈹? 鈹?Pipeline 鈹? 鈹?  Engine    鈹? 鈹?  鈹?鈹? 鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?  鈹?鈹? 鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?  鈹?鈹? 鈹? 鈹侾rovider  鈹? 鈹?DeepSeekProvider (httpx 鈫?api.deepseek) 鈹? 鈹?  鈹?鈹? 鈹? 鈹侻anager   鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹? 鈹?  鈹?鈹? 鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?                                              鈹?  鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## Module Dependency Graph

```
script/
鈹溾攢鈹€ models.py          鈫?dependency of ALL modules (no deps on others)
鈹溾攢鈹€ utils.py           鈫?dependency of loader, search
鈹溾攢鈹€ loader.py          鈫?depends on: models, utils
鈹溾攢鈹€ search.py          鈫?depends on: models
鈹溾攢鈹€ rule_engine.py     鈫?depends on: models
鈹溾攢鈹€ workflow.py        鈫?depends on: models, search
鈹溾攢鈹€ evidence.py        鈫?depends on: models
鈹溾攢鈹€ registry.py        鈫?standalone (skeleton / future)
鈹溾攢鈹€ agent.py           鈫?depends on: loader, search, workflow, rule_engine,
鈹?                       evidence, ai/ (ProviderManager, DeepSeekProvider)
鈹?鈹溾攢鈹€ ai/
鈹?  鈹溾攢鈹€ base.py        鈫?depends on: schemas
鈹?  鈹溾攢鈹€ schemas.py     鈫?standalone (pure dataclasses)
鈹?  鈹溾攢鈹€ exceptions.py  鈫?standalone (pure exceptions)
鈹?  鈹溾攢鈹€ registry.py    鈫?depends on: base
鈹?  鈹溾攢鈹€ provider.py    鈫?depends on: base, registry, exceptions
鈹?  鈹溾攢鈹€ deepseek.py    鈫?depends on: base, exceptions, schemas, httpx
鈹?  鈹溾攢鈹€ prompt_engine.py 鈫?standalone (pathlib, re)
鈹?  鈹溾攢鈹€ context_engine.py 鈫?depends on: workflow (InspectionContext), models
鈹?  鈹溾攢鈹€ inspection_pipeline.py 鈫?depends on: workflow, models, base,
鈹?  鈹?                           context_engine, prompt_engine, schemas
鈹?  鈹溾攢鈹€ writing_engine.py 鈫?depends on: base, context_engine,
鈹?  鈹?                       inspection_pipeline, prompt_engine, schemas
鈹?  鈹斺攢鈹€ prompts.py     鈫?standalone (placeholders)

api/
鈹溾攢鈹€ schemas.py         鈫?depends on: pydantic
鈹溾攢鈹€ server.py          鈫?depends on: core (FoodAuditAgent)
```

---

## Data Flow

```
   CLI / API Request
         鈹?         鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?FoodAuditAgent  鈹?  鈹?.initialize()   鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?           鈹?           鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?KnowledgeLoader 鈹?  鈹?.load_all()     鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?           鈹?           鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?KnowledgeRepo   鈹?  鈹?(registry,      鈹?  鈹? taxonomy,      鈹?  鈹? checkpoints)   鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?           鈹?           鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?SearchEngine    鈹?  鈹?Workflow        鈹?  鈹?RuleEngine      鈹?  鈹?                鈹?  鈹?InspectionCtx   鈹傗梽鈹€鈹€鈹€鈹€ Evidence
  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?           鈹?           鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?AI Pipeline (inspect_ai)        鈹?  鈹?                                鈹?  鈹?1. ContextEngine.build_context  鈹?  鈹?2. PromptEngine.build_prompt    鈹?  鈹?3. DeepSeekProvider.chat        鈹?  鈹?4. AIInspectionResult           鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?           鈹?           鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?WritingEngine   鈹?  鈹?.generate_all() 鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?           鈹?           鈻?  鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?  鈹?AuditWritingRes 鈹?  鈹?(report ready)  鈹?  鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## Runtime Flow

### Knowledge Loading

```
1. FoodAuditAgent.initialize()
2.   KnowledgeLoader(knowledge_dir)
3.     .initialize()              鈫?warn if missing directory
4.     .load_registry()           鈫?dict[str, RegistryEntry]
5.     .load_taxonomy()           鈫?dict[str, TaxonomyNode]
6.     .discover_checkpoints()    鈫?list of .md paths
7.     .load_checkpoint(path)     鈫?Checkpoint (parse frontmatter + sections)
8.     .load_all()                鈫?KnowledgeRepository
9.   KnowledgeSearchEngine(repo)
10.  InspectionWorkflow(repo, search, risk_rules)
11.  RuleEngine(repo, risk_rules)
12.  ProviderManager.register("deepseek") 鈫?optional
13. Return startup summary
```

### Inspection Workflow

```
1. FoodAuditAgent.inspect(query, checkpoint_id, category, risk_level, evidence)
2.   InspectionRequest(query, ...)
3.   InspectionWorkflow.build_context(request)
4.     _search_checkpoints()      鈫?matched checkpoints
5.     _lookup_registry()         鈫?registry entries
6.     _lookup_risk_rules()       鈫?applicable risk rules
7.     _lookup_taxonomy()         鈫?taxonomy nodes
8.     _validate()                鈫?warnings
9.   Attach evidence + evaluate   鈫?evaluation results
10. Return InspectionContext
```

### AI Inspection Workflow

```
1. FoodAuditAgent.inspect_ai(query, ...)
2.   InspectionPipeline.run(request)
3.     Step 1: InspectionWorkflow.build_context()     鈫?InspectionContext
4.     Step 2: ContextEngine.build_context()           鈫?AIContext
5.     Step 3: PromptEngine.build_inspection_prompt()  鈫?prompt string
6.     Step 4: DeepSeekProvider.chat(request)          鈫?AIResponse
7.     Return AIInspectionResult
```

### Audit Writing Workflow

```
1. AuditWritingEngine(inspection_result)
2.   generate_nonconformity()     鈫?nonconformity text
3.   generate_risk_analysis()     鈫?risk analysis text
4.   generate_corrective_action() 鈫?corrective action text
5.   generate_regulation_reference() 鈫?regulation text
6.   generate_audit_conclusion()  鈫?conclusion text
7.   generate_full_report()       鈫?complete report
8.   Return AuditWritingResult
```

---

## Knowledge Workflow

```
knowledge/
鈹溾攢鈹€ registry/
鈹?  鈹斺攢鈹€ beverage_raw_material_registry.yaml  鈫?RegistryEntry (25 entries)
鈹溾攢鈹€ taxonomy/
鈹?  鈹斺攢鈹€ beverage_knowledge_tree.yaml         鈫?TaxonomyNode tree (16 domains)
鈹溾攢鈹€ checkpoints/
鈹?  鈹斺攢鈹€ beverage/raw_material/CP-BEV-RM-*.md 鈫?Checkpoint (25 files)
鈹斺攢鈹€ risk_rules/
    鈹斺攢鈹€ beverage/raw_material/RR-CP-BEV-RM-*.yaml 鈫?RiskRule (25 files)

Loading:
  YAML files 鈫?read_yaml() 鈫?dataclass instances 鈫?KnowledgeRepository
  Markdown  鈫?read_markdown() 鈫?section parsing 鈫?Checkpoint 鈫?repo
```

---

## Package Structure

```
Food-Audit-Agent/
鈹溾攢鈹€ script/               # Core engine (24 Python files)
鈹?  鈹溾攢鈹€ ai/             # AI provider layer (13 Python files)
鈹?  鈹溾攢鈹€ __init__.py     # Public API exports
鈹?  鈹溾攢鈹€ agent.py        # FoodAuditAgent orchestrator
鈹?  鈹溾攢鈹€ loader.py       # Knowledge loading (704 lines)
鈹?  鈹溾攢鈹€ models.py       # Data models (210 lines)
鈹?  鈹溾攢鈹€ search.py       # Search engine
鈹?  鈹溾攢鈹€ workflow.py     # Inspection workflow
鈹?  鈹溾攢鈹€ rule_engine.py  # Rule evaluation engine
鈹?  鈹溾攢鈹€ evidence.py     # Evidence management
鈹?  鈹溾攢鈹€ registry.py     # Checkpoint registry (skeleton)
鈹?  鈹斺攢鈹€ utils.py        # Shared utilities
鈹溾攢鈹€ api/                # FastAPI REST API
鈹?  鈹溾攢鈹€ server.py       # FastAPI application
鈹?  鈹斺攢鈹€ schemas.py      # Pydantic request/response models
鈹溾攢鈹€ knowledge/          # Knowledge base data
鈹?  鈹溾攢鈹€ checkpoints/    # 25 checkpoint markdown files
鈹?  鈹溾攢鈹€ registry/       # 1 registry YAML file
鈹?  鈹溾攢鈹€ risk_rules/     # 25 risk rule YAML files
鈹?  鈹斺攢鈹€ taxonomy/       # 1 taxonomy YAML file
鈹溾攢鈹€ tests/              # Test suite (7 test files, 118 tests)
鈹溾攢鈹€ docs/               # Architecture documentation
鈹溾攢鈹€ reports/            # Sprint reports (19 reports)
鈹溾攢鈹€ main.py             # CLI entry point
鈹溾攢鈹€ demo*.py            # Demo scripts (4 files)
鈹溾攢鈹€ README.md           # Project README
鈹溾攢鈹€ requirements.txt    # Python dependencies
鈹斺攢鈹€ pyproject.toml      # Project metadata
```
