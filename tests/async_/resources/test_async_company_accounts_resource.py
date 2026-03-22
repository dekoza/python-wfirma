"""Tests for asynchronous company_accounts resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.company_accounts import CompanyAccountsResource

pytestmark = pytest.mark.aicomplete


class TestCompanyAccountsResourceGet:
    """Tests for CompanyAccountsResource.get() method."""

    @pytest.mark.asyncio
    # RED: Async company_accounts resource GET returns company_account payload
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = CompanyAccountsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/company_accounts/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "company_accounts": {
                                "0": {
                                    "company_account": {
                                        "id": 456,
                                        "account_number": "12345678901234567890",
                                        "bank_name": "Example Bank",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(company_account_id=456)

        assert route.called
        assert result["id"] == 456
        assert result["account_number"] == "12345678901234567890"


class TestCompanyAccountsResourceFind:
    """Tests for CompanyAccountsResource.find() method."""

    # RED: Async company_accounts resource FIND returns list of company_accounts
    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = CompanyAccountsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/company_accounts/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "company_accounts": {
                                "0": {
                                    "company_account": {
                                        "id": 1,
                                        "account_number": "11111111111111111111",
                                    }
                                },
                                "1": {
                                    "company_account": {
                                        "id": 2,
                                        "account_number": "22222222222222222222",
                                    }
                                },
                            },
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 2,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    # RED: Async company_accounts resource FIND handles empty result
    @pytest.mark.asyncio
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = CompanyAccountsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/company_accounts/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "company_accounts": {},
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 0,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert result == []
