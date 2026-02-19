"""Tests for async WFirmaClient.terms property."""

import pytest

from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.terms import TermsResource


@pytest.mark.asyncio
async def test_client_terms_property_returns_resource() -> None:
    """Test that client.terms returns a TermsResource instance."""
    from wfirma.async_.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="key", secret_key="secret", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    resource = client.terms

    assert isinstance(resource, TermsResource)


@pytest.mark.asyncio
async def test_client_terms_property_is_cached() -> None:
    """Test that client.terms property returns same instance on multiple calls."""
    from wfirma.async_.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="key", secret_key="secret", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    first = client.terms
    second = client.terms

    assert first is second
