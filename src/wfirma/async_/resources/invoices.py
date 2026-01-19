"""Invoice-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "invoices" group.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma.async_.client import WFirmaClient
from wfirma.models.invoice import Invoice


class InvoicesResource:
    """Asynchronous invoices resource.

    Args:
        client: A configured asynchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, invoice_id: int) -> Invoice:
        """Get invoice by ID.

        Endpoint: GET /invoices/get/{invoiceId}
        """
        data = await self._client.get_json(f"/invoices/get/{invoice_id}")
        payload = self._extract_invoice_payload(data)
        return Invoice.model_validate(payload)

    async def find(self) -> list[Invoice]:
        """Find/list invoices.

        Endpoint: GET /invoices/find
        """
        data = await self._client.get_json("/invoices/find")
        return self._extract_invoice_list(data)

    async def add(self, *, invoice: dict[str, Any]) -> Invoice:
        """Create a new invoice.

        Endpoint: POST /invoices/add

        Args:
            invoice: Raw invoice payload (without the outer "invoices" wrapper).

        Returns:
            Created invoice model.
        """
        payload = {"invoices": [{"invoice": invoice}]}
        data = await self._client.post_json("/invoices/add", data=payload)
        result_payload = self._extract_invoice_payload(data)
        return Invoice.model_validate(result_payload)

    async def edit(self, invoice_id: int, *, invoice: dict[str, Any]) -> Invoice:
        """Update an existing invoice.

        Endpoint: POST /invoices/edit/{invoiceId}

        Args:
            invoice_id: Invoice identifier.
            invoice: Raw invoice payload (without the outer "invoices" wrapper).

        Returns:
            Updated invoice model.
        """
        payload = {"invoices": [{"invoice": invoice}]}
        data = await self._client.post_json(f"/invoices/edit/{invoice_id}", data=payload)
        result_payload = self._extract_invoice_payload(data)
        return Invoice.model_validate(result_payload)

    async def delete(self, invoice_id: int) -> bool:
        """Delete an invoice.

        Endpoint: DELETE /invoices/delete/{invoiceId}
        """
        await self._client.delete_json(f"/invoices/delete/{invoice_id}")
        return True

    @staticmethod
    def _extract_invoice_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract Invoice payload from a wFirma JSON response."""
        container = data.get("invoices")
        if isinstance(container, dict):
            first_item = next(iter(container.values()), None)
            if isinstance(first_item, dict):
                inner = first_item.get("invoice")
                if isinstance(inner, dict):
                    return inner
            if "invoice" in container and isinstance(container["invoice"], dict):
                return container["invoice"]

        raise KeyError("Unable to locate invoice payload in response.")

    @staticmethod
    def _extract_invoice_list(data: dict[str, Any]) -> list[Invoice]:
        """Extract list of Invoices from a wFirma JSON response."""
        container = data.get("invoices")
        if not isinstance(container, dict):
            return []

        invoices: list[Invoice] = []
        for key, item in container.items():
            if not key.isdigit():
                continue
            if isinstance(item, dict):
                inner = item.get("invoice")
                if isinstance(inner, dict):
                    invoices.append(Invoice.model_validate(inner))

        return invoices


__all__ = [
    "InvoicesResource",
]
