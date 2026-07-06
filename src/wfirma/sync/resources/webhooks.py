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

from wfirma._payloads import (
    build_find_parameters,
    build_module_payload,
    extract_object_list_payloads,
    extract_single_object_payload,
)
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

    def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list webhooks.

        Endpoint: GET /webhooks/find

        Returns:
            List of raw webhook payload dicts.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = self._client.get_json("/webhooks/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = self._client.post_json(
                "/webhooks/find",
                data={"webhooks": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(
            data, container_key="webhooks", object_key="webhook"
        )
        return [dict(payload) for payload in payloads]

    def add(
        self,
        webhook: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        url: str | None = None,
        event: str | None = None,
        data_type: str | None = None,
    ) -> dict[str, Any]:
        """Create a new webhook.

        Endpoint: POST /webhooks/add

        Args:
            webhook: Full webhook payload dict (documented fields include
                ``url``, ``event``, and ``data_type``).
            name: Webhook name, merged into the payload when given.
            url: Webhook URL, merged into the payload when given.
            event: Triggering event (e.g. "invoice/add"), merged when given.
            data_type: Delivery format ("xml" or "json"), merged when given.

        Returns:
            Created webhook payload.
        """
        fields: dict[str, Any] = dict(webhook or {})
        if name is not None:
            fields["name"] = name
        if url is not None:
            fields["url"] = url
        if event is not None:
            fields["event"] = event
        if data_type is not None:
            fields["data_type"] = data_type

        data = self._client.post_json(
            "/webhooks/add",
            data=build_module_payload(container_key="webhooks", object_key="webhook", obj=fields),
        )
        return self._extract_webhook_payload(data)

    def edit(
        self,
        webhook_id: int,
        webhook: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        url: str | None = None,
        event: str | None = None,
        data_type: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing webhook.

        Endpoint: PATCH /webhooks/edit/{webhookId}

        Args:
            webhook_id: Webhook identifier.
            webhook: Full webhook payload dict with updated fields.
            name: New webhook name, merged into the payload when given.
            url: New webhook URL, merged into the payload when given.
            event: New triggering event, merged when given.
            data_type: New delivery format, merged when given.

        Returns:
            Updated webhook payload.
        """
        fields: dict[str, Any] = dict(webhook or {})
        if name is not None:
            fields["name"] = name
        if url is not None:
            fields["url"] = url
        if event is not None:
            fields["event"] = event
        if data_type is not None:
            fields["data_type"] = data_type

        data = self._client.patch_json(
            f"/webhooks/edit/{webhook_id}",
            data=build_module_payload(container_key="webhooks", object_key="webhook", obj=fields),
        )
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
