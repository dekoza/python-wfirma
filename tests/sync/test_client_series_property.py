"""Tests for client.series property (synchronous)."""

from __future__ import annotations

import pytest

from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.series import SeriesResource


@pytest.fixture
def client() -> WFirmaClient:
    """Create a test client."""
    from wfirma.sync.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="test_access", secret_key="test_secret", app_key="test_app")
    return WFirmaClient(auth=auth, company_id="123")


def test_series_property_returns_series_resource(client: WFirmaClient) -> None:
    """Verify client.series property returns SeriesResource instance."""
    result = client.series
    assert isinstance(result, SeriesResource)


def test_series_property_is_cached(client: WFirmaClient) -> None:
    """Verify client.series property is cached (same instance returned)."""
    first = client.series
    second = client.series
    assert first is second
