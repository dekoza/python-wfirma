"""Tests for WFirmaClient convenience interests resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.interests import InterestsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientInterestsProperty:
    """Tests for WFirmaClient.interests property."""

    def test_interests_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.interests

        assert isinstance(resource, InterestsResource)

        client.close()

    def test_interests_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.interests
        second = client.interests

        assert first is second

        client.close()
