"""Tests for async TermsResource."""

from typing import Any

import pytest

from wfirma.async_.resources.terms import TermsResource


@pytest.fixture
def client_mock() -> Any:
    """Mock WFirmaClient for testing."""
    from unittest.mock import AsyncMock, Mock

    client = Mock()
    client.post_json = AsyncMock()
    client.get_json = AsyncMock()
    client.put_json = AsyncMock()
    client.delete_json = AsyncMock()
    return client


@pytest.mark.asyncio
async def test_add_calls_expected_endpoint_and_returns_dict(client_mock: Any) -> None:
    """Test add() calls POST /terms/add and returns extracted payload."""
    client_mock.post_json.return_value = {
        "status": {"code": "OK"},
        "terms": {"0": {"term": {"id": 1, "description": "Payment term A"}}},
    }

    resource = TermsResource(client_mock)
    result = await resource.add({"description": "Payment term A"})

    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["description"] == "Payment term A"
    client_mock.post_json.assert_called_once()
    call_args = client_mock.post_json.call_args
    assert call_args[0][0] == "/terms/add"
    assert call_args[1]["data"]["terms"]["0"]["term"]["description"] == "Payment term A"


@pytest.mark.asyncio
async def test_find_calls_expected_endpoint_and_returns_list(client_mock: Any) -> None:
    """Test find() calls GET /terms/find and returns list of dicts."""
    client_mock.get_json.return_value = {
        "status": {"code": "OK"},
        "terms": {
            "0": {"term": {"id": 1, "description": "Term 1"}},
            "1": {"term": {"id": 2, "description": "Term 2"}},
        },
    }

    resource = TermsResource(client_mock)
    result = await resource.find()

    assert isinstance(result, list)
    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2
    client_mock.get_json.assert_called_once_with("/terms/find", params=None)


@pytest.mark.asyncio
async def test_find_with_params(client_mock: Any) -> None:
    """Test find() passes through optional params."""
    client_mock.get_json.return_value = {
        "status": {"code": "OK"},
        "terms": {"0": {"term": {"id": 1, "description": "Term 1"}}},
    }

    resource = TermsResource(client_mock)
    await resource.find(params={"filter": "active"})

    client_mock.get_json.assert_called_once_with("/terms/find", params={"filter": "active"})


@pytest.mark.asyncio
async def test_find_returns_empty_list_when_container_is_empty(client_mock: Any) -> None:
    """Test find() returns empty list when container is empty."""
    client_mock.get_json.return_value = {"status": {"code": "OK"}, "terms": {}}

    resource = TermsResource(client_mock)
    result = await resource.find()

    assert result == []


@pytest.mark.asyncio
async def test_get_calls_expected_endpoint_and_returns_dict(client_mock: Any) -> None:
    """Test get() calls GET /terms/get/{id} and returns extracted payload."""
    client_mock.get_json.return_value = {
        "status": {"code": "OK"},
        "terms": {"0": {"term": {"id": 123, "description": "Term 123"}}},
    }

    resource = TermsResource(client_mock)
    result = await resource.get(123)

    assert isinstance(result, dict)
    assert result["id"] == 123
    assert result["description"] == "Term 123"
    client_mock.get_json.assert_called_once_with("/terms/get/123")


@pytest.mark.asyncio
async def test_edit_calls_expected_endpoint_and_returns_dict(client_mock: Any) -> None:
    """Test edit() calls POST /terms/edit/{id} and returns extracted payload."""
    client_mock.post_json.return_value = {
        "status": {"code": "OK"},
        "terms": {"0": {"term": {"id": 1, "description": "Updated Term"}}},
    }

    resource = TermsResource(client_mock)
    result = await resource.edit(1, {"description": "Updated Term"})

    assert isinstance(result, dict)
    assert result["id"] == 1
    assert result["description"] == "Updated Term"
    client_mock.post_json.assert_called_once()
    call_args = client_mock.post_json.call_args
    assert call_args[0][0] == "/terms/edit/1"
    assert call_args[1]["data"]["terms"]["0"]["term"]["description"] == "Updated Term"


@pytest.mark.asyncio
async def test_delete_calls_expected_endpoint_and_returns_dict(client_mock: Any) -> None:
    """Test delete() calls DELETE /terms/delete/{id} and returns extracted payload."""
    client_mock.delete_json.return_value = {
        "status": {"code": "OK"},
        "terms": {"0": {"term": {"id": 1, "description": "Term 1"}}},
    }

    resource = TermsResource(client_mock)
    result = await resource.delete(1)

    assert isinstance(result, dict)
    client_mock.delete_json.assert_called_once_with("/terms/delete/1")


@pytest.mark.asyncio
async def test_edit_uses_post_method(client_mock: Any) -> None:
    """Test that edit() uses POST method (API spec shows POST, not PUT)."""
    client_mock.post_json.return_value = {
        "status": {"code": "OK"},
        "terms": {"0": {"term": {"id": 1}}},
    }

    resource = TermsResource(client_mock)
    await resource.edit(1, {"description": "Updated"})

    client_mock.post_json.assert_called_once()
    assert not client_mock.put_json.called
