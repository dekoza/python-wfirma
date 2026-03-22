"""Tests for asynchronous interests resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.interests import InterestsResource

pytestmark = pytest.mark.aicomplete


class TestInterestsResourceFind:
    """Tests for InterestsResource.find() method."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InterestsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/interests/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "interests": {
                                "0": {
                                    "interest": {
                                        "id": 1,
                                        "name": "Interest 1",
                                    }
                                },
                                "1": {
                                    "interest": {
                                        "id": 2,
                                        "name": "Interest 2",
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

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert result[0]["id"] == 1
        assert result[1]["id"] == 2

    @pytest.mark.asyncio
    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = InterestsResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/interests/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "interests": {},
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 0,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert result == []
