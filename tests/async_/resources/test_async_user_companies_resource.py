"""Tests for asynchronous user_companies resource.

These tests verify that the resource wrapper calls the expected endpoints
and handles user-scoped responses (no company_id parameter).
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.user_companies import UserCompaniesResource

pytestmark = pytest.mark.aicomplete


class TestUserCompaniesResourceGet:
    """Tests for UserCompaniesResource.get() method (async)."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
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

                result = await resource.get(999)

                assert route.called
                assert result["id"] == 999
                assert result["company_id"] == 123
                call_params = route.calls[0].request.url.params
                assert "company_id" not in call_params

    @pytest.mark.asyncio
    async def test_get_does_not_include_company_id_parameter(self) -> None:
        """Verify that GET requests do NOT include company_id (user-scoped endpoint)."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
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

                await resource.get(999)

                assert route.called
                call_params = route.calls[0].request.url.params
                assert "company_id" not in call_params


class TestUserCompaniesResourceFind:
    """Tests for UserCompaniesResource.find() method (async)."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
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

                result = await resource.find()

                assert route.called
                assert len(result) == 2
                assert result[0]["id"] == 999
                assert result[1]["id"] == 1000
                call_params = route.calls[0].request.url.params
                assert "company_id" not in call_params

    @pytest.mark.asyncio
    async def test_find_returns_empty_list_when_container_is_empty(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
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

                result = await resource.find()

                assert route.called
                assert result == []
