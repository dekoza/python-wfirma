"""Test sync client term_groups property."""

from __future__ import annotations

import pytest

from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.term_groups import TermGroupsResource
from wfirma.sync.auth import APIKeyAuth


class TestClientTermGroupsProperty:
    """Test WFirmaClient.term_groups property."""

    def test_returns_resource_instance(self) -> None:
        """term_groups property should return TermGroupsResource instance."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        with WFirmaClient(auth=auth, company_id=123) as client:
            resource = client.term_groups
            assert isinstance(resource, TermGroupsResource)

    def test_is_cached(self) -> None:
        """term_groups property should cache the resource instance."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        with WFirmaClient(auth=auth, company_id=123) as client:
            first = client.term_groups
            second = client.term_groups
            assert first is second
