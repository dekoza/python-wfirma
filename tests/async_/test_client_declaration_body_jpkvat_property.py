"""Tests for WFirmaClient convenience declaration_body_jpkvat resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.declaration_body_jpkvat import DeclarationBodyJpkvatResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientDeclarationBodyJpkvatProperty:
    """Tests for WFirmaClient.declaration_body_jpkvat property."""

    @pytest.mark.asyncio
    async def test_declaration_body_jpkvat_property_returns_resource(self) -> None:
        """Verify client.declaration_body_jpkvat returns resource instance."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.declaration_body_jpkvat

        assert isinstance(resource, DeclarationBodyJpkvatResource)

        await client.close()

    @pytest.mark.asyncio
    async def test_declaration_body_jpkvat_property_is_cached(self) -> None:
        """Verify client.declaration_body_jpkvat caches resource instance."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.declaration_body_jpkvat
        second = client.declaration_body_jpkvat

        assert first is second

        await client.close()
