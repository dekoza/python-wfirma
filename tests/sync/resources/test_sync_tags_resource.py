"""Tests for synchronous tags resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.tags import TagsResource

pytestmark = pytest.mark.aicomplete


class TestTagsResourceGet:
    """Tests for TagsResource.get() method."""

    # AICOMPLETE: Sync tags resource GET returns tag payload - ready for review
    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/tags/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "tags": {
                            "0": {
                                "tag": {
                                    "id": 456,
                                    "name": "Test tag",
                                    "visibility": "visible",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(tag_id=456)

        client.close()

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "Test tag"


class TestTagsResourceFind:
    """Tests for TagsResource.find() method."""

    # AICOMPLETE: Sync tags resource FIND returns list of tags - ready for review
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/tags/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "tags": {
                            "0": {"tag": {"id": 1, "name": "A"}},
                            "1": {"tag": {"id": 2, "name": "B"}},
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

    # AICOMPLETE: Sync tags resource FIND handles empty result - ready for review
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/tags/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "tags": {},
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


class TestTagsResourceAdd:
    """Tests for TagsResource.add() method."""

    # AICOMPLETE: Sync tags resource ADD sends payload and returns tag payload - ready for review
    def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        with respx.mock:
            route = respx.post(
                "https://sandbox-api2.wfirma.pl/tags/add",
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
                        "tags": {
                            "0": {
                                "tag": {
                                    "id": 10,
                                    "name": "New",
                                    "visibility": "visible",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.add(name="New", visibility="visible")

        client.close()

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "New"


class TestTagsResourceEdit:
    """Tests for TagsResource.edit() method."""

    # AICOMPLETE: Sync tags resource EDIT sends payload and returns tag payload - ready for review
    def test_edit_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        with respx.mock:
            route = respx.post(
                "https://sandbox-api2.wfirma.pl/tags/edit/10",
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
                        "tags": {
                            "0": {
                                "tag": {
                                    "id": 10,
                                    "name": "Renamed",
                                    "visibility": "visible",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.edit(tag_id=10, name="Renamed")

        client.close()

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "Renamed"


class TestTagsResourceDelete:
    """Tests for TagsResource.delete() method."""

    # AICOMPLETE: Sync tags resource DELETE returns True - ready for review
    def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        with respx.mock:
            route = respx.delete(
                "https://sandbox-api2.wfirma.pl/tags/delete/10",
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

            result = resource.delete(tag_id=10)

        client.close()

        assert route.called
        assert result is True
