"""Tests for WFirmaClient convenience contractors resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.contractors import ContractorResource


class TestWFirmaClientContractorsProperty:
    """Tests for async WFirmaClient.contractors property."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async client exposes `contractors` resource - ready for review
    async def test_contractors_property_returns_contractor_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.contractors

        assert isinstance(resource, ContractorResource)

        await client.close()

    @pytest.mark.asyncio
    # AICOMPLETE: Async client caches `contractors` resource - ready for review
    async def test_contractors_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.contractors
        second = client.contractors

        assert first is second

        await client.close()
