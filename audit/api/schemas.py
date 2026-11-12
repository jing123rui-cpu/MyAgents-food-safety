"""Pydantic request/response schemas for the Food Audit Agent API."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


# ── Evidence ───────────────────────────────────────────────────────

class EvidenceItem(BaseModel):
    """A single piece of inspection evidence submitted via the API."""
    id: str
    evidence_type: str = Field(description="OBSERVATION | PHOTO | DOCUMENT | MEASUREMENT | LAB_REPORT | VIDEO | SYSTEM_RECORD")
    checkpoint_id: str
    description: str = ""
    source: str = ""
    attachments: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ── Checkpoint / Registry / Rule ───────────────────────────────────

class CheckpointResponse(BaseModel):
    """Checkpoint as returned by the API."""
    checkpoint_id: str
    checkpoint_name: str
    domain: str = ""
    module: str = ""
    unit: str = ""
    category: str = ""
    applicable_products: List[str] = Field(default_factory=list)
    risk_level: str = ""
    priority: str = ""
    estimated_time: str = ""
    objective: str = ""


class RegistryEntryResponse(BaseModel):
    """Registry entry as returned by the API."""
    id: str
    title: str
    category: str = ""
    subcategory: str = ""
    risk_level: str = ""
    laws: List[str] = Field(default_factory=list)
    keywords: List[str] = Field(default_factory=list)
    evidence_required: List[str] = Field(default_factory=list)


class RiskRuleResponse(BaseModel):
    """Risk rule as returned by the API."""
    rule_id: str
    risk_level: str = ""
    condition: str = ""
    description: str = ""


class TaxonomyNodeResponse(BaseModel):
    """Taxonomy node as returned by the API."""
    id: str
    name: str


class EvaluationResultResponse(BaseModel):
    """Evaluation result as returned by the API."""
    checkpoint_id: str
    rule_id: str
    evidence_id: str
    status: str
    score: float = 0.0
    reason: str = ""
    violated_laws: List[str] = Field(default_factory=list)
    recommendation: str = ""
    metadata: Dict[str, Any] = Field(default_factory=dict)


# ── Request Schemas ────────────────────────────────────────────────

class SearchRequest(BaseModel):
    """Search parameters."""
    query: str = Field(default="", description="Keyword search across titles, keywords, and markdown body")
    checkpoint_id: str = Field(default="", description="Exact checkpoint ID lookup")
    category: str = Field(default="", description="Category or subcategory name")
    risk_level: str = Field(default="", description="Risk level (High, Medium, Low, etc.)")


class InspectRequest(BaseModel):
    """Inspection parameters — same as SearchRequest plus optional evidence."""
    query: str = Field(default="", description="Keyword search across titles, keywords, and markdown body")
    checkpoint_id: str = Field(default="", description="Exact checkpoint ID lookup")
    category: str = Field(default="", description="Category or subcategory name")
    risk_level: str = Field(default="", description="Risk level (High, Medium, Low, etc.)")
    evidence: List[EvidenceItem] = Field(default_factory=list, description="Optional evidence items to validate and evaluate")


# ── Response Schemas ───────────────────────────────────────────────

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    registry: int = 0
    checkpoints: int = 0
    risk_rules: int = 0
    taxonomy_nodes: int = 0
    warnings: int = 0
    errors: int = 0
    message: str = ""


class SearchResponse(BaseModel):
    """Search results."""
    total: int = 0
    checkpoints: List[CheckpointResponse] = Field(default_factory=list)
    registry_entries: List[RegistryEntryResponse] = Field(default_factory=list)
    risk_rules: List[RiskRuleResponse] = Field(default_factory=list)
    taxonomy_nodes: List[TaxonomyNodeResponse] = Field(default_factory=list)


class InspectResponse(BaseModel):
    """Full inspection results."""
    request: SearchRequest = Field(default_factory=SearchRequest)
    matched_checkpoints: List[CheckpointResponse] = Field(default_factory=list)
    matched_registry_entries: List[RegistryEntryResponse] = Field(default_factory=list)
    matched_risk_rules: List[RiskRuleResponse] = Field(default_factory=list)
    matched_taxonomy_nodes: List[TaxonomyNodeResponse] = Field(default_factory=list)
    evidence: List[EvidenceItem] = Field(default_factory=list)
    evaluation_results: List[EvaluationResultResponse] = Field(default_factory=list)
    warnings: List[str] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class RootResponse(BaseModel):
    """Root endpoint response."""
    name: str
    version: str
    status: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + "Z")
