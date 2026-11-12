"""Prompt template builders for AI provider interactions.

Each function returns a prompt string built from the provided context.
Currently all functions return empty strings — concrete implementations
will be added when providers are integrated.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional


def build_checkpoint_prompt(
    checkpoint_id: str,
    checkpoint_name: str,
    evidence_description: str,
    risk_level: str,
    laws: Optional[List[str]] = None,
) -> str:
    """Build a prompt that asks the AI to evaluate a single checkpoint.

    Parameters
    ----------
    checkpoint_id
        The checkpoint identifier (e.g. ``CP-BEV-RM-001``).
    checkpoint_name
        Human-readable checkpoint name.
    evidence_description
        Description of the evidence collected for this checkpoint.
    risk_level
        Risk level string (e.g. ``"High"``, ``"Critical"``).
    laws
        Applicable laws and regulations.

    Returns
    -------
    str
        The formatted prompt.

    TODO: Build a structured prompt for checkpoint evaluation.
    """
    return ""


def build_image_prompt(
    checkpoint_id: str,
    image_description: str,
    requirements: Optional[List[str]] = None,
) -> str:
    """Build a prompt that asks the AI to analyse an audit image.

    Parameters
    ----------
    checkpoint_id
        Associated checkpoint identifier.
    image_description
        Human description of what the image should contain.
    requirements
        Specific requirements the image should satisfy.

    Returns
    -------
    str
        The formatted prompt.

    TODO: Build a structured prompt for image analysis.
    """
    return ""


def build_document_prompt(
    checkpoint_id: str,
    document_type: str,
    expected_fields: Optional[List[str]] = None,
    laws: Optional[List[str]] = None,
) -> str:
    """Build a prompt that asks the AI to analyse an audit document.

    Parameters
    ----------
    checkpoint_id
        Associated checkpoint identifier.
    document_type
        Type of document (e.g. ``"生产许可证"``, ``"COA报告"``).
    expected_fields
        Fields the AI should extract from the document.
    laws
        Applicable laws and regulations.

    Returns
    -------
    str
        The formatted prompt.

    TODO: Build a structured prompt for document analysis.
    """
    return ""


def build_report_prompt(
    checkpoints: List[Dict[str, Any]],
    evaluation_results: List[Dict[str, Any]],
    facility_name: str = "",
    auditor_name: str = "",
) -> str:
    """Build a prompt that asks the AI to draft an audit report.

    Parameters
    ----------
    checkpoints
        List of checkpoint dicts with id, name, status, etc.
    evaluation_results
        List of evaluation result dicts.
    facility_name
        Name of the audited facility.
    auditor_name
        Name of the auditor.

    Returns
    -------
    str
        The formatted prompt.

    TODO: Build a structured prompt for report generation.
    """
    return ""
