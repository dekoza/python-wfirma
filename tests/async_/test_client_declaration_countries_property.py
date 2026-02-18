"""Tests for WFirmaClient convenience declaration_countries resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.declaration_countries import DeclarationCountriesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientDeclarationCountriesProperty:
    """Tests for WFirmaClient.declaration_countries property."""

    @pytest.mark.asyncio
    async def test_declaration_countries_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = client.declaration_countries

            assert isinstance(resource, DeclarationCountriesResource)

    @pytest.mark.asyncio
    async def test_declaration_countries_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            first = client.declaration_countries
            second = client.declaration_countries

            assert first is second
