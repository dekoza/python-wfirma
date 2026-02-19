"""Tests for user_companies property in asynchronous client."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.user_companies import UserCompaniesResource

pytestmark = pytest.mark.aicomplete


class TestClientUserCompaniesProperty:
    """Tests for WFirmaClient.user_companies property (async)."""

    @pytest.mark.asyncio
    async def test_returns_resource_instance(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = client.user_companies

            assert isinstance(resource, UserCompaniesResource)

    @pytest.mark.asyncio
    async def test_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            first = client.user_companies
            second = client.user_companies

            assert first is second
