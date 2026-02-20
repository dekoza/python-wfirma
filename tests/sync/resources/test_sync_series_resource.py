"""Tests for synchronous SeriesResource."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.client import WFirmaClient


@respx.mock
def test_add_calls_expected_endpoint(client: WFirmaClient) -> None:
    """Verify add() POSTs to /series/add with correct payload structure."""
    series_data = {
        "name": "Test Series",
        "template": "FV [numer]/[rok]",
        "initnumber": 1,
    }

    respx.post(
        "/series/add", params={"company_id": "123", "outputFormat": "json", "inputFormat": "json"}
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": {"code": "OK"},
                "series": {"0": {"series": {"id": 1, **series_data}}},
            },
        )
    )

    result = client.series.add(series=series_data)

    assert result["id"] == 1
    assert result["name"] == "Test Series"


@respx.mock
def test_find_calls_expected_endpoint(client: WFirmaClient) -> None:
    """Verify find() GETs /series/find and returns list."""
    series1 = {"id": 1, "name": "Series 1", "template": "FV [numer]/[rok]"}
    series2 = {"id": 2, "name": "Series 2", "template": "FA [numer]/[rok]"}

    respx.get("/series/find", params={"company_id": "123", "outputFormat": "json"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": {"code": "OK"},
                "series": {
                    "0": {"series": series1},
                    "1": {"series": series2},
                },
            },
        )
    )

    result = client.series.find()

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


@respx.mock
def test_find_returns_empty_list_when_container_is_empty(client: WFirmaClient) -> None:
    """Verify find() returns empty list when container is empty."""
    respx.get("/series/find", params={"company_id": "123", "outputFormat": "json"}).mock(
        return_value=httpx.Response(
            200,
            json={"status": {"code": "OK"}, "series": {}},
        )
    )

    result = client.series.find()

    assert result == []


@respx.mock
def test_get_calls_expected_endpoint(client: WFirmaClient) -> None:
    """Verify get() GETs /series/get/{id}."""
    series_data = {"id": 123, "name": "Test Series", "template": "FV [numer]/[rok]"}

    respx.get(
        "/series/get/123",
        params={"company_id": "123", "outputFormat": "json"},
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": {"code": "OK"},
                "series": {"0": {"series": series_data}},
            },
        )
    )

    result = client.series.get(123)

    assert result["id"] == 123
    assert result["name"] == "Test Series"


@respx.mock
def test_edit_calls_expected_endpoint_with_correct_path(client: WFirmaClient) -> None:
    """CRITICAL: Verify edit() PUTs to /series/edit/{id} (NOT /series/notes/)."""
    series_id = 123
    updated_data = {"name": "Updated Series"}

    respx.put(
        "/series/edit/123",
        params={"company_id": "123", "outputFormat": "json", "inputFormat": "json"},
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": {"code": "OK"},
                "series": {"0": {"series": {"id": series_id, "name": "Updated Series"}}},
            },
        )
    )

    result = client.series.edit(series_id, series=updated_data)

    assert result["id"] == series_id
    assert result["name"] == "Updated Series"


@respx.mock
def test_delete_calls_expected_endpoint_with_correct_path(client: WFirmaClient) -> None:
    """CRITICAL: Verify delete() DELETEs /series/del/{id} (NOT /series/delete/)."""
    series_id = 123

    respx.delete(
        "/series/del/123",
        params={"company_id": "123", "outputFormat": "json"},
    ).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": {"code": "OK"},
                "series": {"0": {"series": {"id": series_id}}},
            },
        )
    )

    result = client.series.delete(series_id)

    assert result["id"] == series_id


@respx.mock
def test_series_resource_returns_dict_not_raw_response(client: WFirmaClient) -> None:
    """Verify that resource methods return extracted dict, not raw response."""
    respx.get("/series/get/1", params={"company_id": "123", "outputFormat": "json"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "status": {"code": "OK"},
                "series": {"0": {"series": {"id": 1, "name": "Test"}}},
            },
        )
    )

    result = client.series.get(1)

    assert isinstance(result, dict)
    assert "status" not in result
    assert "series" not in result
    assert result["id"] == 1


@pytest.fixture
def client() -> WFirmaClient:
    """Create a test client."""
    from wfirma.sync.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="test_access", secret_key="test_secret", app_key="test_app")
    return WFirmaClient(auth=auth, company_id="123")
