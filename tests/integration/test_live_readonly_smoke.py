"""Live read-only production checks for the supported beta surface."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_api_key_sync_client_can_read_company(
    live_api_key_sync_client, integration_company_id
) -> None:
    """API key auth should support a read-only company fetch."""
    with live_api_key_sync_client as client:
        company = client.company.get()

    assert company.id == integration_company_id
    assert company.name


@pytest.mark.asyncio
async def test_api_key_async_client_can_read_company(
    live_api_key_async_client, integration_company_id
) -> None:
    """Async API key auth should support a read-only company fetch."""
    async with live_api_key_async_client as client:
        company = await client.company.get()

    assert company.id == integration_company_id
    assert company.name


def test_oauth2_sync_client_can_read_company(
    live_oauth2_sync_client, integration_company_id
) -> None:
    """OAuth2 should work in the sync client when a live token is provided."""
    with live_oauth2_sync_client as client:
        company = client.company.get()

    assert company.id == integration_company_id
    assert company.name


@pytest.mark.asyncio
async def test_oauth2_async_client_can_read_company(
    live_oauth2_async_client, integration_company_id
) -> None:
    """OAuth2 should work in the async client when a live token is provided."""
    async with live_oauth2_async_client as client:
        company = await client.company.get()

    assert company.id == integration_company_id
    assert company.name
