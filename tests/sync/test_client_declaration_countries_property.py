"""Tests for WFirmaClient convenience declaration_countries resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.declaration_countries import DeclarationCountriesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientDeclarationCountriesProperty:
    """Tests for WFirmaClient.declaration_countries property."""

    def test_declaration_countries_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.declaration_countries

        assert isinstance(resource, DeclarationCountriesResource)

        client.close()

    def test_declaration_countries_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.declaration_countries
        second = client.declaration_countries

        assert first is second

        client.close()
