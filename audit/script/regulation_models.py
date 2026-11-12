"""Regulation Knowledge Model — structured data types for legal traceability.

Hierarchy
---------
Regulation
  └── RegulationChapter  (organisational grouping)
        └── RegulationArticle  (individual legal provision)
              └── RegulationRequirement  (inspectable criterion)
                    └── maps to → Checkpoint → RiskRule

Cross-reference
---------------
RegulationCitation — lightweight reference model for inclusion in
EvaluationResult, AuditReport, and AI contexts without loading
the full regulation tree.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional


class DocumentType(str, Enum):
    """Type of legal document."""
    NATIONAL_LAW = "national_law"                       # 法律（e.g. 食品安全法）
    NATIONAL_STANDARD = "national_standard"              # 国家标准（e.g. GB 14881）
    ADMINISTRATIVE_REGULATION = "administrative_regulation"  # 行政法规（e.g. 许可管理办法）
    INDUSTRY_STANDARD = "industry_standard"              # 行业标准
    GUIDELINE = "guideline"                              # 指导性文件


class RegulationStatus(str, Enum):
    """Lifecycle status of a regulation."""
    EFFECTIVE = "effective"          # 现行有效
    DRAFT = "draft"                  # 征求意见稿
    REPLACED = "replaced"            # 被替代
    ABOLISHED = "abolished"          # 废止


class SeverityLevel(str, Enum):
    """Severity classification for regulatory requirements."""
    CRITICAL = "CRITICAL"            # 食品安全直接相关，违反即构成严重不符合
    HIGH = "HIGH"                    # 系统性要求，违反影响整体合规
    MEDIUM = "MEDIUM"                # 管理性要求，违反属于一般不符合
    LOW = "LOW"                      # 建议性要求


# ── Core Models ────────────────────────────────────────────────────────────────

@dataclass
class Regulation:
    """A complete regulation document with structured articles.

    Represents the top-level container for a law, standard, or
    administrative regulation. Each ``Regulation`` is identified
    by a ``REG-*`` code (e.g. ``REG-GB-14881``) and contains
    one or more chapters with articles.
    """
    id: str
    title: str
    title_zh: str
    document_type: DocumentType
    issuing_authority: str
    effective_date: str
    status: RegulationStatus
    scope: str = ""
    purpose: str = ""
    keywords: List[str] = field(default_factory=list)
    last_revision: str = ""
    enterprise_types: List[str] = field(default_factory=list)
    chapters: List[RegulationChapter] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegulationChapter:
    """A chapter or section within a regulation.

    Chapters group related articles (e.g. "Chapter 3 — Production
    Process Control"). Chapters may nest sub-chapters.
    """
    chapter_id: str
    title: str
    title_zh: str = ""
    number: str = ""                  # e.g. "3", "4.1"
    parent_chapter_id: Optional[str] = None
    articles: List[RegulationArticle] = field(default_factory=list)
    sub_chapters: List[RegulationChapter] = field(default_factory=list)


@dataclass
class RegulationArticle:
    """A single legal provision / article.

    Each article is the finest unit of legal text that can be
    referenced independently (e.g. "Article 33(1)").
    """
    article_id: str
    chapter: str                      # chapter_id reference
    number: str                       # e.g. "33", "33.1", "4.2.3"
    title: str = ""
    title_zh: str = ""
    text: str = ""                    # Full text of the article
    summary: str = ""                 # One-sentence summary for reports
    keywords: List[str] = field(default_factory=list)
    inspection_topics: List[str] = field(default_factory=list)
    risk_tags: List[str] = field(default_factory=list)
    related_checkpoint_ids: List[str] = field(default_factory=list)
    related_rule_ids: List[str] = field(default_factory=list)
    severity: SeverityLevel = SeverityLevel.MEDIUM
    requirements: List[RegulationRequirement] = field(default_factory=list)


@dataclass
class RegulationRequirement:
    """A specific, inspectable requirement derived from an article.

    One article may contain multiple requirements. Each requirement
    maps to one or more checkpoints and risk rules in the audit system.

    This is the bridge between legal text and audit criteria.
    """
    requirement_id: str
    article_id: str
    description: str
    inspection_method: str = ""
    required_evidence: List[str] = field(default_factory=list)
    decision_logic: str = ""          # Deterministic condition
    common_nonconformities: List[str] = field(default_factory=list)
    recommended_actions: List[str] = field(default_factory=list)
    related_checkpoint_ids: List[str] = field(default_factory=list)
    related_rule_ids: List[str] = field(default_factory=list)
    severity: SeverityLevel = SeverityLevel.MEDIUM


@dataclass
class RegulationCitation:
    """Lightweight reference to a regulation for use in results and reports.

    Used in ``EvaluationResult``, ``AuditReport``, and AI contexts
    to cite specific legal provisions without loading the full model.
    """
    regulation_id: str
    title_zh: str = ""
    article_numbers: List[str] = field(default_factory=list)  # e.g. ["33", "44"]
    article_texts: List[str] = field(default_factory=list)
    chapter: str = ""
    severity: SeverityLevel = SeverityLevel.MEDIUM
    reason: str = ""


# ── Container ──────────────────────────────────────────────────────────────────

@dataclass
class RegulationKnowledgeBase:
    """Top-level container for all loaded regulation models."""
    regulations: Dict[str, Regulation] = field(default_factory=dict)
    chapters: Dict[str, RegulationChapter] = field(default_factory=dict)
    articles: Dict[str, RegulationArticle] = field(default_factory=dict)
    requirements: Dict[str, RegulationRequirement] = field(default_factory=dict)
    warnings: List[str] = field(default_factory=list)
    errors: List[str] = field(default_factory=list)

    def get_article(self, article_id: str) -> Optional[RegulationArticle]:
        return self.articles.get(article_id)

    def get_requirement(self, requirement_id: str) -> Optional[RegulationRequirement]:
        return self.requirements.get(requirement_id)

    def get_checkpoint_requirements(self, checkpoint_id: str) -> List[RegulationRequirement]:
        """Return all requirements that reference a given checkpoint."""
        return [
            req for req in self.requirements.values()
            if checkpoint_id in req.related_checkpoint_ids
        ]

    def get_rule_requirements(self, rule_id: str) -> List[RegulationRequirement]:
        """Return all requirements that reference a given risk rule."""
        return [
            req for req in self.requirements.values()
            if rule_id in req.related_rule_ids
        ]
