"""Tests for WFirmaClient convenience goods resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.goods import GoodsResource


class TestWFirmaClientGoodsProperty:
    """Tests for async WFirmaClient.goods property."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async client exposes `goods` resource - ready for review
    async def test_goods_property_returns_goods_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.goods

        assert isinstance(resource, GoodsResource)

        await client.close()

    @pytest.mark.asyncio
    # AICOMPLETE: Async client caches `goods` resource - ready for review
    async def test_goods_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.goods
        second = client.goods

        assert first is second

        await client.close()
