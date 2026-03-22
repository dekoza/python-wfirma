"""Tests for asynchronous translation_languages resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.translation_languages import TranslationLanguagesResource

pytestmark = pytest.mark.aicomplete


class TestTranslationLanguagesResourceGet:
    """Tests for TranslationLanguagesResource.get() method."""

    async def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = TranslationLanguagesResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/translation_languages/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "translation_languages": {
                                "0": {
                                    "translation_language": {
                                        "id": 456,
                                        "name": "English",
                                        "code": "en_US",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(translation_language_id=456)

            assert route.called
            assert result["id"] == 456
            assert result["name"] == "English"


class TestTranslationLanguagesResourceFind:
    """Tests for TranslationLanguagesResource.find() method."""

    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = TranslationLanguagesResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/translation_languages/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "translation_languages": {
                                "0": {
                                    "translation_language": {
                                        "id": 1,
                                        "name": "English",
                                        "code": "en_US",
                                    }
                                },
                                "1": {
                                    "translation_language": {
                                        "id": 2,
                                        "name": "Polish",
                                        "code": "pl_PL",
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

    async def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = TranslationLanguagesResource(client)

            with respx.mock:
                route = respx.get(
                    "https://api2.wfirma.pl/translation_languages/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "translation_languages": {},
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
