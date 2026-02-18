"""Tests for WFirmaClient convenience ledger_accountant_years resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.ledger_accountant_years import LedgerAccountantYearsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientLedgerAccountantYearsProperty:
    """Tests for WFirmaClient.ledger_accountant_years property."""

    # RED: Async client exposes ledger_accountant_years resource
    def test_ledger_accountant_years_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.ledger_accountant_years

        assert isinstance(resource, LedgerAccountantYearsResource)

        import asyncio

        asyncio.run(client.close())

    # RED: Async client caches ledger_accountant_years resource
    def test_ledger_accountant_years_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.ledger_accountant_years
        second = client.ledger_accountant_years

        assert first is second

        import asyncio

        asyncio.run(client.close())
