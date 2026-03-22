"""Tests for async NotesResource."""

import json

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.notes import NotesResource


@pytest.fixture
def mock_auth():
    """Mock authentication."""
    return APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")


@pytest.fixture
def client(mock_auth):
    """Create async test client."""
    return WFirmaClient(auth=mock_auth, company_id=123)


@pytest.fixture
def resource(client):
    """Create NotesResource instance."""
    return NotesResource(client)


class TestNotesResourceAdd:
    """Tests for add() method."""

    @pytest.mark.asyncio
    async def test_add_calls_expected_endpoint_and_returns_dict(self, resource):
        """Verify add() calls POST /notes/add and returns dict."""
        with respx.mock:
            respx.post(
                "https://sandbox-api2.wfirma.pl/notes/add",
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

            result = await resource.add(
                {"object_name": "invoice", "object_id": 100, "text": "Test note"}
            )

            assert isinstance(result, dict)
            assert result["id"] == 1
            assert result["text"] == "Test note"

    @pytest.mark.asyncio
    async def test_add_sends_correct_payload_wrapping(self, resource):
        """Verify add() wraps payload in {'note': {...}}."""
        with respx.mock:
            route = respx.post(
                "https://sandbox-api2.wfirma.pl/notes/add",
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

            await resource.add({"object_name": "invoice", "text": "Test"})

            assert route.called
            request_data = json.loads(route.calls.last.request.content)
            assert "note" in request_data
            assert request_data["note"]["object_name"] == "invoice"


class TestNotesResourceFind:
    """Tests for find() method."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self, resource):
        """Verify find() calls GET /notes/find and returns list."""
        with respx.mock:
            respx.get(
                "https://sandbox-api2.wfirma.pl/notes/find",
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

            result = await resource.find()

            assert isinstance(result, list)
            assert len(result) == 2
            assert result[0]["id"] == 1
            assert result[1]["id"] == 2

    @pytest.mark.asyncio
    async def test_find_returns_empty_list_when_container_is_empty(self, resource):
        """Verify find() returns [] when container is empty."""
        with respx.mock:
            respx.get(
                "https://sandbox-api2.wfirma.pl/notes/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}, "notes": {}}))

            result = await resource.find()

            assert result == []

    @pytest.mark.asyncio
    async def test_find_with_params(self, resource):
        """Verify find() passes optional params to request."""
        with respx.mock:
            route = respx.get("https://sandbox-api2.wfirma.pl/notes/find").mock(
                return_value=httpx.Response(200, json={"status": {"code": "OK"}, "notes": {}})
            )

            await resource.find(params={"filter": "value"})

            assert route.called
            assert "filter=value" in str(route.calls.last.request.url)


class TestNotesResourceGet:
    """Tests for get() method."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_dict(self, resource):
        """Verify get() calls GET /notes/get/{id} and returns dict."""
        with respx.mock:
            respx.get(
                "https://sandbox-api2.wfirma.pl/notes/get/123",
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

            result = await resource.get(123)

            assert isinstance(result, dict)
            assert result["id"] == 123
            assert result["text"] == "Test note"


class TestNotesResourceEdit:
    """Tests for edit() method."""

    @pytest.mark.asyncio
    async def test_edit_calls_expected_endpoint_and_returns_dict(self, resource):
        """Verify edit() calls PUT /notes/edit/{id} and returns dict."""
        with respx.mock:
            respx.put(
                "https://sandbox-api2.wfirma.pl/notes/edit/123",
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

            result = await resource.edit(123, {"text": "Updated note"})

            assert isinstance(result, dict)
            assert result["id"] == 123
            assert result["text"] == "Updated note"

    @pytest.mark.asyncio
    async def test_edit_uses_correct_url_not_goods_notes(self, resource):
        """CRITICAL: Verify edit() uses /notes/edit/{id} NOT /goods/notes/{id}."""
        with respx.mock:
            route = respx.put(
                "https://sandbox-api2.wfirma.pl/notes/edit/123",
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

            respx.put("https://sandbox-api2.wfirma.pl/goods/notes/123").mock(
                side_effect=Exception("Wrong endpoint!")
            )

            await resource.edit(123, {"text": "Updated"})

            assert route.called

    @pytest.mark.asyncio
    async def test_edit_sends_correct_payload_wrapping(self, resource):
        """Verify edit() wraps payload in {'note': {...}}."""
        with respx.mock:
            route = respx.put(
                "https://sandbox-api2.wfirma.pl/notes/edit/123",
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

            await resource.edit(123, {"text": "Updated"})

            assert route.called
            request_data = json.loads(route.calls.last.request.content)
            assert "note" in request_data
            assert request_data["note"]["text"] == "Updated"


class TestNotesResourceDelete:
    """Tests for delete() method."""

    @pytest.mark.asyncio
    async def test_delete_calls_expected_endpoint_and_returns_dict(self, resource):
        """Verify delete() calls DELETE /notes/delete/{id} and returns dict."""
        with respx.mock:
            respx.delete(
                "https://sandbox-api2.wfirma.pl/notes/delete/123",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

            result = await resource.delete(123)

            assert isinstance(result, dict)
