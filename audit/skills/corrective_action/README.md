# Corrective Action

## Purpose

Recommends specific corrective actions for each non-compliant finding, including root cause analysis, immediate corrections, preventive measures, responsible parties, and deadlines.

## Current Engine

AuditWritingEngine.generate_corrective_action() 鈥?assembles inspection context, builds a prompt via PromptEngine, and invokes the AI provider (or uses offline fallback) to produce professional corrective action text.

In offline mode, generates deterministic Chinese-language corrective requirements without requiring an API key.

## Inputs

- evaluation_results (List[EvaluationResult]): Non-compliant results requiring corrective action.
- inspection_context (InspectionContext): Evidence, checkpoints, and risk assessment data.

## Outputs

- corrective_requirements (str): Formatted text for Section 8 (鏁存敼瑕佹眰) of the inspection report.

## Workflow Position

Stage 5 鈥?after Enterprise Evaluation, before Report Generation.

## Status

implemented

## Limitations

- AI-generated recommendations depend on prompt quality; offline mode uses template-based text.
- Does not track CAPA lifecycle (verification, closure dates); output is advisory text only.

## Example

Input: Non-compliant result for CP-BEV-RM-001 (supplier license expired) 鈫?Output: "渚涘簲鍟嗚鍙瘉宸茶繃鏈燂紝搴旂珛鍗虫洿鏂拌鍙瘉锛屽姞寮轰緵搴斿晢璧勮川瀹℃牳..."
