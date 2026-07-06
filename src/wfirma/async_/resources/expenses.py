"""Expenses-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "expenses" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /expenses/get/{expenseId}
- GET /expenses/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient


class ExpensesResource:
    """Asynchronous expenses resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, expense_id: int) -> dict[str, Any]:
        """Get expense by ID.

        Endpoint: GET /expenses/get/{expenseId}

        Args:
            expense_id: Expense identifier.

        Returns:
            Raw expense payload dict.
        """
        data = await self._client.get_json(f"/expenses/get/{expense_id}")
        return self._extract_expense_payload(data)

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list expenses.

        Endpoint: GET /expenses/find

        Returns:
            List of raw expense payload dicts.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/expenses/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/expenses/find",
                data={"expenses": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(
            data, container_key="expenses", object_key="expense"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_expense_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract expense payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="expenses",
            object_key="expense",
        )
        return dict(payload)


__all__ = [
    "ExpensesResource",
]
