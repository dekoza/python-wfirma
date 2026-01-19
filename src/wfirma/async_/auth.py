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

import logging
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode

import httpx

from wfirma.auth.common import (
    FileTokenStore,
    MemoryTokenStore,
    TokenStore,
)
from wfirma.auth.common import (
    OAuthToken as SharedOAuthToken,
)
from wfirma.config import Environment
from wfirma.exceptions import (
    AuthenticationError,
    ConnectionError,
    MissingConfigurationError,
    TimeoutError,
    TokenExpiredError,
    ValidationError,
)

logger = logging.getLogger(__name__)


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


@dataclass(slots=True)
class OAuth2Auth:
    """OAuth 2.0 Authorization Code flow helper (asynchronous)."""

    client_id: str
    client_secret: str
    redirect_uri: str
    environment: Environment
    token_store: TokenStore
    store_key: str = "default"
    debug: bool = False

    def __init__(
        self,
        *,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        environment: Environment,
        token_store: TokenStore | None = None,
        store_key: str = "default",
        debug: bool = False,
    ) -> None:
        self._validate_str(client_id, "client_id")
        self._validate_str(client_secret, "client_secret")
        self._validate_str(redirect_uri, "redirect_uri")
        if not isinstance(environment, Environment):
            raise ValidationError("Field 'environment' must be an Environment enum value.")
        if not isinstance(store_key, str) or not store_key:
            raise ValidationError("Field 'store_key' must be a non-empty string.")
        if not isinstance(debug, bool):
            raise ValidationError("Field 'debug' must be a boolean.")

        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.environment = environment
        self.token_store = token_store or MemoryTokenStore()
        self.store_key = store_key
        self.debug = debug

    @property
    def token_url(self) -> str:
        return f"{self.environment.base_url}/oauth2/token"

    @property
    def authorize_url(self) -> str:
        # wFirma OAuth2 consent/authorization endpoint is on the main domain.
        return "https://wfirma.pl/oauth2/auth"

    def build_authorization_url(
        self,
        *,
        scope: str | list[str] | None = None,
        state: str | None = None,
        response_type: str = "code",
    ) -> str:
        """Build the OAuth2 authorization URL for the Authorization Code flow.

        This method is synchronous because it only builds a URL.

        Args:
            scope: OAuth2 scope as a single string (e.g. "invoices-read") or a list
                of scopes. When a list is provided, values are joined with a single
                space.
            state: Optional state parameter for CSRF protection.
            response_type: OAuth2 response type (defaults to "code").

        Returns:
            A full URL that can be used to redirect the user to the wFirma consent page.

        Raises:
            ValidationError: When inputs are invalid.
        """
        self._validate_str(response_type, "response_type")

        params: dict[str, str] = {
            "response_type": response_type,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
        }

        if scope is not None:
            if isinstance(scope, str):
                if not scope.strip():
                    raise ValidationError("Field 'scope' must be a non-empty string when provided.")
                params["scope"] = scope
            elif isinstance(scope, list):
                normalized = [s.strip() for s in scope if isinstance(s, str) and s.strip()]
                if not normalized:
                    raise ValidationError(
                        "Field 'scope' must contain at least one non-empty scope."
                    )
                params["scope"] = " ".join(normalized)
            else:
                raise ValidationError("Field 'scope' must be a string, a list of strings, or None.")

        if state is not None:
            self._validate_str(state, "state")
            params["state"] = state

        return f"{self.authorize_url}?{urlencode(params)}"

    async def exchange_code(self, code: str) -> OAuthToken:
        self._validate_str(code, "code")

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            if self.debug:
                logger.exception(
                    "OAuth2 token request failed (status=%s, url=%s).",
                    err.response.status_code,
                    err.request.url,
                )
            raise AuthenticationError("OAuth2 token request failed.") from err
        except httpx.TimeoutException as err:
            if self.debug:
                logger.exception("OAuth2 token request timed out (url=%s).", err.request.url)
            raise TimeoutError("OAuth2 token request timed out.") from err
        except httpx.RequestError as err:
            if self.debug:
                logger.exception(
                    "OAuth2 token request failed due to network error (url=%s).", err.request.url
                )
            raise ConnectionError("OAuth2 token request failed due to network error.") from err

        token = OAuthToken.from_oauth2_response(response.json())
        self.token_store.set(self.store_key, token)
        return token

    async def _refresh(self, refresh_token: str) -> OAuthToken:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(self.token_url, data=payload)
            response.raise_for_status()
        except httpx.HTTPStatusError as err:
            if self.debug:
                logger.exception(
                    "OAuth2 token refresh failed (status=%s, url=%s).",
                    err.response.status_code,
                    err.request.url,
                )
            raise AuthenticationError("OAuth2 token refresh failed.") from err
        except httpx.TimeoutException as err:
            if self.debug:
                logger.exception("OAuth2 token refresh timed out (url=%s).", err.request.url)
            raise TimeoutError("OAuth2 token refresh timed out.") from err
        except httpx.RequestError as err:
            if self.debug:
                logger.exception(
                    "OAuth2 token refresh failed due to network error (url=%s).", err.request.url
                )
            raise ConnectionError("OAuth2 token refresh failed due to network error.") from err

        token = OAuthToken.from_oauth2_response(response.json())
        self.token_store.set(self.store_key, token)
        return token

    async def get_token(self) -> OAuthToken:
        token = self.token_store.get(self.store_key)
        if token is None:
            raise MissingConfigurationError("OAuth2 token is not available in the token store.")

        if token.is_expired():
            if token.refresh_token:
                return await self._refresh(token.refresh_token)
            raise TokenExpiredError("OAuth2 token expired and no refresh_token provided.")

        return token

    @staticmethod
    def _validate_str(value: Any, field_name: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValidationError(f"Field '{field_name}' must be a non-empty string.")


@dataclass(slots=True)
class OAuth1Auth:
    """OAuth 1.0a helper (PLAINTEXT signature) for async workflows."""

    consumer_key: str
    consumer_secret: str
    scope: str
    callback_url: str | None
    token_store: TokenStore
    store_key: str = "default"

    request_token_url: str = "https://wfirma.pl/oauth/requestToken"
    authorize_url: str = "https://wfirma.pl/oauth/authorize"
    access_token_url: str = "https://wfirma.pl/oauth/accessToken"

    def __init__(
        self,
        *,
        consumer_key: str,
        consumer_secret: str,
        scope: str,
        callback_url: str | None,
        token_store: TokenStore | None = None,
        store_key: str = "default",
    ) -> None:
        for name, value in (
            ("consumer_key", consumer_key),
            ("consumer_secret", consumer_secret),
            ("scope", scope),
        ):
            self._validate_str(value, name)

        if callback_url is not None and (not isinstance(callback_url, str) or not callback_url):
            raise ValidationError("Field 'callback_url' must be a non-empty string when provided.")
        if not isinstance(store_key, str) or not store_key:
            raise ValidationError("Field 'store_key' must be a non-empty string.")

        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.scope = scope
        self.callback_url = callback_url
        self.token_store = token_store or MemoryTokenStore()
        self.store_key = store_key
        self.request_token_url = "https://wfirma.pl/oauth/requestToken"
        self.authorize_url = "https://wfirma.pl/oauth/authorize"
        self.access_token_url = "https://wfirma.pl/oauth/accessToken"

    async def fetch_request_token(self) -> OAuthToken:
        params = {"scope": self.scope}
        if self.callback_url:
            params["callback"] = self.callback_url

        async with httpx.AsyncClient() as client:
            response = await client.get(self.request_token_url, params=params)
        response.raise_for_status()
        return self._parse_oauth1_response(response.text)

    def build_authorization_url(self, token: OAuthToken) -> str:
        return f"{self.authorize_url}?oauth_token={token.access_token}"

    async def fetch_access_token(
        self,
        *,
        oauth_token: str,
        oauth_token_secret: str,
        oauth_verifier: str,
    ) -> OAuthToken:
        for name, value in (
            ("oauth_token", oauth_token),
            ("oauth_token_secret", oauth_token_secret),
            ("oauth_verifier", oauth_verifier),
        ):
            self._validate_str(value, name)

        params = {"oauth_token": oauth_token, "oauth_verifier": oauth_verifier}

        async with httpx.AsyncClient() as client:
            response = await client.get(self.access_token_url, params=params)
        response.raise_for_status()

        token = self._parse_oauth1_response(response.text)
        self.token_store.set(self.store_key, token)
        return token

    async def get_token(self) -> OAuthToken:
        token = self.token_store.get(self.store_key)
        if token is None:
            raise MissingConfigurationError("OAuth1 token is not available in the token store.")
        return token

    @staticmethod
    def _parse_oauth1_response(payload: str) -> OAuthToken:
        return OAuthToken.from_oauth1_response(payload)

    @staticmethod
    def _validate_str(value: Any, field_name: str) -> None:
        if not isinstance(value, str) or not value:
            raise ValidationError(f"Field '{field_name}' must be a non-empty string.")


__all__ = [
    "TokenStore",
    "MemoryTokenStore",
    "FileTokenStore",
    "APIKeyAuth",
    "OAuthToken",
    "OAuth2Auth",
    "OAuth1Auth",
]
