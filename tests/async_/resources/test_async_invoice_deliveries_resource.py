"""Tests for InvoiceDeliveriesResource (asynchronous)."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.invoice_deliveries import InvoiceDeliveriesResource


@pytest.fixture
def auth():
    """Mock authentication."""
    from wfirma.async_.auth import APIKeyAuth

    return APIKeyAuth(
        access_key="test_access",
        secret_key="test_secret",
        app_key="test_app",
    )


@pytest.fixture
def client(auth):
    """Create a test client."""
    return WFirmaClient(auth=auth, company_id=1)


@pytest.fixture
def resource(client):
    """Create a test resource."""
    return InvoiceDeliveriesResource(client)


class TestInvoiceDeliveriesResourceAdd:
    """Tests for add method."""

    @pytest.mark.asyncio
    async def test_add_calls_expected_endpoint(self, resource):
        """Verify add() makes POST request to correct endpoint."""
        with respx.mock:
            respx.post(
                "https://api2.wfirma.pl/invoice_deliveries/add",
                params={
                    "outputFormat": "json",
                    "inputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 1,
                                    "invoice_id": 123,
                                    "delivery_date": "2025-02-19",
                                }
                            }
                        },
                    },
                )
            )

            payload = {
                "invoice_id": 123,
                "delivery_date": "2025-02-19",
            }
            result = await resource.add(payload)

            assert isinstance(result, dict)
            assert result["id"] == 1
            assert result["invoice_id"] == 123

    @pytest.mark.asyncio
    async def test_add_returns_extracted_payload(self, resource):
        """Verify add() returns unwrapped payload dict."""
        with respx.mock:
            respx.post(
                "https://api2.wfirma.pl/invoice_deliveries/add",
                params={
                    "outputFormat": "json",
                    "inputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 42,
                                    "invoice_id": 456,
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.add({"invoice_id": 456})

            assert result == {"id": 42, "invoice_id": 456}


class TestInvoiceDeliveriesResourceFind:
    """Tests for find method."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint(self, resource):
        """Verify find() makes GET request to correct endpoint."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/invoice_deliveries/find",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 1,
                                    "invoice_id": 123,
                                }
                            },
                            "1": {
                                "invoice_delivery": {
                                    "id": 2,
                                    "invoice_id": 124,
                                }
                            },
                        },
                    },
                )
            )

            result = await resource.find()

            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(item, dict) for item in result)

    @pytest.mark.asyncio
    async def test_find_with_params(self, resource):
        """Verify find() accepts optional parameters."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/invoice_deliveries/find",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                    "some_filter": "value",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 1,
                                    "invoice_id": 123,
                                }
                            },
                        },
                    },
                )
            )

            result = await resource.find(params={"some_filter": "value"})

            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_find_returns_empty_list_on_empty_container(self, resource):
        """Verify find() returns empty list when container is empty."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/invoice_deliveries/find",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {},
                    },
                )
            )

            result = await resource.find()

            assert result == []


class TestInvoiceDeliveriesResourceGet:
    """Tests for get method."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint(self, resource):
        """Verify get() makes GET request with ID in path."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/invoice_deliveries/get/42",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 42,
                                    "invoice_id": 789,
                                    "delivery_date": "2025-02-19",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(42)

            assert isinstance(result, dict)
            assert result["id"] == 42
            assert result["invoice_id"] == 789

    @pytest.mark.asyncio
    async def test_get_returns_extracted_payload(self, resource):
        """Verify get() returns unwrapped payload dict."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/invoice_deliveries/get/99",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 99,
                                    "invoice_id": 555,
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(99)

            assert result == {"id": 99, "invoice_id": 555}


class TestInvoiceDeliveriesResourceDelete:
    """Tests for delete method."""

    @pytest.mark.asyncio
    async def test_delete_calls_expected_endpoint(self, resource):
        """Verify delete() makes DELETE request with ID in path."""
        with respx.mock:
            respx.delete(
                "https://api2.wfirma.pl/invoice_deliveries/delete/42",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 42,
                                    "deleted": True,
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.delete(42)

            assert isinstance(result, dict)
            assert result["id"] == 42

    @pytest.mark.asyncio
    async def test_delete_returns_extracted_payload(self, resource):
        """Verify delete() returns unwrapped payload dict."""
        with respx.mock:
            respx.delete(
                "https://api2.wfirma.pl/invoice_deliveries/delete/88",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "invoice_deliveries": {
                            "0": {
                                "invoice_delivery": {
                                    "id": 88,
                                    "status": "deleted",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.delete(88)

            assert result == {"id": 88, "status": "deleted"}
