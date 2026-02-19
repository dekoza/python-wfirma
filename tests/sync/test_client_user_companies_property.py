"""Tests for user_companies property in synchronous client."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.user_companies import UserCompaniesResource

pytestmark = pytest.mark.aicomplete


class TestClientUserCompaniesProperty:
    """Tests for WFirmaClient.user_companies property."""

    def test_returns_resource_instance(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.user_companies

        assert isinstance(resource, UserCompaniesResource)

    def test_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.user_companies
        second = client.user_companies

        assert first is second
