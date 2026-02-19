"""Tests for async WFirmaClient.notes property."""

import pytest
import respx
import httpx

from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.notes import NotesResource


@pytest.fixture
def mock_auth():
    """Mock authentication."""
    from wfirma.async_.auth import APIKeyAuth

    return APIKeyAuth(access_key="test", secret_key="test", app_key="test")


@pytest.fixture
def client(mock_auth):
    """Create async test client."""
    return WFirmaClient(auth=mock_auth, company_id=123)


def test_notes_property_returns_resource_instance(client):
    """Verify client.notes returns NotesResource instance."""
    resource = client.notes
    assert isinstance(resource, NotesResource)


def test_notes_property_is_cached(client):
    """Verify client.notes uses caching (same instance on second access)."""
    first = client.notes
    second = client.notes
    assert first is second
