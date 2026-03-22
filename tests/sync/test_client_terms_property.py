"""Tests for WFirmaClient.terms property."""

from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.terms import TermsResource


def test_client_terms_property_returns_resource() -> None:
    """Test that client.terms returns a TermsResource instance."""
    from wfirma.sync.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="key", secret_key="secret", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    resource = client.terms

    assert isinstance(resource, TermsResource)


def test_client_terms_property_is_cached() -> None:
    """Test that client.terms property returns same instance on multiple calls."""
    from wfirma.sync.auth import APIKeyAuth

    auth = APIKeyAuth(access_key="key", secret_key="secret", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    first = client.terms
    second = client.terms

    assert first is second
