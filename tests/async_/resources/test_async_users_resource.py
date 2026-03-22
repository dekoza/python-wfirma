"""Tests for asynchronous users resource.

These tests verify that async UsersResource calls expected endpoints and
returns User Pydantic models.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.users import UsersResource
from wfirma.models.employee import User


class TestUsersResource:
    """Tests for async UsersResource."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_user_model(self) -> None:
        """Should call /users/get/{userCompanyId} and return User model."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = UsersResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/users/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "users": {"0": {"user": {"id": 456, "login": "test@example.com"}}},
                        },
                    )
                )

                result = await resource.get(456)

        assert route.called
        assert isinstance(result, User)
        assert result.id == 456
        assert result.login == "test@example.com"
