"""Tests for WFirmaClient convenience declaration_body_jpkvat resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.declaration_body_jpkvat import DeclarationBodyJpkvatResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientDeclarationBodyJpkvatProperty:
    """Tests for WFirmaClient.declaration_body_jpkvat property."""

    def test_declaration_body_jpkvat_property_returns_resource(self) -> None:
        """Verify client.declaration_body_jpkvat returns resource instance."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.declaration_body_jpkvat

        assert isinstance(resource, DeclarationBodyJpkvatResource)

        client.close()

    def test_declaration_body_jpkvat_property_is_cached(self) -> None:
        """Verify client.declaration_body_jpkvat caches resource instance."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.declaration_body_jpkvat
        second = client.declaration_body_jpkvat

        assert first is second

        client.close()
