"""Tests for WFirmaClient convenience resource properties (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.company import CompanyResource


class TestWFirmaClientCompanyProperty:
    """Tests for async WFirmaClient.company property."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async client exposes `company` resource - ready for review
    async def test_company_property_returns_company_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        async with client:
            resource = client.company
            assert isinstance(resource, CompanyResource)

    @pytest.mark.asyncio
    # AICOMPLETE: Async client caches `company` resource - ready for review
    async def test_company_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        async with client:
            first = client.company
            second = client.company
            assert first is second
