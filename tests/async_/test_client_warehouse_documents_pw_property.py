"""Tests for WFirmaClient convenience warehouse_documents_pw resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.warehouse_documents_pw import WarehouseDocumentPWResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientWarehouseDocumentsPWProperty:
    """Tests for async WFirmaClient.warehouse_documents_pw property."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async client exposes `warehouse_documents_pw` resource - ready for review
    async def test_warehouse_documents_pw_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.warehouse_documents_pw

        assert isinstance(resource, WarehouseDocumentPWResource)

        await client.close()

    @pytest.mark.asyncio
    # AICOMPLETE: Async client caches `warehouse_documents_pw` resource - ready for review
    async def test_warehouse_documents_pw_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.warehouse_documents_pw
        second = client.warehouse_documents_pw

        assert first is second

        await client.close()
