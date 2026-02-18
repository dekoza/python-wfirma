"""Tests for WFirmaClient convenience company_packs resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.company_packs import CompanyPacksResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientCompanyPacksProperty:
    """Tests for WFirmaClient.company_packs property."""

    # RED: Sync client exposes company_packs resource
    def test_company_packs_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.company_packs

        assert isinstance(resource, CompanyPacksResource)

        client.close()

    # RED: Sync client caches company_packs resource
    def test_company_packs_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.company_packs
        second = client.company_packs

        assert first is second

        client.close()
