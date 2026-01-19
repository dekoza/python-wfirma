"""Tests for WFirmaClient convenience resource properties (sync)."""

from __future__ import annotations

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.company import CompanyResource


class TestWFirmaClientCompanyProperty:
    """Tests for WFirmaClient.company property."""

    # AICOMPLETE: Sync client exposes `company` resource - ready for review
    def test_company_property_returns_company_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.company

        assert isinstance(resource, CompanyResource)

        client.close()

    # AICOMPLETE: Sync client caches `company` resource - ready for review
    def test_company_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.company
        second = client.company

        assert first is second

        client.close()
