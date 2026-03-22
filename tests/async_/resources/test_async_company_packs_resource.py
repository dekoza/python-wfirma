"""Tests for asynchronous company_packs resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.company_packs import CompanyPacksResource

pytestmark = pytest.mark.aicomplete


class TestCompanyPacksResourceGet:
    """Tests for CompanyPacksResource.get() method."""

    # RED: Async company_packs resource GET returns company_pack payload
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = CompanyPacksResource(client)

            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/company_packs/get/789",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "company_packs": {
                                "0": {
                                    "company_pack": {
                                        "id": 789,
                                        "name": "Test Pack",
                                        "description": "A test pack",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(company_pack_id=789)

            assert route.called
            assert result["id"] == 789
            assert result["name"] == "Test Pack"
