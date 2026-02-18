"""VAT codes-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "vat_codes" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /vat_codes/get/{vatCodeId}
- GET /vat_codes/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class VatCodesResource:
    """Synchronous vat_codes resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, vat_code_id: int) -> dict[str, Any]:
        """Get VAT code by ID.

        Endpoint: GET /vat_codes/get/{vatCodeId}

        Args:
            vat_code_id: VAT code identifier.

        Returns:
            Raw VAT code payload dict.
        """
        data = self._client.get_json(f"/vat_codes/get/{vat_code_id}")
        return self._extract_vat_code_payload(data)

    def find(self) -> list[dict[str, Any]]:
        """Find/list VAT codes.

        Endpoint: GET /vat_codes/find

        Returns:
            List of raw VAT code payload dicts.
        """
        data = self._client.get_json("/vat_codes/find")
        payloads = extract_object_list_payloads(
            data, container_key="vat_codes", object_key="vat_code"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_vat_code_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract VAT code payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="vat_codes",
            object_key="vat_code",
        )
        return dict(payload)


__all__ = [
    "VatCodesResource",
]
