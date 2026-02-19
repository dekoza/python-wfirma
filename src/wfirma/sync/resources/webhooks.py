"""Webhook-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "webhooks" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /webhooks/get/{webhookId}
- GET /webhooks/find
- POST /webhooks/add
- PATCH /webhooks/edit/{webhookId}
- DELETE /webhooks/delete/{webhookId}
- GET /webhooks/trigger/{webhookId}

This resource uses ``webhook_id`` in its public methods.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class WebhooksResource:
    """Synchronous webhooks resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, webhook_id: int) -> dict[str, Any]:
        """Get webhook by ID.

        Endpoint: GET /webhooks/get/{webhookId}

        Args:
            webhook_id: Webhook identifier.

        Returns:
            Raw webhook payload dict.
        """
        data = self._client.get_json(f"/webhooks/get/{webhook_id}")
        return self._extract_webhook_payload(data)

    def trigger(self, webhook_id: int) -> dict[str, Any]:
        """Trigger a webhook.

        Endpoint: GET /webhooks/trigger/{webhookId}

        Args:
            webhook_id: Webhook identifier.

        Returns:
            Response payload from trigger operation.
        """
        return self._client.get_json(f"/webhooks/trigger/{webhook_id}")

    def find(self) -> list[dict[str, Any]]:
        """Find/list webhooks.

        Endpoint: GET /webhooks/find

        Returns:
            List of raw webhook payload dicts.
        """
        data = self._client.get_json("/webhooks/find")
        payloads = extract_object_list_payloads(
            data, container_key="webhooks", object_key="webhook"
        )
        return [dict(payload) for payload in payloads]

    def add(self, *, name: str, url: str | None = None) -> dict[str, Any]:
        """Create a new webhook.

        Endpoint: POST /webhooks/add

        Args:
            name: Webhook name.
            url: Webhook URL, if supported.

        Returns:
            Created webhook payload.
        """
        webhook: dict[str, Any] = {"name": name}
        if url is not None:
            webhook["url"] = url

        data = self._client.post_json("/webhooks/add", data={"webhook": webhook})
        return self._extract_webhook_payload(data)

    def edit(
        self,
        webhook_id: int,
        *,
        name: str | None = None,
        url: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing webhook.

        Endpoint: PATCH /webhooks/edit/{webhookId}

        Args:
            webhook_id: Webhook identifier.
            name: New webhook name.
            url: New webhook URL.

        Returns:
            Updated webhook payload.
        """
        webhook: dict[str, Any] = {}
        if name is not None:
            webhook["name"] = name
        if url is not None:
            webhook["url"] = url

        data = self._client.patch_json(f"/webhooks/edit/{webhook_id}", data={"webhook": webhook})
        return self._extract_webhook_payload(data)

    def delete(self, webhook_id: int) -> bool:
        """Delete a webhook.

        Endpoint: DELETE /webhooks/delete/{webhookId}

        Args:
            webhook_id: Webhook identifier.

        Returns:
            True when request succeeds.
        """
        self._client.delete_json(f"/webhooks/delete/{webhook_id}")
        return True

    @staticmethod
    def _extract_webhook_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract webhook payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="webhooks",
            object_key="webhook",
        )
        return dict(payload)


__all__ = [
    "WebhooksResource",
]
