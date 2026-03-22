"""Tests for synchronous company resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.exceptions import InvalidConfigurationError
from wfirma.models.company import CompanyAddress, CompanyDetail
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.company import CompanyResource


class TestCompanyResource:
    """Tests for CompanyResource."""

    # AICOMPLETE: Sync company resource returns Pydantic models + default company_id - ready for review
    def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        """Should call /companies/get/{companyId} and return CompanyDetail."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = CompanyResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/companies/get/123",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "company": {"0": {"company": {"id": 123, "name": "Test Company"}}},
                    },
                )
            )

            result = resource.get()

        client.close()

        assert route.called
        assert isinstance(result, CompanyDetail)
        assert result.id == 123
        assert result.name == "Test Company"

    # AICOMPLETE: Sync company resource requires company_id when client.company_id is missing - ready for review
    def test_get_raises_configuration_error_when_company_id_missing(self) -> None:
        """Should raise when company_id isn't provided and client.company_id is None."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=None)
        resource = CompanyResource(client)

        with pytest.raises(InvalidConfigurationError, match="company_id is required"):
            resource.get()

        client.close()

    # AICOMPLETE: Sync company resource findMain returns CompanyAddress - ready for review
    def test_find_main_calls_expected_endpoint_and_returns_model(self) -> None:
        """Should call /company_addresses/findmain and return CompanyAddress."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = CompanyResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/company_addresses/findmain",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "company_addresses": {
                            "0": {
                                "company_address": {
                                    "id": 1,
                                    "street": "Main",
                                    "building_number": "1",
                                    "zip": "00-001",
                                    "city": "Warsaw",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.find_main_address()

        client.close()

        assert route.called
        assert isinstance(result, CompanyAddress)
        assert result.id == 1
        assert result.city == "Warsaw"
