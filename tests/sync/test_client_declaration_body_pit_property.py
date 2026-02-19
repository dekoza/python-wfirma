"""Tests for sync WFirmaClient declaration_body_pit property."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.declaration_body_pit import DeclarationBodyPitResource


class TestClientDeclarationBodyPitProperty:
    """Test declaration_body_pit property on sync WFirmaClient."""

    @pytest.fixture
    def client(self) -> WFirmaClient:
        """Create a test client."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        return WFirmaClient(auth=auth, company_id=123)

    def test_returns_resource_instance(self, client: WFirmaClient) -> None:
        """Test that client.declaration_body_pit returns DeclarationBodyPitResource."""
        resource = client.declaration_body_pit
        assert isinstance(resource, DeclarationBodyPitResource)

    def test_is_cached(self, client: WFirmaClient) -> None:
        """Test that client.declaration_body_pit returns cached instance."""
        first = client.declaration_body_pit
        second = client.declaration_body_pit
        assert first is second
