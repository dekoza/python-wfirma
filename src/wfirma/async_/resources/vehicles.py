"""Vehicle-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "vehicles" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API docs list these endpoints:
- GET /vehicles/get/{vehicleId}
- GET /vehicles/find
- POST /vehicles/add
- POST /vehicles/edit/{vehicleId}
- GET /vehicles/delete/{vehicleId}

The delete endpoint uses GET method per wFirma API spec.
This resource uses ``vehicle_id`` in its public methods.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class VehiclesResource:
    """Asynchronous vehicles resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, vehicle_id: int) -> dict[str, Any]:
        """Get vehicle by ID.

        Endpoint: GET /vehicles/get/{vehicleId}

        Args:
            vehicle_id: Vehicle identifier.

        Returns:
            Raw vehicle payload dict.
        """
        data = await self._client.get_json(f"/vehicles/get/{vehicle_id}")
        return self._extract_vehicle_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list vehicles.

        Endpoint: GET /vehicles/find

        Returns:
            List of raw vehicle payloads.
        """
        data = await self._client.get_json("/vehicles/find")
        payloads = extract_object_list_payloads(
            data, container_key="vehicles", object_key="vehicle"
        )
        return [dict(payload) for payload in payloads]

    async def add(self, *, name: str, visibility: str | None = None) -> dict[str, Any]:
        """Create a new vehicle.

        Endpoint: POST /vehicles/add

        Args:
            name: Vehicle name.
            visibility: Vehicle visibility (e.g. "visible"), if supported.

        Returns:
            Created vehicle payload.
        """
        vehicle: dict[str, Any] = {"name": name}
        if visibility is not None:
            vehicle["visibility"] = visibility
        data = await self._client.post_json("/vehicles/add", data={"vehicle": vehicle})
        return self._extract_vehicle_payload(data)

    async def edit(
        self, vehicle_id: int, *, name: str | None = None, visibility: str | None = None
    ) -> dict[str, Any]:
        """Update an existing vehicle.

        Endpoint: POST /vehicles/edit/{vehicleId}

        Args:
            vehicle_id: Vehicle identifier.
            name: New vehicle name.
            visibility: New visibility value.

        Returns:
            Updated vehicle payload.
        """
        vehicle: dict[str, Any] = {}
        if name is not None:
            vehicle["name"] = name
        if visibility is not None:
            vehicle["visibility"] = visibility
        data = await self._client.post_json(
            f"/vehicles/edit/{vehicle_id}", data={"vehicle": vehicle}
        )
        return self._extract_vehicle_payload(data)

    async def delete(self, vehicle_id: int) -> dict[str, Any]:
        """Delete a vehicle.

        Endpoint: GET /vehicles/delete/{vehicleId}

        Note: This endpoint uses GET method (not DELETE) per wFirma API spec.

        Args:
            vehicle_id: Vehicle identifier.

        Returns:
            Response payload from delete operation.
        """
        return await self._client.get_json(f"/vehicles/delete/{vehicle_id}")

    @staticmethod
    def _extract_vehicle_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract vehicle payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="vehicles",
            object_key="vehicle",
        )
        return dict(payload)


__all__ = [
    "VehiclesResource",
]
