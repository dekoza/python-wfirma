"""Tests for WFirmaClient convenience resource properties (async users)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.users import UsersResource


class TestWFirmaClientUsersProperty:
    """Tests for async WFirmaClient.users property."""

    @pytest.mark.asyncio
    async def test_users_property_returns_users_resource(self) -> None:
        """Should return UsersResource instance."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        async with client:
            resource = client.users
            assert isinstance(resource, UsersResource)

    @pytest.mark.asyncio
    async def test_users_property_is_cached(self) -> None:
        """Should return same instance on multiple accesses."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        async with client:
            first = client.users
            second = client.users
            assert first is second
