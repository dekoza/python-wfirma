"""Tests for WFirmaClient convenience expenses resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.expenses import ExpensesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientExpensesProperty:
    """Tests for WFirmaClient.expenses property."""

    def test_expenses_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.expenses

        assert isinstance(resource, ExpensesResource)

        client.close()

    def test_expenses_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.expenses
        second = client.expenses

        assert first is second

        client.close()
