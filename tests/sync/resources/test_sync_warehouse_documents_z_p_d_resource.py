"""Tests for synchronous ZPD warehouse documents resource.

These tests verify that resource wrappers call the expected endpoints and
map payloads into ``wfirma.models.warehouse.WarehouseDocument``.
"""

from __future__ import annotations

import httpx
import respx

from wfirma.models.warehouse import WarehouseDocument
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.warehouse_documents_z_p_d import WarehouseDocumentZPDResource


class TestWarehouseDocumentZPDResourceGet:
    """Tests for WarehouseDocumentZPDResource.get() method."""

    # AICOMPLETE: Sync warehouse_document_z_p_d GET returns WarehouseDocument model - ready for review
    def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentZPDResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/warehouse_document_z_p_d/get/53487196",
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
                                    "fullnumber": "ZPD 1/2024",
                                    "date": "2024-01-15",
                                    "type": "z_p_d",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(warehouse_document_id=53487196)

        client.close()

        assert route.called
        assert isinstance(result, WarehouseDocument)
        assert result.id == 53487196
        assert result.fullnumber == "ZPD 1/2024"
        assert result.type is not None


class TestWarehouseDocumentZPDResourceFind:
    """Tests for WarehouseDocumentZPDResource.find() method."""

    # AICOMPLETE: Sync warehouse_document_z_p_d FIND returns list of WarehouseDocuments - ready for review
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentZPDResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/warehouse_document_z_p_d/find",
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
                            "0": {"warehouse_document": {"id": 100, "fullnumber": "ZPD 1/2024"}},
                            "1": {"warehouse_document": {"id": 101, "fullnumber": "ZPD 2/2024"}},
                        },
                        "parameters": {"page": 1, "limit": 20, "total": 2},
                    },
                )
            )

            result = resource.find()

        client.close()

        assert route.called
        assert len(result) == 2
        assert result[0].id == 100
        assert result[1].id == 101

    # AICOMPLETE: Sync warehouse_document_z_p_d FIND handles empty result - ready for review
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentZPDResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/warehouse_document_z_p_d/find",
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

            result = resource.find()

        client.close()

        assert route.called
        assert result == []


class TestWarehouseDocumentZPDResourceAdd:
    """Tests for WarehouseDocumentZPDResource.add() method."""

    # AICOMPLETE: Sync warehouse_document_z_p_d ADD creates and returns WarehouseDocument - ready for review
    def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentZPDResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/warehouse_document_z_p_d/add",
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
                            "0": {"warehouse_document": {"id": 789, "fullnumber": "ZPD 3/2024"}}
                        },
                    },
                )
            )

            result = resource.add({"fullnumber": "ZPD 3/2024", "date": "2024-01-20", "type": "z_p_d"})

        client.close()

        assert route.called
        assert result.id == 789
        assert result.fullnumber == "ZPD 3/2024"


class TestWarehouseDocumentZPDResourceEdit:
    """Tests for WarehouseDocumentZPDResource.edit() method."""

    # AICOMPLETE: Sync warehouse_document_z_p_d EDIT updates and returns WarehouseDocument - ready for review
    def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentZPDResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/warehouse_document_z_p_d/edit/456",
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
                            "0": {"warehouse_document": {"id": 456, "fullnumber": "ZPD 9/2024"}}
                        },
                    },
                )
            )

            result = resource.edit(456, {"fullnumber": "ZPD 9/2024"})

        client.close()

        assert route.called
        assert isinstance(result, WarehouseDocument)
        assert result.id == 456
        assert result.fullnumber == "ZPD 9/2024"


class TestWarehouseDocumentZPDResourceDelete:
    """Tests for WarehouseDocumentZPDResource.delete() method."""

    # AICOMPLETE: Sync warehouse_document_z_p_d DELETE returns True - ready for review
    def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = WarehouseDocumentZPDResource(client)

        with respx.mock:
            route = respx.delete(
                "https://api2.wfirma.pl/warehouse_document_z_p_d/delete/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

            result = resource.delete(warehouse_document_id=456)

        client.close()

        assert route.called
        assert result is True
