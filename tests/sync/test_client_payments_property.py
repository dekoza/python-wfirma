"""Tests for WFirmaClient convenience payments resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.payments import PaymentsResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientPaymentsProperty:
    """Tests for WFirmaClient.payments property."""

    # AICOMPLETE: Sync client exposes `payments` resource - ready for review
    def test_payments_property_returns_payments_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.payments

        assert isinstance(resource, PaymentsResource)

        client.close()

    # AICOMPLETE: Sync client caches `payments` resource - ready for review
    def test_payments_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.payments
        second = client.payments

        assert first is second

        client.close()
