"""Asynchronous authentication helpers.

This module provides authentication mechanisms for wFirma API (async version):
- APIKeyAuth: API Key authentication (accessKey, secretKey, appKey headers)
- OAuthToken: OAuth token container for OAuth 1.0a/2.0 flows

Note:
    APIKeyAuth and OAuthToken are synchronous data classes shared between
    sync and async implementations. The async-specific auth workflows
    (HTTP-based refresh/login) will be implemented separately.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from wfirma.auth.common import (
    FileTokenStore,
    MemoryTokenStore,
    OAuthToken as SharedOAuthToken,
    TokenStore,
)
from wfirma.exceptions import (
    ConfigurationError,
    MissingConfigurationError,
    ValidationError,
)


@dataclass(frozen=True, slots=True)
class APIKeyAuth:
    """API Key authentication for wFirma API (async-friendly).

    wFirma API Key authentication requires 3 keys sent as HTTP headers:
    - accessKey: User's access key
    - secretKey: User's secret key
    - appKey: Application key (provided by wFirma for integrations)

    The keys can be obtained from wFirma settings:
    Settings >> Security >> Applications >> API Keys

    Attributes:
        access_key: User's access key for API authentication.
        secret_key: User's secret key for API authentication.
        app_key: Application key for the integration.

    Example:
        >>> auth = APIKeyAuth(
        ...     access_key="your_access_key",
        ...     secret_key="your_secret_key",
        ...     app_key="your_app_key",
        ... )
        >>> headers = auth.get_headers()
        >>> headers
        {'accessKey': 'your_access_key', 'secretKey': '...', 'appKey': '...'}
    """

    access_key: str
    secret_key: str
    app_key: str

    def __post_init__(self) -> None:
        """Validate authentication keys after initialization."""
        # Check for None values first (type validation)
        if self.access_key is None:
            raise ValidationError("Field 'access_key' must be a string, got None.")
        if self.secret_key is None:
            raise ValidationError("Field 'secret_key' must be a string, got None.")
        if self.app_key is None:
            raise ValidationError("Field 'app_key' must be a string, got None.")

        # Check for empty/whitespace strings (missing value validation)
        if not self.access_key or not self.access_key.strip():
            raise MissingConfigurationError(
                "Configuration field 'access_key' is required but was empty."
            )
        if not self.secret_key or not self.secret_key.strip():
            raise MissingConfigurationError(
                "Configuration field 'secret_key' is required but was empty."
            )
        if not self.app_key or not self.app_key.strip():
            raise MissingConfigurationError(
                "Configuration field 'app_key' is required but was empty."
            )

    def get_headers(self) -> dict[str, str]:
        """Return HTTP headers for API Key authentication.

        Returns:
            Dictionary with accessKey, secretKey, and appKey headers.
        """
        return {
            "accessKey": self.access_key,
            "secretKey": self.secret_key,
            "appKey": self.app_key,
        }

    def to_dict(self, *, include_secrets: bool = False) -> dict[str, str]:
        """Convert to dictionary representation.

        By default, excludes the secret_key for safe logging/display.

        Args:
            include_secrets: If True, include secret_key in output.

        Returns:
            Dictionary with authentication keys.
        """
        result = {
            "access_key": self.access_key,
            "app_key": self.app_key,
        }
        if include_secrets:
            result["secret_key"] = self.secret_key
        return result

    def __repr__(self) -> str:
        """Return string representation without exposing secrets."""
        return (
            f"APIKeyAuth("
            f"access_key={self.access_key!r}, "
            f"secret_key='***HIDDEN***', "
            f"app_key={self.app_key!r})"
        )

    @classmethod
    def from_env(
        cls,
        *,
        access_key: str | None = None,
        secret_key: str | None = None,
        app_key: str | None = None,
    ) -> APIKeyAuth:
        """Create APIKeyAuth from environment variables.

        Environment variables used:
            - WFIRMA_ACCESS_KEY
            - WFIRMA_SECRET_KEY
            - WFIRMA_APP_KEY

        Explicit arguments override environment variables.

        Args:
            access_key: Override for WFIRMA_ACCESS_KEY.
            secret_key: Override for WFIRMA_SECRET_KEY.
            app_key: Override for WFIRMA_APP_KEY.

        Returns:
            APIKeyAuth instance.

        Raises:
            MissingConfigurationError: If required environment variables are missing.
        """
        resolved_access_key = access_key or os.environ.get("WFIRMA_ACCESS_KEY", "")
        resolved_secret_key = secret_key or os.environ.get("WFIRMA_SECRET_KEY", "")
        resolved_app_key = app_key or os.environ.get("WFIRMA_APP_KEY", "")

        if not resolved_access_key:
            raise MissingConfigurationError(
                "Environment variable 'WFIRMA_ACCESS_KEY' is required but not set."
            )
        if not resolved_secret_key:
            raise MissingConfigurationError(
                "Environment variable 'WFIRMA_SECRET_KEY' is required but not set."
            )
        if not resolved_app_key:
            raise MissingConfigurationError(
                "Environment variable 'WFIRMA_APP_KEY' is required but not set."
            )

        return cls(
            access_key=resolved_access_key,
            secret_key=resolved_secret_key,
            app_key=resolved_app_key,
        )


OAuthToken = SharedOAuthToken
"""Backward-compatible alias for shared OAuthToken (type alias, not subclass)."""


__all__ = [
    "TokenStore",
    "MemoryTokenStore",
    "FileTokenStore",
    "APIKeyAuth",
    "OAuthToken",
]
