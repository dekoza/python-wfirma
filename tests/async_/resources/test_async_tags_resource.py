"""Tests for asynchronous tags resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.tags import TagsResource

pytestmark = pytest.mark.aicomplete


class TestTagsResourceGet:
    """Tests for async TagsResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async tags resource GET returns tag payload - ready for review
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        async with client:
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

                result = await resource.get(tag_id=456)

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "Test tag"


class TestTagsResourceFind:
    """Tests for async TagsResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async tags resource FIND returns list of tags - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        async with client:
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

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.asyncio
    # AICOMPLETE: Async tags resource FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        async with client:
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

                result = await resource.find()

        assert route.called
        assert result == []


class TestTagsResourceAdd:
    """Tests for async TagsResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async tags resource ADD sends payload and returns tag payload - ready for review
    async def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        async with client:
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

                result = await resource.add(name="New", visibility="visible")

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "New"


class TestTagsResourceEdit:
    """Tests for async TagsResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async tags resource EDIT sends payload and returns tag payload - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        async with client:
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

                result = await resource.edit(tag_id=10, name="Renamed")

        assert route.called
        assert result["id"] == 10
        assert result["name"] == "Renamed"


class TestTagsResourceDelete:
    """Tests for async TagsResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async tags resource DELETE returns True - ready for review
    async def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TagsResource(client)

        async with client:
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

                result = await resource.delete(tag_id=10)

        assert route.called
        assert result is True
