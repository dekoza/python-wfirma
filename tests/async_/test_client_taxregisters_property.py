"""Tests for async client taxregisters property."""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.taxregisters import TaxregistersResource

pytestmark = pytest.mark.asyncio


async def test_returns_resource_instance() -> None:
    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    resource = client.taxregisters

    await client.close()

    assert isinstance(resource, TaxregistersResource)


async def test_is_cached() -> None:
    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
    client = WFirmaClient(auth=auth, company_id=123)

    first = client.taxregisters
    second = client.taxregisters

    await client.close()

    assert first is second
