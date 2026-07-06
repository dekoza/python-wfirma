"""Request-envelope tests for asynchronous write endpoints.

Mirrors ``tests/sync/resources/test_sync_write_envelopes.py``: the wFirma
API requires request bodies to nest records under the plural module branch,
numbered by key and wrapped in the singular object branch::

    {"tags": {"0": {"tag": {...}}}}
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient

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


class TestSimpleModuleEnvelopes:
    async def test_tags_add_wraps_tag_in_numbered_module_branch(self) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/tags/add").mock(
                    return_value=_ok_response("tags", "tag", {"id": 10, "name": "New"})
                )
                await client.tags.add(name="New", visibility="visible")

        assert _last_body(route) == {
            "tags": {"0": {"tag": {"name": "New", "visibility": "visible"}}}
        }

    async def test_tags_edit_wraps_tag_in_numbered_module_branch(self) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/tags/edit/10").mock(
                    return_value=_ok_response("tags", "tag", {"id": 10, "name": "Renamed"})
                )
                await client.tags.edit(tag_id=10, name="Renamed")

        assert _last_body(route) == {"tags": {"0": {"tag": {"name": "Renamed"}}}}

    async def test_notes_add_and_post_edit_use_numbered_module_branch(self) -> None:
        note = {"object_name": "invoice", "object_id": 1, "text": "Treść"}
        async with _client() as client:
            with respx.mock:
                add_route = respx.post("https://api2.wfirma.pl/notes/add").mock(
                    return_value=_ok_response("notes", "note", {"id": 5, **note})
                )
                edit_route = respx.post("https://api2.wfirma.pl/notes/edit/5").mock(
                    return_value=_ok_response("notes", "note", {"id": 5, "text": "Nowa"})
                )
                await client.notes.add(note)
                await client.notes.edit(5, {"text": "Nowa"})

        assert _last_body(add_route) == {"notes": {"0": {"note": note}}}
        assert _last_body(edit_route) == {"notes": {"0": {"note": {"text": "Nowa"}}}}

    async def test_term_groups_add_and_edit_use_numbered_module_branch(self) -> None:
        async with _client() as client:
            with respx.mock:
                add_route = respx.post("https://api2.wfirma.pl/term_groups/add").mock(
                    return_value=_ok_response("term_groups", "term_group", {"id": 7, "name": "g"})
                )
                edit_route = respx.post("https://api2.wfirma.pl/term_groups/edit/7").mock(
                    return_value=_ok_response("term_groups", "term_group", {"id": 7, "name": "g2"})
                )
                await client.term_groups.add({"name": "g"})
                await client.term_groups.edit(7, {"name": "g2"})

        assert _last_body(add_route) == {"term_groups": {"0": {"term_group": {"name": "g"}}}}
        assert _last_body(edit_route) == {"term_groups": {"0": {"term_group": {"name": "g2"}}}}

    async def test_series_add_and_post_edit_use_numbered_module_branch(self) -> None:
        series = {"name": "Seria", "type": "normal"}
        async with _client() as client:
            with respx.mock:
                add_route = respx.post("https://api2.wfirma.pl/series/add").mock(
                    return_value=_ok_response("series", "series", {"id": 3, **series})
                )
                edit_route = respx.post("https://api2.wfirma.pl/series/edit/3").mock(
                    return_value=_ok_response("series", "series", {"id": 3, "name": "S2"})
                )
                await client.series.add(series)
                await client.series.edit(3, {"name": "S2"})

        assert _last_body(add_route) == {"series": {"0": {"series": series}}}
        assert _last_body(edit_route) == {"series": {"0": {"series": {"name": "S2"}}}}

    async def test_webhooks_add_and_patch_edit_use_numbered_module_branch(self) -> None:
        webhook = {"url": "https://example.pl", "event": "invoice/add", "data_type": "xml"}
        async with _client() as client:
            with respx.mock:
                add_route = respx.post("https://api2.wfirma.pl/webhooks/add").mock(
                    return_value=_ok_response("webhooks", "webhook", {"id": 4, **webhook})
                )
                edit_route = respx.patch("https://api2.wfirma.pl/webhooks/edit/4").mock(
                    return_value=_ok_response(
                        "webhooks", "webhook", {"id": 4, "url": "https://x.pl"}
                    )
                )
                await client.webhooks.add(webhook=webhook)
                await client.webhooks.edit(4, url="https://x.pl")

        assert _last_body(add_route) == {"webhooks": {"0": {"webhook": webhook}}}
        assert _last_body(edit_route) == {"webhooks": {"0": {"webhook": {"url": "https://x.pl"}}}}

    async def test_vehicles_add_and_edit_use_numbered_module_branch(self) -> None:
        vehicle = {"name": "Aston Martin DB9", "register": "DW435457"}
        async with _client() as client:
            with respx.mock:
                add_route = respx.post("https://api2.wfirma.pl/vehicles/add").mock(
                    return_value=_ok_response("vehicles", "vehicle", {"id": 9, **vehicle})
                )
                edit_route = respx.post("https://api2.wfirma.pl/vehicles/edit/9").mock(
                    return_value=_ok_response("vehicles", "vehicle", {"id": 9, "name": "DB11"})
                )
                await client.vehicles.add(vehicle=vehicle)
                await client.vehicles.edit(9, name="DB11")

        assert _last_body(add_route) == {"vehicles": {"0": {"vehicle": vehicle}}}
        assert _last_body(edit_route) == {"vehicles": {"0": {"vehicle": {"name": "DB11"}}}}


class TestWarehouseDocumentsWriteEnvelope:
    @pytest.mark.parametrize(("accessor", "slug"), WAREHOUSE_DOCUMENT_TYPES)
    async def test_add_and_edit_use_warehouse_documents_container(
        self, accessor: str, slug: str
    ) -> None:
        document = {"date": "2021-06-30"}
        async with _client() as client:
            with respx.mock:
                add_route = respx.post(f"https://api2.wfirma.pl/{slug}/add").mock(
                    return_value=_ok_response(
                        "warehouse_documents", "warehouse_document", {"id": 1, **document}
                    )
                )
                edit_route = respx.post(f"https://api2.wfirma.pl/{slug}/edit/11").mock(
                    return_value=_ok_response(
                        "warehouse_documents", "warehouse_document", {"id": 11, **document}
                    )
                )
                await getattr(client, accessor).add(document)
                await getattr(client, accessor).edit(11, document)

        assert _last_body(add_route) == {
            "warehouse_documents": {"0": {"warehouse_document": document}}
        }
        assert _last_body(edit_route) == {
            "warehouse_documents": {"0": {"warehouse_document": document}}
        }


class TestNumberedEnvelopeForListWrappedResources:
    async def test_invoices_add_and_edit_use_numbered_branch(self) -> None:
        invoice = {"type": "normal"}
        async with _client() as client:
            with respx.mock:
                add_route = respx.post("https://api2.wfirma.pl/invoices/add").mock(
                    return_value=_ok_response("invoices", "invoice", {"id": 1, **invoice})
                )
                edit_route = respx.post("https://api2.wfirma.pl/invoices/edit/1").mock(
                    return_value=_ok_response("invoices", "invoice", {"id": 1, **invoice})
                )
                await client.invoices.add(invoice=invoice)
                await client.invoices.edit(1, invoice=invoice)

        assert _last_body(add_route) == {"invoices": {"0": {"invoice": invoice}}}
        assert _last_body(edit_route) == {"invoices": {"0": {"invoice": invoice}}}

    async def test_contractors_add_uses_numbered_branch(self) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
                    return_value=_ok_response("contractors", "contractor", {"id": 2, "name": "N"})
                )
                await client.contractors.add(name="N")

        assert _last_body(route) == {"contractors": {"0": {"contractor": {"name": "N"}}}}

    async def test_goods_add_uses_numbered_branch(self) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/goods/add").mock(
                    return_value=_ok_response("goods", "good", {"id": 3, "name": "G"})
                )
                await client.goods.add(name="G")

        body = _last_body(route)
        assert set(body) == {"goods"}
        assert set(body["goods"]) == {"0"}
        assert body["goods"]["0"]["good"]["name"] == "G"

    async def test_payments_add_uses_numbered_branch(self) -> None:
        payment = {"object_name": "invoice", "object_id": 68, "value": "100.00"}
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/payments/add").mock(
                    return_value=_ok_response("payments", "payment", {"id": 6, **payment})
                )
                await client.payments.add(payment=payment)

        assert _last_body(route) == {"payments": {"0": {"payment": payment}}}

    async def test_documents_add_uses_numbered_branch(self) -> None:
        document = {"name": "doc", "date": "2019-09-16"}
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/documents/add").mock(
                    return_value=_ok_response("documents", "document", {"id": 8, **document})
                )
                await client.documents.add(document)

        assert _last_body(route) == {"documents": {"0": {"document": document}}}

    async def test_terms_add_uses_numbered_branch(self) -> None:
        term = {"description": "termin A"}
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/terms/add").mock(
                    return_value=_ok_response("terms", "term", {"id": 9, **term})
                )
                await client.terms.add(term)

        assert _last_body(route) == {"terms": {"0": {"term": term}}}

    async def test_invoice_deliveries_add_uses_numbered_branch(self) -> None:
        delivery = {"invoice_id": 12}
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/invoice_deliveries/add").mock(
                    return_value=_ok_response(
                        "invoice_deliveries", "invoice_delivery", {"id": 13, **delivery}
                    )
                )
                await client.invoice_deliveries.add(delivery)

        assert _last_body(route) == {"invoice_deliveries": {"0": {"invoice_delivery": delivery}}}


class TestInvoiceParameterEnvelopes:
    async def test_download_builds_numbered_parameter_list(self) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/invoices/download/15").mock(
                    return_value=httpx.Response(200, content=b"%PDF-1.4")
                )
                content = await client.invoices.download(
                    15, parameters={"page": "all", "address": 0}
                )

        assert content == b"%PDF-1.4"
        assert _last_body(route) == {
            "invoices": {
                "parameters": {
                    "0": {"parameter": {"name": "page", "value": "all"}},
                    "1": {"parameter": {"name": "address", "value": 0}},
                }
            }
        }

    async def test_send_builds_numbered_parameter_list(self) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post("https://api2.wfirma.pl/invoices/send/15").mock(
                    return_value=httpx.Response(200, json={"status": {"code": "OK"}})
                )
                await client.invoices.send(15, parameters={"email": "a@b.pl"})

        assert _last_body(route) == {
            "invoices": {
                "parameters": {
                    "0": {"parameter": {"name": "email", "value": "a@b.pl"}},
                }
            }
        }


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
