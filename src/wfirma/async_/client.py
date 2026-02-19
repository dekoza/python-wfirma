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
    def invoice_deliveries(self) -> Any:
        """Convenience accessor for invoice delivery-related endpoints.

        Returns:
            InvoiceDeliveriesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.invoice_deliveries import InvoiceDeliveriesResource

        resource = self._resources.get("invoice_deliveries")
        if resource is None:
            resource = InvoiceDeliveriesResource(self)
            self._resources["invoice_deliveries"] = resource
        return resource

    @property
    def notes(self) -> Any:
        """Convenience accessor for note-related endpoints.

        Returns:
            NotesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.notes import NotesResource

        resource = self._resources.get("notes")
        if resource is None:
            resource = NotesResource(self)
            self._resources["notes"] = resource
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

    @property
    def warehouse_documents_pw(self) -> Any:
        """Convenience accessor for PW warehouse document endpoints.

        Returns:
            WarehouseDocumentPWResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_pw import WarehouseDocumentPWResource

        resource = self._resources.get("warehouse_documents_pw")
        if resource is None:
            resource = WarehouseDocumentPWResource(self)
            self._resources["warehouse_documents_pw"] = resource
        return resource

    @property
    def warehouse_documents_pz(self) -> Any:
        """Convenience accessor for PZ warehouse document endpoints.

        Returns:
            WarehouseDocumentPZResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_p_z import WarehouseDocumentPZResource

        resource = self._resources.get("warehouse_documents_pz")
        if resource is None:
            resource = WarehouseDocumentPZResource(self)
            self._resources["warehouse_documents_pz"] = resource
        return resource

    @property
    def warehouse_documents_r(self) -> Any:
        """Convenience accessor for R warehouse document endpoints.

        Returns:
            WarehouseDocumentRResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_r import WarehouseDocumentRResource

        resource = self._resources.get("warehouse_documents_r")
        if resource is None:
            resource = WarehouseDocumentRResource(self)
            self._resources["warehouse_documents_r"] = resource
        return resource

    @property
    def warehouse_documents_rw(self) -> Any:
        """Convenience accessor for RW warehouse document endpoints.

        Returns:
            WarehouseDocumentRWResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_r_w import WarehouseDocumentRWResource

        resource = self._resources.get("warehouse_documents_rw")
        if resource is None:
            resource = WarehouseDocumentRWResource(self)
            self._resources["warehouse_documents_rw"] = resource
        return resource

    @property
    def warehouse_documents_wz(self) -> Any:
        """Convenience accessor for WZ warehouse document endpoints.

        Returns:
            WarehouseDocumentWZResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_w_z import WarehouseDocumentWZResource

        resource = self._resources.get("warehouse_documents_wz")
        if resource is None:
            resource = WarehouseDocumentWZResource(self)
            self._resources["warehouse_documents_wz"] = resource
        return resource

    @property
    def warehouse_documents_zd(self) -> Any:
        """Convenience accessor for ZD warehouse document endpoints.

        Returns:
            WarehouseDocumentZDResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_z_d import WarehouseDocumentZDResource

        resource = self._resources.get("warehouse_documents_zd")
        if resource is None:
            resource = WarehouseDocumentZDResource(self)
            self._resources["warehouse_documents_zd"] = resource
        return resource

    @property
    def warehouse_documents_zpd(self) -> Any:
        """Convenience accessor for ZPD warehouse document endpoints.

        Returns:
            WarehouseDocumentZPDResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_z_p_d import WarehouseDocumentZPDResource

        resource = self._resources.get("warehouse_documents_zpd")
        if resource is None:
            resource = WarehouseDocumentZPDResource(self)
            self._resources["warehouse_documents_zpd"] = resource
        return resource

    @property
    def warehouse_documents_zpm(self) -> Any:
        """Convenience accessor for ZPM warehouse document endpoints.

        Returns:
            WarehouseDocumentZPMResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouse_documents_z_p_m import WarehouseDocumentZPMResource

        resource = self._resources.get("warehouse_documents_zpm")
        if resource is None:
            resource = WarehouseDocumentZPMResource(self)
            self._resources["warehouse_documents_zpm"] = resource
        return resource

    @property
    def tags(self) -> Any:
        """Convenience accessor for tag-related endpoints.

        Returns:
            TagsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.tags import TagsResource

        resource = self._resources.get("tags")
        if resource is None:
            resource = TagsResource(self)
            self._resources["tags"] = resource
        return resource

    @property
    def terms(self) -> Any:
        """Convenience accessor for term-related endpoints.

        Returns:
            TermsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.terms import TermsResource

        resource = self._resources.get("terms")
        if resource is None:
            resource = TermsResource(self)
            self._resources["terms"] = resource
        return resource

    @property
    def translation_languages(self) -> Any:
        """Convenience accessor for translation languages endpoints.

        Returns:
            TranslationLanguagesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.translation_languages import TranslationLanguagesResource

        resource = self._resources.get("translation_languages")
        if resource is None:
            resource = TranslationLanguagesResource(self)
            self._resources["translation_languages"] = resource
        return resource

    @property
    def taxregisters(self) -> Any:
        """Convenience accessor for taxregisters endpoints.

        Returns:
            TaxregistersResource instance bound to this client.
        """
        from wfirma.async_.resources.taxregisters import TaxregistersResource

        resource = self._resources.get("taxregisters")
        if resource is None:
            resource = TaxregistersResource(self)
            self._resources["taxregisters"] = resource
        return resource

    @property
    def term_groups(self) -> Any:
        """Convenience accessor for term group endpoints.

        Returns:
            TermGroupsResource instance bound to this client.
        """
        from wfirma.async_.resources.term_groups import TermGroupsResource

        resource = self._resources.get("term_groups")
        if resource is None:
            resource = TermGroupsResource(self)
            self._resources["term_groups"] = resource
        return resource

    @property
    def user_companies(self) -> Any:
        """Convenience accessor for user companies endpoints.

        Returns:
            UserCompaniesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.user_companies import UserCompaniesResource

        resource = self._resources.get("user_companies")
        if resource is None:
            resource = UserCompaniesResource(self)
            self._resources["user_companies"] = resource
        return resource

    @property
    def vat_codes(self) -> Any:
        """Convenience accessor for VAT codes endpoints.

        Returns:
            VatCodesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.vat_codes import VatCodesResource

        resource = self._resources.get("vat_codes")
        if resource is None:
            resource = VatCodesResource(self)
            self._resources["vat_codes"] = resource
        return resource

    @property
    def vehicle_run_rates(self) -> Any:
        """Convenience accessor for vehicle run rates endpoints.

        Returns:
            VehicleRunRatesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.vehicle_run_rates import VehicleRunRatesResource

        resource = self._resources.get("vehicle_run_rates")
        if resource is None:
            resource = VehicleRunRatesResource(self)
            self._resources["vehicle_run_rates"] = resource
        return resource

    @property
    def vehicles(self) -> Any:
        """Convenience accessor for vehicles endpoints.

        Returns:
            VehiclesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.vehicles import VehiclesResource

        resource = self._resources.get("vehicles")
        if resource is None:
            resource = VehiclesResource(self)
            self._resources["vehicles"] = resource
        return resource

    @property
    def warehouses(self) -> Any:
        """Convenience accessor for warehouses endpoints.

        Returns:
            WarehousesResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.warehouses import WarehousesResource

        resource = self._resources.get("warehouses")
        if resource is None:
            resource = WarehousesResource(self)
            self._resources["warehouses"] = resource
        return resource

    @property
    def company_accounts(self) -> Any:
        """Convenience accessor for company accounts endpoints.

        Returns:
            CompanyAccountsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.company_accounts import CompanyAccountsResource

        resource = self._resources.get("company_accounts")
        if resource is None:
            resource = CompanyAccountsResource(self)
            self._resources["company_accounts"] = resource
        return resource

    @property
    def company_packs(self) -> Any:
        """Convenience accessor for company packs endpoints.

        Returns:
            CompanyPacksResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.company_packs import CompanyPacksResource

        resource = self._resources.get("company_packs")
        if resource is None:
            resource = CompanyPacksResource(self)
            self._resources["company_packs"] = resource
        return resource

    @property
    def documents(self) -> Any:
        """Convenience accessor for documents endpoints.

        Returns:
            DocumentsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.documents import DocumentsResource

        resource = self._resources.get("documents")
        if resource is None:
            resource = DocumentsResource(self)
            self._resources["documents"] = resource
        return resource

    @property
    def expenses(self) -> Any:
        """Convenience accessor for expenses endpoints.

        Returns:
            ExpensesResource instance bound to this client.
        """
        from wfirma.async_.resources.expenses import ExpensesResource

        resource = self._resources.get("expenses")
        if resource is None:
            resource = ExpensesResource(self)
            self._resources["expenses"] = resource
        return resource

    @property
    def invoice_descriptions(self) -> Any:
        """Convenience accessor for invoice descriptions endpoints.

        Returns:
            InvoiceDescriptionsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.invoice_descriptions import InvoiceDescriptionsResource

        resource = self._resources.get("invoice_descriptions")
        if resource is None:
            resource = InvoiceDescriptionsResource(self)
            self._resources["invoice_descriptions"] = resource
        return resource

    @property
    def declaration_countries(self) -> Any:
        """Convenience accessor for declaration countries endpoints.

        Returns:
            DeclarationCountriesResource instance bound to this client.
        """
        from wfirma.async_.resources.declaration_countries import DeclarationCountriesResource

        resource = self._resources.get("declaration_countries")
        if resource is None:
            resource = DeclarationCountriesResource(self)
            self._resources["declaration_countries"] = resource
        return resource

    @property
    def declaration_body_jpkvat(self) -> Any:
        """Convenience accessor for declaration body jpkvat endpoints.

        Returns:
            DeclarationBodyJpkvatResource instance bound to this client.
        """
        from wfirma.async_.resources.declaration_body_jpkvat import DeclarationBodyJpkvatResource

        resource = self._resources.get("declaration_body_jpkvat")
        if resource is None:
            resource = DeclarationBodyJpkvatResource(self)
            self._resources["declaration_body_jpkvat"] = resource
        return resource

    @property
    def declaration_body_pit(self) -> Any:
        """Convenience accessor for declaration body PIT endpoints.

        Returns:
            DeclarationBodyPitResource instance bound to this client.
        """
        from wfirma.async_.resources.declaration_body_pit import DeclarationBodyPitResource

        resource = self._resources.get("declaration_body_pit")
        if resource is None:
            resource = DeclarationBodyPitResource(self)
            self._resources["declaration_body_pit"] = resource
        return resource

    @property
    def ledger_accountant_years(self) -> Any:
        """Convenience accessor for ledger accountant years endpoints.

        Returns:
            LedgerAccountantYearsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.ledger_accountant_years import LedgerAccountantYearsResource

        resource = self._resources.get("ledger_accountant_years")
        if resource is None:
            resource = LedgerAccountantYearsResource(self)
            self._resources["ledger_accountant_years"] = resource
        return resource

    @property
    def interests(self) -> Any:
        """Convenience accessor for interests endpoints.

        Returns:
            InterestsResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.interests import InterestsResource

        resource = self._resources.get("interests")
        if resource is None:
            resource = InterestsResource(self)
            self._resources["interests"] = resource
        return resource

    @property
    def ledger_operation_schemas(self) -> Any:
        """Convenience accessor for ledger operation schemas endpoints.

        Returns:
            LedgerOperationSchemasResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.ledger_operation_schemas import LedgerOperationSchemasResource

        resource = self._resources.get("ledger_operation_schemas")
        if resource is None:
            resource = LedgerOperationSchemasResource(self)
            self._resources["ledger_operation_schemas"] = resource
        return resource

    @property
    def users(self) -> Any:
        """Convenience accessor for users endpoints.

        Returns:
            UsersResource instance bound to this client.
        """
        # Local import to avoid circular dependency between client and resources.
        from wfirma.async_.resources.users import UsersResource

        resource = self._resources.get("users")
        if resource is None:
            resource = UsersResource(self)
            self._resources["users"] = resource
        return resource

    @property
    def payment_cashboxes(self) -> Any:
        """Convenience accessor for payment_cashboxes endpoints.

        Returns:
            PaymentCashboxesResource instance bound to this client.
        """
        from wfirma.async_.resources.payment_cashboxes import PaymentCashboxesResource

        resource = self._resources.get("payment_cashboxes")
        if resource is None:
            resource = PaymentCashboxesResource(self)
            self._resources["payment_cashboxes"] = resource
        return resource

    @property
    def series(self) -> Any:
        """Convenience accessor for series-related endpoints.

        Returns:
            SeriesResource instance bound to this client.
        """
        from wfirma.async_.resources.series import SeriesResource

        resource = self._resources.get("series")
        if resource is None:
            resource = SeriesResource(self)
            self._resources["series"] = resource
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

    def _handle_binary_response(self, response: httpx.Response) -> bytes:
        if response.status_code == 429:
            raise RateLimitError("Rate limit exceeded (HTTP 429).")
        if response.status_code >= 500:
            if response.status_code == 503:
                raise ServiceUnavailableError(f"Service unavailable (HTTP {response.status_code}).")
            raise ServerError(f"Server error (HTTP {response.status_code}).")

        return response.content

    async def get(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
        user_scoped: bool = False,
    ) -> dict[str, Any]:
        """Send a GET request to the API.

        Args:
            path: The API endpoint path (e.g., "/users/get/123").
            params: Optional query parameters.
            user_scoped: If True, skip automatic company_id injection (for user-scoped endpoints).

        Returns:
            Parsed response data.
        """
        url = self._build_url(path)
        headers = await self._get_auth_headers()
        params = (
            self._add_default_params(params)
            if not user_scoped
            else (params.copy() if params else {})
        )

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
        user_scoped: bool = False,
    ) -> dict[str, Any]:
        """Send a GET request expecting JSON response.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.
            user_scoped: If True, skip automatic company_id injection (for user-scoped endpoints).

        Returns:
            Parsed JSON response data.
        """
        params = params.copy() if params else {}
        params["outputFormat"] = "json"
        return await self.get(path, params=params, user_scoped=user_scoped)

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

    async def patch(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        content: str | bytes | None = None,
        content_type: str = "application/json",
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a PATCH request to the API.

        Args:
            path: The API endpoint path.
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
                response = await self._http_client.patch(
                    url, headers=headers, json=json, params=params
                )
            else:
                response = await self._http_client.patch(
                    url, headers=headers, content=content, params=params
                )
        except httpx.TimeoutException as err:
            raise TimeoutError("Request timed out.") from err
        except httpx.ConnectError as err:
            raise ConnectionError("Failed to connect to the server.") from err
        except httpx.RequestError as err:
            raise ConnectionError(f"Network error: {err}") from err

        return self._handle_response(response)

    async def patch_json(
        self,
        path: str,
        *,
        data: dict[str, Any],
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a PATCH request with JSON data.

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
        return await self.patch(path, json=data, params=params)

    async def put(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        content: str | bytes | None = None,
        content_type: str = "application/json",
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a PUT request to the API.

        Args:
            path: The API endpoint path.
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
                response = await self._http_client.put(
                    url, headers=headers, json=json, params=params
                )
            else:
                response = await self._http_client.put(
                    url, headers=headers, content=content, params=params
                )
        except httpx.TimeoutException as err:
            raise TimeoutError("Request timed out.") from err
        except httpx.ConnectError as err:
            raise ConnectionError("Failed to connect to the server.") from err
        except httpx.RequestError as err:
            raise ConnectionError(f"Network error: {err}") from err

        return self._handle_response(response)

    async def put_json(
        self,
        path: str,
        *,
        data: dict[str, Any],
        params: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """Send a PUT request with JSON data.

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
        return await self.put(path, json=data, params=params)

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

    async def get_binary(
        self,
        path: str,
        *,
        params: dict[str, str] | None = None,
    ) -> bytes:
        """Send a GET request and return raw bytes.

        Args:
            path: The API endpoint path.
            params: Optional query parameters.

        Returns:
            Raw response bytes.
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

        return self._handle_binary_response(response)

    async def post_binary(
        self,
        path: str,
        *,
        data: dict[str, Any] | None = None,
        params: dict[str, str] | None = None,
    ) -> bytes:
        """Send a POST request and return raw bytes.

        Args:
            path: The API endpoint path.
            data: JSON data to send.
            params: Optional query parameters.

        Returns:
            Raw response bytes.
        """
        url = self._build_url(path)
        headers = await self._get_auth_headers()
        params = self._add_default_params(params)

        try:
            response = await self._http_client.post(url, headers=headers, json=data, params=params)
        except httpx.TimeoutException as err:
            raise TimeoutError("Request timed out.") from err
        except httpx.ConnectError as err:
            raise ConnectionError("Failed to connect to the server.") from err
        except httpx.RequestError as err:
            raise ConnectionError(f"Network error: {err}") from err

        return self._handle_binary_response(response)


__all__ = [
    "WFirmaClient",
]
