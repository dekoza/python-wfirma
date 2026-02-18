"""Tests for WFirmaClient convenience expenses resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.expenses import ExpensesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientExpensesProperty:
    """Tests for WFirmaClient.expenses property."""

    def test_expenses_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.expenses

        assert isinstance(resource, ExpensesResource)

    def test_expenses_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.expenses
        second = client.expenses

        assert first is second
