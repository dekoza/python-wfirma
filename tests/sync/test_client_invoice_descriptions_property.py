"""Tests for WFirmaClient convenience invoice_descriptions resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.invoice_descriptions import InvoiceDescriptionsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientInvoiceDescriptionsProperty:
    """Tests for WFirmaClient.invoice_descriptions property."""

    def test_invoice_descriptions_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.invoice_descriptions

        assert isinstance(resource, InvoiceDescriptionsResource)

        client.close()

    def test_invoice_descriptions_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.invoice_descriptions
        second = client.invoice_descriptions

        assert first is second

        client.close()
