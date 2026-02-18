"""Company packs-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "company_packs" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /company_packs/get/{companyPackId}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class CompanyPacksResource:
    """Asynchronous company_packs resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, company_pack_id: int) -> dict[str, Any]:
        """Get company pack by ID.

        Endpoint: GET /company_packs/get/{companyPackId}

        Args:
            company_pack_id: Company pack identifier.

        Returns:
            Raw company pack payload dict.
        """
        data = await self._client.get_json(f"/company_packs/get/{company_pack_id}")
        return self._extract_company_pack_payload(data)

    @staticmethod
    def _extract_company_pack_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract company pack payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="company_packs",
            object_key="company_pack",
        )
        return dict(payload)


__all__ = [
    "CompanyPacksResource",
]
