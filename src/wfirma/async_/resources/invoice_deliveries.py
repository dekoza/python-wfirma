"""Invoice delivery-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "invoice_deliveries" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- POST /invoice_deliveries/add
- GET /invoice_deliveries/find
- GET /invoice_deliveries/get/{invoiceDeliveryId}
- DELETE /invoice_deliveries/delete/{invoiceDeliveryId}

No edit method available for this resource.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class InvoiceDeliveriesResource:
    """Asynchronous invoice deliveries resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def add(self, invoice_delivery: dict[str, Any]) -> dict[str, Any]:
        """Create a new invoice delivery.

        Endpoint: POST /invoice_deliveries/add

        Args:
            invoice_delivery: Invoice delivery payload dict.

        Returns:
            Created invoice delivery payload.
        """
        data = await self._client.post_json(
            "/invoice_deliveries/add",
            data={"invoice_deliveries": [{"invoice_delivery": invoice_delivery}]},
        )
        return self._extract_invoice_delivery_payload(data)

    async def find(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Find/list invoice deliveries.

        Endpoint: GET /invoice_deliveries/find

        Args:
            params: Optional query parameters.

        Returns:
            List of raw invoice delivery payload dicts.
        """
        data = await self._client.get_json("/invoice_deliveries/find", params=params)
        payloads = extract_object_list_payloads(
            data, container_key="invoice_deliveries", object_key="invoice_delivery"
        )
        return [dict(payload) for payload in payloads]

    async def get(self, invoice_delivery_id: int) -> dict[str, Any]:
        """Get invoice delivery by ID.

        Endpoint: GET /invoice_deliveries/get/{invoiceDeliveryId}

        Args:
            invoice_delivery_id: Invoice delivery identifier.

        Returns:
            Raw invoice delivery payload dict.
        """
        data = await self._client.get_json(f"/invoice_deliveries/get/{invoice_delivery_id}")
        return self._extract_invoice_delivery_payload(data)

    async def delete(self, invoice_delivery_id: int) -> dict[str, Any]:
        """Delete an invoice delivery.

        Endpoint: DELETE /invoice_deliveries/delete/{invoiceDeliveryId}

        Args:
            invoice_delivery_id: Invoice delivery identifier.

        Returns:
            Deleted invoice delivery payload.
        """
        data = await self._client.delete_json(f"/invoice_deliveries/delete/{invoice_delivery_id}")
        return self._extract_invoice_delivery_payload(data)

    @staticmethod
    def _extract_invoice_delivery_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract invoice delivery payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="invoice_deliveries",
            object_key="invoice_delivery",
        )
        return dict(payload)


__all__ = [
    "InvoiceDeliveriesResource",
]
