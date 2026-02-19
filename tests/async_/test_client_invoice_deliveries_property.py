"""Tests for client.invoice_deliveries property (asynchronous)."""

import pytest

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


def test_invoice_deliveries_property_returns_resource_instance(client):
    """Verify client.invoice_deliveries returns InvoiceDeliveriesResource."""
    resource = client.invoice_deliveries
    assert isinstance(resource, InvoiceDeliveriesResource)


def test_invoice_deliveries_property_is_cached(client):
    """Verify client.invoice_deliveries uses caching (same instance)."""
    first = client.invoice_deliveries
    second = client.invoice_deliveries
    assert first is second
