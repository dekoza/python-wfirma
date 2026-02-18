"""Company accounts-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "company_accounts" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /company_accounts/get/{companyAccountId}
- GET /company_accounts/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class CompanyAccountsResource:
    """Asynchronous company_accounts resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, company_account_id: int) -> dict[str, Any]:
        """Get company account by ID.

        Endpoint: GET /company_accounts/get/{companyAccountId}

        Args:
            company_account_id: Company account identifier.

        Returns:
            Raw company account payload dict.
        """
        data = await self._client.get_json(f"/company_accounts/get/{company_account_id}")
        return self._extract_company_account_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list company accounts.

        Endpoint: GET /company_accounts/find

        Returns:
            List of raw company account payload dicts.
        """
        data = await self._client.get_json("/company_accounts/find")
        payloads = extract_object_list_payloads(
            data, container_key="company_accounts", object_key="company_account"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_company_account_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract company account payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="company_accounts",
            object_key="company_account",
        )
        return dict(payload)


__all__ = [
    "CompanyAccountsResource",
]
