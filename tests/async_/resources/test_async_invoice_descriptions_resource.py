"""Tests for asynchronous invoice_descriptions resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.invoice_descriptions import InvoiceDescriptionsResource

pytestmark = pytest.mark.aicomplete


class TestInvoiceDescriptionsResourceGet:
    """Tests for InvoiceDescriptionsResource.get() method."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoiceDescriptionsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/invoice_descriptions/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "invoice_descriptions": {
                                "0": {
                                    "invoice_description": {
                                        "id": 456,
                                        "name": "Service Description",
                                        "vat_rate": "23",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(invoice_description_id=456)

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "Service Description"


class TestInvoiceDescriptionsResourceFind:
    """Tests for InvoiceDescriptionsResource.find() method."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoiceDescriptionsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/invoice_descriptions/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "invoice_descriptions": {
                                "0": {
                                    "invoice_description": {
                                        "id": 1,
                                        "name": "Description 1",
                                    }
                                },
                                "1": {
                                    "invoice_description": {
                                        "id": 2,
                                        "name": "Description 2",
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

    @pytest.mark.asyncio
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoiceDescriptionsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/invoice_descriptions/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "invoice_descriptions": {},
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
