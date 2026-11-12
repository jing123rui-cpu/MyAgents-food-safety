"""AI provider exception hierarchy."""


class AIProviderError(Exception):
    """Base exception for all AI provider errors."""


class ProviderUnavailable(AIProviderError):
    """Raised when a provider cannot be reached or is not initialised."""


class PromptError(AIProviderError):
    """Raised when a prompt is malformed or exceeds limits."""


class AuthenticationError(AIProviderError):
    """Raised when API credentials are invalid or missing."""


class RateLimitError(AIProviderError):
    """Raised when the provider rate limit has been exceeded."""


class ModelError(AIProviderError):
    """Raised when the provider model returns an unexpected result."""
