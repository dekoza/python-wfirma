"""Tests for WFirmaClient convenience invoices resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.invoices import InvoicesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientInvoicesProperty:
    """Tests for WFirmaClient.invoices property."""

    # AICOMPLETE: Sync client exposes `invoices` resource - ready for review
    def test_invoices_property_returns_invoices_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.invoices

        assert isinstance(resource, InvoicesResource)

        client.close()

    # AICOMPLETE: Sync client caches `invoices` resource - ready for review
    def test_invoices_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.invoices
        second = client.invoices

        assert first is second

        client.close()
