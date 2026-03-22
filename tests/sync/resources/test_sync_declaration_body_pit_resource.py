"""Tests for sync DeclarationBodyPitResource."""

from __future__ import annotations

import httpx
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.declaration_body_pit import DeclarationBodyPitResource


class TestDeclarationBodyPitResourceGet:
    """Tests for DeclarationBodyPitResource.get() method."""

    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyPitResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_pit/get/pit11/2025",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_pit": {
                            "0": {
                                "declaration_body_pit": {
                                    "id": "pit11",
                                    "year": 2025,
                                    "data": "some_data",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(pit_type="pit11", year=2025)

        client.close()

        assert route.called
        assert result["id"] == "pit11"
        assert result["year"] == 2025
        assert result["data"] == "some_data"

    def test_get_with_different_pit_type(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyPitResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_pit/get/pit38/2026",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_pit": {
                            "0": {
                                "declaration_body_pit": {
                                    "pit_type": "pit38",
                                    "year": 2026,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(pit_type="pit38", year=2026)

        client.close()

        assert route.called
        assert result["pit_type"] == "pit38"
        assert result["year"] == 2026

    def test_get_with_pit28s(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyPitResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_pit/get/pit28s/2024",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_pit": {
                            "0": {
                                "declaration_body_pit": {
                                    "pit_type": "pit28s",
                                    "year": 2024,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(pit_type="pit28s", year=2024)

        client.close()

        assert isinstance(result, dict)
        assert route.called

    def test_get_extracts_payload_correctly(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyPitResource(client)

        with respx.mock:
            respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_pit/get/pit11/2025",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_pit": {
                            "0": {
                                "declaration_body_pit": {
                                    "custom_field": "custom_value",
                                    "another_field": 42,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(pit_type="pit11", year=2025)

        client.close()

        assert result["custom_field"] == "custom_value"
        assert result["another_field"] == 42

    def test_get_handles_pit_ub(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyPitResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_pit/get/pit_ub/2025",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_pit": {
                            "0": {
                                "declaration_body_pit": {
                                    "id": "pit_ub",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(pit_type="pit_ub", year=2025)

        client.close()

        assert isinstance(result, dict)
        assert route.called
