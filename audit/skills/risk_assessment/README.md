# Risk Assessment

## Purpose

Determines whether each inspection finding is compliant or non-compliant against predefined risk rules. Provides scoring and risk-level classification.

## Current Engine

RuleEngine 鈥?deterministic rule evaluation engine. No AI or LLM involved.

Logic: For each evidence item, the engine locates the corresponding risk rule, evaluates evidence completeness and description quality, applies severity-based attachment requirements, and returns a structured EvaluationResult.

## Inputs

- evidence (List[Evidence]): Evidence items with descriptions and attachments.
- matched_checkpoints (List[Checkpoint]): Checkpoints providing context.

## Outputs

- evaluation_results (List[EvaluationResult]): Status (COMPLIANT / NON_COMPLIANT / NOT_APPLICABLE), score (0.0-1.0), reason, violated laws, recommendation.
- statistics (Dict): Summary counts including key_risk and general_risk breakdown.

## Workflow Position

Stage 3 鈥?depends on Checkpoint Match and Regulation Lookup. Output drives Enterprise Evaluation.

## Status

implemented

## Limitations

- Evaluation is rule-based; severity thresholds are hardcoded.
- Critical/High severity rules require attachments for compliance determination.
- No continuous scoring; binary pass/fail per checkpoint.

## Example

Input: evidence with empty description on CP-BEV-RM-001 鈫?Output: NON_COMPLIANT, score 0.0, recommendation to verify supplier license
