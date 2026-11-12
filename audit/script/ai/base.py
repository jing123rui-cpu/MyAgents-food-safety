"""Abstract base class for all AI providers."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional

from .schemas import AIRequest, AIResponse, DocumentAnalysis, ImageAnalysis, ReportDraft


class AIProvider(ABC):
    """Abstract interface that every AI provider must implement.

    Subclasses must override all methods.  Every method currently raises
    ``NotImplementedError`` — concrete implementations will be added
    when a provider (e.g. DeepSeek) is integrated.
    """

    # ── Metadata ─────────────────────────────────────────────────

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Human-readable name, e.g. ``"deepseek"``, ``"tongyi-qwen"``."""

    @property
    @abstractmethod
    def model_name(self) -> str:
        """Default model identifier for this provider."""

    # ── Lifecycle ────────────────────────────────────────────────

    @abstractmethod
    def initialize(self) -> None:
        """Initialise the provider (load config, validate credentials).

        TODO: Implement provider-specific initialisation.
        """
        raise NotImplementedError

    @abstractmethod
    def health(self) -> bool:
        """Return ``True`` if the provider is reachable and ready.

        TODO: Implement health check (e.g. lightweight API ping).
        """
        raise NotImplementedError

    def shutdown(self) -> None:
        """Release provider resources.  Override in subclasses that own
        network clients, file handles, or thread pools.
        """

    # ── Chat / Text ──────────────────────────────────────────────

    @abstractmethod
    def chat(self, request: AIRequest) -> AIResponse:
        """Send a chat request and return the provider response.

        TODO: Implement chat completion call.
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_text(self, text: str, checkpoint_id: str = "") -> AIResponse:
        """Analyse free‑text audit notes and return structured feedback.

        TODO: Implement text analysis.
        """
        raise NotImplementedError

    # ── Multimodal ───────────────────────────────────────────────

    @abstractmethod
    def analyze_image(self, image_path: str, checkpoint_id: str = "") -> ImageAnalysis:
        """Analyse an audit photograph and extract findings.

        TODO: Implement image analysis (vision model or OCR).
        """
        raise NotImplementedError

    @abstractmethod
    def analyze_document(self, document_path: str, checkpoint_id: str = "") -> DocumentAnalysis:
        """Analyse a scanned document and extract key fields.

        TODO: Implement document analysis.
        """
        raise NotImplementedError

    # ── Report Generation ────────────────────────────────────────

    @abstractmethod
    def generate_report(self, context: str) -> ReportDraft:
        """Generate a draft audit report from the given context.

        TODO: Implement report drafting.
        """
        raise NotImplementedError
