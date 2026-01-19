"""Tests for WFirmaClient convenience tags resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.tags import TagsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientTagsProperty:
    """Tests for WFirmaClient.tags property."""

    # AICOMPLETE: Sync client exposes `tags` resource - ready for review
    def test_tags_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.tags

        assert isinstance(resource, TagsResource)

        client.close()

    # AICOMPLETE: Sync client caches `tags` resource - ready for review
    def test_tags_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.tags
        second = client.tags

        assert first is second

        client.close()
