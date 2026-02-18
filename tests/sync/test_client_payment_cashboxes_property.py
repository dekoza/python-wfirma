"""Tests for WFirmaClient convenience payment_cashboxes resource property (sync)."""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.payment_cashboxes import PaymentCashboxesResource

pytestmark = pytest.mark.aicomplete


class TestWFirmaClientPaymentCashboxesProperty:
    """Tests for WFirmaClient.payment_cashboxes property."""

    # AICOMPLETE: Sync client exposes `payment_cashboxes` resource - ready for review
    def test_payment_cashboxes_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.payment_cashboxes

        assert isinstance(resource, PaymentCashboxesResource)

        client.close()

    # AICOMPLETE: Sync client caches `payment_cashboxes` resource - ready for review
    def test_payment_cashboxes_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.payment_cashboxes
        second = client.payment_cashboxes

        assert first is second

        client.close()
