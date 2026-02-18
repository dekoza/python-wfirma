"""Tests for asynchronous invoices resource.

These tests verify that resource wrappers call the expected endpoints and
map payloads into ``wfirma.models.invoice.Invoice``.
"""

from __future__ import annotations

from decimal import Decimal

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.invoices import InvoicesResource
from wfirma.models.invoice import Invoice


class TestInvoicesResourceGet:
    """Tests for async InvoicesResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async invoices resource GET returns Invoice model - ready for review
    async def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.get(invoice_id=456)

        assert route.called
        assert isinstance(result, Invoice)
        assert result.id == 456
        assert result.fullnumber == "FV/1/2026"
        assert result.netto == Decimal("100.00")


class TestInvoicesResourceFind:
    """Tests for async InvoicesResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async invoices resource FIND returns list of Invoices - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.find()

        assert route.called
        assert len(result) == 2
        assert result[0].id == 100
        assert result[1].id == 101

    @pytest.mark.asyncio
    # AICOMPLETE: Async invoices resource FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.find()

        assert route.called
        assert result == []


class TestInvoicesResourceAdd:
    """Tests for async InvoicesResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async invoices resource ADD creates and returns Invoice - ready for review
    async def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.add(invoice={"type": "normal"})

        assert route.called
        assert result.id == 789
        assert result.fullnumber == "FV/789"


class TestInvoicesResourceEdit:
    """Tests for async InvoicesResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async invoices resource EDIT updates and returns Invoice - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.edit(456, invoice={"type": "normal"})

        assert route.called
        assert result.id == 456
        assert result.netto == Decimal("12.50")


class TestInvoicesResourceDelete:
    """Tests for async InvoicesResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async invoices resource DELETE returns True - ready for review
    async def test_delete_calls_expected_endpoint_and_returns_true(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://api2.wfirma.pl/invoices/delete/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(return_value=httpx.Response(200, json={"status": {"code": "OK"}}))

                result = await resource.delete(invoice_id=456)

        assert route.called
        assert result is True


class TestInvoicesResourceDownload:
    """Tests for async InvoicesResource.download() method."""

    @pytest.mark.asyncio
    async def test_download_calls_expected_endpoint_and_returns_bytes(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        pdf_content = b"%PDF-1.4\n%fake pdf content"

        async with client:
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

                result = await resource.download(invoice_id=456)

        assert route.called
        assert isinstance(result, bytes)
        assert result == pdf_content

    @pytest.mark.asyncio
    async def test_download_with_parameters(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        pdf_content = b"%PDF-1.4\n%fake pdf content"

        async with client:
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

                result = await resource.download(
                    invoice_id=456,
                    parameters={"page": "all", "duplicate": "1"},
                )

        assert route.called
        assert result == pdf_content


class TestInvoicesResourceSend:
    """Tests for async InvoicesResource.send() method."""

    @pytest.mark.asyncio
    async def test_send_calls_expected_endpoint_and_returns_dict(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.send(invoice_id=456)

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"

    @pytest.mark.asyncio
    async def test_send_with_parameters(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.send(
                    invoice_id=456,
                    parameters={
                        "email": "test@example.com",
                        "subject": "Invoice",
                        "body": "Please find attached",
                    },
                )

        assert route.called
        assert result["status"]["code"] == "OK"


class TestInvoicesResourceFiscalize:
    """Tests for async InvoicesResource.fiscalize() method."""

    @pytest.mark.asyncio
    async def test_fiscalize_calls_expected_endpoint_and_returns_dict(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.fiscalize(invoice_id=456)

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"


class TestInvoicesResourceUnfiscalize:
    """Tests for async InvoicesResource.unfiscalize() method."""

    @pytest.mark.asyncio
    async def test_unfiscalize_calls_expected_endpoint_and_returns_dict(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InvoicesResource(client)

        async with client:
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

                result = await resource.unfiscalize(invoice_id=456)

        assert route.called
        assert isinstance(result, dict)
        assert result["status"]["code"] == "OK"
