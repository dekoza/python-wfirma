"""Vehicle-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "vehicles" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
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

from wfirma._payloads import (
    build_find_parameters,
    build_module_payload,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.sync.client import WFirmaClient


class VehiclesResource:
    """Synchronous vehicles resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, vehicle_id: int) -> dict[str, Any]:
        """Get vehicle by ID.

        Endpoint: GET /vehicles/get/{vehicleId}

        Args:
            vehicle_id: Vehicle identifier.

        Returns:
            Raw vehicle payload dict.
        """
        data = self._client.get_json(f"/vehicles/get/{vehicle_id}")
        return self._extract_vehicle_payload(data)

    def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list vehicles.

        Endpoint: GET /vehicles/find

        Returns:
            List of raw vehicle payload dicts.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = self._client.get_json("/vehicles/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = self._client.post_json(
                "/vehicles/find",
                data={"vehicles": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(
            data, container_key="vehicles", object_key="vehicle"
        )
        return [dict(payload) for payload in payloads]

    def add(
        self,
        vehicle: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        visibility: str | None = None,
    ) -> dict[str, Any]:
        """Create a new vehicle.

        Endpoint: POST /vehicles/add

        Args:
            vehicle: Full vehicle payload dict (documented fields include
                ``name``, ``register``, ``type``, ``ownership``, etc.).
            name: Vehicle name, merged into the payload when given.
            visibility: Vehicle visibility, merged into the payload when given.

        Returns:
            Created vehicle payload.
        """
        fields: dict[str, Any] = dict(vehicle or {})
        if name is not None:
            fields["name"] = name
        if visibility is not None:
            fields["visibility"] = visibility

        data = self._client.post_json(
            "/vehicles/add",
            data=build_module_payload(container_key="vehicles", object_key="vehicle", obj=fields),
        )
        return self._extract_vehicle_payload(data)

    def edit(
        self,
        vehicle_id: int,
        vehicle: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        visibility: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing vehicle.

        Endpoint: POST /vehicles/edit/{vehicleId}

        Args:
            vehicle_id: Vehicle identifier.
            vehicle: Full vehicle payload dict with updated fields.
            name: New vehicle name, merged into the payload when given.
            visibility: New visibility value, merged into the payload when given.

        Returns:
            Updated vehicle payload.
        """
        fields: dict[str, Any] = dict(vehicle or {})
        if name is not None:
            fields["name"] = name
        if visibility is not None:
            fields["visibility"] = visibility

        data = self._client.post_json(
            f"/vehicles/edit/{vehicle_id}",
            data=build_module_payload(container_key="vehicles", object_key="vehicle", obj=fields),
        )
        return self._extract_vehicle_payload(data)

    def delete(self, vehicle_id: int) -> dict[str, Any]:
        """Delete a vehicle.

        Endpoint: GET /vehicles/delete/{vehicleId}

        Note: This endpoint uses GET method (not DELETE) per wFirma API spec.

        Args:
            vehicle_id: Vehicle identifier.

        Returns:
            Response payload from delete operation.
        """
        return self._client.get_json(f"/vehicles/delete/{vehicle_id}")

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
