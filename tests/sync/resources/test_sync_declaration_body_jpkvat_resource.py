"""Tests for synchronous declaration_body_jpkvat resource.

These tests verify that the resource calls the expected parameterized-path endpoint
and properly extracts payload from the response.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.declaration_body_jpkvat import DeclarationBodyJpkvatResource

pytestmark = pytest.mark.aicomplete


class TestDeclarationBodyJpkvatResourceGet:
    """Tests for DeclarationBodyJpkvatResource.get() method."""

    def test_get_calls_expected_endpoint_with_path_parameters(self) -> None:
        """Verify get() constructs correct parameterized path."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyJpkvatResource(client)

        with respx.mock:
            route = respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_jpkvat/get/2025/6",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_jpkvat": {
                            "0": {
                                "jpkvat": {
                                    "id": 1,
                                    "year": 2025,
                                    "month": 6,
                                    "total": 1000.00,
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(year=2025, month=6)

        client.close()

        assert route.called
        assert result["id"] == 1
        assert result["year"] == 2025
        assert result["month"] == 6
        assert result["total"] == 1000.00

    def test_get_extracts_payload_correctly(self) -> None:
        """Verify get() extracts jpkvat payload from response."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyJpkvatResource(client)

        with respx.mock:
            respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_jpkvat/get/2025/3",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_jpkvat": {
                            "0": {
                                "jpkvat": {
                                    "summary": "Q1 summary",
                                    "items": [1, 2, 3],
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(year=2025, month=3)

        client.close()

        assert isinstance(result, dict)
        assert result["summary"] == "Q1 summary"
        assert result["items"] == [1, 2, 3]

    def test_get_returns_dict_not_raw_response(self) -> None:
        """Verify get() returns extracted dict, not raw response."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = DeclarationBodyJpkvatResource(client)

        with respx.mock:
            respx.get(
                "https://sandbox-api2.wfirma.pl/declaration_body_jpkvat/get/2024/12",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "declaration_body_jpkvat": {
                            "0": {
                                "jpkvat": {
                                    "data": "test_value",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(year=2024, month=12)

        client.close()

        # Should be the extracted payload dict, not a wrapper
        assert "jpkvat" not in result
        assert "declaration_body_jpkvat" not in result
        assert "status" not in result
        assert result["data"] == "test_value"
