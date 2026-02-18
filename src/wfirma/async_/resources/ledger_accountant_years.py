"""Ledger accountant years-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "ledger_accountant_years" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /ledger_accountant_years/get/{ledgerAccountantYearsId}
- GET /ledger_accountant_years/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class LedgerAccountantYearsResource:
    """Asynchronous ledger_accountant_years resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, ledger_accountant_year_id: int) -> dict[str, Any]:
        """Get ledger accountant year by ID.

        Endpoint: GET /ledger_accountant_years/get/{ledgerAccountantYearsId}

        Args:
            ledger_accountant_year_id: Ledger accountant year identifier.

        Returns:
            Raw ledger accountant year payload dict.
        """
        data = await self._client.get_json(
            f"/ledger_accountant_years/get/{ledger_accountant_year_id}"
        )
        return self._extract_ledger_accountant_year_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list ledger accountant years.

        Endpoint: GET /ledger_accountant_years/find

        Returns:
            List of raw ledger accountant year payload dicts.
        """
        data = await self._client.get_json("/ledger_accountant_years/find")
        payloads = extract_object_list_payloads(
            data, container_key="ledger_accountant_years", object_key="ledger_accountant_year"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_ledger_accountant_year_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract ledger accountant year payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="ledger_accountant_years",
            object_key="ledger_accountant_year",
        )
        return dict(payload)


__all__ = [
    "LedgerAccountantYearsResource",
]
