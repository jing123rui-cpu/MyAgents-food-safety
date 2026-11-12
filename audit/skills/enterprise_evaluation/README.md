# Enterprise Evaluation

## Purpose

Aggregates individual checkpoint compliance results into an enterprise-level conclusion. Determines whether the enterprise passes inspection or requires rectification.

## Current Engine

EnterpriseEvaluation dataclass (script/models.py).

Decision logic:

- If non_compliant_count == 0: overall_result = "浼佷笟閫氳繃妫€鏌?
- If non_compliant_count > 0: overall_result = "浼佷笟闇€瑕佹暣鏀?

## Inputs

- evaluation_results (List[EvaluationResult]): Complete set of per-checkpoint evaluation results.

## Outputs

- enterprise_evaluation (EnterpriseEvaluation): Aggregated evaluation with total_checkpoints, compliant_count, non_compliant_count, not_applicable_count, overall_result, summary.

## Workflow Position

Stage 4 鈥?after Risk Assessment, before Corrective Action and Report Generation.

## Status

implemented

## Limitations

- Decision is binary (pass/rectification); no graded or conditional conclusions.
- Does not weight findings by severity; any non-compliance triggers rectification.

## Example

Input: 10 compliant + 2 non-compliant 鈫?Output: overall_result = "浼佷笟闇€瑕佹暣鏀?, total_checkpoints = 12, compliant_count = 10, non_compliant_count = 2
