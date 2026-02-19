"""Taxregister-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "taxregisters" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /taxregisters/get/{year}/{month}

This is a read-only resource with only a get() method (parameterized by year and month).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class TaxregistersResource:
    """Asynchronous taxregisters resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, *, year: int, month: int) -> dict[str, Any]:
        """Get taxregister by year and month.

        Endpoint: GET /taxregisters/get/{year}/{month}

        Args:
            year: Tax register year.
            month: Tax register month.

        Returns:
            Raw taxregister payload dict.
        """
        data = await self._client.get_json(f"/taxregisters/get/{year}/{month}")
        return self._extract_taxregister_payload(data)

    @staticmethod
    def _extract_taxregister_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract taxregister payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="taxregisters",
            object_key="taxregister",
        )
        return dict(payload)


__all__ = [
    "TaxregistersResource",
]
