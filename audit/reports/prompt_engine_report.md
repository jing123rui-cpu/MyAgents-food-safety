# Prompt Engine Report

**Date:** 2026-07-03

---

## Architecture

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?              PromptEngine                    鈹?鈹? (script/ai/prompt_engine.py)                  鈹?鈹?                                             鈹?鈹? build_inspection_prompt()                   鈹?鈹? build_checkpoint_prompt()                   鈹?鈹? build_report_prompt()                       鈹?鈹? build_question_prompt()                     鈹?鈹?                                             鈹?鈹? load_template(name)                         鈹?鈹? render(template, variables)                 鈹?鈹? list_templates()                            鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?               鈹?reads from disk
               鈻?鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?         Templates Directory                  鈹?鈹?         script/ai/templates/                   鈹?鈹?                                             鈹?鈹? inspection.md    鈥?combined audit prompt    鈹?鈹? checkpoint.md    鈥?single checkpoint eval   鈹?鈹? report.md        鈥?report generation        鈹?鈹? question.md      鈥?free-form Q&A            鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

**Key design decisions:**

- **Zero dependencies on AIProvider** 鈥?PromptEngine only builds strings. It never imports `httpx`, `AIRequest`, or any provider class.
- **Template-first** 鈥?All prompt structure lives in Markdown files, not in Python code. Changing a prompt requires editing a `.md` file, not Python.
- **Cache layer** 鈥?Templates are read from disk once and cached in memory for subsequent calls.
- **Safe placeholder replacement** 鈥?Unrecognized `{{placeholders}}` are left verbatim so missing variables are visible rather than silently dropped.

---

## Template Loading

Templates are loaded from `script/ai/templates/` (relative to `prompt_engine.py`).

| Method | File Loaded |
|--------|-------------|
| `load_template("inspection")` | `templates/inspection.md` |
| `load_template("checkpoint")` | `templates/checkpoint.md` |
| `load_template("report")` | `templates/report.md` |
| `load_template("question")` | `templates/question.md` |

**Caching:** After the first read, the raw content is stored in `self._cache` and never re-read from disk. This avoids I/O overhead on repeated calls.

---

## Placeholder Replacement

The engine uses `re.sub(r"\{\{(\w+)\}\}", ...)` to replace placeholders.

**Example:**

```python
engine.render("checkpoint", {
    "checkpoint_id": "CP-BEV-RM-001",
    "checkpoint_name": "Raw Material Receiving",
    "evidence": "COA verified.",
})
```

Given template snippet:
```
- **ID:** {{checkpoint_id}}
- **Name:** {{checkpoint_name}}
```

Produces:
```
- **ID:** CP-BEV-RM-001
- **Name:** Raw Material Receiving
```

**Missing variables:** If a placeholder has no corresponding key, it is left as-is (e.g. `{{unknown}}` stays `{{unknown}}`).

---

## Example Prompt 鈥?`build_inspection_prompt`

**Input:**

```python
engine.build_inspection_prompt(
    task="Evaluate RM-001 against regulatory requirements.",
    checkpoint_id="CP-BEV-RM-001",
    checkpoint_name="Raw Material Receiving",
    checkpoint_domain="Raw Material Management",
    checkpoint_objective="Verify incoming raw materials conform to specifications.",
    risk_rules="RR-CP-BEV-RM-001: High 鈥?Missing COA 鈫?FAIL",
    evidence="COA for lot #12345 received and verified.",
    regulations="GB 14881-2013 Section 7.2",
    expected_output="Return PASS/FAIL with findings.",
)
```

**Output:**

```markdown
# Role
You are a food safety audit AI assistant for beverage manufacturing.
Your role is to evaluate inspection data against regulatory requirements
and provide structured assessments.

# Task
Evaluate RM-001 against regulatory requirements.

# Checkpoint
- **ID:** CP-BEV-RM-001
- **Name:** Raw Material Receiving
- **Domain:** Raw Material Management
- **Module:** 
- **Objective:** Verify incoming raw materials conform to specifications.
- **Risk Level:** 

# Risk Rule
RR-CP-BEV-RM-001: High 鈥?Missing COA 鈫?FAIL

# Evidence
COA for lot #12345 received and verified.

# Regulations
GB 14881-2013 Section 7.2

# Expected Output
Return PASS/FAIL with findings.
```

---

## Future Multilingual Support

The template architecture makes multilingual support straightforward:

1. **Create locale subdirectories:**

```
templates/
鈹溾攢鈹€ en/
鈹?  鈹溾攢鈹€ inspection.md
鈹?  鈹溾攢鈹€ checkpoint.md
鈹?  鈹溾攢鈹€ report.md
鈹?  鈹斺攢鈹€ question.md
鈹溾攢鈹€ zh/
鈹?  鈹溾攢鈹€ inspection.md
鈹?  鈹溾攢鈹€ checkpoint.md
鈹?  鈹溾攢鈹€ report.md
鈹?  鈹斺攢鈹€ question.md
```

2. **Extended PromptEngine:**

```python
class PromptEngine:
    def __init__(self, templates_dir=None, locale="en"):
        self._locale = locale
        self._templates_dir = Path(templates_dir or ...) / locale
```

3. **Usage:**

```python
engine_en = PromptEngine(locale="en")   # loads templates/en/
engine_zh = PromptEngine(locale="zh")   # loads templates/zh/
```

No changes to the builder methods are needed 鈥?only the Markdown content changes per locale.

---

## File Inventory

| File | Lines | Purpose |
|------|-------|---------|
| `script/ai/prompt_engine.py` | ~170 | PromptEngine class |
| `script/ai/templates/inspection.md` | 25 | Combined inspection prompt |
| `script/ai/templates/checkpoint.md` | 26 | Single checkpoint evaluation |
| `script/ai/templates/report.md` | 30 | Report generation |
| `script/ai/templates/question.md` | 16 | Free-form Q&A |
| `reports/prompt_engine_report.md` | 鈥?| This report |

