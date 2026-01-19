"""Tests for WFirmaClient convenience invoices resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.invoices import InvoicesResource


class TestWFirmaClientInvoicesProperty:
    """Tests for async WFirmaClient.invoices property."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async client exposes `invoices` resource - ready for review
    async def test_invoices_property_returns_invoices_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.invoices

        assert isinstance(resource, InvoicesResource)

        await client.close()

    @pytest.mark.asyncio
    # AICOMPLETE: Async client caches `invoices` resource - ready for review
    async def test_invoices_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.invoices
        second = client.invoices

        assert first is second

        await client.close()
