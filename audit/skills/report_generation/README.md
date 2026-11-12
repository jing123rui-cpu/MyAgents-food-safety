# Report Generation

## Purpose

Produces formal food safety inspection reports in Chinese government regulatory format. Supports both AI-assisted (online) and deterministic (offline) generation.

## Current Engine

- AuditWritingEngine (script/ai/writing_engine.py): Generates all 12 sections of the report content, including enterprise info, inspection overview, statistics, findings, risk analysis, regulation references, corrective requirements, and conclusions.
- ReportExporter (script/ai/report_exporter.py): Converts AuditWritingResult to a formatted Word (.docx) document with page numbers, table borders, color-coded conclusions, and unique timestamped filenames.

## Inputs

- audit_writing_result (AuditWritingResult): All 12 sections of report content.
- enterprise_info (Dict): Enterprise name, enterprise type, auditor name, inspection date.

## Outputs

- word_document (str): Absolute path to the generated .docx file.
- export_result (ReportExportResult): Metadata object with filepath, filename, generated_time, success flag.

## Workflow Position

Stage 6 鈥?final output stage. Consumes outputs from all upstream skills.

## Status

implemented

## Limitations

- Output format is Word (.docx) only; PDF export is not available.
- Offline mode uses deterministic templates; AI-assisted mode requires DeepSeek API key.
- Report layout is fixed (12-section structure); custom section ordering is not supported.

## Example

Input: AuditWritingResult with enterprise_info={"name": "XX楗枡鏈夐檺鍏徃"} 鈫?Output: reports/output/XX楗枡鏈夐檺鍏徃_鐩戠潱妫€鏌ユ姤鍛奯20260708_120000.docx
