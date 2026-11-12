"""AI Provider Framework — pluggable abstraction layer for Chinese AI models."""

from .base import AIProvider
from .context_engine import AIContext, ContextEngine
from .deepseek import DeepSeekProvider
from .exceptions import AIProviderError, AuthenticationError, ModelError, PromptError, ProviderUnavailable, RateLimitError
from .inspection_pipeline import AIInspectionResult, InspectionPipeline
from .prompts import build_checkpoint_prompt, build_document_prompt, build_image_prompt, build_report_prompt
from .writing_engine import AuditWritingEngine, AuditWritingResult
from .prompt_engine import PromptEngine
from .provider import ProviderManager
from .registry import ProviderRegistry
from .schemas import AIMessage, AIRequest, AIResponse, DocumentAnalysis, ImageAnalysis, PromptTemplate, ReportDraft

__all__ = [
    "AIProvider",
    "AIContext",
    "AIInspectionResult",
    "AuditWritingEngine",
    "AuditWritingResult",
    "ContextEngine",
    "DeepSeekProvider",
    "InspectionPipeline",
    "PromptEngine",
    "ProviderManager",
    "ProviderRegistry",
    "AIMessage",
    "AIRequest",
    "AIResponse",
    "ImageAnalysis",
    "DocumentAnalysis",
    "ReportDraft",
    "PromptTemplate",
    "AIProviderError",
    "ProviderUnavailable",
    "PromptError",
    "AuthenticationError",
    "RateLimitError",
    "ModelError",
    "build_checkpoint_prompt",
    "build_image_prompt",
    "build_document_prompt",
    "build_report_prompt",
]
