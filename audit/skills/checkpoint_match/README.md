# Checkpoint Match

## Purpose

Maps free-form inspection findings to structured audit checkpoints. Converts raw auditor observations into indexable, rule-evaluable checkpoint references.

## Current Engine

InspectionPipeline (build_context), taxonomy tree filtering, registry keyword matching.

The 2-character sliding window comparison matches finding text against checkpoint titles and keywords. Matching is deterministic 鈥?no AI or LLM involved.

## Inputs

- findings (List[str]): Raw inspection problem descriptions.
- enterprise_type (str): Enterprise category used to filter applicable checkpoints.

## Outputs

- matched_checkpoints (List[Checkpoint]): Checkpoint candidates with relevance.
- unmatched_findings (List[str]): Findings with no match.

## Workflow Position

Stage 1 鈥?invoked first in the analysis pipeline. Downstream skills (Regulation Lookup, Risk Assessment) depend on its output.

## Status

implemented

## Limitations

- Matching is text-based (2-char sliding window); semantic understanding is not applied.
- Accuracy depends on finding phrasing matching checkpoint keywords.
- No fuzzy or synonym expansion.

## Example

Input: "渚涘簲鍟嗚鍙瘉宸茶繃鏈? 鈫?Matches CP-BEV-RM-001 (渚涘簲鍟嗚祫璐ㄥ鏍?
