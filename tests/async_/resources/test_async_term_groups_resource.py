"""Tests for asynchronous term groups resource."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.term_groups import TermGroupsResource


class TestAsyncTermGroupsResourceAdd:
    """Tests for async TermGroupsResource.add() method."""

    @pytest.mark.asyncio
    async def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
        """add() should POST to /term_groups/add."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TermGroupsResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/term_groups/add",
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
                        "term_groups": {"0": {"term_group": {"id": 1, "name": "test group"}}},
                    },
                )
            )

            result = await resource.add({"name": "test group"})

        await client.close()

        assert route.called
        assert result["id"] == 1
        assert result["name"] == "test group"


class TestAsyncTermGroupsResourceFind:
    """Tests for async TermGroupsResource.find() method."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        """find() should GET /term_groups/find."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TermGroupsResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/term_groups/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "term_groups": {
                            "0": {"term_group": {"id": 1, "name": "group1"}},
                            "1": {"term_group": {"id": 2, "name": "group2"}},
                        },
                    },
                )
            )

            result = await resource.find()

        await client.close()

        assert route.called
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.asyncio
    async def test_find_returns_empty_list_when_container_empty(self) -> None:
        """find() should return empty list when container is empty."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TermGroupsResource(client)

        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/term_groups/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={"status": {"code": "OK"}, "term_groups": {}},
                )
            )

            result = await resource.find()

        await client.close()

        assert result == []


class TestAsyncTermGroupsResourceGet:
    """Tests for async TermGroupsResource.get() method."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        """get() should GET /term_groups/get/{term_group_id}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TermGroupsResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/term_groups/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "term_groups": {"0": {"term_group": {"id": 456, "name": "specific group"}}},
                    },
                )
            )

            result = await resource.get(456)

        await client.close()

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "specific group"


class TestAsyncTermGroupsResourceEdit:
    """Tests for async TermGroupsResource.edit() method."""

    @pytest.mark.asyncio
    async def test_edit_calls_expected_endpoint_with_correct_path(self) -> None:
        """edit() should POST to /term_groups/edit/{term_group_id}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TermGroupsResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/term_groups/edit/1",
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
                        "term_groups": {"0": {"term_group": {"id": 1, "name": "updated"}}},
                    },
                )
            )

            result = await resource.edit(1, {"name": "updated"})

        await client.close()

        assert route.called
        assert result["id"] == 1
        assert result["name"] == "updated"


class TestAsyncTermGroupsResourceDelete:
    """Tests for async TermGroupsResource.delete() method."""

    @pytest.mark.asyncio
    async def test_delete_calls_expected_endpoint(self) -> None:
        """delete() should DELETE /term_groups/delete/{term_group_id}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TermGroupsResource(client)

        with respx.mock:
            route = respx.delete(
                "https://api2.wfirma.pl/term_groups/delete/1",
                params={
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={"status": {"code": "OK"}},
                )
            )

            result = await resource.delete(1)

        await client.close()

        assert route.called
        assert result["status"]["code"] == "OK"
