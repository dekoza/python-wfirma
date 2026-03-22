"""Tests for synchronous ledger_operation_schemas resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the sync HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.ledger_operation_schemas import LedgerOperationSchemasResource

pytestmark = pytest.mark.aicomplete


class TestLedgerOperationSchemasResourceGet:
    """Tests for LedgerOperationSchemasResource.get() method."""

    # RED: Sync ledger_operation_schemas resource GET returns ledger_operation_schema payload
    def test_get_calls_expected_endpoint_and_returns_payload(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = LedgerOperationSchemasResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/ledger_operation_schemas/get/789",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "ledger_operation_schemas": {
                            "0": {
                                "ledger_operation_schema": {
                                    "id": 789,
                                    "name": "Standard Schema",
                                    "description": "Default operation schema",
                                }
                            }
                        },
                    },
                )
            )

            result = resource.get(schema_id=789)

        client.close()

        assert route.called
        assert result["id"] == 789
        assert result["name"] == "Standard Schema"


class TestLedgerOperationSchemasResourceFind:
    """Tests for LedgerOperationSchemasResource.find() method."""

    # RED: Sync ledger_operation_schemas resource FIND returns list of ledger_operation_schemas
    def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = LedgerOperationSchemasResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/ledger_operation_schemas/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "ledger_operation_schemas": {
                            "0": {
                                "ledger_operation_schema": {
                                    "id": 1,
                                    "name": "Schema 1",
                                }
                            },
                            "1": {
                                "ledger_operation_schema": {
                                    "id": 2,
                                    "name": "Schema 2",
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

    # RED: Sync ledger_operation_schemas resource FIND handles empty result
    def test_find_handles_empty_result(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = LedgerOperationSchemasResource(client)

        with respx.mock:
            route = respx.get(
                "https://api2.wfirma.pl/ledger_operation_schemas/find",
                params={
                    "outputFormat": "json",
                    "company_id": "123",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "ledger_operation_schemas": {},
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
