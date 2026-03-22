"""Tests for asynchronous payment_cashboxes resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.payment_cashboxes import PaymentCashboxesResource

pytestmark = pytest.mark.aicomplete


class TestAsyncPaymentCashboxesResourceGet:
    """Tests for PaymentCashboxesResource.get() method (async)."""

    # AICOMPLETE: Async payment_cashboxes resource GET returns payment_cashbox payload - ready for review
    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentCashboxesResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/payment_cashboxes/get/789",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "payment_cashboxes": {
                            "0": {
                                "payment_cashbox": {
                                    "id": 789,
                                    "name": "Test Cashbox",
                                    "type": "bank",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(payment_cashbox_id=789)

        await client.close()

        assert route.called
        assert result["id"] == 789
        assert result["name"] == "Test Cashbox"


class TestAsyncPaymentCashboxesResourceFind:
    """Tests for PaymentCashboxesResource.find() method (async)."""

    # AICOMPLETE: Async payment_cashboxes resource FIND returns list of payment_cashboxes - ready for review
    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentCashboxesResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/payment_cashboxes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "payment_cashboxes": {
                            "0": {"payment_cashbox": {"id": 1, "name": "Cashbox A"}},
                            "1": {"payment_cashbox": {"id": 2, "name": "Cashbox B"}},
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

    # AICOMPLETE: Async payment_cashboxes resource FIND handles empty result - ready for review
    @pytest.mark.asyncio
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentCashboxesResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/payment_cashboxes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "payment_cashboxes": {},
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
