"""Tests for synchronous user_companies resource.

These tests verify that the resource wrapper calls the expected endpoints
and handles user-scoped responses (no company_id parameter).
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.user_companies import UserCompaniesResource

pytestmark = pytest.mark.aicomplete


class TestUserCompaniesResourceGet:
    """Tests for UserCompaniesResource.get() method."""

    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = UserCompaniesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/user_companies/get/999",
                params={
                    "outputFormat": "json",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "user_companies": {
                            "0": {
                                "user_company": {
                                    "id": 999,
                                    "company_id": 123,
                                    "user_id": 456,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(999)

            assert route.called
            assert result["id"] == 999
            assert result["company_id"] == 123
            assert (
                "company_id" not in route.calls[0].request.url.params
                or route.calls[0].request.url.params.get("company_id") is None
            )

    def test_get_does_not_include_company_id_parameter(self) -> None:
        """Verify that GET requests do NOT include company_id (user-scoped endpoint)."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = UserCompaniesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/user_companies/get/999",
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "user_companies": {
                            "0": {
                                "user_company": {
                                    "id": 999,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(999)

            assert route.called
            # Verify company_id is NOT in params
            call_params = route.calls[0].request.url.params
            assert "company_id" not in call_params


class TestUserCompaniesResourceFind:
    """Tests for UserCompaniesResource.find() method."""

    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = UserCompaniesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/user_companies/find",
                params={
                    "outputFormat": "json",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "user_companies": {
                            "0": {
                                "user_company": {
                                    "id": 999,
                                    "company_id": 123,
                                }
                            },
                            "1": {
                                "user_company": {
                                    "id": 1000,
                                    "company_id": 124,
                                }
                            },
                        },
                    },
                )
            )

            result = resource.find()

            assert route.called
            assert len(result) == 2
            assert result[0]["id"] == 999
            assert result[1]["id"] == 1000
            # Verify company_id is NOT in params
            call_params = route.calls[0].request.url.params
            assert "company_id" not in call_params

    def test_find_returns_empty_list_when_container_is_empty(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = UserCompaniesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/user_companies/find",
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "user_companies": {},
                    },
                )
            )

            result = resource.find()

            assert route.called
            assert result == []
