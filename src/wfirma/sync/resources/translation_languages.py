"""Translation language-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "translation_languages" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /translation_languages/get/{translationLanguageId}
- GET /translation_languages/find

This is a read-only resource with no write operations.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.sync.client import WFirmaClient


class TranslationLanguagesResource:
    """Synchronous translation_languages resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, translation_language_id: int) -> dict[str, Any]:
        """Get translation language by ID.

        Endpoint: GET /translation_languages/get/{translationLanguageId}

        Args:
            translation_language_id: Translation language identifier.

        Returns:
            Raw translation language payload dict.
        """
        data = self._client.get_json(f"/translation_languages/get/{translation_language_id}")
        return self._extract_translation_language_payload(data)

    def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list translation languages.

        Endpoint: GET /translation_languages/find

        Returns:
            List of raw translation language payload dicts.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = self._client.get_json("/translation_languages/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = self._client.post_json(
                "/translation_languages/find",
                data={"translation_languages": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(
            data, container_key="translation_languages", object_key="translation_language"
        )
        return [dict(payload) for payload in payloads]

    @staticmethod
    def _extract_translation_language_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract translation language payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="translation_languages",
            object_key="translation_language",
        )
        return dict(payload)


__all__ = [
    "TranslationLanguagesResource",
]
