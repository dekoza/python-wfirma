"""Expenses-related resource endpoints (synchronous).

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

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class ExpensesResource:
    """Synchronous expenses resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, expense_id: int) -> dict[str, Any]:
        """Get expense by ID.

        Endpoint: GET /expenses/get/{expenseId}

        Args:
            expense_id: Expense identifier.

        Returns:
            Raw expense payload dict.
        """
        data = self._client.get_json(f"/expenses/get/{expense_id}")
        return self._extract_expense_payload(data)

    def find(self) -> list[dict[str, Any]]:
        """Find/list expenses.

        Endpoint: GET /expenses/find

        Returns:
            List of raw expense payload dicts.
        """
        data = self._client.get_json("/expenses/find")
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
