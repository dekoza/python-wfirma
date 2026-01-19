"""Payment-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "payments" group.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient
from wfirma.models.payment import Payment


class PaymentsResource:
    """Asynchronous payments resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, payment_id: int) -> Payment:
        """Get payment by ID.

        Endpoint: GET /payments/get/{paymentId}

        Args:
            payment_id: Payment identifier.

        Returns:
            Parsed payment model.
        """
        data = await self._client.get_json(f"/payments/get/{payment_id}")
        payload = self._extract_payment_payload(data)
        return Payment.model_validate(payload)

    async def find(self) -> list[Payment]:
        """Find/list payments.

        Endpoint: GET /payments/find

        Returns:
            List of parsed payment models.
        """
        data = await self._client.get_json("/payments/find")
        return self._extract_payment_list(data)

    async def add(self, *, payment: dict[str, Any]) -> Payment:
        """Create a new payment.

        Endpoint: POST /payments/add

        Args:
            payment: Raw payment payload (without the outer "payments" wrapper).

        Returns:
            Created payment model.
        """
        payload = {"payments": [{"payment": payment}]}
        data = await self._client.post_json("/payments/add", data=payload)
        result_payload = self._extract_payment_payload(data)
        return Payment.model_validate(result_payload)

    async def edit(self, payment_id: int, *, payment: dict[str, Any]) -> Payment:
        """Update an existing payment.

        Endpoint: POST /payments/edit/{paymentId}

        Args:
            payment_id: Payment identifier.
            payment: Raw payment payload (without the outer "payments" wrapper).

        Returns:
            Updated payment model.
        """
        payload = {"payments": [{"payment": payment}]}
        data = await self._client.post_json(f"/payments/edit/{payment_id}", data=payload)
        result_payload = self._extract_payment_payload(data)
        return Payment.model_validate(result_payload)

    async def delete(self, payment_id: int) -> bool:
        """Delete a payment.

        Endpoint: DELETE /payments/delete/{paymentId}
        """
        await self._client.delete_json(f"/payments/delete/{payment_id}")
        return True

    @staticmethod
    def _extract_payment_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract Payment payload from a wFirma JSON response."""
        return extract_single_object_payload(
            data=data,
            container_key="payments",
            object_key="payment",
        )

    @staticmethod
    def _extract_payment_list(data: dict[str, Any]) -> list[Payment]:
        """Extract list of Payments from a wFirma JSON response."""
        payloads = extract_object_list_payloads(
            data,
            container_key="payments",
            object_key="payment",
        )
        return [Payment.model_validate(payload) for payload in payloads]


__all__ = ["PaymentsResource"]
