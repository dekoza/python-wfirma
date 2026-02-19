"""Warehouse document (RW) resource endpoints (synchronous).

This module provides a thin wrapper around the base synchronous HTTP client
for the ``warehouse_document_r_w`` endpoint group.

Notes:
    wFirma exposes separate endpoint groups per warehouse document type.
    This resource currently targets RW.

    These wrappers expect JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.models.warehouse import WarehouseDocument
from wfirma.sync.client import WFirmaClient


class WarehouseDocumentRWResource:
    """Synchronous resource for RW warehouse documents.

    Args:
        client: A configured synchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, warehouse_document_id: int) -> WarehouseDocument:
        """Get RW warehouse document by ID.

        Endpoint: GET /warehouse_document_r_w/get/{warehouseDocumentId}
        """
        data = self._client.get_json(f"/warehouse_document_r_w/get/{warehouse_document_id}")
        payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(payload)

    def find(self) -> list[WarehouseDocument]:
        """Find/list RW warehouse documents.

        Endpoint: GET /warehouse_document_r_w/find
        """
        data = self._client.get_json("/warehouse_document_r_w/find")
        return self._extract_document_list(data)

    def add(self, document: dict[str, Any]) -> WarehouseDocument:
        """Create a new RW warehouse document.

        Endpoint: POST /warehouse_document_r_w/add

        Args:
            document: Warehouse document payload (fields for ``warehouse_document``).

        Returns:
            Created WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = self._client.post_json("/warehouse_document_r_w/add", data=payload)
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    def edit(self, warehouse_document_id: int, document: dict[str, Any]) -> WarehouseDocument:
        """Update an existing RW warehouse document.

        Endpoint: POST /warehouse_document_r_w/edit/{warehouseDocumentId}

        Args:
            warehouse_document_id: Warehouse document identifier.
            document: Partial/complete warehouse document payload.

        Returns:
            Updated WarehouseDocument.
        """
        payload = {"warehouse_document": document}
        data = self._client.post_json(
            f"/warehouse_document_r_w/edit/{warehouse_document_id}",
            data=payload,
        )
        result_payload = self._extract_document_payload(data)
        return WarehouseDocument.model_validate(result_payload)

    def delete(self, warehouse_document_id: int) -> bool:
        """Delete RW warehouse document.

        Endpoint: DELETE /warehouse_document_r_w/delete/{warehouseDocumentId}
        """
        self._client.delete_json(f"/warehouse_document_r_w/delete/{warehouse_document_id}")
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
    "WarehouseDocumentRWResource",
]
