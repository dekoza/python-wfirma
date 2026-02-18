"""Invoice descriptions-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "invoice_descriptions" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /invoice_descriptions/get/{invoiceDescriptionsId}
- GET /invoice_descriptions/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class InvoiceDescriptionsResource:
    """Asynchronous invoice_descriptions resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, invoice_description_id: int) -> dict[str, Any]:
        """Get invoice description by ID.

        Endpoint: GET /invoice_descriptions/get/{invoiceDescriptionsId}

        Args:
            invoice_description_id: Invoice description identifier.

        Returns:
            Raw invoice description payload dict.
        """
        data = await self._client.get_json(f"/invoice_descriptions/get/{invoice_description_id}")
        return self._extract_invoice_description_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list invoice descriptions.

        Endpoint: GET /invoice_descriptions/find

        Returns:
            List of raw invoice description payload dicts.
        """
        data = await self._client.get_json("/invoice_descriptions/find")
        payloads = extract_object_list_payloads(
            data, container_key="invoice_descriptions", object_key="invoice_description"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_invoice_description_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract invoice description payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="invoice_descriptions",
            object_key="invoice_description",
        )
        return dict(payload)


__all__ = [
    "InvoiceDescriptionsResource",
]
