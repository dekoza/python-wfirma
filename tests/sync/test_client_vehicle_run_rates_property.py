"""Tests for sync client vehicle_run_rates property."""

from __future__ import annotations

from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.vehicle_run_rates import VehicleRunRatesResource


def test_client_vehicle_run_rates_property_returns_resource() -> None:
    """Test that client.vehicle_run_rates returns VehicleRunRatesResource."""
    client = WFirmaClient(auth=None, company_id=123)  # type: ignore
    resource = client.vehicle_run_rates

    assert isinstance(resource, VehicleRunRatesResource)


def test_client_vehicle_run_rates_property_is_cached() -> None:
    """Test that client.vehicle_run_rates is cached (same instance)."""
    client = WFirmaClient(auth=None, company_id=123)  # type: ignore
    first = client.vehicle_run_rates
    second = client.vehicle_run_rates

    assert first is second
