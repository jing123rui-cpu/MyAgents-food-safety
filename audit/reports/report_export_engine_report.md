# Report Export Engine Architecture

**Version:** 1.1
**Date:** 2026-07-06
**Sprint:** 40.1

---

## 1. Overview

The Report Export Engine converts `AuditWritingResult` objects into professionally formatted Word (`.docx`) documents suitable for official submission. It is a standalone module with no dependencies on `RuleEngine`, `InspectionPipeline`, `PromptEngine`, `ContextEngine`, or `WritingEngine`.

---

## 2. Architecture Diagram

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                   Application Layer                         鈹?鈹?                                                             鈹?鈹? demo_export.py                                              鈹?鈹?     鈹?                                                      鈹?鈹?     鈹溾攢鈹€ FoodAuditAgent.inspect_ai()                         鈹?鈹?     鈹?      鈫?AIInspectionResult                            鈹?鈹?     鈹?                                                      鈹?鈹?     鈹溾攢鈹€ AuditWritingEngine.generate_all()                   鈹?鈹?     鈹?      鈫?AuditWritingResult                            鈹?鈹?     鈹?                                                      鈹?鈹? 鈹斺攢鈹€ ReportExporter.export_word()                        鈹?鈹?             鈫?ReportExportResult                             鈹?鈹?             鈫?reports/output/{name}_鐩戠潱妫€鏌ユ姤鍛奯{ts}.docx  鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?                  ReportExporter                             鈹?鈹? script/ai/report_exporter.py                                  鈹?鈹?                                                             鈹?鈹? 鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?鈹? 鈹? export_word(writing_result, output_path="")          鈹?   鈹?鈹? 鈹?     鈹?                                              鈹?   鈹?鈹? 鈹?     鈹溾攢鈹€ _generate_unique_path()  鈥?鍞竴鏂囦欢鍚?      鈹?   鈹?鈹? 鈹?     鈹?   鈹斺攢鈹€ {name}_鐩戠潱妫€鏌ユ姤鍛奯{ts}.docx           鈹?   鈹?鈹? 鈹?     鈹?   鈹斺攢鈹€ 闃茶鐩?(counter suffix _01, _02, 鈥?    鈹?   鈹?鈹? 鈹?     鈹?                                              鈹?   鈹?鈹? 鈹?     鈹溾攢鈹€ out.parent.mkdir()      鈥?鑷姩鍒涘缓鐩綍      鈹?   鈹?鈹? 鈹?     鈹?                                              鈹?   鈹?鈹? 鈹?     鈹溾攢鈹€ _create_document()                          鈹?   鈹?鈹? 鈹?     鈹?   鈹溾攢鈹€ _add_header()       鈥?鏍囬 + 浼佷笟淇℃伅  鈹?   鈹?鈹? 鈹?     鈹?   鈹溾攢鈹€ _add_section() 脳 5  鈥?涓€ ~ 浜旂珷        鈹?   鈹?鈹? 鈹?     鈹?   鈹溾攢鈹€ _add_enterprise_conclusion() 鈥?绗叚绔? 鈹?   鈹?鈹? 鈹?     鈹?   鈹斺攢鈹€ _add_footer()       鈥?鐗堟湰椤佃剼         鈹?   鈹?鈹? 鈹?     鈹?                                              鈹?   鈹?鈹? 鈹?     鈹溾攢鈹€ Document.save()        鈥?PermissionError 鈫?  鈹?   鈹?鈹? 鈹?     鈹?   涓枃鍙嬪ソ鎻愮ず                                鈹?   鈹?鈹? 鈹?     鈹?                                              鈹?   鈹?鈹? 鈹? Returns: ReportExportResult                          鈹?   鈹?鈹? 鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?   鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

---

## 3. Call Flow

```
start
  鈹?  鈻?demo_export.py
  鈹?  鈹溾攢鈹€ 1. Agent.initialize()
  鈹?    Load knowledge + AI provider
  鈹?  鈹溾攢鈹€ 2. Agent.inspect_ai(query="production process")
  鈹?    鈹?  鈹?    鈹溾攢鈹€ InspectionWorkflow.build_context()
  鈹?    鈹溾攢鈹€ ContextEngine.build_context()
  鈹?    鈹溾攢鈹€ PromptEngine.build_inspection_prompt()
  鈹?    鈹溾攢鈹€ DeepSeekProvider.chat()
  鈹?    鈹斺攢鈹€ AIInspectionResult
  鈹?  鈹溾攢鈹€ 3. AuditWritingEngine.generate_all(insp_result)
  鈹?    鈹?  鈹?    鈹溾攢鈹€ generate_nonconformity()
  鈹?    鈹溾攢鈹€ generate_risk_analysis()
  鈹?    鈹溾攢鈹€ generate_regulation_reference()
  鈹?    鈹溾攢鈹€ generate_corrective_action()
  鈹?    鈹溾攢鈹€ generate_audit_conclusion()
  鈹?    鈹斺攢鈹€ AuditWritingResult
  鈹?  鈹斺攢鈹€ 4. ReportExporter.export_word(writing_result, output_path="")
        鈹?        鈹溾攢鈹€ _generate_unique_path(base_dir, writing_result)
        鈹?  鈹斺攢鈹€ {enterprise_name}_鐩戠潱妫€鏌ユ姤鍛奯{YYYYMMDD}_{HHMMSS}.docx
        鈹?  鈹斺攢鈹€ 闃茶鐩栵細宸插瓨鍦ㄦ椂杩藉姞 _01, _02, 鈥?        鈹?        鈹溾攢鈹€ out.parent.mkdir(parents=True, exist_ok=True)
        鈹?        鈹溾攢鈹€ _create_document()
        鈹?  鈹溾攢鈹€ ...
        鈹?  鈹斺攢鈹€ ...
        鈹?        鈹溾攢鈹€ Document.save()
        鈹?  鈹溾攢鈹€ PermissionError 鈫?涓枃鍙嬪ソ鎻愮ず
        鈹?  鈹斺攢鈹€ Success 鈫?ReportExportResult
        鈹?        鈹斺攢鈹€ ReportExportResult
              鈹溾攢鈹€ filepath
              鈹溾攢鈹€ filename
              鈹溾攢鈹€ generated_time
              鈹溾攢鈹€ success
              鈹斺攢鈹€ error
```

---

## 4. Word Document Structure

### 4.1 Layout

| Property | Value |
|----------|-------|
| Paper size | A4 (21.0 脳 29.7 cm) |
| Margins | 2.54 cm top/bottom, 3.17 cm left/right |
| Title font | 榛戜綋, 16pt, bold, centered |
| Section heading | 榛戜綋, 16pt, bold |
| Body font | 瀹嬩綋, 12pt |
| Body indent | First line 0.74 cm (2 characters) |
| Footer | 9pt, grey, centered |

### 4.2 Sections

| # | Heading | Source Field |
|---|---------|-------------|
| 鈥?| Title + facility info | `wr.metadata` (facility_name, audit_date, auditor_name) |
| 涓€ | 妫€鏌ユ儏鍐?| `wr.nonconformity` |
| 浜?| 椋庨櫓鍒嗘瀽 | `wr.risk_analysis` |
| 涓?| 娉曡渚濇嵁 | `wr.regulation_reference` |
| 鍥?| 鏁存敼寤鸿 | `wr.corrective_action` |
| 浜?| 妫€鏌ョ粨璁?| `wr.audit_conclusion` |
| 鍏?| 浼佷笟缁煎悎鍒ゅ畾 | `wr.metadata.enterprise_evaluation` |

### 4.3 Enterprise Conclusion Logic

```python
enterprise_evaluation = wr.metadata.get("enterprise_evaluation")
if enterprise_evaluation.overall_result == "浼佷笟閫氳繃妫€鏌?:
    output: "浼佷笟閫氳繃妫€鏌?  (green text)
else:
    output: "浼佷笟闇€瑕佹暣鏀?  (red text, bold)
    append: "闇€15鏃ュ唴鎻愪氦鏁存敼鎶ュ憡鑷冲睘鍦板競鍦虹洃鐫ｇ鐞嗗眬銆?
```

---

## 5. Class Relationships

```
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?             ReportExportResult               鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?+ filepath: str                              鈹?鈹?+ filename: str                              鈹?鈹?+ generated_time: str                        鈹?鈹?+ success: bool                              鈹?鈹?+ error: str                                 鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?
鈹屸攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?              ReportExporter                 鈹?鈹溾攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?鈹?- _doc: Optional[Document]                   鈹?鈹?                                             鈹?鈹?+ export_word(writing_result, path)          鈹?鈹?    鈫?ReportExportResult                     鈹?鈹?                                             鈹?鈹?# _create_document(writing_result)           鈹?鈹?# _add_header(writing_result)                鈹?鈹?# _add_section(heading, body)                鈹?鈹?# _add_enterprise_conclusion(writing_result) 鈹?鈹?# _add_footer()                              鈹?鈹斺攢鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹€鈹?```

### Dependencies

```
ReportExporter
  鈹斺攢鈹€ AuditWritingResult      (from writing_engine.py 鈥?dataclass only)
  鈹斺攢鈹€ EnterpriseEvaluation    (from models.py 鈥?dataclass only, via metadata)
  鈹斺攢鈹€ python-docx             (Document, Paragraph, Run, RGBColor, Pt, Cm)
```

The exporter is strictly read-only with respect to the rest of the system. It never calls `RuleEngine`, `InspectionPipeline`, `PromptEngine`, `ContextEngine`, or `WritingEngine`.

---

## 6. Error Handling

| Scenario | Behaviour |
|----------|-----------|
| `output_path` not specified | Auto-generated unique filename under `reports/output/` |
| `output_path` is a directory | File is created inside the directory via `_generate_unique_path()` |
| `output_path` directory does not exist | Auto-created via `Path.mkdir(parents=True)` |
| File already exists | Counter suffix appended (`_01`, `_02`, 鈥? 鈥?never overwritten |
| `AuditWritingResult` has empty fields | Section body shows "锛堟棤鍐呭锛? |
| No `enterprise_evaluation` in metadata | Enterprise section shows no decision |
| `python-docx` not installed | ImportError at module load time |
| PermissionError (file open in Word) | Friendly Chinese message returned in `result.error` |
| Disk full / other IO error | Returned in `ReportExportResult.error` |
| Invalid path characters | Caught by `Document.save()`, returned as error |

---

## 7. Future: PDF Support Plan

The exporter architecture is designed for extensibility:

```
ReportExporter (abstract base)
  鈹?  鈹溾攢鈹€ WordExporter       (current 鈥?python-docx)
  鈹溾攢鈹€ PdfExporter        (planned 鈥?weasyprint / reportlab)
  鈹斺攢鈹€ HtmlExporter       (planned 鈥?Jinja2 template)
```

Each exporter implements:

```python
class BaseExporter(ABC):
    @abstractmethod
    def export(self, writing_result: AuditWritingResult, output_path: str) -> ReportExportResult:
        ...
```

The current `ReportExporter` is a concrete implementation. A future refactor can extract the common interface.

---

## 8. File Manifest

| File | Size | Description |
|------|------|-------------|
| `script/ai/report_exporter.py` | ~7KB | Main export engine |
| `demo_export.py` | ~2KB | Export demo script |
| `reports/output/` | dir | Generated Word documents |
| `requirements.txt` | +1 line | Added `python-docx>=1.2.0` |
| `README.md` | modified | Added export section + roadmap |

---

## 9. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1 | 2026-07-06 | Auto-generated unique filenames; PermissionError handling; auto-create output dir |
| 1.0 | 2026-07-03 | Initial release 鈥?Report Export Engine |

