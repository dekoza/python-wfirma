"""Tests for ledger_operation_schemas property on async WFirmaClient."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.ledger_operation_schemas import LedgerOperationSchemasResource

pytestmark = pytest.mark.aicomplete


class TestClientLedgerOperationSchemasProperty:
    """Tests for WFirmaClient.ledger_operation_schemas property."""

    # RED: Client property returns LedgerOperationSchemasResource instance
    @pytest.mark.asyncio
    async def test_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        async with client:
            resource = client.ledger_operation_schemas

        assert isinstance(resource, LedgerOperationSchemasResource)

    # RED: Client property caches resource instance
    @pytest.mark.asyncio
    async def test_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        async with client:
            first = client.ledger_operation_schemas
            second = client.ledger_operation_schemas

        assert first is second
