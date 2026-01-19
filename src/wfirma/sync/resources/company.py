"""Company-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "companies" and related groups.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.
"""

from __future__ import annotations

from typing import Any

from wfirma.models.company import CompanyAddress, CompanyDetail
from wfirma.sync.client import WFirmaClient


class CompanyResource:
    """Synchronous company resource.

    Args:
        client: A configured synchronous wFirma HTTP client.

    Notes:
        wFirma payload shapes differ between endpoints and formats.
        This resource currently expects JSON responses (``outputFormat=json``).
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, company_id: int | None = None) -> CompanyDetail:
        """Get company details.

        Endpoint: GET /companies/get/{companyId}

        Args:
            company_id: Company identifier. If omitted, uses ``client.company_id``.

        Returns:
            Parsed company detail model.

        Raises:
            ValueError: If both ``company_id`` and ``client.company_id`` are missing.
        """
        resolved_company_id = company_id if company_id is not None else self._client.company_id
        if resolved_company_id is None:
            raise ValueError("company_id is required (either pass it or set client.company_id).")

        data = self._client.get_json(f"/companies/get/{resolved_company_id}")
        payload = self._extract_company_detail_payload(data)
        return CompanyDetail.model_validate(payload)

    def find_main_address(self) -> CompanyAddress:
        """Get main company address.

        Endpoint: GET /company_addresses/findmain

        Returns:
            Parsed company address model.
        """
        data = self._client.get_json("/company_addresses/findmain")
        payload = self._extract_company_address_payload(data)
        return CompanyAddress.model_validate(payload)

    @staticmethod
    def _extract_company_detail_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract CompanyDetail payload from a wFirma JSON response."""
        # Common shapes (best-effort, based on other endpoints patterns):
        # - {"company": {"0": {"company": {...}}}, "status": {...}}
        # - {"companies": {"0": {"company": {...}}}, "status": {...}}
        for top_key in ("company", "companies"):
            container = data.get(top_key)
            if isinstance(container, dict):
                # Usually indexed dict: {"0": {"company": {...}}}
                first_item = next(iter(container.values()), None)
                if isinstance(first_item, dict):
                    inner = first_item.get("company") or first_item.get("company_detail")
                    if isinstance(inner, dict):
                        return inner
                # Sometimes direct
                if "company" in container and isinstance(container["company"], dict):
                    return container["company"]
                if "company_detail" in container and isinstance(container["company_detail"], dict):
                    return container["company_detail"]

        raise KeyError("Unable to locate company payload in response.")

    @staticmethod
    def _extract_company_address_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract CompanyAddress payload from a wFirma JSON response."""
        container = data.get("company_addresses")
        if isinstance(container, dict):
            first_item = next(iter(container.values()), None)
            if isinstance(first_item, dict):
                inner = first_item.get("company_address") or first_item.get("company_addresses")
                if isinstance(inner, dict):
                    return inner
            if "company_address" in container and isinstance(container["company_address"], dict):
                return container["company_address"]

        raise KeyError("Unable to locate company address payload in response.")
