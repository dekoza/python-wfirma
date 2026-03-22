"""Tests for asynchronous vat_codes resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.vat_codes import VatCodesResource

pytestmark = pytest.mark.aicomplete


class TestAsyncVatCodesResourceGet:
    """Tests for VatCodesResource.get() method (async)."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VatCodesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/vat_codes/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "vat_codes": {
                            "0": {
                                "vat_code": {
                                    "id": 456,
                                    "name": "VAT 23%",
                                    "rate": 23,
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(vat_code_id=456)

        await client.close()

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "VAT 23%"


class TestAsyncVatCodesResourceFind:
    """Tests for VatCodesResource.find() method (async)."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VatCodesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/vat_codes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "vat_codes": {
                            "0": {
                                "vat_code": {
                                    "id": 1,
                                    "name": "VAT 23%",
                                    "rate": 23,
                                }
                            },
                            "1": {
                                "vat_code": {
                                    "id": 2,
                                    "name": "VAT 8%",
                                    "rate": 8,
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

        await client.close()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.asyncio
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = VatCodesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/vat_codes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "vat_codes": {},
                        "parameters": {
                            "page": 1,
                            "limit": 20,
                            "total": 0,
                        },
                    },
                )
            )

            result = await resource.find()

        await client.close()

        assert route.called
        assert result == []
