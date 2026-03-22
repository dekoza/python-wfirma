"""Tests for synchronous expenses resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.expenses import ExpensesResource

pytestmark = pytest.mark.aicomplete


class TestExpensesResourceGet:
    """Tests for ExpensesResource.get() method."""

    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ExpensesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/expenses/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "expenses": {
                            "0": {
                                "expense": {
                                    "id": 456,
                                    "description": "Office supplies",
                                    "amount": 100.50,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(expense_id=456)

        client.close()

        assert route.called
        assert result["id"] == 456
        assert result["description"] == "Office supplies"


class TestExpensesResourceFind:
    """Tests for ExpensesResource.find() method."""

    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ExpensesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/expenses/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "expenses": {
                            "0": {
                                "expense": {
                                    "id": 1,
                                    "description": "Travel",
                                    "amount": 50.00,
                                }
                            },
                            "1": {
                                "expense": {
                                    "id": 2,
                                    "description": "Meals",
                                    "amount": 25.00,
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

            result = resource.find()

        client.close()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ExpensesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/expenses/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "expenses": {},
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
