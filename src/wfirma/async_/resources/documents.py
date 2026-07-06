"""Document-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "documents" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- POST /documents/add
- GET /documents/find
- GET /documents/get/{documentId}
- DELETE /documents/delete/{documentId}
- GET /documents/download/{documentId}

No edit method available for this resource.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    build_module_payload,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient


class DocumentsResource:
    """Asynchronous documents resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def add(self, document: dict[str, Any]) -> dict[str, Any]:
        """Create a new document.

        Endpoint: POST /documents/add

        Args:
            document: Document payload dict.

        Returns:
            Created document payload.
        """
        data = await self._client.post_json(
            "/documents/add",
            data=build_module_payload(
                container_key="documents", object_key="document", obj=document
            ),
        )
        return self._extract_document_payload(data)

    async def find(
        self,
        params: dict[str, Any] | None = None,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list documents.

        Endpoint: GET /documents/find

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
            params: Optional query parameters.

        Returns:
            List of raw document payload dicts.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/documents/find", params=params)
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/documents/find",
                data={"documents": {"parameters": parameters}},
                params=params,
            )
        payloads = extract_object_list_payloads(
            data, container_key="documents", object_key="document"
        )
        return [dict(payload) for payload in payloads]

    async def get(self, document_id: int) -> dict[str, Any]:
        """Get document by ID.

        Endpoint: GET /documents/get/{documentId}

        Args:
            document_id: Document identifier.

        Returns:
            Raw document payload dict.
        """
        data = await self._client.get_json(f"/documents/get/{document_id}")
        return self._extract_document_payload(data)

    async def download(self, document_id: int) -> bytes:
        """Download document as binary PDF.

        Endpoint: GET /documents/download/{documentId}

        Args:
            document_id: Document identifier.

        Returns:
            Binary PDF content.
        """
        return await self._client.get_binary(f"/documents/download/{document_id}")

    async def delete(self, document_id: int) -> dict[str, Any]:
        """Delete a document.

        Endpoint: DELETE /documents/delete/{documentId}

        Args:
            document_id: Document identifier.

        Returns:
            Deleted document payload.
        """
        data = await self._client.delete_json(f"/documents/delete/{document_id}")
        return self._extract_document_payload(data)

    @staticmethod
    def _extract_document_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract document payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="documents",
            object_key="document",
        )
        return dict(payload)


__all__ = [
    "DocumentsResource",
]
