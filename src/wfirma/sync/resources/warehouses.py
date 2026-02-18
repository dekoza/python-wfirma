"""Warehouse-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "warehouses" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /warehouses/find
- GET /warehouses/get/{warehouseId}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class WarehousesResource:
    """Synchronous warehouses resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, warehouse_id: int) -> dict[str, Any]:
        """Get warehouse by ID.

        Endpoint: GET /warehouses/get/{warehouseId}

        Args:
            warehouse_id: Warehouse identifier.

        Returns:
            Raw warehouse payload dict.
        """
        data = self._client.get_json(f"/warehouses/get/{warehouse_id}")
        return self._extract_warehouse_payload(data)

    def find(self) -> list[dict[str, Any]]:
        """Find/list warehouses.

        Endpoint: GET /warehouses/find

        Returns:
            List of raw warehouse payload dicts.
        """
        data = self._client.get_json("/warehouses/find")
        payloads = extract_object_list_payloads(
            data, container_key="warehouses", object_key="warehouse"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_warehouse_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract warehouse payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="warehouses",
            object_key="warehouse",
        )
        return dict(payload)


__all__ = [
    "WarehousesResource",
]
