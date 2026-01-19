"""Tag-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "tags" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- GET /tags/get/{tagId}
- GET /tags/find
- POST /tags/add
- POST /tags/edit/{termId}
- DELETE /tags/delete/{termId}

The docs are inconsistent in naming the identifier (tagId vs termId). This
resource uses ``tag_id`` in its public methods.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.sync.client import WFirmaClient


class TagsResource:
    """Synchronous tags resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, tag_id: int) -> dict[str, Any]:
        """Get tag by ID.

        Endpoint: GET /tags/get/{tagId}

        Args:
            tag_id: Tag identifier.

        Returns:
            Raw tag payload dict.
        """
        data = self._client.get_json(f"/tags/get/{tag_id}")
        return self._extract_tag_payload(data)

    def find(self) -> list[dict[str, Any]]:
        """Find/list tags.

        Endpoint: GET /tags/find

        Returns:
            List of raw tag payload dicts.
        """
        data = self._client.get_json("/tags/find")
        payloads = extract_object_list_payloads(data, container_key="tags", object_key="tag")
        return [dict(payload) for payload in payloads]

    def add(self, *, name: str, visibility: str | None = None) -> dict[str, Any]:
        """Create a new tag.

        Endpoint: POST /tags/add

        Args:
            name: Tag name.
            visibility: Tag visibility (e.g. "visible"), if supported.

        Returns:
            Created tag payload.
        """
        tag: dict[str, Any] = {"name": name}
        if visibility is not None:
            tag["visibility"] = visibility

        data = self._client.post_json("/tags/add", data={"tag": tag})
        return self._extract_tag_payload(data)

    def edit(
        self,
        tag_id: int,
        *,
        name: str | None = None,
        visibility: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing tag.

        Endpoint: POST /tags/edit/{termId}

        Args:
            tag_id: Tag identifier.
            name: New tag name.
            visibility: New visibility value.

        Returns:
            Updated tag payload.
        """
        tag: dict[str, Any] = {}
        if name is not None:
            tag["name"] = name
        if visibility is not None:
            tag["visibility"] = visibility

        data = self._client.post_json(f"/tags/edit/{tag_id}", data={"tag": tag})
        return self._extract_tag_payload(data)

    def delete(self, tag_id: int) -> bool:
        """Delete a tag.

        Endpoint: DELETE /tags/delete/{termId}

        Args:
            tag_id: Tag identifier.

        Returns:
            True when request succeeds.
        """
        self._client.delete_json(f"/tags/delete/{tag_id}")
        return True

    @staticmethod
    def _extract_tag_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract tag payload from a wFirma JSON response."""
        payload = extract_single_object_payload(
            data=data,
            container_key="tags",
            object_key="tag",
        )
        return dict(payload)


__all__ = [
    "TagsResource",
]
