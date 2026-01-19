"""Asynchronous HTTP client for wFirma API.

This module provides the async base HTTP client for communicating with the wFirma API.
It handles authentication, request formatting, response parsing, and error handling.
"""

from __future__ import annotations

import logging
from types import TracebackType
from typing import Any, Protocol, cast

import httpx

from wfirma.config import Environment
from wfirma.exceptions import (
    APIError,
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
    ServiceUnavailableError,
    TimeoutError,
    ValidationError,
)

logger = logging.getLogger(__name__)

# Default timeout for HTTP requests (in seconds)
DEFAULT_TIMEOUT = 30.0


class AuthProvider(Protocol):
    """Protocol for authentication providers."""

    def get_headers(self) -> dict[str, str]:
        """Return HTTP headers for authentication."""
        ...


class OAuth2AuthProvider(Protocol):
    """Protocol for OAuth2 authentication providers."""

    def get_token(self) -> Any:
        """Return the current OAuth token."""
        ...


class WFirmaClient:
    """Asynchronous HTTP client for wFirma API.

    This client handles:
    - Authentication (API Key or OAuth2)
    - Request formatting (JSON or XML)
    - Response parsing
    - Error handling based on wFirma API status codes
    - Automatic company_id injection

    Example:
        >>> import asyncio
        >>> from wfirma.async_.auth import APIKeyAuth
        >>>
        >>> async def main() -> None:
        ...     auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        ...     async with WFirmaClient(auth=auth) as client:
        ...         users = await client.get_json("/users/get/123")
        ...         print(users["users"]["0"]["user"]["login"])
        >>>
        >>> asyncio.run(main())

    Attributes:
        auth: Authentication provider (APIKeyAuth or OAuth2Auth).
        environment: API environment (PRODUCTION or SANDBOX).
        company_id: Optional company ID for multi-company accounts.
        timeout: HTTP request timeout in seconds.
    """

    def __init__(
        self,
        auth: AuthProvider | OAuth2AuthProvider,
        *,
        environment: Environment = Environment.PRODUCTION,
        company_id: int | None = None,
        timeout: float = DEFAULT_TIMEOUT,
    ) -> None:
        """Initialize the wFirma client.

        Args:
            auth: Authentication provider instance.
            environment: API environment (default: PRODUCTION).
            company_id: Optional company ID for multi-company accounts.
            timeout: HTTP request timeout in seconds (default: 30.0).
        """
        self.auth = auth
        self.environment = environment
        self.company_id = company_id
        self.timeout = timeout
        self._http_client = httpx.AsyncClient(timeout=timeout)
        self._resources: dict[str, Any] = {}

    @property
    def base_url(self) -> str:
        """Return the base URL for the API."""
        return self.environment.base_url

    @property
    def company(self) -> Any:
        """Convenience accessor for company-related endpoints.

        Returns:
            CompanyResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.company import CompanyResource

        resource = self._resources.get("company")
        if resource is None:
            resource = CompanyResource(self)
            self._resources["company"] = resource
        return resource

    @property
    def contractors(self) -> Any:
        """Convenience accessor for contractor-related endpoints.

        Returns:
            ContractorResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.contractors import ContractorResource

        resource = self._resources.get("contractors")
        if resource is None:
            resource = ContractorResource(self)
            self._resources["contractors"] = resource
        return resource

    @property
    def goods(self) -> Any:
        """Convenience accessor for goods-related endpoints.

        Returns:
            GoodsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.goods import GoodsResource

        resource = self._resources.get("goods")
        if resource is None:
            resource = GoodsResource(self)
            self._resources["goods"] = resource
        return resource

    @property
    def invoices(self) -> Any:
        """Convenience accessor for invoice-related endpoints.

        Returns:
            InvoicesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.invoices import InvoicesResource

        resource = self._resources.get("invoices")
        if resource is None:
            resource = InvoicesResource(self)
            self._resources["invoices"] = resource
        return resource

    @property
    def payments(self) -> Any:
        """Convenience accessor for payment-related endpoints.

        Returns:
            PaymentsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.payments import PaymentsResource

        resource = self._resources.get("payments")
        if resource is None:
            resource = PaymentsResource(self)
            self._resources["payments"] = resource
        return resource

    async def __aenter__(self) -> WFirmaClient:
        """Enter the async context manager."""
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        """Exit the async context manager and close the HTTP client."""
        await self.close()

    async def close(self) -> None:
        """Close the HTTP client."""
        await self._http_client.aclose()

    async def _get_auth_headers(self) -> dict[str, str]:
        """Get authentication headers based on auth type."""
        # Check if it's an OAuth2Auth by looking for get_token method
        if hasattr(self.auth, "get_token"):
            # Safe to cast - we just checked for get_token attribute
            auth_with_token = cast(OAuth2AuthProvider, self.auth)
            token = await auth_with_token.get_token()
            return {"Authorization": f"Bearer {token.access_token}"}
        # Otherwise it's API Key auth
        return self.auth.get_headers()

    def _build_url(self, path: str) -> str:
        """Build the full URL for the given path."""
        # Ensure path starts with /
        if not path.startswith("/"):
            path = f"/{path}"
        return f"{self.base_url}{path}"

    def _add_default_params(self, params: dict[str, str] | None) -> dict[str, str]:
        """Add default query parameters."""
        result = params.copy() if params else {}

        # Add company_id if set
        if self.company_id is not None:
            result["company_id"] = str(self.company_id)

        # Add oauth_version=2 for OAuth2 auth
        if hasattr(self.auth, "get_token"):
            result["oauth_version"] = "2"

        return result

    def _handle_response(self, response: httpx.Response) -> dict[str, Any]:
        """Handle API response and raise appropriate exceptions.

        Args:
            response: The HTTP response object.

        Returns:
            Parsed response data.

        Raises:
            Various exceptions based on HTTP status and API status codes.
        """
        # Handle HTTP errors first
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded (HTTP 429).")
        if response.status_code >= 500:
            if response.status_code == 503:
                raise ServiceUnavailableError(f"Service unavailable (HTTP {response.status_code}).")
            raise ServerError(f"Server error (HTTP {response.status_code}).")

        # Try to parse response as JSON
        try:
            data: dict[str, Any] = response.json()
        except Exception:
            # If not JSON, return raw text wrapped in a dict
            return {"raw": response.text, "status": {"code": "OK"}}

        # Check API status code
        status: dict[str, Any] = data.get("status", {})
        code: str = status.get("code", "")

        if code == "OK":
            return data

        # Map wFirma status codes to exceptions
        self._raise_for_status_code(code, data)

        return dict(data)

    def _raise_for_status_code(self, code: str, _data: dict[str, Any]) -> None:
        """Raise appropriate exception based on wFirma status code.

        Args:
            code: The wFirma API status code.
            _data: The full response data (reserved for future use).

        Raises:
            Various exceptions based on the status code.
        """
        if code in ("AUTH", "AUTH FAILED LIMIT WAIT 5 MINUTES"):
            raise AuthenticationError(f"Authentication failed: {code}")

        if code == "DENIED SCOPE REQUESTED":
            raise AuthenticationError(f"Access denied: {code}")

        if code == "ACCESS DENIED":
            raise AuthenticationError(f"Access denied: {code}")

        if code == "NOT FOUND":
            raise ResourceNotFoundError("Resource not found.")

        if code == "ACTION NOT FOUND":
            raise ResourceNotFoundError(f"Action not found: {code}")

        if code == "INPUT ERROR":
            raise BadRequestError(f"Invalid input: {code}")

        if code == "ERROR":
            # This is a validation error - extract error details if available
            raise ValidationError(f"Validation error: {code}")

        if code == "FATAL":
            raise ServerError(f"Internal server error: {code}")

        if code == "OUT OF SERVICE":
            raise ServiceUnavailableError(f"Service unavailable: {code}")

        if code == "SNAPSHOT LOCK":
            raise ServiceUnavailableError(f"Service locked: {code}")

        if code in ("TOTAL REQUESTS LIMIT EXCEEDED", "TOTAL EXECUTION TIME LIMIT EXCEEDED"):
            raise RateLimitError(f"Rate limit exceeded: {code}")

        if code == "COMPANY ID REQUIRED":
            raise BadRequestError(f"Company ID required: {code}")

        # Unknown error code
        raise APIError(f"API error: {code}")

    async def get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a GET request to the API.

        Args:
            path: The API endpoint path (e.g., "/users/get/123").
            params: Optional query parameters.

        Returns:
            Parsed response data.
        """
        url = self._build_url(path)
        headers = await self._get_auth_headers()
        params = self._add_default_params(params)

        try:
            response = await self._http_client.get(url, headers=headers, params=params)
        except httpx.TimeoutException as err:
            raise TimeoutError("Request timed out.") from err
        except httpx.ConnectError as err:
            raise ConnectionError("Failed to connect to the server.") from err
        except httpx.RequestError as err:
            raise ConnectionError(f"Network error: {err}") from err

        return self._handle_response(response)

    async def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        content: str | bytes | None = None,
        content_type: str = "application/json",
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a POST request to the API.

        Args:
            path: The API endpoint path (e.g., "/contractors/add").
            json: JSON data to send (mutually exclusive with content).
            content: Raw content to send (mutually exclusive with json).
            content_type: Content type for raw content.
            params: Optional query parameters.

        Returns:
            Parsed response data.
        """
        url = self._build_url(path)
        headers = await self._get_auth_headers()
        params = self._add_default_params(params)

        if content is not None:
            headers["Content-Type"] = content_type

        try:
            if json is not None:
                response = await self._http_client.post(
                    url, headers=headers, json=json, params=params
                )
            else:
                response = await self._http_client.post(
                    url, headers=headers, content=content, params=params
                )
        except httpx.TimeoutException as err:
            raise TimeoutError("Request timed out.") from err
        except httpx.ConnectError as err:
            raise ConnectionError("Failed to connect to the server.") from err
        except httpx.RequestError as err:
            raise ConnectionError(f"Network error: {err}") from err

        return self._handle_response(response)

    async def get_json(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a GET request expecting JSON response.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.

        Returns:
            Parsed JSON response data.
        """
        params = params.copy() if params else {}
        params["outputFormat"] = "json"
        return await self.get(path, params=params)

    async def get_xml(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> str:
        """Send a GET request expecting XML response.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.

        Returns:
            Raw XML response string.
        """
        params = params.copy() if params else {}
        params["outputFormat"] = "xml"
        result = await self.get(path, params=params)
        # If the response was XML, it will be in the "raw" key
        if "raw" in result:
            return str(result["raw"])
        # Otherwise return the JSON representation (shouldn't happen normally)
        return str(result)

    async def post_json(
        self,
        path: str,
        *,
        data: dict[str, Any],
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a POST request with JSON data.

        Args:
            path: The API endpoint path.
            data: JSON data to send.
            params: Optional query parameters.

        Returns:
            Parsed JSON response data.
        """
        params = params.copy() if params else {}
        params["inputFormat"] = "json"
        params["outputFormat"] = "json"
        return await self.post(path, json=data, params=params)

    async def post_xml(
        self,
        path: str,
        *,
        data: str,
        params: dict[str, str] | None = None,
    ) -> str:
        """Send a POST request with XML data.

        Args:
            path: The API endpoint path.
            data: XML data string to send.
            params: Optional query parameters.

        Returns:
            Raw XML response string.
        """
        params = params.copy() if params else {}
        params["inputFormat"] = "xml"
        params["outputFormat"] = "xml"
        result = await self.post(path, content=data, content_type="application/xml", params=params)
        # If the response was XML, it will be in the "raw" key
        if "raw" in result:
            return str(result["raw"])
        # Otherwise return the JSON representation (shouldn't happen normally)
        return str(result)

    async def delete(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a DELETE request to the API.

        Args:
            path: The API endpoint path (e.g., "/contractors/delete/123").
            params: Optional query parameters.

        Returns:
            Parsed response data.
        """
        url = self._build_url(path)
        headers = await self._get_auth_headers()
        params = self._add_default_params(params)

        try:
            response = await self._http_client.delete(url, headers=headers, params=params)
        except httpx.TimeoutException as err:
            raise TimeoutError("Request timed out.") from err
        except httpx.ConnectError as err:
            raise ConnectionError("Failed to connect to the server.") from err
        except httpx.RequestError as err:
            raise ConnectionError(f"Network error: {err}") from err

        return self._handle_response(response)

    async def delete_json(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a DELETE request expecting JSON response.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.

        Returns:
            Parsed JSON response data.
        """
        params = params.copy() if params else {}
        params["outputFormat"] = "json"
        return await self.delete(path, params=params)


__all__ = [
    "WFirmaClient",
]
