"""Filtered ``find`` tests for asynchronous resources.

Mirrors ``tests/sync/resources/test_sync_find_filters.py``: every ``find``
endpoint accepts a ``parameters`` block (conditions, limit, page) that must
be POSTed under the module branch; unfiltered ``find()`` keeps using GET.
"""

from __future__ import annotations

import json
from typing import Any

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient

# (client accessor, endpoint module slug, request container key)
FIND_RESOURCES = [
    ("company_accounts", "company_accounts", "company_accounts"),
    ("contractors", "contractors", "contractors"),
    ("declaration_countries", "declaration_countries", "declaration_countries"),
    ("documents", "documents", "documents"),
    ("expenses", "expenses", "expenses"),
    ("goods", "goods", "goods"),
    ("interests", "interests", "interests"),
    ("invoice_deliveries", "invoice_deliveries", "invoice_deliveries"),
    ("invoice_descriptions", "invoice_descriptions", "invoice_descriptions"),
    ("invoices", "invoices", "invoices"),
    ("ledger_accountant_years", "ledger_accountant_years", "ledger_accountant_years"),
    ("ledger_operation_schemas", "ledger_operation_schemas", "ledger_operation_schemas"),
    ("notes", "notes", "notes"),
    ("payment_cashboxes", "payment_cashboxes", "payment_cashboxes"),
    ("payments", "payments", "payments"),
    ("series", "series", "series"),
    ("tags", "tags", "tags"),
    ("term_groups", "term_groups", "term_groups"),
    ("terms", "terms", "terms"),
    ("translation_languages", "translation_languages", "translation_languages"),
    ("user_companies", "user_companies", "user_companies"),
    ("vat_codes", "vat_codes", "vat_codes"),
    ("vehicle_run_rates", "vehicle_run_rates", "vehicle_run_rates"),
    ("vehicles", "vehicles", "vehicles"),
    ("warehouses", "warehouses", "warehouses"),
    ("webhooks", "webhooks", "webhooks"),
    ("warehouse_documents_pw", "warehouse_document_p_w", "warehouse_documents"),
    ("warehouse_documents_pz", "warehouse_document_p_z", "warehouse_documents"),
    ("warehouse_documents_r", "warehouse_document_r", "warehouse_documents"),
    ("warehouse_documents_rw", "warehouse_document_r_w", "warehouse_documents"),
    ("warehouse_documents_wz", "warehouse_document_w_z", "warehouse_documents"),
    ("warehouse_documents_zd", "warehouse_document_z_d", "warehouse_documents"),
    ("warehouse_documents_zpd", "warehouse_document_z_p_d", "warehouse_documents"),
    ("warehouse_documents_zpm", "warehouse_document_z_p_m", "warehouse_documents"),
]

CONDITIONS = [{"field": "id", "operator": "eq", "value": 7}]

EXPECTED_PARAMETERS = {
    "conditions": {"0": {"condition": {"field": "id", "operator": "eq", "value": 7}}},
    "limit": 5,
    "page": 2,
}


def _client() -> WFirmaClient:
    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
    return WFirmaClient(auth=auth, company_id=123)


def _empty_response(container: str) -> httpx.Response:
    return httpx.Response(200, json={"status": {"code": "OK"}, container: {}})


class TestFilteredFind:
    @pytest.mark.parametrize(("accessor", "slug", "container"), FIND_RESOURCES)
    async def test_find_with_filters_posts_parameters_block(
        self, accessor: str, slug: str, container: str
    ) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.post(f"https://api2.wfirma.pl/{slug}/find").mock(
                    return_value=_empty_response(container)
                )
                result = await getattr(client, accessor).find(
                    conditions=CONDITIONS, limit=5, page=2
                )

        assert result == []
        body: dict[str, Any] = json.loads(route.calls.last.request.content)
        assert body == {container: {"parameters": EXPECTED_PARAMETERS}}

    @pytest.mark.parametrize(("accessor", "slug", "container"), FIND_RESOURCES)
    async def test_find_without_filters_uses_get(
        self, accessor: str, slug: str, container: str
    ) -> None:
        async with _client() as client:
            with respx.mock:
                route = respx.get(f"https://api2.wfirma.pl/{slug}/find").mock(
                    return_value=_empty_response(container)
                )
                result = await getattr(client, accessor).find()

        assert route.called
        assert result == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
