"""Tests for sync NotesResource."""

import json

import httpx
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.notes import NotesResource


class TestNotesResourceAdd:
    """Tests for add() method."""

    def test_add_calls_expected_endpoint_and_returns_dict(self) -> None:
        """Verify add() calls POST /notes/add and returns dict."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            respx.post(
                "https://api2.wfirma.pl/notes/add",
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
                        "notes": {
                            "0": {
                                "note": {
                                    "id": 1,
                                    "object_name": "invoice",
                                    "object_id": 100,
                                    "text": "Test note",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.add({"object_name": "invoice", "object_id": 100, "text": "Test note"})

            assert isinstance(result, dict)
            assert result["id"] == 1
            assert result["text"] == "Test note"

    def test_add_sends_correct_payload_wrapping(self) -> None:
        """Verify add() wraps payload in {'note': {...}}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/notes/add",
                params={
                    "inputFormat": "json",
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200, json={"status": {"code": "OK"}, "notes": {"0": {"note": {"id": 1}}}}
                )
            )

            resource.add({"object_name": "invoice", "text": "Test"})

            assert route.called
            request_data = json.loads(route.calls.last.request.content)
            assert "note" in request_data
            assert request_data["note"]["object_name"] == "invoice"


class TestNotesResourceFind:
    """Tests for find() method."""

    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        """Verify find() calls GET /notes/find and returns list."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/notes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "notes": {
                            "0": {"note": {"id": 1, "text": "Note 1"}},
                            "1": {"note": {"id": 2, "text": "Note 2"}},
                        },
                    },
                )
            )

            result = resource.find()

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2

    def test_find_returns_empty_list_when_container_is_empty(self) -> None:
        """Verify find() returns [] when container is empty."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/notes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}, "notes": {}}))

            result = resource.find()

            assert result == []

    def test_find_with_params(self) -> None:
        """Verify find() passes optional params to request."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            route = respx.get("https://api2.wfirma.pl/notes/find").mock(
                return_value=httpx.Response(200, json={"status": {"code": "OK"}, "notes": {}})
            )

            resource.find(params={"filter": "value"})

            assert route.called
            assert "filter=value" in str(route.calls.last.request.url)


class TestNotesResourceGet:
    """Tests for get() method."""

    def test_get_calls_expected_endpoint_and_returns_dict(self) -> None:
        """Verify get() calls GET /notes/get/{id} and returns dict."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/notes/get/123",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "notes": {"0": {"note": {"id": 123, "text": "Test note"}}},
                    },
                )
            )

            result = resource.get(123)

            assert isinstance(result, dict)
            assert result["id"] == 123
            assert result["text"] == "Test note"


class TestNotesResourceEdit:
    """Tests for edit() method."""

    def test_edit_calls_expected_endpoint_and_returns_dict(self) -> None:
        """Verify edit() calls PUT /notes/edit/{id} and returns dict."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            respx.put(
                "https://api2.wfirma.pl/notes/edit/123",
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
                        "notes": {"0": {"note": {"id": 123, "text": "Updated note"}}},
                    },
                )
            )

            result = resource.edit(123, {"text": "Updated note"})

            assert isinstance(result, dict)
            assert result["id"] == 123
            assert result["text"] == "Updated note"

    def test_edit_uses_correct_url_not_goods_notes(self) -> None:
        """CRITICAL: Verify edit() uses /notes/edit/{id} NOT /goods/notes/{id}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            route = respx.put(
                "https://api2.wfirma.pl/notes/edit/123",
                params={
                    "inputFormat": "json",
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200, json={"status": {"code": "OK"}, "notes": {"0": {"note": {"id": 123}}}}
                )
            )

            respx.put("https://api2.wfirma.pl/goods/notes/123").mock(
                side_effect=Exception("Wrong endpoint!")
            )

            resource.edit(123, {"text": "Updated"})

            assert route.called

    def test_edit_sends_correct_payload_wrapping(self) -> None:
        """Verify edit() wraps payload in {'note': {...}}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            route = respx.put(
                "https://api2.wfirma.pl/notes/edit/123",
                params={
                    "inputFormat": "json",
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200, json={"status": {"code": "OK"}, "notes": {"0": {"note": {"id": 123}}}}
                )
            )

            resource.edit(123, {"text": "Updated"})

            assert route.called
            request_data = json.loads(route.calls.last.request.content)
            assert "note" in request_data
            assert request_data["note"]["text"] == "Updated"


class TestNotesResourceDelete:
    """Tests for delete() method."""

    def test_delete_calls_expected_endpoint_and_returns_dict(self) -> None:
        """Verify delete() calls DELETE /notes/delete/{id} and returns dict."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = NotesResource(client)

        with respx.mock:
            respx.delete(
                "https://api2.wfirma.pl/notes/delete/123",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

            result = resource.delete(123)

            assert isinstance(result, dict)
