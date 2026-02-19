"""Tests for synchronous term groups resource."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.term_groups import TermGroupsResource


class TestTermGroupsResourceAdd:
    """Tests for TermGroupsResource.add() method."""

    def test_add_calls_expected_endpoint_and_returns_payload(self) -> None:
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

            result = resource.add({"name": "test group"})

        client.close()

        assert route.called
        assert result["id"] == 1
        assert result["name"] == "test group"


class TestTermGroupsResourceFind:
    """Tests for TermGroupsResource.find() method."""

    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
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

            result = resource.find()

        client.close()

        assert route.called
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    def test_find_returns_empty_list_when_container_empty(self) -> None:
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

            result = resource.find()

        client.close()

        assert result == []


class TestTermGroupsResourceGet:
    """Tests for TermGroupsResource.get() method."""

    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
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

            result = resource.get(456)

        client.close()

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "specific group"


class TestTermGroupsResourceEdit:
    """Tests for TermGroupsResource.edit() method."""

    def test_edit_calls_expected_endpoint_with_correct_path(self) -> None:
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

            result = resource.edit(1, {"name": "updated"})

        client.close()

        assert route.called
        assert result["id"] == 1
        assert result["name"] == "updated"


class TestTermGroupsResourceDelete:
    """Tests for TermGroupsResource.delete() method."""

    def test_delete_calls_expected_endpoint(self) -> None:
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

            result = resource.delete(1)

        client.close()

        assert route.called
        assert result["status"]["code"] == "OK"
