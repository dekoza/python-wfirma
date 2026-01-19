"""Warehouse document (PW) resource endpoints (asynchronous).

This module provides a thin wrapper around the base asynchronous HTTP client
for the ``warehouse_document_p_w`` endpoint group.

Notes:
    wFirma exposes separate endpoint groups per warehouse document type.
    This resource currently targets PW ("Przyjęcie Wewnętrzne").

    These wrappers expect JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma.async_.client import WFirmaClient
from wfirma.models.warehouse import WarehouseDocument


class WarehouseDocumentPWResource:
    """Asynchronous resource for PW warehouse documents.

    Args:
        client: A configured asynchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, warehouse_document_id: int) -> WarehouseDocument:
        """Get PW warehouse document by ID.

        Endpoint: GET /warehouse_document_p_w/get/{warehouseDocumentId}
        """
        data = await self._client.get_json(f"/warehouse_document_p_w/get/{warehouse_document_id}")
        payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(payload)

    async def find(self) -> list[WarehouseDocument]:
        """Find/list PW warehouse documents.

        Endpoint: GET /warehouse_document_p_w/find
        """
        data = await self._client.get_json("/warehouse_document_p_w/find")
        return self._extract_document_list(data)

    async def add(self, document: dict[str, Any]) -> WarehouseDocument:
        """Create a new PW warehouse document.

        Endpoint: POST /warehouse_document_p_w/add

        Args:
            document: Warehouse document payload (fields for ``warehouse_document``).

        Returns:
            Created WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = await self._client.post_json("/warehouse_document_p_w/add", data=payload)
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    async def edit(self, warehouse_document_id: int, document: dict[str, Any]) -> WarehouseDocument:
        """Update an existing PW warehouse document.

        Endpoint: POST /warehouse_document_p_w/edit/{warehouseDocumentId}

        Args:
            warehouse_document_id: Warehouse document identifier.
            document: Partial/complete warehouse document payload.

        Returns:
            Updated WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = await self._client.post_json(
            f"/warehouse_document_p_w/edit/{warehouse_document_id}",
            data=payload,
        )
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    async def delete(self, warehouse_document_id: int) -> bool:
        """Delete PW warehouse document.

        Endpoint: DELETE /warehouse_document_p_w/delete/{warehouseDocumentId}
        """
        await self._client.delete_json(f"/warehouse_document_p_w/delete/{warehouse_document_id}")
        return True

    @staticmethod
    def _extract_document_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract WarehouseDocument payload from a wFirma JSON response."""
        container = data.get("warehouse_documents")
        if isinstance(container, dict):
            first_item = next(iter(container.values()), None)
            if isinstance(first_item, dict):
                inner = first_item.get("warehouse_document")
                if isinstance(inner, dict):
                    return inner
            if "warehouse_document" in container and isinstance(
                container["warehouse_document"], dict
            ):
                return container["warehouse_document"]

        raise KeyError("Unable to locate warehouse_document payload in response.")

    @staticmethod
    def _extract_document_list(data: dict[str, Any]) -> list[WarehouseDocument]:
        """Extract list of WarehouseDocuments from a wFirma JSON response."""
        container = data.get("warehouse_documents")
        if not isinstance(container, dict):
            return []

        documents: list[WarehouseDocument] = []
        for key, item in container.items():
            if not key.isdigit():
                continue
            if isinstance(item, dict):
                inner = item.get("warehouse_document")
                if isinstance(inner, dict):
                    documents.append(WarehouseDocument.model_validate(inner))

        return documents


__all__ = [
    "WarehouseDocumentPWResource",
]
