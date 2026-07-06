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

from wfirma._payloads import (
    build_find_parameters,
    extract_object_list_payloads,
    extract_single_object_payload,
)
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

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[Invoice]:
        """Find/list invoices, optionally filtered.

        Endpoint: GET /invoices/find (plain), or POST /invoices/find with a
        ``parameters`` block when any filter is given.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value``
                keys, e.g. ``{"field": "type", "operator": "eq", "value": "normal"}``.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/invoices/find")
            return self._extract_invoice_list(data)

        parameters = build_find_parameters(conditions, limit=limit, page=page)
        data = await self._client.post_json(
            "/invoices/find", data={"invoices": {"parameters": parameters}}
        )
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

    async def download(
        self,
        invoice_id: int,
        *,
        parameters: dict[str, Any] | None = None,
    ) -> bytes:
        """Download invoice as PDF.

        Endpoint: POST /invoices/download/{invoiceId}

        Args:
            invoice_id: Invoice identifier.
            parameters: Optional download parameters (page, duplicate, etc.).

        Returns:
            PDF file content as bytes.
        """
        payload: dict[str, Any] | None = None
        if parameters:
            payload = {"invoices": [{"parameters": parameters}]}

        return await self._client.post_binary(f"/invoices/download/{invoice_id}", data=payload)

    async def send(
        self,
        invoice_id: int,
        *,
        parameters: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send invoice via email.

        Endpoint: POST /invoices/send/{invoiceId}

        Args:
            invoice_id: Invoice identifier.
            parameters: Optional send parameters (email, subject, body, etc.).

        Returns:
            API response as dict.
        """
        payload: dict[str, Any] = {}
        if parameters:
            payload = {"invoices": [{"parameters": parameters}]}

        return await self._client.post_json(f"/invoices/send/{invoice_id}", data=payload)

    async def fiscalize(self, invoice_id: int) -> dict[str, Any]:
        """Mark invoice as fiscalized.

        Endpoint: GET /invoices/fiscalize/{invoiceId}

        Args:
            invoice_id: Invoice identifier.

        Returns:
            API response as dict.
        """
        return await self._client.get_json(f"/invoices/fiscalize/{invoice_id}")

    async def unfiscalize(self, invoice_id: int) -> dict[str, Any]:
        """Remove fiscalization from invoice.

        Endpoint: GET /invoices/unfiscalize/{invoiceId}

        Args:
            invoice_id: Invoice identifier.

        Returns:
            API response as dict.
        """
        return await self._client.get_json(f"/invoices/unfiscalize/{invoice_id}")

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
