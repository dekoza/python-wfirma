"""Declaration countries-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "declaration_countries" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /declaration_countries/get/{declarationCountryId}
- GET /declaration_countries/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient


class DeclarationCountriesResource:
    """Asynchronous declaration_countries resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, declaration_country_id: int) -> dict[str, Any]:
        """Get declaration country by ID.

        Endpoint: GET /declaration_countries/get/{declarationCountryId}

        Args:
            declaration_country_id: Declaration country identifier.

        Returns:
            Raw declaration country payload dict.
        """
        data = await self._client.get_json(f"/declaration_countries/get/{declaration_country_id}")
        return self._extract_declaration_country_payload(data)

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list declaration countries.

        Endpoint: GET /declaration_countries/find

        Returns:
            List of raw declaration country payload dicts.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/declaration_countries/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/declaration_countries/find",
                data={"declaration_countries": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(
            data, container_key="declaration_countries", object_key="declaration_country"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_declaration_country_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract declaration country payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="declaration_countries",
            object_key="declaration_country",
        )
        return dict(payload)


__all__ = [
    "DeclarationCountriesResource",
]
