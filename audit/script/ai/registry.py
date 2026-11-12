"""Provider registry — maps provider names to provider classes."""

from __future__ import annotations

from typing import Dict, Optional, Type

from .base import AIProvider


class ProviderRegistry:
    """Registry of available AI provider classes.

    Providers are registered by name and tracked with a status
    (``"DISABLED"``, ``"ENABLED"``, ``"ERROR"``).
    """

    _providers: Dict[str, Type[AIProvider]] = {}
    _statuses: Dict[str, str] = {}
    _default: str = "deepseek"

    @classmethod
    def register(cls, name: str, provider_cls: Type[AIProvider]) -> None:
        """Register a provider class under *name*.

        Parameters
        ----------
        name
            Provider identifier (e.g. ``"deepseek"``).
        provider_cls
            The provider class (must subclass ``AIProvider``).
        """
        cls._providers[name] = provider_cls
        cls._statuses.setdefault(name, "DISABLED")

    @classmethod
    def unregister(cls, name: str) -> None:
        """Remove a provider from the registry."""
        cls._providers.pop(name, None)
        cls._statuses.pop(name, None)

    @classmethod
    def get(cls, name: str) -> Optional[Type[AIProvider]]:
        """Return the provider class for *name*, or ``None``."""
        return cls._providers.get(name)

    @classmethod
    def list_providers(cls) -> Dict[str, str]:
        """Return ``{name: status}`` for every registered provider."""
        return {
            name: cls._statuses.get(name, "DISABLED")
            for name in cls._providers
        }

    @classmethod
    def set_provider_status(cls, name: str, status: str) -> None:
        """Set the status for a registered provider.

        Parameters
        ----------
        name
            Provider identifier.
        status
            One of ``"DISABLED"``, ``"ENABLED"``, or ``"ERROR"``.
        """
        if name in cls._providers:
            cls._statuses[name] = status

    @classmethod
    def default(cls) -> str:
        """Return the default provider name."""
        return cls._default

    @classmethod
    def set_default(cls, name: str) -> None:
        """Set the default provider name."""
        cls._default = name
