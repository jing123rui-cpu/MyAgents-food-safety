"""ProviderManager — runtime facade for the AI provider layer.

Manages provider instances, switching, and lifecycle.
No implementation — only interfaces.
"""

from __future__ import annotations

import logging
from typing import Dict, List, Optional

from .base import AIProvider
from .exceptions import ProviderUnavailable
from .registry import ProviderRegistry

logger = logging.getLogger(__name__)


class ProviderManager:
    """Runtime manager for AI provider instances.

    Usage
    -----
    manager = ProviderManager()
    provider = manager.get_provider("deepseek")      # → None (not yet implemented)
    available = manager.list_providers()               # → {"deepseek": "DISABLED"}
    """

    def __init__(self) -> None:
        self._instances: Dict[str, AIProvider] = {}

    # ── Registration ─────────────────────────────────────────────

    def register(self, name: str, provider_cls: type) -> None:
        """Register a provider class in the registry.

        Parameters
        ----------
        name
            Provider identifier (e.g. ``"deepseek"``).
        provider_cls
            Subclass of ``AIProvider``.

        TODO: Validate that *provider_cls* is a subclass of AIProvider.
        """
        ProviderRegistry.register(name, provider_cls)

    def unregister(self, name: str) -> None:
        """Remove a provider from the registry and discard its instance."""
        ProviderRegistry.unregister(name)
        self._instances.pop(name, None)

    # ── Access ───────────────────────────────────────────────────

    def get_provider(self, name: Optional[str] = None) -> Optional[AIProvider]:
        """Return an initialised provider instance.

        Parameters
        ----------
        name
            Provider name.  If ``None``, uses the default provider.

        Returns
        -------
        AIProvider or None
            The provider instance, or ``None`` if not registered /
            initialisation failed.
        """
        provider_name = name or ProviderRegistry.default()
        instance = self._instances.get(provider_name)
        if instance is not None:
            return instance
        # Lazy initialise on first access
        try:
            self.initialize_provider(provider_name)
        except Exception:
            return None
        return self._instances.get(provider_name)

    def list_providers(self) -> Dict[str, str]:
        """Return ``{provider_name: status}`` for all registered providers."""
        return ProviderRegistry.list_providers()

    # ── Lifecycle ────────────────────────────────────────────────

    def initialize_provider(self, name: str) -> None:
        """Initialise a specific provider.

        Parameters
        ----------
        name
            Provider name.

        Raises
        ------
        ProviderUnavailable
            If the provider class is not registered or initialisation fails.
        """
        cls = ProviderRegistry.get(name)
        if cls is None:
            raise ProviderUnavailable(f"Provider '{name}' is not registered")

        provider: AIProvider = cls()
        try:
            provider.initialize()
            self._instances[name] = provider
            ProviderRegistry.set_provider_status(name, "ENABLED")
            logger.info("Provider '%s' initialised successfully", name)
        except Exception as exc:
            ProviderRegistry.set_provider_status(name, "ERROR")
            self._instances.pop(name, None)
            raise ProviderUnavailable(
                f"Failed to initialise provider '{name}': {exc}"
            ) from exc

    def shutdown_all(self) -> None:
        """Shut down all active provider instances."""
        for name, inst in self._instances.items():
            try:
                inst.shutdown()
            except Exception:
                logger.warning("Error shutting down provider '%s'", name)
        self._instances.clear()
