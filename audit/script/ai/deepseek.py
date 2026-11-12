"""DeepSeek AI provider — HTTP REST implementation using httpx.

Reads configuration from environment variables:

- ``DEEPSEEK_API_KEY``  (required for operation)
- ``DEEPSEEK_BASE_URL`` (optional, default ``https://api.deepseek.com``)

No SDK — only raw HTTP calls via httpx.
"""

from __future__ import annotations

import json
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

import httpx

from .base import AIProvider
from .exceptions import (
    AuthenticationError,
    ModelError,
    PromptError,
    ProviderUnavailable,
    RateLimitError,
)
from .schemas import (
    AIRequest,
    AIResponse,
    AIMessage,
    DocumentAnalysis,
    ImageAnalysis,
    ReportDraft,
)

logger = logging.getLogger(__name__)

_CHAT_ENDPOINT = "/chat/completions"
_DEFAULT_MODEL = "deepseek-chat"
_DEFAULT_TIMEOUT = 60.0


class DeepSeekProvider(AIProvider):
    """DeepSeek API provider using httpx for HTTP communication."""

    # ── Metadata ─────────────────────────────────────────────────

    @property
    def provider_name(self) -> str:
        return "deepseek"

    @property
    def model_name(self) -> str:
        return self._model or _DEFAULT_MODEL

    # ── Lifecycle ────────────────────────────────────────────────

    def initialize(self) -> None:
        """Read environment variables and configure the HTTP client.

        Raises
        ------
        ProviderUnavailable
            If ``DEEPSEEK_API_KEY`` is not set.
        """
        self._api_key = os.environ.get("DEEPSEEK_API_KEY", "")
        base_url = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self._base_url = base_url.rstrip("/")
        self._model = os.environ.get("DEEPSEEK_MODEL", _DEFAULT_MODEL)

        if not self._api_key:
            raise ProviderUnavailable(
                "DEEPSEEK_API_KEY environment variable is not set"
            )

        self._client = httpx.Client(
            base_url=self._base_url,
            headers={
                "Authorization": f"Bearer {self._api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            timeout=httpx.Timeout(_DEFAULT_TIMEOUT),
        )
        logger.info(
            "DeepSeekProvider initialised (base_url=%s, model=%s)",
            self._base_url,
            self._model,
        )

    def health(self) -> bool:
        """Check provider reachability by listing models.

        Returns ``True`` if the API responds successfully.
        """
        try:
            response = self._client.get("/models")
            response.raise_for_status()
            return True
        except Exception as exc:
            logger.warning("DeepSeek health check failed: %s", exc)
            return False

    def shutdown(self) -> None:
        """Close the underlying HTTP client connection."""
        if hasattr(self, "_client"):
            self._client.close()

    # ── Internal Helpers ─────────────────────────────────────────

    def _post_chat(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Send a POST to ``/chat/completions`` and return parsed JSON.

        Raises
        ------
        AuthenticationError
            HTTP 401.
        RateLimitError
            HTTP 429.
        ProviderUnavailable
            HTTP 5xx, network error, timeout, or invalid JSON.
        """
        try:
            raw = self._client.post(_CHAT_ENDPOINT, json=payload)
        except httpx.TimeoutException as exc:
            raise ProviderUnavailable(
                f"DeepSeek request timed out after {_DEFAULT_TIMEOUT}s"
            ) from exc
        except httpx.RequestError as exc:
            raise ProviderUnavailable(
                f"DeepSeek network error: {exc}"
            ) from exc

        if raw.status_code == 401:
            raise AuthenticationError(
                "DeepSeek API key is invalid or missing"
            )
        if raw.status_code == 429:
            raise RateLimitError(
                "DeepSeek rate limit exceeded — reduce request frequency"
            )
        if raw.status_code >= 500:
            raise ProviderUnavailable(
                f"DeepSeek server error (HTTP {raw.status_code})"
            )

        try:
            raw.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise ProviderUnavailable(
                f"DeepSeek returned HTTP {exc.response.status_code}"
            ) from exc

        try:
            return raw.json()
        except json.JSONDecodeError as exc:
            raise ProviderUnavailable(
                f"DeepSeek returned invalid JSON: {exc}"
            ) from exc

    def _build_messages(
        self,
        user_content: str,
        system_prompt: str = "",
    ) -> List[Dict[str, str]]:
        """Build the OpenAI-compatible messages array."""
        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": user_content})
        return messages

    def _parse_chat_response(self, data: Dict[str, Any]) -> AIResponse:
        """Parse the DeepSeek chat completion response into ``AIResponse``."""
        try:
            choice = data["choices"][0]
            content = choice.get("message", {}).get("content", "")
            finish = choice.get("finish_reason", "")
        except (KeyError, IndexError) as exc:
            raise ModelError(
                f"Unexpected DeepSeek response structure: {exc}"
            ) from exc

        usage = data.get("usage", {})
        return AIResponse(
            content=content,
            model=data.get("model", ""),
            usage={
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0),
            },
            finish_reason=finish,
        )

    # ── Chat / Text ──────────────────────────────────────────────

    def chat(self, request: AIRequest) -> AIResponse:
        """Send a chat request and return the provider response.

        Parameters
        ----------
        request
            The ``AIRequest`` with messages, system_prompt, temperature, etc.

        Returns
        -------
        AIResponse
            The parsed response from DeepSeek.

        Raises
        ------
        ProviderUnavailable
            If the provider is not initialised or the API is unreachable.
        """
        if not hasattr(self, "_client"):
            raise ProviderUnavailable("DeepSeekProvider not initialised")

        messages: List[Dict[str, str]] = []
        if request.system_prompt:
            messages.append({"role": "system", "content": request.system_prompt})
        for msg in request.messages:
            messages.append({"role": msg.role, "content": msg.content})

        payload: Dict[str, Any] = {
            "model": request.model or self._model,
            "messages": messages,
            "temperature": request.temperature,
            "max_tokens": request.max_tokens,
        }

        data = self._post_chat(payload)
        return self._parse_chat_response(data)

    def analyze_text(self, text: str, checkpoint_id: str = "") -> AIResponse:
        """Analyse free‑text audit notes using DeepSeek chat.

        Parameters
        ----------
        text
            The audit notes or observation text to analyse.
        checkpoint_id
            Optional checkpoint identifier for context.

        Returns
        -------
        AIResponse
            DeepSeek's analysis response.
        """
        system = (
            "You are a food safety audit assistant. "
            "Analyse the following audit observation and identify any "
            "compliance issues, risks, or non-conformities."
        )
        prefix = f"[Checkpoint: {checkpoint_id}]\n" if checkpoint_id else ""
        req = AIRequest(
            messages=[AIMessage(role="user", content=f"{prefix}{text}")],
            system_prompt=system,
            temperature=0.3,
        )
        return self.chat(req)

    # ── Multimodal ───────────────────────────────────────────────

    def analyze_image(self, image_path: str, checkpoint_id: str = "") -> ImageAnalysis:
        """Analyse an audit photograph.

        DeepSeek does not currently support vision input via the chat API.
        This method reads the image metadata and sends a text description
        for analysis.  For true vision analysis, use a multimodal provider.

        Parameters
        ----------
        image_path
            Path to the image file on disk.
        checkpoint_id
            Optional checkpoint identifier.

        Returns
        -------
        ImageAnalysis
            Analysis result with findings and risk assessment.
        """
        path = Path(image_path)
        if not path.is_file():
            raise PromptError(f"Image file not found: {image_path}")

        desc = f"[Image: {path.name} ({path.stat().st_size} bytes)]"
        system = (
            "You are a food safety audit assistant reviewing site photographs. "
            "Based on the image file name and size, provide your best assessment "
            "of what should be verified during an on-site audit."
        )
        prefix = f"[Checkpoint: {checkpoint_id}]\n" if checkpoint_id else ""
        req = AIRequest(
            messages=[AIMessage(role="user", content=f"{prefix}{desc}")],
            system_prompt=system,
            temperature=0.3,
        )
        resp = self.chat(req)

        return ImageAnalysis(
            checkpoint_id=checkpoint_id,
            description=resp.content,
            findings=[resp.content] if resp.content else [],
            risk_level="",
            confidence=0.0,
        )

    def analyze_document(self, document_path: str, checkpoint_id: str = "") -> DocumentAnalysis:
        """Analyse a document by reading its content and sending to DeepSeek.

        Supports plain text and small markdown files.  Binary formats
        (PDF, DOCX, images) are not parsed — the file name and size
        are sent as context.

        Parameters
        ----------
        document_path
            Path to the document file on disk.
        checkpoint_id
            Optional checkpoint identifier.

        Returns
        -------
        DocumentAnalysis
            Analysis result with summary and compliance issues.
        """
        path = Path(document_path)
        if not path.is_file():
            raise PromptError(f"Document file not found: {document_path}")

        # Try to read as text; fall back to metadata-only
        content: str = ""
        try:
            content = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            content = (
                f"[Binary document: {path.name} ({path.stat().st_size} bytes)]"
            )

        system = (
            "You are a food safety audit assistant. "
            "Analyse the following document and extract key information: "
            "summary, important points, and any compliance issues found."
        )
        prefix = f"[Checkpoint: {checkpoint_id}]\n" if checkpoint_id else ""
        req = AIRequest(
            messages=[AIMessage(role="user", content=f"{prefix}{content}")],
            system_prompt=system,
            temperature=0.2,
        )
        resp = self.chat(req)

        return DocumentAnalysis(
            checkpoint_id=checkpoint_id,
            summary=resp.content[:500] if resp.content else "",
            key_points=(
                [resp.content] if resp.content and len(resp.content) < 200
                else [resp.content[:200]] if resp.content
                else []
            ),
            compliance_issues=[],
            confidence=0.0,
        )

    # ── Report Generation ────────────────────────────────────────

    def generate_report(self, context: str) -> ReportDraft:
        """Generate a draft audit report from the given context.

        Parameters
        ----------
        context
            Serialised inspection context (checkpoints, evidence,
            evaluation results) as a string.

        Returns
        -------
        ReportDraft
            A draft report with sections and recommendations.
        """
        system = (
            "You are a food safety audit report writer. "
            "Based on the following inspection data, generate a professional "
            "audit report with: a title, executive summary, detailed findings "
            "section, and actionable recommendations."
        )
        req = AIRequest(
            messages=[AIMessage(role="user", content=context)],
            system_prompt=system,
            temperature=0.4,
            max_tokens=4096,
        )
        resp = self.chat(req)

        return ReportDraft(
            title="Food Safety Audit Report",
            summary=(resp.content[:500] if resp.content else ""),
            sections={"full_report": resp.content} if resp.content else {},
            recommendations=(
                [resp.content] if resp.content and len(resp.content) < 500
                else []
            ),
        )
