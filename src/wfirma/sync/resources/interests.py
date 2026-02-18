"""Interests-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "interests" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /interests/find
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads
from wfirma.sync.client import WFirmaClient


class InterestsResource:
    """Synchronous interests resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def find(self) -> list[dict[str, Any]]:
        """Find/list interests.

        Endpoint: GET /interests/find

        Returns:
            List of raw interest payload dicts.
        """
        data = self._client.get_json("/interests/find")
        payloads = extract_object_list_payloads(
            data, container_key="interests", object_key="interest"
        )
        return [dict(payload) for payload in payloads]


__all__ = [
    "InterestsResource",
]
