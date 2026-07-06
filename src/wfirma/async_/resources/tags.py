"""Tag-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "tags" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API docs list these endpoints:
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

from wfirma._payloads import (
    build_find_parameters,
    build_module_payload,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient


class TagsResource:
    """Asynchronous tags resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, tag_id: int) -> dict[str, Any]:
        """Get tag by ID.

        Endpoint: GET /tags/get/{tagId}

        Args:
            tag_id: Tag identifier.

        Returns:
            Raw tag payload dict.
        """
        data = await self._client.get_json(f"/tags/get/{tag_id}")
        return self._extract_tag_payload(data)

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list tags.

        Endpoint: GET /tags/find

        Returns:
            List of raw tag payloads.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/tags/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/tags/find",
                data={"tags": {"parameters": parameters}},
            )
        payloads = extract_object_list_payloads(data, container_key="tags", object_key="tag")
        return [dict(payload) for payload in payloads]

    async def add(
        self,
        tag: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        visibility: str | None = None,
    ) -> dict[str, Any]:
        """Create a new tag.

        Endpoint: POST /tags/add

        Args:
            tag: Full tag payload dict (documented fields include ``name``,
                ``color_background``, ``color_text``, module flags, etc.).
            name: Tag name, merged into the payload when given.
            visibility: Tag visibility, merged into the payload when given.

        Returns:
            Created tag payload.
        """
        tag = dict(tag or {})
        if name is not None:
            tag["name"] = name
        if visibility is not None:
            tag["visibility"] = visibility
        data = await self._client.post_json(
            "/tags/add",
            data=build_module_payload(container_key="tags", object_key="tag", obj=tag),
        )
        return self._extract_tag_payload(data)

    async def edit(
        self,
        tag_id: int,
        tag: dict[str, Any] | None = None,
        *,
        name: str | None = None,
        visibility: str | None = None,
    ) -> dict[str, Any]:
        """Update an existing tag.

        Endpoint: POST /tags/edit/{termId}

        Args:
            tag_id: Tag identifier.
            tag: Full tag payload dict with updated fields.
            name: New tag name, merged into the payload when given.
            visibility: New visibility value, merged into the payload when given.

        Returns:
            Updated tag payload.
        """
        tag = dict(tag or {})
        if name is not None:
            tag["name"] = name
        if visibility is not None:
            tag["visibility"] = visibility
        data = await self._client.post_json(
            f"/tags/edit/{tag_id}",
            data=build_module_payload(container_key="tags", object_key="tag", obj=tag),
        )
        return self._extract_tag_payload(data)

    async def delete(self, tag_id: int) -> bool:
        """Delete a tag.

        Endpoint: DELETE /tags/delete/{termId}

        Args:
            tag_id: Tag identifier.

        Returns:
            True when request succeeds.
        """
        await self._client.delete_json(f"/tags/delete/{tag_id}")
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
