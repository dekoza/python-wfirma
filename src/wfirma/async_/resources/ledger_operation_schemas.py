"""Ledger operation schemas-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "ledger_operation_schemas" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /ledger_operation_schemas/get/{schema_id}
- GET /ledger_operation_schemas/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class LedgerOperationSchemasResource:
    """Asynchronous ledger_operation_schemas resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, schema_id: int) -> dict[str, Any]:
        """Get ledger operation schema by ID.

        Endpoint: GET /ledger_operation_schemas/get/{schema_id}

        Args:
            schema_id: Ledger operation schema identifier.

        Returns:
            Raw ledger operation schema payload dict.
        """
        data = await self._client.get_json(f"/ledger_operation_schemas/get/{schema_id}")
        return self._extract_ledger_operation_schema_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list ledger operation schemas.

        Endpoint: GET /ledger_operation_schemas/find

        Returns:
            List of raw ledger operation schema payload dicts.
        """
        data = await self._client.get_json("/ledger_operation_schemas/find")
        payloads = extract_object_list_payloads(
            data, container_key="ledger_operation_schemas", object_key="ledger_operation_schema"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_ledger_operation_schema_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract ledger operation schema payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="ledger_operation_schemas",
            object_key="ledger_operation_schema",
        )
        return dict(payload)


__all__ = [
    "LedgerOperationSchemasResource",
]
