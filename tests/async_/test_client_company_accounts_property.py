"""Tests for WFirmaClient convenience company_accounts resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.company_accounts import CompanyAccountsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientCompanyAccountsProperty:
    """Tests for WFirmaClient.company_accounts property."""

    # RED: Async client exposes company_accounts resource
    def test_company_accounts_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.company_accounts

        assert isinstance(resource, CompanyAccountsResource)

    # RED: Async client caches company_accounts resource
    def test_company_accounts_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.company_accounts
        second = client.company_accounts

        assert first is second
