"""Request-envelope tests for synchronous write endpoints.

The wFirma API ("Format wymiany danych", doc.wfirma.pl) requires every
request body to nest records under the plural module branch, with each
record numbered by key (even when there is only one) and wrapped in the
singular object branch:

    {"tags": {"0": {"tag": {...}}}}

These tests assert the exact JSON body sent on the wire, because a bare
object (``{"tag": {...}}``) is silently ignored or rejected by the API.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient

WAREHOUSE_DOCUMENT_TYPES = [
    ("warehouse_documents_pw", "warehouse_document_p_w"),
    ("warehouse_documents_pz", "warehouse_document_p_z"),
    ("warehouse_documents_r", "warehouse_document_r"),
    ("warehouse_documents_rw", "warehouse_document_r_w"),
    ("warehouse_documents_wz", "warehouse_document_w_z"),
    ("warehouse_documents_zd", "warehouse_document_z_d"),
    ("warehouse_documents_zpd", "warehouse_document_z_p_d"),
    ("warehouse_documents_zpm", "warehouse_document_z_p_m"),
]


def _client() -> WFirmaClient:
    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
    return WFirmaClient(auth=auth, company_id=123)


def _ok_response(container: str, object_key: str, obj: dict[str, Any]) -> httpx.Response:
    return httpx.Response(
        200,
        json={
            "status": {"code": "OK"},
            container: {"0": {object_key: obj}},
        },
    )


def _last_body(route: respx.Route) -> dict[str, Any]:
    body = json.loads(route.calls.last.request.content)
    assert isinstance(body, dict)
    return body


class TestTagsWriteEnvelope:
    def test_add_wraps_tag_in_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/tags/add").mock(
                return_value=_ok_response("tags", "tag", {"id": 10, "name": "New"})
            )
            client.tags.add(name="New", visibility="visible")
        client.close()

        assert _last_body(route) == {
            "tags": {"0": {"tag": {"name": "New", "visibility": "visible"}}}
        }

    def test_add_accepts_full_payload_dict(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/tags/add").mock(
                return_value=_ok_response("tags", "tag", {"id": 10, "name": "New"})
            )
            client.tags.add(tag={"name": "New", "color_background": "ec7000", "invoice": 1})
        client.close()

        assert _last_body(route) == {
            "tags": {"0": {"tag": {"name": "New", "color_background": "ec7000", "invoice": 1}}}
        }

    def test_edit_wraps_tag_in_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/tags/edit/10").mock(
                return_value=_ok_response("tags", "tag", {"id": 10, "name": "Renamed"})
            )
            client.tags.edit(tag_id=10, name="Renamed")
        client.close()

        assert _last_body(route) == {"tags": {"0": {"tag": {"name": "Renamed"}}}}


class TestNotesWriteEnvelope:
    def test_add_wraps_note_in_numbered_module_branch(self) -> None:
        client = _client()
        note = {"object_name": "invoice", "object_id": 1, "text": "Treść"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/notes/add").mock(
                return_value=_ok_response("notes", "note", {"id": 5, **note})
            )
            client.notes.add(note)
        client.close()

        assert _last_body(route) == {"notes": {"0": {"note": note}}}

    def test_edit_uses_post_with_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/notes/edit/5").mock(
                return_value=_ok_response("notes", "note", {"id": 5, "text": "Nowa"})
            )
            client.notes.edit(5, {"text": "Nowa"})
        client.close()

        assert route.called
        assert _last_body(route) == {"notes": {"0": {"note": {"text": "Nowa"}}}}


class TestTermGroupsWriteEnvelope:
    def test_add_wraps_term_group_in_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/term_groups/add").mock(
                return_value=_ok_response("term_groups", "term_group", {"id": 7, "name": "g"})
            )
            client.term_groups.add({"name": "g", "is_readonly": 1})
        client.close()

        assert _last_body(route) == {
            "term_groups": {"0": {"term_group": {"name": "g", "is_readonly": 1}}}
        }

    def test_edit_wraps_term_group_in_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/term_groups/edit/7").mock(
                return_value=_ok_response("term_groups", "term_group", {"id": 7, "name": "g2"})
            )
            client.term_groups.edit(7, {"name": "g2"})
        client.close()

        assert _last_body(route) == {"term_groups": {"0": {"term_group": {"name": "g2"}}}}


class TestSeriesWriteEnvelope:
    def test_add_wraps_series_in_numbered_module_branch(self) -> None:
        client = _client()
        series = {"name": "Seria", "template": "FV [numer]/[rok]", "type": "normal"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/series/add").mock(
                return_value=_ok_response("series", "series", {"id": 3, **series})
            )
            client.series.add(series)
        client.close()

        assert _last_body(route) == {"series": {"0": {"series": series}}}

    def test_edit_uses_post_with_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/series/edit/3").mock(
                return_value=_ok_response("series", "series", {"id": 3, "name": "S2"})
            )
            client.series.edit(3, {"name": "S2"})
        client.close()

        assert route.called
        assert _last_body(route) == {"series": {"0": {"series": {"name": "S2"}}}}


class TestWebhooksWriteEnvelope:
    def test_add_wraps_webhook_in_numbered_module_branch(self) -> None:
        client = _client()
        webhook = {"url": "https://example.pl", "event": "invoice/add", "data_type": "xml"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/webhooks/add").mock(
                return_value=_ok_response("webhooks", "webhook", {"id": 4, **webhook})
            )
            client.webhooks.add(webhook=webhook)
        client.close()

        assert _last_body(route) == {"webhooks": {"0": {"webhook": webhook}}}

    def test_edit_uses_patch_with_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.patch("https://api2.wfirma.pl/webhooks/edit/4").mock(
                return_value=_ok_response("webhooks", "webhook", {"id": 4, "url": "https://x.pl"})
            )
            client.webhooks.edit(4, url="https://x.pl")
        client.close()

        assert _last_body(route) == {"webhooks": {"0": {"webhook": {"url": "https://x.pl"}}}}


class TestVehiclesWriteEnvelope:
    def test_add_wraps_vehicle_in_numbered_module_branch(self) -> None:
        client = _client()
        vehicle = {"name": "Aston Martin DB9", "register": "DW435457", "type": "car"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/vehicles/add").mock(
                return_value=_ok_response("vehicles", "vehicle", {"id": 9, **vehicle})
            )
            client.vehicles.add(vehicle=vehicle)
        client.close()

        assert _last_body(route) == {"vehicles": {"0": {"vehicle": vehicle}}}

    def test_edit_wraps_vehicle_in_numbered_module_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/vehicles/edit/9").mock(
                return_value=_ok_response("vehicles", "vehicle", {"id": 9, "name": "DB11"})
            )
            client.vehicles.edit(9, name="DB11")
        client.close()

        assert _last_body(route) == {"vehicles": {"0": {"vehicle": {"name": "DB11"}}}}


class TestWarehouseDocumentsWriteEnvelope:
    @pytest.mark.parametrize(("accessor", "slug"), WAREHOUSE_DOCUMENT_TYPES)
    def test_add_uses_warehouse_documents_container(self, accessor: str, slug: str) -> None:
        client = _client()
        document = {"date": "2021-06-30"}
        with respx.mock:
            route = respx.post(f"https://api2.wfirma.pl/{slug}/add").mock(
                return_value=_ok_response(
                    "warehouse_documents", "warehouse_document", {"id": 1, **document}
                )
            )
            getattr(client, accessor).add(document)
        client.close()

        assert _last_body(route) == {"warehouse_documents": {"0": {"warehouse_document": document}}}

    @pytest.mark.parametrize(("accessor", "slug"), WAREHOUSE_DOCUMENT_TYPES)
    def test_edit_uses_warehouse_documents_container(self, accessor: str, slug: str) -> None:
        client = _client()
        document = {"date": "2021-07-01"}
        with respx.mock:
            route = respx.post(f"https://api2.wfirma.pl/{slug}/edit/11").mock(
                return_value=_ok_response(
                    "warehouse_documents", "warehouse_document", {"id": 11, **document}
                )
            )
            getattr(client, accessor).edit(11, document)
        client.close()

        assert _last_body(route) == {"warehouse_documents": {"0": {"warehouse_document": document}}}


class TestNumberedEnvelopeForListWrappedResources:
    """Resources that previously used JSON arrays must emit numbered branches."""

    def test_invoices_add_uses_numbered_branch(self) -> None:
        client = _client()
        invoice = {"type": "normal"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/invoices/add").mock(
                return_value=_ok_response("invoices", "invoice", {"id": 1, **invoice})
            )
            client.invoices.add(invoice=invoice)
        client.close()

        assert _last_body(route) == {"invoices": {"0": {"invoice": invoice}}}

    def test_invoices_edit_uses_numbered_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/invoices/edit/1").mock(
                return_value=_ok_response("invoices", "invoice", {"id": 1, "type": "normal"})
            )
            client.invoices.edit(1, invoice={"type": "normal"})
        client.close()

        assert _last_body(route) == {"invoices": {"0": {"invoice": {"type": "normal"}}}}

    def test_contractors_add_uses_numbered_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
                return_value=_ok_response("contractors", "contractor", {"id": 2, "name": "N"})
            )
            client.contractors.add(name="N")
        client.close()

        assert _last_body(route) == {"contractors": {"0": {"contractor": {"name": "N"}}}}

    def test_goods_add_uses_numbered_branch(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/goods/add").mock(
                return_value=_ok_response("goods", "good", {"id": 3, "name": "G"})
            )
            client.goods.add(name="G")
        client.close()

        body = _last_body(route)
        assert set(body) == {"goods"}
        assert set(body["goods"]) == {"0"}
        assert body["goods"]["0"]["good"]["name"] == "G"

    def test_payments_add_uses_numbered_branch(self) -> None:
        client = _client()
        payment = {"object_name": "invoice", "object_id": 68, "value": "100.00"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/payments/add").mock(
                return_value=_ok_response("payments", "payment", {"id": 6, **payment})
            )
            client.payments.add(payment=payment)
        client.close()

        assert _last_body(route) == {"payments": {"0": {"payment": payment}}}

    def test_documents_add_uses_numbered_branch(self) -> None:
        client = _client()
        document = {"name": "doc", "date": "2019-09-16"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/documents/add").mock(
                return_value=_ok_response("documents", "document", {"id": 8, **document})
            )
            client.documents.add(document)
        client.close()

        assert _last_body(route) == {"documents": {"0": {"document": document}}}

    def test_terms_add_uses_numbered_branch(self) -> None:
        client = _client()
        term = {"description": "termin A", "date": "2020-08-04"}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/terms/add").mock(
                return_value=_ok_response("terms", "term", {"id": 9, **term})
            )
            client.terms.add(term)
        client.close()

        assert _last_body(route) == {"terms": {"0": {"term": term}}}

    def test_invoice_deliveries_add_uses_numbered_branch(self) -> None:
        client = _client()
        delivery = {"invoice_id": 12}
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/invoice_deliveries/add").mock(
                return_value=_ok_response(
                    "invoice_deliveries", "invoice_delivery", {"id": 13, **delivery}
                )
            )
            client.invoice_deliveries.add(delivery)
        client.close()

        assert _last_body(route) == {"invoice_deliveries": {"0": {"invoice_delivery": delivery}}}


class TestInvoiceParameterEnvelopes:
    """Download/send take name/value parameter lists directly under the module branch."""

    def test_download_builds_numbered_parameter_list(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/invoices/download/15").mock(
                return_value=httpx.Response(200, content=b"%PDF-1.4")
            )
            content = client.invoices.download(15, parameters={"page": "all", "address": 0})
        client.close()

        assert content == b"%PDF-1.4"
        assert _last_body(route) == {
            "invoices": {
                "parameters": {
                    "0": {"parameter": {"name": "page", "value": "all"}},
                    "1": {"parameter": {"name": "address", "value": 0}},
                }
            }
        }

    def test_send_builds_numbered_parameter_list(self) -> None:
        client = _client()
        with respx.mock:
            route = respx.post("https://api2.wfirma.pl/invoices/send/15").mock(
                return_value=httpx.Response(200, json={"status": {"code": "OK"}})
            )
            client.invoices.send(15, parameters={"email": "a@b.pl"})
        client.close()

        assert _last_body(route) == {
            "invoices": {
                "parameters": {
                    "0": {"parameter": {"name": "email", "value": "a@b.pl"}},
                }
            }
        }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
