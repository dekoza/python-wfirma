"""Tests for async DeclarationBodyPitResource."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.declaration_body_pit import DeclarationBodyPitResource


class TestAsyncDeclarationBodyPitResourceGet:
    """Tests for async DeclarationBodyPitResource.get() method."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = DeclarationBodyPitResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/declaration_body_pit/get/pit11/2025",
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

                result = await resource.get(pit_type="pit11", year=2025)

                assert route.called
                assert result["id"] == "pit11"
                assert result["year"] == 2025
                assert result["data"] == "some_data"

    @pytest.mark.asyncio
    async def test_get_with_different_pit_type(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = DeclarationBodyPitResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/declaration_body_pit/get/pit38/2026",
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

                result = await resource.get(pit_type="pit38", year=2026)

                assert route.called
                assert result["pit_type"] == "pit38"
                assert result["year"] == 2026

    @pytest.mark.asyncio
    async def test_get_with_pit28s(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = DeclarationBodyPitResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/declaration_body_pit/get/pit28s/2024",
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

                result = await resource.get(pit_type="pit28s", year=2024)

                assert isinstance(result, dict)
                assert route.called

    @pytest.mark.asyncio
    async def test_get_extracts_payload_correctly(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = DeclarationBodyPitResource(client)

            with respx.mock:
                respx.get(
                    "https://api2.wfirma.pl/declaration_body_pit/get/pit11/2025",
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

                result = await resource.get(pit_type="pit11", year=2025)

                assert result["custom_field"] == "custom_value"
                assert result["another_field"] == 42

    @pytest.mark.asyncio
    async def test_get_handles_pit_ub(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = DeclarationBodyPitResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/declaration_body_pit/get/pit_ub/2025",
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

                result = await resource.get(pit_type="pit_ub", year=2025)

                assert isinstance(result, dict)
                assert route.called
