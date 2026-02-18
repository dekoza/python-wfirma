"""Tests for WFirmaClient convenience payment_cashboxes resource property (async)."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.payment_cashboxes import PaymentCashboxesResource

pytestmark = pytest.mark.aicomplete


class TestAsyncWFirmaClientPaymentCashboxesProperty:
    """Tests for WFirmaClient.payment_cashboxes property (async)."""

    # AICOMPLETE: Async client exposes `payment_cashboxes` resource - ready for review
    def test_payment_cashboxes_property_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.payment_cashboxes

        assert isinstance(resource, PaymentCashboxesResource)

    # AICOMPLETE: Async client caches `payment_cashboxes` resource - ready for review
    def test_payment_cashboxes_property_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.payment_cashboxes
        second = client.payment_cashboxes

        assert first is second
