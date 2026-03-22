"""Tests for synchronous ledger_accountant_years resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.ledger_accountant_years import LedgerAccountantYearsResource

pytestmark = pytest.mark.aicomplete


class TestLedgerAccountantYearsResourceGet:
    """Tests for LedgerAccountantYearsResource.get() method."""

    # RED: Sync ledger_accountant_years resource GET returns ledger_accountant_year payload
    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = LedgerAccountantYearsResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/ledger_accountant_years/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "ledger_accountant_years": {
                            "0": {
                                "ledger_accountant_year": {
                                    "id": 456,
                                    "year": 2024,
                                    "is_active": 1,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(ledger_accountant_year_id=456)

        client.close()

        assert route.called
        assert result["id"] == 456
        assert result["year"] == 2024


class TestLedgerAccountantYearsResourceFind:
    """Tests for LedgerAccountantYearsResource.find() method."""

    # RED: Sync ledger_accountant_years resource FIND returns list of ledger_accountant_years
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = LedgerAccountantYearsResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/ledger_accountant_years/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "ledger_accountant_years": {
                            "0": {
                                "ledger_accountant_year": {
                                    "id": 1,
                                    "year": 2023,
                                }
                            },
                            "1": {
                                "ledger_accountant_year": {
                                    "id": 2,
                                    "year": 2024,
                                }
                            },
                        },
                        "parameters": {
                            "page": 1,
                            "limit": 20,
                            "total": 2,
                        },
                    },
                )
            )

            result = resource.find()

        client.close()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    # RED: Sync ledger_accountant_years resource FIND handles empty result
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = LedgerAccountantYearsResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/ledger_accountant_years/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "ledger_accountant_years": {},
                        "parameters": {
                            "page": 1,
                            "limit": 20,
                            "total": 0,
                        },
                    },
                )
            )

            result = resource.find()

        client.close()

        assert route.called
        assert result == []
