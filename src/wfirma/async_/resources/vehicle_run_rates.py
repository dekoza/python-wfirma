"""Vehicle run rates-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "vehicle_run_rates" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /vehicle_run_rates/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import build_find_parameters, extract_object_list_payloads
from wfirma.async_.client import WFirmaClient


class VehicleRunRatesResource:
    """Asynchronous vehicle_run_rates resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list vehicle run rates.

        Endpoint: GET /vehicle_run_rates/find

        Returns:
            List of raw vehicle_run_rate payload dicts.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/vehicle_run_rates/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/vehicle_run_rates/find",
                data={"vehicle_run_rates": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(
            data, container_key="vehicle_run_rates", object_key="vehicle_run_rate"
        )
        return [dict(payload) for payload in payloads]


__all__ = [
    "VehicleRunRatesResource",
]
