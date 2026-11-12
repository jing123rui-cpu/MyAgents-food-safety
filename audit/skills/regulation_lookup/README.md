# Regulation Lookup

## Purpose

Retrieves food safety regulations applicable to the enterprise type and matched checkpoints. Populates the regulation reference table in the inspection report.

## Current Engine

RegulationLoader 鈥?reads regulation_registry.yaml and Markdown full-text files from knowledge/regulations/. Supports enterprise type hierarchy (general_food 鈫?beverage 鈫?packaged_water) for applicable regulation filtering.

## Inputs

- matched_checkpoints (List[Checkpoint]): Checkpoints from the previous stage.
- enterprise_type (str): Used to resolve applicable regulations via the type hierarchy.

## Outputs

- regulation_references (List[RegulationReference]): Applicable regulation metadata and content.
- regulation_table (List[Dict]): Ordered table rows for Section 7 of the report.

## Workflow Position

Stage 2 鈥?consumes Checkpoint Match output and feeds into Risk Assessment.

## Status

implemented

## Limitations

- Requires pre-defined regulation registry entries; novel regulations must be added manually.
- Full-text content is in Markdown; no legal database or version tracking.

## Example

Input: checkpoint CP-BEV-RM-001 鈫?Output: REG-FOOD-SAFETY-LAW (椋熷搧瀹夊叏娉?, Article 33, 50
