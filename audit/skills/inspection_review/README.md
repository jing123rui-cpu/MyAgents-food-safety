# Inspection Review

## Purpose

Orchestrates the end-to-end inspection review process. Coordinates knowledge retrieval, context assembly, prompt generation, and AI provider invocation into a single pipeline.

## Current Engine

InspectionPipeline 鈥?wires InspectionWorkflow, ContextEngine, PromptEngine, and AIProvider into a unified run() call.

Steps:

1. InspectionWorkflow.build_context() 鈥?search and enrich
2. ContextEngine.build_context() 鈥?summarise and format
3. PromptEngine.build_inspection_prompt() 鈥?template to prompt
4. AIProvider.chat() 鈥?LLM invocation (optional; offline mode available)

## Inputs

- inspection_request (InspectionRequest): Query parameters, evidence, and filter criteria.
- knowledge_repository (KnowledgeRepository): Pre-loaded knowledge base.

## Outputs

- inspection_context (InspectionContext): Aggregated context from knowledge base and workflow.
- ai_inspection_result (AIInspectionResult): Structured result with prompt, response, latency, provider metadata.

## Workflow Position

Orchestration layer spanning stages 1-3. Provides the integrated context consumed by Report Generation and Corrective Action.

## Status

implemented

## Limitations

- AI provider is optional; offline mode produces InspectionContext without LLM response.
- Requires pre-loaded KnowledgeRepository; does not perform live knowledge discovery.

## Example

Input: InspectionRequest(query="supplier", evidence=[...]) 鈫?Output: AIInspectionResult with matched checkpoints and AI analysis
