"""Tests for asynchronous webhooks resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.webhooks import WebhooksResource

pytestmark = pytest.mark.aicomplete


class TestWebhooksResourceGet:
    """Tests for async WebhooksResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async webhooks resource GET returns webhook payload - ready for review
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/webhooks/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "webhooks": {
                                "0": {
                                    "webhook": {
                                        "id": 456,
                                        "name": "Test webhook",
                                        "url": "https://example.com",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(webhook_id=456)

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "Test webhook"


class TestWebhooksResourceTrigger:
    """Tests for async WebhooksResource.trigger() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async webhooks resource TRIGGER calls expected endpoint with GET - ready for review
    async def test_trigger_calls_expected_endpoint_with_get(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/webhooks/trigger/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "result": "triggered",
                        },
                    )
                )

                result = await resource.trigger(webhook_id=456)

        assert route.called
        assert result["status"]["code"] == "OK"


class TestWebhooksResourceFind:
    """Tests for async WebhooksResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async webhooks resource FIND returns list of webhooks - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/webhooks/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "webhooks": {
                                "0": {"webhook": {"id": 1, "name": "A"}},
                                "1": {"webhook": {"id": 2, "name": "B"}},
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
    # AICOMPLETE: Async webhooks resource FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/webhooks/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "webhooks": {},
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


class TestWebhooksResourceAdd:
    """Tests for async WebhooksResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async webhooks resource ADD sends payload and returns webhook payload - ready for review
    async def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://api2.wfirma.pl/webhooks/add",
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
                            "webhooks": {
                                "0": {
                                    "webhook": {
                                        "id": 10,
                                        "name": "New",
                                        "url": "https://example.com",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.add(name="New", url="https://example.com")

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "New"


class TestWebhooksResourceEdit:
    """Tests for async WebhooksResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async webhooks resource EDIT uses PATCH and returns webhook payload - ready for review
    async def test_edit_calls_expected_endpoint_with_patch_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.patch(
                    "https://api2.wfirma.pl/webhooks/edit/10",
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
                            "webhooks": {
                                "0": {
                                    "webhook": {
                                        "id": 10,
                                        "name": "Renamed",
                                        "url": "https://example.com",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.edit(webhook_id=10, name="Renamed")

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "Renamed"


class TestWebhooksResourceDelete:
    """Tests for async WebhooksResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async webhooks resource DELETE returns True - ready for review
    async def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://api2.wfirma.pl/webhooks/delete/10",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                        },
                    )
                )

                result = await resource.delete(webhook_id=10)

        assert route.called
        assert result is True
