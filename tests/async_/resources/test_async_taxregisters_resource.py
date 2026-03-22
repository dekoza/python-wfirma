"""Tests for asynchronous taxregisters resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.taxregisters import TaxregistersResource

pytestmark = pytest.mark.aicomplete


class TestTaxregistersResourceGet:
    """Tests for async TaxregistersResource.get() method."""

    # AICOMPLETE: Async taxregisters resource GET returns taxregister payload - ready for review
    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TaxregistersResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/taxregisters/get/2025/6",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "taxregisters": {
                            "0": {
                                "taxregister": {
                                    "id": 1,
                                    "year": 2025,
                                    "month": 6,
                                    "total_income": "1000.00",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(year=2025, month=6)

        await client.close()

        assert route.called
        assert result["id"] == 1
        assert result["year"] == 2025
        assert result["month"] == 6

    # AICOMPLETE: Async taxregisters resource GET with different year/month - ready for review
    @pytest.mark.asyncio
    async def test_get_with_different_year_month(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=456)
        resource = TaxregistersResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/taxregisters/get/2024/12",
                params={
                    "outputFormat": "json",
                    "company_id": "456",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "taxregisters": {
                            "0": {
                                "taxregister": {
                                    "id": 2,
                                    "year": 2024,
                                    "month": 12,
                                    "total_income": "5000.00",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(year=2024, month=12)

        await client.close()

        assert route.called
        assert result["year"] == 2024
        assert result["month"] == 12

    # AICOMPLETE: Async taxregisters resource GET handles single entry payload - ready for review
    @pytest.mark.asyncio
    async def test_get_handles_single_entry_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TaxregistersResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/taxregisters/get/2025/1",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "taxregisters": {
                            "0": {
                                "taxregister": {
                                    "id": 3,
                                    "year": 2025,
                                    "month": 1,
                                    "total_expenses": "2000.00",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(year=2025, month=1)

        await client.close()

        assert route.called
        assert isinstance(result, dict)
        assert result["id"] == 3


class TestTaxregistersResourceGetResponseFormats:
    """Tests for async TaxregistersResource.get() with various response formats."""

    # AICOMPLETE: Async taxregisters resource GET preserves payload structure - ready for review
    @pytest.mark.asyncio
    async def test_get_preserves_all_payload_fields(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TaxregistersResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/taxregisters/get/2025/3",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "taxregisters": {
                            "0": {
                                "taxregister": {
                                    "id": 100,
                                    "year": 2025,
                                    "month": 3,
                                    "total_income": "10000.00",
                                    "total_expenses": "5000.00",
                                    "net_profit": "5000.00",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(year=2025, month=3)

        await client.close()

        assert route.called
        assert result["id"] == 100
        assert result["total_income"] == "10000.00"
        assert result["total_expenses"] == "5000.00"
        assert result["net_profit"] == "5000.00"

    # AICOMPLETE: Async taxregisters resource GET with minimal payload - ready for review
    @pytest.mark.asyncio
    async def test_get_with_minimal_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = TaxregistersResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/taxregisters/get/2025/5",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "taxregisters": {
                            "0": {
                                "taxregister": {
                                    "year": 2025,
                                    "month": 5,
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(year=2025, month=5)

        await client.close()

        assert route.called
        assert result["year"] == 2025
        assert result["month"] == 5
