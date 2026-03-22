"""Tests for synchronous webhooks resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.webhooks import WebhooksResource

pytestmark = pytest.mark.aicomplete


class TestWebhooksResourceGet:
    """Tests for WebhooksResource.get() method."""

    # AICOMPLETE: Sync webhooks resource GET returns webhook payload - ready for review
    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/webhooks/get/456",
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

            result = resource.get(webhook_id=456)

        client.close()

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "Test webhook"


class TestWebhooksResourceTrigger:
    """Tests for WebhooksResource.trigger() method."""

    # AICOMPLETE: Sync webhooks resource TRIGGER calls expected endpoint - ready for review
    def test_trigger_calls_expected_endpoint_with_get(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/webhooks/trigger/456",
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

            result = resource.trigger(webhook_id=456)

        client.close()

        assert route.called
        assert result["status"]["code"] == "OK"


class TestWebhooksResourceFind:
    """Tests for WebhooksResource.find() method."""

    # AICOMPLETE: Sync webhooks resource FIND returns list of webhooks - ready for review
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/webhooks/find",
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

            result = resource.find()

        client.close()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    # AICOMPLETE: Sync webhooks resource FIND handles empty result - ready for review
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/webhooks/find",
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

            result = resource.find()

        client.close()

        assert route.called
        assert result == []


class TestWebhooksResourceAdd:
    """Tests for WebhooksResource.add() method."""

    # AICOMPLETE: Sync webhooks resource ADD sends payload and returns webhook payload - ready for review
    def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.post(
                "https://sandbox-api2.wfirma.pl/webhooks/add",
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

            result = resource.add(name="New", url="https://example.com")

        client.close()

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "New"


class TestWebhooksResourceEdit:
    """Tests for WebhooksResource.edit() method."""

    # AICOMPLETE: Sync webhooks resource EDIT uses PATCH and returns webhook payload - ready for review
    def test_edit_calls_expected_endpoint_with_patch_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.patch(
                "https://sandbox-api2.wfirma.pl/webhooks/edit/10",
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

            result = resource.edit(webhook_id=10, name="Renamed")

        client.close()

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "Renamed"


class TestWebhooksResourceDelete:
    """Tests for WebhooksResource.delete() method."""

    # AICOMPLETE: Sync webhooks resource DELETE returns True - ready for review
    def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WebhooksResource(client)

        with respx.mock:
            route = respx.delete(
                "https://sandbox-api2.wfirma.pl/webhooks/delete/10",
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

            result = resource.delete(webhook_id=10)

        client.close()

        assert route.called
        assert result is True
