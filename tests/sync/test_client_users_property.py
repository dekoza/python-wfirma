"""Tests for WFirmaClient convenience resource properties (sync users)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.users import UsersResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientUsersProperty:
    """Tests for WFirmaClient.users property."""

    def test_users_property_returns_users_resource(self) -> None:
        """Should return UsersResource instance."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.users

        assert isinstance(resource, UsersResource)

        client.close()

    def test_users_property_is_cached(self) -> None:
        """Should return same instance on multiple accesses."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.users
        second = client.users

        assert first is second

        client.close()
