"""Tests for asynchronous SeriesResource."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.client import WFirmaClient


@respx.mock
@pytest.mark.asyncio
async def test_add_calls_expected_endpoint(async_client: WFirmaClient) -> None:
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

    result = await async_client.series.add(series=series_data)

    assert result["id"] == 1
    assert result["name"] == "Test Series"


@respx.mock
@pytest.mark.asyncio
async def test_find_calls_expected_endpoint(async_client: WFirmaClient) -> None:
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

    result = await async_client.series.find()

    assert len(result) == 2
    assert result[0]["id"] == 1
    assert result[1]["id"] == 2


@respx.mock
@pytest.mark.asyncio
async def test_find_returns_empty_list_when_container_is_empty(async_client: WFirmaClient) -> None:
    """Verify find() returns empty list when container is empty."""
    respx.get("/series/find", params={"company_id": "123", "outputFormat": "json"}).mock(
        return_value=httpx.Response(
            200,
            json={"status": {"code": "OK"}, "series": {}},
        )
    )

    result = await async_client.series.find()

    assert result == []


@respx.mock
@pytest.mark.asyncio
async def test_get_calls_expected_endpoint(async_client: WFirmaClient) -> None:
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

    result = await async_client.series.get(123)

    assert result["id"] == 123
    assert result["name"] == "Test Series"


@respx.mock
@pytest.mark.asyncio
async def test_edit_calls_expected_endpoint_with_correct_path(async_client: WFirmaClient) -> None:
    """CRITICAL: Verify edit() POSTs to /series/edit/{id} (NOT /series/notes/)."""
    series_id = 123
    updated_data = {"name": "Updated Series"}

    respx.post(
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

    result = await async_client.series.edit(series_id, series=updated_data)

    assert result["id"] == series_id
    assert result["name"] == "Updated Series"


@respx.mock
@pytest.mark.asyncio
async def test_delete_calls_expected_endpoint_with_correct_path(async_client: WFirmaClient) -> None:
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

    result = await async_client.series.delete(series_id)

    assert result["id"] == series_id


@respx.mock
@pytest.mark.asyncio
async def test_series_resource_returns_dict_not_raw_response(async_client: WFirmaClient) -> None:
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

    result = await async_client.series.get(1)

    assert isinstance(result, dict)
    assert "status" not in result
    assert "series" not in result
    assert result["id"] == 1


@pytest.fixture
async def async_client() -> WFirmaClient:
    """Create a test async client."""
    from wfirma.async_.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="test_access", secret_key="test_secret", app_key="test_app")
    async with WFirmaClient(auth=auth, company_id="123") as client:
        yield client
