"""Tests for ledger_operation_schemas property on sync WFirmaClient."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.ledger_operation_schemas import LedgerOperationSchemasResource

pytestmark = pytest.mark.aicomplete


class TestClientLedgerOperationSchemasProperty:
    """Tests for WFirmaClient.ledger_operation_schemas property."""

    # RED: Client property returns LedgerOperationSchemasResource instance
    def test_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.ledger_operation_schemas

        client.close()

        assert isinstance(resource, LedgerOperationSchemasResource)

    # RED: Client property caches resource instance
    def test_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.ledger_operation_schemas
        second = client.ledger_operation_schemas

        client.close()

        assert first is second
