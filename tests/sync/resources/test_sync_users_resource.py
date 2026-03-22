"""Tests for synchronous users resource.

These tests verify that the UsersResource calls the expected endpoints and
returns User Pydantic models.
"""

from __future__ import annotations

import httpx
import respx

from wfirma.models.employee import User
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.users import UsersResource


class TestUsersResource:
    """Tests for UsersResource."""

    def test_get_calls_expected_endpoint_and_returns_user_model(self) -> None:
        """Should call /users/get/{userCompanyId} and return User model."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = UsersResource(client)

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

            result = resource.get(456)

        client.close()

        assert route.called
        assert isinstance(result, User)
        assert result.id == 456
        assert result.login == "test@example.com"
