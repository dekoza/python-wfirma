"""Tests for WFirmaClient convenience contractors resource property (sync)."""

from __future__ import annotations

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.contractors import ContractorResource


class TestWFirmaClientContractorsProperty:
    """Tests for WFirmaClient.contractors property."""

    # AICOMPLETE: Sync client exposes `contractors` resource - ready for review
    def test_contractors_property_returns_contractor_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.contractors

        assert isinstance(resource, ContractorResource)

        client.close()

    # AICOMPLETE: Sync client caches `contractors` resource - ready for review
    def test_contractors_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.contractors
        second = client.contractors

        assert first is second

        client.close()

