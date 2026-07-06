"""Tests for synchronous invoices resource.

These tests verify that resource wrappers call the expected endpoints and
map payloads into ``wfirma.models.invoice.Invoice``.
"""

from __future__ import annotations

import json
from decimal import Decimal

import httpx
import respx

from wfirma.models.invoice import Invoice
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.invoices import InvoicesResource


class TestInvoicesResourceGet:
    """Tests for InvoicesResource.get() method."""

    # AICOMPLETE: Sync invoices resource GET returns Invoice model - ready for review
    def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/invoices/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoices": {
                            "0": {
                                "invoice": {
                                    "id": 456,
                                    "fullnumber": "FV/1/2026",
                                    "type": "normal",
                                    "netto": "100.00",
                                    "brutto": "123.00",
                                    "currency": "PLN",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(invoice_id=456)

        client.close()

        assert route.called
        assert isinstance(result, Invoice)
        assert result.id == 456
        assert result.fullnumber == "FV/1/2026"
        assert result.netto == Decimal("100.00")


class TestInvoicesResourceFind:
    """Tests for InvoicesResource.find() method."""

    # AICOMPLETE: Sync invoices resource FIND returns list of Invoices - ready for review
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/invoices/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoices": {
                            "0": {"invoice": {"id": 100, "fullnumber": "FV/100"}},
                            "1": {"invoice": {"id": 101, "fullnumber": "FV/101"}},
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

    # AICOMPLETE: Sync invoices resource FIND handles empty result - ready for review
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/invoices/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoices": {},
                        "parameters": {"page": 1, "limit": 20, "total": 0},
                    },
                )
            )

            result = resource.find()

        client.close()

        assert route.called
        assert result == []


class TestInvoicesResourceAdd:
    """Tests for InvoicesResource.add() method."""

    # AICOMPLETE: Sync invoices resource ADD creates and returns Invoice - ready for review
    def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/add",
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
                        "invoices": {
                            "0": {
                                "invoice": {
                                    "id": 789,
                                    "fullnumber": "FV/789",
                                    "type": "normal",
                                    "netto": "10.00",
                                    "brutto": "12.30",
                                    "currency": "PLN",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.add(invoice={"type": "normal"})

        client.close()

        assert route.called
        assert result.id == 789
        assert result.fullnumber == "FV/789"


class TestInvoicesResourceEdit:
    """Tests for InvoicesResource.edit() method."""

    # AICOMPLETE: Sync invoices resource EDIT updates and returns Invoice - ready for review
    def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/edit/456",
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
                        "invoices": {
                            "0": {
                                "invoice": {
                                    "id": 456,
                                    "fullnumber": "FV/456",
                                    "type": "normal",
                                    "netto": "12.50",
                                    "brutto": "15.38",
                                    "currency": "PLN",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.edit(456, invoice={"type": "normal"})

        client.close()

        assert route.called
        assert result.id == 456
        assert result.netto == Decimal("12.50")


class TestInvoicesResourceDelete:
    """Tests for InvoicesResource.delete() method."""

    # AICOMPLETE: Sync invoices resource DELETE returns True - ready for review
    def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.delete(
                "https://api2.wfirma.pl/invoices/delete/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

            result = resource.delete(invoice_id=456)

        client.close()

        assert route.called
        assert result is True


class TestInvoicesResourceDownload:
    """Tests for InvoicesResource.download() method."""

    def test_download_calls_expected_endpoint_and_returns_bytes(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        pdf_content = b"%PDF-1.4\n%fake pdf content"

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/download/456",
                params={"company_id": "123"},
            ).mock(
                return_value=httpx.Response(
                    200,
                    content=pdf_content,
                    headers={"Content-Type": "application/pdf"},
                )
            )

            result = resource.download(invoice_id=456)

        client.close()

        assert route.called
        assert isinstance(result, bytes)
        assert result == pdf_content

    def test_download_with_parameters(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        pdf_content = b"%PDF-1.4\n%fake pdf content"

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/download/456",
                params={"company_id": "123"},
            ).mock(
                return_value=httpx.Response(
                    200,
                    content=pdf_content,
                    headers={"Content-Type": "application/pdf"},
                )
            )

            result = resource.download(
                invoice_id=456,
                parameters={"page": "all", "duplicate": "1"},
            )

        client.close()

        assert route.called
        assert result == pdf_content


class TestInvoicesResourceSend:
    """Tests for InvoicesResource.send() method."""

    def test_send_calls_expected_endpoint_and_returns_dict(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/send/456",
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
                        "invoices": {"0": {"invoice": {"id": 456}}},
                    },
                )
            )

            result = resource.send(invoice_id=456)

        client.close()

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"

    def test_send_with_parameters(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/send/456",
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
                        "invoices": {"0": {"invoice": {"id": 456}}},
                    },
                )
            )

            result = resource.send(
                invoice_id=456,
                parameters={
                    "email": "test@example.com",
                    "subject": "Invoice",
                    "body": "Please find attached",
                },
            )

        client.close()

        assert route.called
        assert result["status"]["code"] == "OK"


class TestInvoicesResourceFiscalize:
    """Tests for InvoicesResource.fiscalize() method."""

    def test_fiscalize_calls_expected_endpoint_and_returns_dict(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/invoices/fiscalize/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoices": {"0": {"invoice": {"id": 456, "fiscalized": "1"}}},
                    },
                )
            )

            result = resource.fiscalize(invoice_id=456)

        client.close()

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"


class TestInvoicesResourceUnfiscalize:
    """Tests for InvoicesResource.unfiscalize() method."""

    def test_unfiscalize_calls_expected_endpoint_and_returns_dict(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/invoices/unfiscalize/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoices": {"0": {"invoice": {"id": 456, "fiscalized": "0"}}},
                    },
                )
            )

            result = resource.unfiscalize(invoice_id=456)

        client.close()

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"


class TestSyncInvoicesFindFiltered:
    """Filtered find posts the documented numbered-object parameters body."""

    def test_find_with_conditions_posts_parameters(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            route = respx.post(
                "https://api2.wfirma.pl/invoices/find",
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
                        "invoices": {
                            "0": {"invoice": {"id": 100, "fullnumber": "FV/100"}},
                        },
                    },
                )
            )

            invoices = resource.find(
                conditions=[{"field": "description", "operator": "eq", "value": "BN:x"}],
                limit=5,
                page=2,
            )

        assert [invoice.id for invoice in invoices] == [100]
        sent = json.loads(route.calls.last.request.content)
        # Per doc.wfirma.pl: repeated JSON branches must be numbered objects.
        assert sent == {
            "invoices": {
                "parameters": {
                    "conditions": {
                        "0": {
                            "condition": {
                                "field": "description",
                                "operator": "eq",
                                "value": "BN:x",
                            }
                        }
                    },
                    "limit": 5,
                    "page": 2,
                }
            }
        }

    def test_find_without_filters_keeps_plain_get(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/invoices/find",
                params={"outputFormat": "json", "company_id": "123"},
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={"status": {"code": "OK"}, "invoices": {}},
                )
            )

            assert resource.find() == []
