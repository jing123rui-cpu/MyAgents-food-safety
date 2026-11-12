"""Data models for audit checkpoints, knowledge base, and reports."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional


class RiskLevel(str, Enum):
    """Risk level classification."""
    CRITICAL = "RISK-01"
    MAJOR = "RISK-02"
    MODERATE = "RISK-03"
    LOW = "RISK-04"


class AuditStatus(str, Enum):
    """Audit result status."""
    OK = "OK"
    NOK = "NOK"
    PENDING = "PENDING"
    NA = "NA"


@dataclass
class Checkpoint:
    """A single audit checkpoint definition."""
    checkpoint_id: str
    checkpoint_name: str
    domain: str = ""
    module: str = ""
    unit: str = ""
    category: str = ""
    applicable_products: List[str] = field(default_factory=list)
    risk_level: str = ""
    priority: str = ""
    estimated_time: str = ""
    objective: str = ""
    inspection_methods: List[Dict[str, str]] = field(default_factory=list)
    required_evidence: List[Dict[str, str]] = field(default_factory=list)
    common_findings: List[Dict[str, str]] = field(default_factory=list)
    regulatory_references: List[str] = field(default_factory=list)
    ai_guidance: List[Dict[str, str]] = field(default_factory=list)
    filepath: Path | None = None
    raw_content: str = ""


@dataclass
class RegistryEntry:
    """A single registry entry linking a checkpoint to the taxonomy."""
    id: str
    title: str
    domain: str = ""
    sub_domain: str = ""
    category: str = ""
    subcategory: str = ""
    risk_level: str = ""
    laws: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    evidence_required: List[str] = field(default_factory=list)
    checkpoint_file: str = ""


@dataclass
class TaxonomyNode:
    """A node in the audit taxonomy tree.

    Represents a domain, sub-domain, or category with its
    hierarchical children.
    """
    id: str
    name: str
    name_zh: str = ""
    children: List[TaxonomyNode] = field(default_factory=list)


@dataclass
class RiskRule:
    """A risk rule that maps conditions to a risk level."""
    rule_id: str
    condition: str
    risk_level: str
    description: str = ""


@dataclass
class KnowledgeBase:
    """Top-level container for all loaded knowledge assets.

    Aggregates registry entries, taxonomy nodes, checkpoints,
    and risk rules into a single object.
    """
    registry: Dict[str, RegistryEntry] = field(default_factory=dict)
    taxonomy: Dict[str, TaxonomyNode] = field(default_factory=dict)
    checkpoints: Dict[str, Checkpoint] = field(default_factory=dict)
    risk_rules: List[RiskRule] = field(default_factory=list)


@dataclass
class KnowledgeRepository:
    """Container for all knowledge assets loaded by the KnowledgeLoader."""
    registry: Dict[str, RegistryEntry] = field(default_factory=dict)
    taxonomy: Dict[str, Any] = field(default_factory=dict)
    checkpoints: Dict[str, Checkpoint] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def get_checkpoint(self, checkpoint_id: str) -> Optional[Checkpoint]:
        return self.checkpoints.get(checkpoint_id)

    def get_checkpoints_by_domain(self, domain: str) -> List[Checkpoint]:
        return [cp for cp in self.checkpoints.values() if cp.domain == domain]

    def get_checkpoints_by_module(self, module: str) -> List[Checkpoint]:
        return [cp for cp in self.checkpoints.values() if cp.module == module]


@dataclass
class LoaderStatistics:
    """Statistics collected during knowledge loading."""
    registry_files: int = 0
    taxonomy_files: int = 0
    checkpoint_files: int = 0
    domains: int = 0
    sub_domains: int = 0
    categories: int = 0
    total_nodes: int = 0
    warnings: int = 0
    errors: int = 0


class EvidenceType(str, Enum):
    """Classification of inspection evidence."""
    OBSERVATION = "OBSERVATION"
    PHOTO = "PHOTO"
    DOCUMENT = "DOCUMENT"
    MEASUREMENT = "MEASUREMENT"
    LAB_REPORT = "LAB_REPORT"
    VIDEO = "VIDEO"
    SYSTEM_RECORD = "SYSTEM_RECORD"


@dataclass
class Evidence:
    """A single piece of inspection evidence.

    Represents a factual observation, photo, document, measurement,
    lab report, video, or system record collected during an audit.
    """
    id: str
    evidence_type: EvidenceType
    checkpoint_id: str
    description: str
    source: str = ""
    attachments: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Finding:
    """An audit finding (non-conformance)."""
    checkpoint_id: str
    severity: str
    description: str
    evidence: List[str] = field(default_factory=list)
    risk_level: str = ""


@dataclass
class AuditResult:
    """Result of a single checkpoint audit."""
    checkpoint_id: str
    status: AuditStatus
    findings: List[Finding] = field(default_factory=list)
    evidence_collected: List[str] = field(default_factory=list)
    notes: str = ""


class EvaluationStatus(str, Enum):
    """Evaluation result status — aligned with food safety regulatory inspection practices.

    Values
    ------
    COMPLIANT       合格 — all requirements satisfied
    NON_COMPLIANT   不合格 — any required condition missing
    NOT_APPLICABLE  不适用 — checkpoint or rule does not apply
    """
    COMPLIANT = "COMPLIANT"
    NON_COMPLIANT = "NON_COMPLIANT"
    NOT_APPLICABLE = "NOT_APPLICABLE"

    @property
    def chinese(self) -> str:
        return _EVALUATION_STATUS_ZH[self]


# Chinese labels for evaluation statuses
_EVALUATION_STATUS_ZH = {
    EvaluationStatus.COMPLIANT: "合格",
    EvaluationStatus.NON_COMPLIANT: "不合格",
    EvaluationStatus.NOT_APPLICABLE: "不适用",
}


@dataclass
class EnterpriseEvaluation:
    """Enterprise-level evaluation result aggregated from all checkpoints.

    Decision logic
    --------------
    If non_compliant_count == 0:
        overall_result = "企业通过检查"
    Else:
        overall_result = "企业需要整改"
    """
    total_checkpoints: int = 0
    compliant_count: int = 0
    non_compliant_count: int = 0
    not_applicable_count: int = 0
    overall_result: str = ""
    summary: str = ""


@dataclass
class EvaluationResult:
    """Result of evaluating one evidence item against a risk rule."""
    checkpoint_id: str
    rule_id: str
    evidence_id: str
    status: EvaluationStatus
    score: float = 0.0
    reason: str = ""
    violated_laws: List[str] = field(default_factory=list)
    recommendation: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditReport:
    """Complete audit report."""
    title: str
    date: str
    auditor: str
    facility: str
    results: Dict[str, AuditResult] = field(default_factory=dict)
    summary: Dict[str, Any] = field(default_factory=dict)
