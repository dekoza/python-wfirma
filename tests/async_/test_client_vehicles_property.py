"""Tests for WFirmaClient convenience vehicles resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.vehicles import VehiclesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientVehiclesProperty:
    async def test_vehicles_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.vehicles

        assert isinstance(resource, VehiclesResource)

        await client.close()

    async def test_vehicles_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.vehicles
        second = client.vehicles

        assert first is second

        await client.close()
