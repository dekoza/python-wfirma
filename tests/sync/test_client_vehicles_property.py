"""Tests for WFirmaClient convenience vehicles resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.vehicles import VehiclesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientVehiclesProperty:
    def test_vehicles_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.vehicles

        assert isinstance(resource, VehiclesResource)

        client.close()

    def test_vehicles_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.vehicles
        second = client.vehicles

        assert first is second

        client.close()
