"""Tests for WFirmaClient convenience vat_codes resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.vat_codes import VatCodesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientVatCodesProperty:
    """Tests for WFirmaClient.vat_codes property."""

    def test_vat_codes_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.vat_codes

        assert isinstance(resource, VatCodesResource)

        client.close()

    def test_vat_codes_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.vat_codes
        second = client.vat_codes

        assert first is second

        client.close()
