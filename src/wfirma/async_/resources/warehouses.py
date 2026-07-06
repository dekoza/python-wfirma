"""Warehouse-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "warehouses" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API docs list these endpoints:
- GET /warehouses/find
- GET /warehouses/get/{warehouseId}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient


class WarehousesResource:
    """Asynchronous warehouses resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, warehouse_id: int) -> dict[str, Any]:
        """Get warehouse by ID.

        Endpoint: GET /warehouses/get/{warehouseId}

        Args:
            warehouse_id: Warehouse identifier.

        Returns:
            Raw warehouse payload dict.
        """
        data = await self._client.get_json(f"/warehouses/get/{warehouse_id}")
        return self._extract_warehouse_payload(data)

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list warehouses.

        Endpoint: GET /warehouses/find

        Returns:
            List of raw warehouse payloads.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/warehouses/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/warehouses/find",
                data={"warehouses": {"parameters": parameters}},
            )
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
