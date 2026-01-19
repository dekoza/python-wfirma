"""Invoice-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "invoices" group.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.models.invoice import Invoice
from wfirma.sync.client import WFirmaClient


class InvoicesResource:
    """Synchronous invoices resource.

    Args:
        client: A configured synchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, invoice_id: int) -> Invoice:
        """Get invoice by ID.

        Endpoint: GET /invoices/get/{invoiceId}
        """
        data = self._client.get_json(f"/invoices/get/{invoice_id}")
        payload = self._extract_invoice_payload(data)
        return Invoice.model_validate(payload)

    def find(self) -> list[Invoice]:
        """Find/list invoices.

        Endpoint: GET /invoices/find
        """
        data = self._client.get_json("/invoices/find")
        return self._extract_invoice_list(data)

    def add(self, *, invoice: dict[str, Any]) -> Invoice:
        """Create a new invoice.

        Endpoint: POST /invoices/add

        Args:
            invoice: Raw invoice payload (without the outer "invoices" wrapper).

        Returns:
            Created invoice model.
        """
        payload = {"invoices": [{"invoice": invoice}]}
        data = self._client.post_json("/invoices/add", data=payload)
        result_payload = self._extract_invoice_payload(data)
        return Invoice.model_validate(result_payload)

    def edit(self, invoice_id: int, *, invoice: dict[str, Any]) -> Invoice:
        """Update an existing invoice.

        Endpoint: POST /invoices/edit/{invoiceId}

        Args:
            invoice_id: Invoice identifier.
            invoice: Raw invoice payload (without the outer "invoices" wrapper).

        Returns:
            Updated invoice model.
        """
        payload = {"invoices": [{"invoice": invoice}]}
        data = self._client.post_json(f"/invoices/edit/{invoice_id}", data=payload)
        result_payload = self._extract_invoice_payload(data)
        return Invoice.model_validate(result_payload)

    def delete(self, invoice_id: int) -> bool:
        """Delete an invoice.

        Endpoint: DELETE /invoices/delete/{invoiceId}
        """
        self._client.delete_json(f"/invoices/delete/{invoice_id}")
        return True

    @staticmethod
    def _extract_invoice_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract Invoice payload from a wFirma JSON response."""
        return extract_single_object_payload(
            data=data,
            container_key="invoices",
            object_key="invoice",
        )

    @staticmethod
    def _extract_invoice_list(data: dict[str, Any]) -> list[Invoice]:
        """Extract list of Invoices from a wFirma JSON response."""
        payloads = extract_object_list_payloads(
            data,
            container_key="invoices",
            object_key="invoice",
        )
        return [Invoice.model_validate(payload) for payload in payloads]


__all__ = [
    "InvoicesResource",
]
