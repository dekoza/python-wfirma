"""Term group-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "term_groups" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /term_groups/get/{termGroupId}
- GET /term_groups/find
- POST /term_groups/add
- POST /term_groups/edit/{termGroupId}
- DELETE /term_groups/delete/{termGroupId}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class TermGroupsResource:
    """Synchronous term groups resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def add(self, term_group: dict[str, Any]) -> dict[str, Any]:
        """Create a new term group.

        Endpoint: POST /term_groups/add

        Args:
            term_group: Term group payload dict.

        Returns:
            Created term group payload.
        """
        data = self._client.post_json("/term_groups/add", data={"term_group": term_group})
        return self._extract_term_group_payload(data)

    def find(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Find/list term groups.

        Endpoint: GET /term_groups/find

        Args:
            params: Optional query parameters.

        Returns:
            List of raw term group payload dicts.
        """
        data = self._client.get_json("/term_groups/find", params=params)
        payloads = extract_object_list_payloads(
            data, container_key="term_groups", object_key="term_group"
        )
        return [dict(payload) for payload in payloads]

    def get(self, term_group_id: int) -> dict[str, Any]:
        """Get term group by ID.

        Endpoint: GET /term_groups/get/{termGroupId}

        Args:
            term_group_id: Term group identifier.

        Returns:
            Raw term group payload dict.
        """
        data = self._client.get_json(f"/term_groups/get/{term_group_id}")
        return self._extract_term_group_payload(data)

    def edit(self, term_group_id: int, term_group: dict[str, Any]) -> dict[str, Any]:
        """Update an existing term group.

        Endpoint: POST /term_groups/edit/{termGroupId}

        Args:
            term_group_id: Term group identifier.
            term_group: Term group payload dict with updated fields.

        Returns:
            Updated term group payload.
        """
        data = self._client.post_json(
            f"/term_groups/edit/{term_group_id}", data={"term_group": term_group}
        )
        return self._extract_term_group_payload(data)

    def delete(self, term_group_id: int) -> dict[str, Any]:
        """Delete a term group.

        Endpoint: DELETE /term_groups/delete/{termGroupId}

        Args:
            term_group_id: Term group identifier.

        Returns:
            API response dict.
        """
        return self._client.delete_json(f"/term_groups/delete/{term_group_id}")

    @staticmethod
    def _extract_term_group_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract term group payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="term_groups",
            object_key="term_group",
        )
        return dict(payload)


__all__ = [
    "TermGroupsResource",
]
