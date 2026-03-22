"""Tests for asynchronous PW warehouse documents resource.

These tests verify that resource wrappers call the expected endpoints and
map payloads into ``wfirma.models.warehouse.WarehouseDocument``.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.warehouse_documents_pw import WarehouseDocumentPWResource
from wfirma.models.warehouse import WarehouseDocument


class TestWarehouseDocumentPWResourceGet:
    """Tests for WarehouseDocumentPWResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async warehouse_document_p_w GET returns WarehouseDocument model - ready for review
    async def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentPWResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/warehouse_document_p_w/get/53487196",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "warehouse_documents": {
                                "0": {
                                    "warehouse_document": {
                                        "id": 53487196,
                                        "fullnumber": "PW 1/2024",
                                        "date": "2024-01-15",
                                        "type": "p_w",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(warehouse_document_id=53487196)

        assert route.called
        assert isinstance(result, WarehouseDocument)
        assert result.id == 53487196
        assert result.fullnumber == "PW 1/2024"
        assert result.type is not None


class TestWarehouseDocumentPWResourceFind:
    """Tests for WarehouseDocumentPWResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async warehouse_document_p_w FIND returns list of WarehouseDocuments - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentPWResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/warehouse_document_p_w/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "warehouse_documents": {
                                "0": {"warehouse_document": {"id": 100, "fullnumber": "PW 1/2024"}},
                                "1": {"warehouse_document": {"id": 101, "fullnumber": "PW 2/2024"}},
                            },
                            "parameters": {"page": 1, "limit": 20, "total": 2},
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert len(result) == 2
        assert result[0].id == 100
        assert result[1].id == 101

    @pytest.mark.asyncio
    # AICOMPLETE: Async warehouse_document_p_w FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentPWResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/warehouse_document_p_w/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "warehouse_documents": {},
                            "parameters": {"page": 1, "limit": 20, "total": 0},
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert result == []


class TestWarehouseDocumentPWResourceAdd:
    """Tests for WarehouseDocumentPWResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async warehouse_document_p_w ADD creates and returns WarehouseDocument - ready for review
    async def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentPWResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/warehouse_document_p_w/add",
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
                            "warehouse_documents": {
                                "0": {"warehouse_document": {"id": 789, "fullnumber": "PW 3/2024"}}
                            },
                        },
                    )
                )

                result = await resource.add(
                    {"fullnumber": "PW 3/2024", "date": "2024-01-20", "type": "p_w"}
                )

        assert route.called
        assert result.id == 789
        assert result.fullnumber == "PW 3/2024"


class TestWarehouseDocumentPWResourceEdit:
    """Tests for WarehouseDocumentPWResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async warehouse_document_p_w EDIT updates and returns WarehouseDocument - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentPWResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/warehouse_document_p_w/edit/456",
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
                            "warehouse_documents": {
                                "0": {"warehouse_document": {"id": 456, "fullnumber": "PW 9/2024"}}
                            },
                        },
                    )
                )

                result = await resource.edit(456, {"fullnumber": "PW 9/2024"})

        assert route.called
        assert isinstance(result, WarehouseDocument)
        assert result.id == 456
        assert result.fullnumber == "PW 9/2024"


class TestWarehouseDocumentPWResourceDelete:
    """Tests for WarehouseDocumentPWResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async warehouse_document_p_w DELETE returns True - ready for review
    async def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentPWResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://sandbox-api2.wfirma.pl/warehouse_document_p_w/delete/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

                result = await resource.delete(warehouse_document_id=456)

        assert route.called
        assert result is True
