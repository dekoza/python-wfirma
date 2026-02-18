"""Vehicle run rates-related resource endpoints (synchronous).

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

from wfirma._payloads import extract_object_list_payloads
from wfirma.sync.client import WFirmaClient


class VehicleRunRatesResource:
    """Synchronous vehicle_run_rates resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def find(self) -> list[dict[str, Any]]:
        """Find/list vehicle run rates.

        Endpoint: GET /vehicle_run_rates/find

        Returns:
            List of raw vehicle_run_rate payload dicts.
        """
        data = self._client.get_json("/vehicle_run_rates/find")
        payloads = extract_object_list_payloads(
            data, container_key="vehicle_run_rates", object_key="vehicle_run_rate"
        )
        return [dict(payload) for payload in payloads]


__all__ = [
    "VehicleRunRatesResource",
]
