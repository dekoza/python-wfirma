"""Payment cashbox-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "payment_cashboxes" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /payment_cashboxes/get/{paymentCashboxId}
- GET /payment_cashboxes/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class PaymentCashboxesResource:
    """Asynchronous payment_cashboxes resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, payment_cashbox_id: int) -> dict[str, Any]:
        """Get payment cashbox by ID.

        Endpoint: GET /payment_cashboxes/get/{paymentCashboxId}

        Args:
            payment_cashbox_id: Payment cashbox identifier.

        Returns:
            Raw payment_cashbox payload dict.
        """
        data = await self._client.get_json(f"/payment_cashboxes/get/{payment_cashbox_id}")
        return self._extract_payment_cashbox_payload(data)

    async def find(self) -> list[dict[str, Any]]:
        """Find/list payment cashboxes.

        Endpoint: GET /payment_cashboxes/find

        Returns:
            List of raw payment_cashbox payload dicts.
        """
        data = await self._client.get_json("/payment_cashboxes/find")
        payloads = extract_object_list_payloads(
            data, container_key="payment_cashboxes", object_key="payment_cashbox"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_payment_cashbox_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract payment_cashbox payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="payment_cashboxes",
            object_key="payment_cashbox",
        )
        return dict(payload)


__all__ = [
    "PaymentCashboxesResource",
]
