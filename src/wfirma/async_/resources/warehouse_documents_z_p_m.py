"""Warehouse document (ZPM) resource endpoints (asynchronous).

This module provides a thin wrapper around the base asynchronous HTTP client
for the ``warehouse_document_z_p_m`` endpoint group.

Notes:
    wFirma exposes separate endpoint groups per warehouse document type.
    This resource currently targets ZPM.

    These wrappers expect JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient
from wfirma.models.warehouse import WarehouseDocument


class WarehouseDocumentZPMResource:
    """Asynchronous resource for ZPM warehouse documents.

    Args:
        client: A configured asynchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, warehouse_document_id: int) -> WarehouseDocument:
        """Get ZPM warehouse document by ID.

        Endpoint: GET /warehouse_document_z_p_m/get/{warehouseDocumentId}
        """
        data = await self._client.get_json(f"/warehouse_document_z_p_m/get/{warehouse_document_id}")
        payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(payload)

    async def find(self) -> list[WarehouseDocument]:
        """Find/list ZPM warehouse documents.

        Endpoint: GET /warehouse_document_z_p_m/find
        """
        data = await self._client.get_json("/warehouse_document_z_p_m/find")
        return self._extract_document_list(data)

    async def add(self, document: dict[str, Any]) -> WarehouseDocument:
        """Create a new ZPM warehouse document.

        Endpoint: POST /warehouse_document_z_p_m/add

        Args:
            document: Warehouse document payload (fields for ``warehouse_document``).

        Returns:
            Created WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = await self._client.post_json("/warehouse_document_z_p_m/add", data=payload)
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    async def edit(self, warehouse_document_id: int, document: dict[str, Any]) -> WarehouseDocument:
        """Update an existing ZPM warehouse document.

        Endpoint: POST /warehouse_document_z_p_m/edit/{warehouseDocumentId}

        Args:
            warehouse_document_id: Warehouse document identifier.
            document: Partial/complete warehouse document payload.

        Returns:
            Updated WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = await self._client.post_json(
            f"/warehouse_document_z_p_m/edit/{warehouse_document_id}",
            data=payload,
        )
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    async def delete(self, warehouse_document_id: int) -> bool:
        """Delete ZPM warehouse document.

        Endpoint: DELETE /warehouse_document_z_p_m/delete/{warehouseDocumentId}
        """
        await self._client.delete_json(f"/warehouse_document_z_p_m/delete/{warehouse_document_id}")
        return True

    @staticmethod
    def _extract_document_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract WarehouseDocument payload from a wFirma JSON response."""
        return extract_single_object_payload(
            data=data,
            container_key="warehouse_documents",
            object_key="warehouse_document",
        )

    @staticmethod
    def _extract_document_list(data: dict[str, Any]) -> list[WarehouseDocument]:
        """Extract list of WarehouseDocuments from a wFirma JSON response."""
        payloads = extract_object_list_payloads(
            data,
            container_key="warehouse_documents",
            object_key="warehouse_document",
        )
        return [WarehouseDocument.model_validate(payload) for payload in payloads]


__all__ = [
    "WarehouseDocumentZPMResource",
]
