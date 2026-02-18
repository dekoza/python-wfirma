"""Tests for WFirmaClient convenience vat_codes resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.vat_codes import VatCodesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientAsyncVatCodesProperty:
    """Tests for WFirmaClient.vat_codes property (async)."""

    def test_vat_codes_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.vat_codes

        assert isinstance(resource, VatCodesResource)

    def test_vat_codes_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.vat_codes
        second = client.vat_codes

        assert first is second
