"""Series-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "series" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- POST /series/add
- GET /series/find
- GET /series/get/{seriesId}
- PUT /series/edit/{seriesId}
- DELETE /series/del/{seriesId}
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


class SeriesResource:
    """Asynchronous series resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def add(self, series: dict[str, Any]) -> dict[str, Any]:
        """Create a new series.

        Endpoint: POST /series/add

        Args:
            series: Series data payload.

        Returns:
            Created series payload.
        """
        data = await self._client.post_json(
            "/series/add",
            data=build_module_payload(container_key="series", object_key="series", obj=series),
        )
        return self._extract_series_payload(data)

    async def find(
        self,
        params: dict[str, Any] | None = None,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list series.

        Endpoint: GET /series/find

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
            params: Optional query parameters.

        Returns:
            List of raw series payload dicts.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/series/find", params=params)
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/series/find",
                data={"series": {"parameters": parameters}},
                params=params,
            )
        payloads = extract_object_list_payloads(data, container_key="series", object_key="series")
        return [dict(payload) for payload in payloads]

    async def get(self, series_id: int) -> dict[str, Any]:
        """Get series by ID.

        Endpoint: GET /series/get/{seriesId}

        Args:
            series_id: Series identifier.

        Returns:
            Raw series payload dict.
        """
        data = await self._client.get_json(f"/series/get/{series_id}")
        return self._extract_series_payload(data)

    async def edit(self, series_id: int, series: dict[str, Any]) -> dict[str, Any]:
        """Update an existing series.

        Endpoint: PUT /series/edit/{seriesId}

        Args:
            series_id: Series identifier.
            series: Updated series data payload.

        Returns:
            Updated series payload.
        """
        data = await self._client.post_json(
            f"/series/edit/{series_id}",
            data=build_module_payload(container_key="series", object_key="series", obj=series),
        )
        return self._extract_series_payload(data)

    async def delete(self, series_id: int) -> dict[str, Any]:
        """Delete a series.

        Endpoint: DELETE /series/del/{seriesId}

        Args:
            series_id: Series identifier.

        Returns:
            Response payload from deletion.
        """
        data = await self._client.delete_json(f"/series/del/{series_id}")
        return self._extract_series_payload(data)

    @staticmethod
    def _extract_series_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract series payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="series",
            object_key="series",
        )
        return dict(payload)


__all__ = [
    "SeriesResource",
]
