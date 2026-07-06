"""Tests for asynchronous payments resource.

These tests verify that resource wrappers call the expected endpoints and
return parsed Pydantic models.
"""

from __future__ import annotations

import json
from decimal import Decimal

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.payments import PaymentsResource
from wfirma.models.payment import Payment


@pytest.mark.aicomplete
class TestPaymentsResource:
    """Tests for PaymentsResource methods."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        """Should call /payments/get/{paymentId} and return Payment."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/payments/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "payments": {"0": {"payment": {"id": 456, "value": "100.00"}}},
                        },
                    )
                )

                result = await resource.get(payment_id=456)

        assert route.called
        assert isinstance(result, Payment)
        assert result.id == 456
        assert result.value == Decimal("100.00")

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        """Should call /payments/find and return list of Payment."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/payments/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "payments": {
                                "0": {"payment": {"id": 1, "value": "10.00"}},
                                "1": {"payment": {"id": 2, "value": "20.00"}},
                            },
                            "parameters": {"page": 1, "limit": 20, "total": 2},
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert [p.id for p in result] == [1, 2]

    @pytest.mark.asyncio
    async def test_find_handles_empty_result(self) -> None:
        """Should return empty list when no payments found."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/payments/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={"status": {"code": "OK"}, "payments": {}},
                    )
                )

                result = await resource.find()

        assert route.called
        assert result == []


class TestPaymentsResourceAdd:
    """Tests for PaymentsResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async payments resource ADD creates and returns Payment - ready for review
    async def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentsResource(client)

        async with client:
            with respx.mock:

                def _check_request(request: httpx.Request) -> httpx.Response:
                    assert request.headers.get("Content-Type") == "application/json"
                    assert json.loads(request.content.decode("utf-8")) == {
                        "payments": {
                            "0": {
                                "payment": {
                                    "object_name": "invoice",
                                    "object_id": 1000,
                                    "value": "100.00",
                                    "date": "2026-01-19",
                                }
                            }
                        }
                    }
                    return httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "payments": {"0": {"payment": {"id": 789, "value": "100.00"}}},
                        },
                    )

                route = respx.post(
                    "https://api2.wfirma.pl/payments/add",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(side_effect=_check_request)

                result = await resource.add(
                    payment={
                        "object_name": "invoice",
                        "object_id": 1000,
                        "value": "100.00",
                        "date": "2026-01-19",
                    }
                )

        assert route.called
        assert isinstance(result, Payment)
        assert result.id == 789


class TestPaymentsResourceEdit:
    """Tests for PaymentsResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async payments resource EDIT updates and returns Payment - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentsResource(client)

        async with client:
            with respx.mock:

                def _check_request(request: httpx.Request) -> httpx.Response:
                    assert json.loads(request.content.decode("utf-8")) == {
                        "payments": {"0": {"payment": {"description": "Updated"}}}
                    }
                    return httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "payments": {"0": {"payment": {"id": 456, "description": "Updated"}}},
                        },
                    )

                route = respx.post(
                    "https://api2.wfirma.pl/payments/edit/456",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(side_effect=_check_request)

                result = await resource.edit(456, payment={"description": "Updated"})

        assert route.called
        assert isinstance(result, Payment)
        assert result.id == 456
        assert result.description == "Updated"


class TestPaymentsResourceDelete:
    """Tests for PaymentsResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async payments resource DELETE returns True - ready for review
    async def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = PaymentsResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://api2.wfirma.pl/payments/delete/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

                result = await resource.delete(payment_id=456)

        assert route.called
        assert result is True
