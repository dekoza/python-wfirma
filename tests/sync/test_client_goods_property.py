"""Tests for WFirmaClient convenience goods resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.goods import GoodsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientGoodsProperty:
    """Tests for WFirmaClient.goods property."""

    # AICOMPLETE: Sync client exposes `goods` resource - ready for review
    def test_goods_property_returns_goods_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.goods

        assert isinstance(resource, GoodsResource)

        client.close()

    # AICOMPLETE: Sync client caches `goods` resource - ready for review
    def test_goods_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.goods
        second = client.goods

        assert first is second

        client.close()
