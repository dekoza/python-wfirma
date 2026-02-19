"""Tests for sync client taxregisters property."""

from __future__ import annotations

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.taxregisters import TaxregistersResource


def test_returns_resource_instance() -> None:
    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    resource = client.taxregisters

    client.close()

    assert isinstance(resource, TaxregistersResource)


def test_is_cached() -> None:
    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    first = client.taxregisters
    second = client.taxregisters

    client.close()

    assert first is second
