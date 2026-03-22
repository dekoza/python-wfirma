"""Tests for synchronous goods resource.

These tests verify that resource wrappers call the expected endpoints and
map payloads into ``wfirma.models.good.Good``.
"""

from __future__ import annotations

from decimal import Decimal

import httpx
import respx

from wfirma.models.good import Good
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.goods import GoodsResource


class TestGoodsResourceGet:
    """Tests for GoodsResource.get() method."""

    # AICOMPLETE: Sync goods resource GET returns Good model - ready for review
    def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

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

            result = resource.get(good_id=456)

        client.close()

        assert route.called
        assert isinstance(result, Good)
        assert result.id == 456
        assert result.name == "Premium Widget"
        assert result.code == "WID-001"
        assert result.netto == Decimal("99.99")


class TestGoodsResourceFind:
    """Tests for GoodsResource.find() method."""

    # AICOMPLETE: Sync goods resource FIND returns list of Goods - ready for review
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

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

            result = resource.find()

        client.close()

        assert route.called
        assert len(result) == 2
        assert result[0].id == 100
        assert result[1].id == 101

    # AICOMPLETE: Sync goods resource FIND handles empty result - ready for review
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

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

            result = resource.find()

        client.close()

        assert route.called
        assert result == []


class TestGoodsResourceAdd:
    """Tests for GoodsResource.add() method."""

    # AICOMPLETE: Sync goods resource ADD creates and returns Good - ready for review
    def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

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
                            "0": {
                                "good": {
                                    "id": 789,
                                    "name": "New Good",
                                    "netto": "10.00",
                                    "vat": "23",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.add(
                name="New Good",
                netto=Decimal("10.00"),
                vat="23",
            )

        client.close()

        assert route.called
        assert result.id == 789
        assert result.name == "New Good"
        assert result.netto == Decimal("10.00")


class TestGoodsResourceDelete:
    """Tests for GoodsResource.delete() method."""

    # AICOMPLETE: Sync goods resource DELETE returns True - ready for review
    def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

        with respx.mock:
            route = respx.delete(
                "https://api2.wfirma.pl/goods/delete/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

            result = resource.delete(good_id=456)

        client.close()

        assert route.called
        assert result is True


class TestGoodsResourceEdit:
    """Tests for GoodsResource.edit() method."""

    # AICOMPLETE: Sync goods resource EDIT updates and returns Good - ready for review
    def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = GoodsResource(client)

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

            result = resource.edit(
                456,
                name="Updated Good",
                netto=Decimal("12.50"),
                vat="23",
            )

        client.close()

        assert route.called
        assert isinstance(result, Good)
        assert result.id == 456
        assert result.name == "Updated Good"
        assert result.netto == Decimal("12.50")
