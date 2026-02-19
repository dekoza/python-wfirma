"""Declaration body PIT-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "declaration_body_pit" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /declaration_body_pit/get/{type}/{year}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class DeclarationBodyPitResource:
    """Asynchronous declaration_body_pit resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, pit_type: str, year: int) -> dict[str, Any]:
        """Get declaration body PIT data for a given type and year.

        Endpoint: GET /declaration_body_pit/get/{type}/{year}

        Args:
            pit_type: PIT form type (e.g., "pit11", "pit38", "pit_ub").
            year: Tax year.

        Returns:
            Raw declaration body PIT payload dict.
        """
        data = await self._client.get_json(f"/declaration_body_pit/get/{pit_type}/{year}")
        return self._extract_declaration_body_pit_payload(data)

    @staticmethod
    def _extract_declaration_body_pit_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract declaration body PIT payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="declaration_body_pit",
            object_key="declaration_body_pit",
        )
        return dict(payload)


__all__ = [
    "DeclarationBodyPitResource",
]
