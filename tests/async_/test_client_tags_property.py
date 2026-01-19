"""Tests for WFirmaClient convenience tags resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.tags import TagsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaAsyncClientTagsProperty:
    """Tests for async WFirmaClient.tags property."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async client exposes `tags` resource - ready for review
    async def test_tags_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.tags

        assert isinstance(resource, TagsResource)

        await client.close()

    @pytest.mark.asyncio
    # AICOMPLETE: Async client caches `tags` resource - ready for review
    async def test_tags_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.tags
        second = client.tags

        assert first is second

        await client.close()
