"""Tests for synchronous payment_cashboxes resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.payment_cashboxes import PaymentCashboxesResource

pytestmark = pytest.mark.aicomplete


class TestPaymentCashboxesResourceGet:
    """Tests for PaymentCashboxesResource.get() method."""

    # AICOMPLETE: Sync payment_cashboxes resource GET returns payment_cashbox payload - ready for review
    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentCashboxesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/payment_cashboxes/get/789",
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

            result = resource.get(payment_cashbox_id=789)

        client.close()

        assert route.called
        assert result["id"] == 789
        assert result["name"] == "Test Cashbox"


class TestPaymentCashboxesResourceFind:
    """Tests for PaymentCashboxesResource.find() method."""

    # AICOMPLETE: Sync payment_cashboxes resource FIND returns list of payment_cashboxes - ready for review
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentCashboxesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/payment_cashboxes/find",
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

            result = resource.find()

        client.close()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    # AICOMPLETE: Sync payment_cashboxes resource FIND handles empty result - ready for review
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentCashboxesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/payment_cashboxes/find",
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

            result = resource.find()

        client.close()

        assert route.called
        assert result == []
