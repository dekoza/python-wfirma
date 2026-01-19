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

import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from wfirma.exceptions import (
    ConfigurationError,
    MissingConfigurationError,
    ValidationError,
)
from wfirma.models import format_wfirma_datetime, parse_wfirma_datetime


class TokenStore(Protocol):
    """A minimal storage interface for OAuth tokens.

    Implementations are responsible only for persisting and retrieving tokens.
    Token refreshing/renewal is handled by higher-level auth workflows.
    """

    def get(self, key: str) -> OAuthToken | None:
        """Retrieve token for a given key."""

    def set(self, key: str, token: OAuthToken) -> None:
        """Store token under a given key."""

    def delete(self, key: str) -> None:
        """Delete token for a given key if present."""

    def clear(self) -> None:
        """Remove all stored tokens."""


@dataclass(slots=True)
class MemoryTokenStore:
    """In-memory token storage.

    This store keeps tokens in the current Python process memory.
    It is suitable for short-lived scripts and tests.

    Notes:
        This implementation is not persistent and is not designed to be
        thread-safe.
    """

    _tokens: dict[str, OAuthToken]

    def __init__(self) -> None:
        self._tokens = {}

    def get(self, key: str) -> OAuthToken | None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        return self._tokens.get(key)

    def set(self, key: str, token: OAuthToken) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        self._tokens[key] = token

    def delete(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        self._tokens.pop(key, None)

    def clear(self) -> None:
        self._tokens.clear()


@dataclass(slots=True)
class FileTokenStore:
    """File-based token storage.

    Stores tokens in a JSON file as a mapping: {key: token_dict}.

    Notes:
        This implementation is not designed to be thread-safe.
    """

    path: Path

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)

    def get(self, key: str) -> OAuthToken | None:
        self._validate_key(key)
        payload = self._read_payload()
        token_payload = payload.get(key)
        if token_payload is None:
            return None
        if not isinstance(token_payload, dict):
            raise ValidationError("Stored token payload must be a dictionary.")
        return OAuthToken.from_dict(token_payload)

    def set(self, key: str, token: OAuthToken) -> None:
        self._validate_key(key)
        payload = self._read_payload()
        payload[key] = token.to_dict()
        self._write_payload(payload)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        payload = self._read_payload()
        payload.pop(key, None)
        self._write_payload(payload)

    def clear(self) -> None:
        self._write_payload({})

    @staticmethod
    def _validate_key(key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

    def _read_payload(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}

        if not self.path.is_file():
            raise ConfigurationError("Token store path must point to a file.")

        try:
            raw = self.path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else {}
        except (OSError, json.JSONDecodeError) as err:
            raise ValidationError("Token store file contains invalid JSON.") from err

        if not isinstance(data, dict):
            raise ValidationError("Token store JSON must be an object mapping keys to tokens.")

        return data

    def _write_payload(self, payload: dict[str, Any]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=str(self.path.parent),
                delete=False,
            ) as tmp:
                tmp_path = Path(tmp.name)
                tmp.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))

            tmp_path.replace(self.path)
        except OSError as err:
            raise ConfigurationError("Failed to write token store file.") from err
        finally:
            try:
                if "tmp_path" in locals() and tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
            except OSError:
                # Best-effort cleanup.
                pass


@dataclass(frozen=True, slots=True)
class APIKeyAuth:
    """API Key authentication for wFirma API.

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


@dataclass(frozen=True, slots=True)
class OAuthToken:
    """OAuth token container.

    Attributes:
        access_token: OAuth access token string.
        refresh_token: Optional refresh token string.
        expires_at: Absolute expiration time. If None, token is treated as non-expiring.

    Notes:
        Serialization uses the wFirma datetime format ("YYYY-MM-DD HH:MM:SS") for
        compatibility with other parts of the library.
    """

    access_token: str
    refresh_token: str | None = None
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.access_token, str) or not self.access_token:
            raise ValidationError("Field 'access_token' must be a non-empty string.")

        if self.refresh_token is not None and (
            not isinstance(self.refresh_token, str) or not self.refresh_token
        ):
            raise ValidationError("Field 'refresh_token' must be a non-empty string when provided.")

        if self.expires_at is not None and not isinstance(self.expires_at, datetime):
            raise ValidationError("Field 'expires_at' must be a datetime instance when provided.")

    def is_expired(self, *, at: datetime | None = None) -> bool:
        """Return True if token is expired at given time.

        Args:
            at: Time to compare with. Defaults to current local time.

        Returns:
            True if expires_at is set and expires_at <= at.
        """
        if self.expires_at is None:
            return False

        now = at or datetime.now()
        return self.expires_at <= now

    def to_dict(self) -> dict[str, Any]:
        """Serialize token to a JSON-friendly dictionary.

        The expires_at field is serialized to a string in wFirma datetime format.
        """
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": format_wfirma_datetime(self.expires_at),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> OAuthToken:
        """Create token from dictionary.

        The expires_at field can be provided as:
        - datetime
        - wFirma-format datetime string ("YYYY-MM-DD HH:MM:SS")
        - None

        Raises:
            ValidationError: When payload is missing required fields or contains invalid types.
        """
        if not isinstance(data, dict):
            raise ValidationError("Token payload must be a dictionary.")

        access_token: str = data.get("access_token", "")  # validated in __post_init__
        refresh_token: str | None = data.get("refresh_token")

        expires_at_raw = data.get("expires_at")
        try:
            expires_at = parse_wfirma_datetime(expires_at_raw)
        except ValueError as err:
            raise ValidationError(
                "Field 'expires_at' must be a datetime or wFirma datetime string."
            ) from err

        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )
