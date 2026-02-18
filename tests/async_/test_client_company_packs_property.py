"""Tests for WFirmaClient convenience company_packs resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.company_packs import CompanyPacksResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientCompanyPacksProperty:
    """Tests for WFirmaClient.company_packs property."""

    # RED: Async client exposes company_packs resource
    async def test_company_packs_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = client.company_packs

            assert isinstance(resource, CompanyPacksResource)

    # RED: Async client caches company_packs resource
    async def test_company_packs_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            first = client.company_packs
            second = client.company_packs

            assert first is second
