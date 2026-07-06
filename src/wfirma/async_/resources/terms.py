"""Term-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "terms" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- POST /terms/add
- GET /terms/find
- GET /terms/get/{termId}
- POST /terms/edit/{termId}  (API spec shows /terms/notes/ typo - use /terms/edit/)
- DELETE /terms/delete/{termId}
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    build_module_payload,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient


class TermsResource:
    """Asynchronous terms resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def add(self, term: dict[str, Any]) -> dict[str, Any]:
        """Create a new term.

        Endpoint: POST /terms/add

        Args:
            term: Term payload dict with required fields.

        Returns:
            Created term payload.
        """
        data = await self._client.post_json(
            "/terms/add",
            data=build_module_payload(container_key="terms", object_key="term", obj=term),
        )
        return self._extract_term_payload(data)

    async def find(
        self,
        params: dict[str, Any] | None = None,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list terms.

        Endpoint: GET /terms/find

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
            params: Optional query parameters.

        Returns:
            List of raw term payload dicts.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/terms/find", params=params)
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/terms/find",
                data={"terms": {"parameters": parameters}},
                params=params,
            )
        payloads = extract_object_list_payloads(data, container_key="terms", object_key="term")
        return [dict(payload) for payload in payloads]

    async def get(self, term_id: int) -> dict[str, Any]:
        """Get term by ID.

        Endpoint: GET /terms/get/{termId}

        Args:
            term_id: Term identifier.

        Returns:
            Raw term payload dict.
        """
        data = await self._client.get_json(f"/terms/get/{term_id}")
        return self._extract_term_payload(data)

    async def edit(self, term_id: int, term: dict[str, Any]) -> dict[str, Any]:
        """Update an existing term.

        Endpoint: POST /terms/edit/{termId}

        Args:
            term_id: Term identifier.
            term: Term payload dict with fields to update.

        Returns:
            Updated term payload.
        """
        data = await self._client.post_json(
            f"/terms/edit/{term_id}",
            data=build_module_payload(container_key="terms", object_key="term", obj=term),
        )
        return self._extract_term_payload(data)

    async def delete(self, term_id: int) -> dict[str, Any]:
        """Delete a term.

        Endpoint: DELETE /terms/delete/{termId}

        Args:
            term_id: Term identifier.

        Returns:
            Response payload from deletion.
        """
        data = await self._client.delete_json(f"/terms/delete/{term_id}")
        return self._extract_term_payload(data)

    @staticmethod
    def _extract_term_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract term payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="terms",
            object_key="term",
        )
        return dict(payload)


__all__ = [
    "TermsResource",
]
