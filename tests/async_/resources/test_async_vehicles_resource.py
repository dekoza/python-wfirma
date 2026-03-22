"""Tests for asynchronous vehicles resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.vehicles import VehiclesResource

pytestmark = pytest.mark.aicomplete


class TestVehiclesResourceGet:
    """Tests for async VehiclesResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async vehicles resource GET returns vehicle payload - ready for review
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VehiclesResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/vehicles/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "vehicles": {
                                "0": {
                                    "vehicle": {
                                        "id": 456,
                                        "name": "Test vehicle",
                                        "visibility": "visible",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(vehicle_id=456)

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "Test vehicle"


class TestVehiclesResourceFind:
    """Tests for async VehiclesResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async vehicles resource FIND returns list of vehicles - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VehiclesResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/vehicles/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "vehicles": {
                                "0": {"vehicle": {"id": 1, "name": "A"}},
                                "1": {"vehicle": {"id": 2, "name": "B"}},
                            },
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 2,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.asyncio
    # AICOMPLETE: Async vehicles resource FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VehiclesResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/vehicles/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "vehicles": {},
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 0,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert result == []


class TestVehiclesResourceAdd:
    """Tests for async VehiclesResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async vehicles resource ADD sends payload and returns vehicle payload - ready for review
    async def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VehiclesResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/vehicles/add",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "vehicles": {
                                "0": {
                                    "vehicle": {
                                        "id": 10,
                                        "name": "New",
                                        "visibility": "visible",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.add(name="New", visibility="visible")

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "New"


class TestVehiclesResourceEdit:
    """Tests for async VehiclesResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async vehicles resource EDIT sends payload and returns vehicle payload - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VehiclesResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/vehicles/edit/10",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "vehicles": {
                                "0": {
                                    "vehicle": {
                                        "id": 10,
                                        "name": "Renamed",
                                        "visibility": "visible",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.edit(vehicle_id=10, name="Renamed")

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "Renamed"


class TestVehiclesResourceDelete:
    """Tests for async VehiclesResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async vehicles resource DELETE uses GET and returns payload - ready for review
    async def test_delete_calls_expected_endpoint_with_get_method(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VehiclesResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/vehicles/delete/10",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                        },
                    )
                )

                result = await resource.delete(vehicle_id=10)

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"
