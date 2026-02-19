"""Declaration body jpkvat-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "declaration_body_jpkvat" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /declaration_body_jpkvat/get/{year}/{month}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class DeclarationBodyJpkvatResource:
    """Asynchronous declaration_body_jpkvat resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, year: int, month: int) -> dict[str, Any]:
        """Get declaration body jpkvat for specified year and month.

        Endpoint: GET /declaration_body_jpkvat/get/{year}/{month}

        Args:
            year: Year for declaration body.
            month: Month for declaration body.

        Returns:
            Raw declaration body jpkvat payload dict.
        """
        data = await self._client.get_json(f"/declaration_body_jpkvat/get/{year}/{month}")
        return self._extract_declaration_body_jpkvat_payload(data)

    @staticmethod
    def _extract_declaration_body_jpkvat_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract declaration body jpkvat payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="declaration_body_jpkvat",
            object_key="jpkvat",
        )
        return dict(payload)


__all__ = [
    "DeclarationBodyJpkvatResource",
]
