"""Tests for asynchronous goods resource.

These tests verify that resource wrappers call the expected endpoints and
map payloads into ``wfirma.models.good.Good``.
"""

from __future__ import annotations

from decimal import Decimal

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.goods import GoodsResource
from wfirma.models.good import Good


class TestGoodsResourceGet:
    """Tests for async GoodsResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async goods resource GET returns Good model - ready for review
    async def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/goods/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "goods": {
                                "0": {
                                    "good": {
                                        "id": 456,
                                        "name": "Premium Widget",
                                        "code": "WID-001",
                                        "unit": "szt.",
                                        "netto": "99.99",
                                        "vat": "23",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(good_id=456)

        assert route.called
        assert isinstance(result, Good)
        assert result.id == 456
        assert result.name == "Premium Widget"
        assert result.netto == Decimal("99.99")


class TestGoodsResourceFind:
    """Tests for async GoodsResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async goods resource FIND returns list of Goods - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/goods/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "goods": {
                                "0": {"good": {"id": 100, "name": "Good A"}},
                                "1": {"good": {"id": 101, "name": "Good B"}},
                            },
                            "parameters": {"page": 1, "limit": 20, "total": 2},
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert len(result) == 2
        assert result[0].id == 100
        assert result[1].id == 101

    @pytest.mark.asyncio
    # AICOMPLETE: Async goods resource FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/goods/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "goods": {},
                            "parameters": {"page": 1, "limit": 20, "total": 0},
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert result == []


class TestGoodsResourceAdd:
    """Tests for async GoodsResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async goods resource ADD creates and returns Good - ready for review
    async def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://api2.wfirma.pl/goods/add",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "goods": {
                                "0": {"good": {"id": 789, "name": "New Good", "netto": "10.00"}}
                            },
                        },
                    )
                )

                result = await resource.add(name="New Good", netto=Decimal("10.00"))

        assert route.called
        assert result.id == 789
        assert result.netto == Decimal("10.00")


class TestGoodsResourceDelete:
    """Tests for async GoodsResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async goods resource DELETE returns True - ready for review
    async def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://api2.wfirma.pl/goods/delete/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

                result = await resource.delete(good_id=456)

        assert route.called
        assert result is True


class TestGoodsResourceEdit:
    """Tests for async GoodsResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async goods resource EDIT updates and returns Good - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://api2.wfirma.pl/goods/edit/456",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "goods": {
                                "0": {
                                    "good": {
                                        "id": 456,
                                        "name": "Updated Good",
                                        "netto": "12.50",
                                        "vat": "23",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.edit(
                    456,
                    name="Updated Good",
                    netto=Decimal("12.50"),
                    vat="23",
                )

        assert route.called
        assert isinstance(result, Good)
        assert result.id == 456
        assert result.name == "Updated Good"
        assert result.netto == Decimal("12.50")
