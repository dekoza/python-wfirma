"""Tests for client.series property (asynchronous)."""

from __future__ import annotations

import pytest

from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.series import SeriesResource


@pytest.fixture
async def async_client() -> WFirmaClient:
    """Create a test async client."""
    from wfirma.async_.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="test_access", secret_key="test_secret", app_key="test_app")
    async with WFirmaClient(auth=auth, company_id="123") as client:
        yield client


@pytest.mark.asyncio
async def test_series_property_returns_series_resource(async_client: WFirmaClient) -> None:
    """Verify client.series property returns SeriesResource instance."""
    result = async_client.series
    assert isinstance(result, SeriesResource)


@pytest.mark.asyncio
async def test_series_property_is_cached(async_client: WFirmaClient) -> None:
    """Verify client.series property is cached (same instance returned)."""
    first = async_client.series
    second = async_client.series
    assert first is second
