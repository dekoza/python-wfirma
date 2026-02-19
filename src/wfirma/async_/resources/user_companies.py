"""User company resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "user_companies" group.

Notes:
    User-scoped endpoints: These endpoints do NOT use the company_id parameter.
    The API automatically returns only companies associated with the authenticated user.

The wFirma API reference lists these endpoints:
- GET /user_companies/find
- GET /user_companies/get/{userCompanyId}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class UserCompaniesResource:
    """Asynchronous user_companies resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, user_company_id: int) -> dict[str, Any]:
        """Get user company by ID.

        Endpoint: GET /user_companies/get/{userCompanyId}

        Args:
            user_company_id: User company identifier.

        Returns:
            Raw user company payload dict.
        """
        data = await self._client.get_json(
            f"/user_companies/get/{user_company_id}", user_scoped=True
        )
        return self._extract_user_company_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list user companies.

        Endpoint: GET /user_companies/find

        Returns:
            List of raw user company payload dicts.
        """
        data = await self._client.get_json("/user_companies/find", user_scoped=True)
        payloads = extract_object_list_payloads(
            data, container_key="user_companies", object_key="user_company"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_user_company_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract user company payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="user_companies",
            object_key="user_company",
        )
        return dict(payload)


__all__ = [
    "UserCompaniesResource",
]
