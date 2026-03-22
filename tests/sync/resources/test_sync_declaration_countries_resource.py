"""Tests for synchronous declaration_countries resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.declaration_countries import DeclarationCountriesResource

pytestmark = pytest.mark.aicomplete


class TestDeclarationCountriesResourceGet:
    """Tests for DeclarationCountriesResource.get() method."""

    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationCountriesResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_countries/get/456",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_countries": {
                            "0": {
                                "declaration_country": {
                                    "id": 456,
                                    "name": "PL",
                                    "code": "PL",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(declaration_country_id=456)

        client.close()

        assert route.called
        assert result["id"] == 456
        assert result["name"] == "PL"


class TestDeclarationCountriesResourceFind:
    """Tests for DeclarationCountriesResource.find() method."""

    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationCountriesResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_countries/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_countries": {
                            "0": {
                                "declaration_country": {
                                    "id": 1,
                                    "name": "PL",
                                }
                            },
                            "1": {
                                "declaration_country": {
                                    "id": 2,
                                    "name": "DE",
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

    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationCountriesResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_countries/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_countries": {},
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
