"""Warehouse document (ZD) resource endpoints (synchronous).

This module provides a thin wrapper around the base synchronous HTTP client
for the ``warehouse_document_z_d`` endpoint group.

Notes:
    wFirma exposes separate endpoint groups per warehouse document type.
    This resource currently targets ZD.

    These wrappers expect JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.models.warehouse import WarehouseDocument
from wfirma.sync.client import WFirmaClient


class WarehouseDocumentZDResource:
    """Synchronous resource for ZD warehouse documents.

    Args:
        client: A configured synchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, warehouse_document_id: int) -> WarehouseDocument:
        """Get ZD warehouse document by ID.

        Endpoint: GET /warehouse_document_z_d/get/{warehouseDocumentId}
        """
        data = self._client.get_json(f"/warehouse_document_z_d/get/{warehouse_document_id}")
        payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(payload)

    def find(self) -> list[WarehouseDocument]:
        """Find/list ZD warehouse documents.

        Endpoint: GET /warehouse_document_z_d/find
        """
        data = self._client.get_json("/warehouse_document_z_d/find")
        return self._extract_document_list(data)

    def add(self, document: dict[str, Any]) -> WarehouseDocument:
        """Create a new ZD warehouse document.

        Endpoint: POST /warehouse_document_z_d/add

        Args:
            document: Warehouse document payload (fields for ``warehouse_document``).

        Returns:
            Created WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = self._client.post_json("/warehouse_document_z_d/add", data=payload)
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    def edit(self, warehouse_document_id: int, document: dict[str, Any]) -> WarehouseDocument:
        """Update an existing ZD warehouse document.

        Endpoint: POST /warehouse_document_z_d/edit/{warehouseDocumentId}

        Args:
            warehouse_document_id: Warehouse document identifier.
            document: Partial/complete warehouse document payload.

        Returns:
            Updated WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = self._client.post_json(
            f"/warehouse_document_z_d/edit/{warehouse_document_id}",
            data=payload,
        )
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    def delete(self, warehouse_document_id: int) -> bool:
        """Delete ZD warehouse document.

        Endpoint: DELETE /warehouse_document_z_d/delete/{warehouseDocumentId}
        """
        self._client.delete_json(f"/warehouse_document_z_d/delete/{warehouse_document_id}")
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
    "WarehouseDocumentZDResource",
]
