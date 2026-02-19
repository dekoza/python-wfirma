"""Series-related resource endpoints (synchronous).

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

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class SeriesResource:
    """Synchronous series resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def add(self, series: dict[str, Any]) -> dict[str, Any]:
        """Create a new series.

        Endpoint: POST /series/add

        Args:
            series: Series data payload.

        Returns:
            Created series payload.
        """
        data = self._client.post_json("/series/add", data={"series": series})
        return self._extract_series_payload(data)

    def find(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Find/list series.

        Endpoint: GET /series/find

        Args:
            params: Optional query parameters.

        Returns:
            List of raw series payload dicts.
        """
        data = self._client.get_json("/series/find", params=params)
        payloads = extract_object_list_payloads(data, container_key="series", object_key="series")
        return [dict(payload) for payload in payloads]

    def get(self, series_id: int) -> dict[str, Any]:
        """Get series by ID.

        Endpoint: GET /series/get/{seriesId}

        Args:
            series_id: Series identifier.

        Returns:
            Raw series payload dict.
        """
        data = self._client.get_json(f"/series/get/{series_id}")
        return self._extract_series_payload(data)

    def edit(self, series_id: int, series: dict[str, Any]) -> dict[str, Any]:
        """Update an existing series.

        Endpoint: PUT /series/edit/{seriesId}

        Args:
            series_id: Series identifier.
            series: Updated series data payload.

        Returns:
            Updated series payload.
        """
        data = self._client.put_json(f"/series/edit/{series_id}", data={"series": series})
        return self._extract_series_payload(data)

    def delete(self, series_id: int) -> dict[str, Any]:
        """Delete a series.

        Endpoint: DELETE /series/del/{seriesId}

        Args:
            series_id: Series identifier.

        Returns:
            Response payload from deletion.
        """
        data = self._client.delete_json(f"/series/del/{series_id}")
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
