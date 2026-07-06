"""Note-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "notes" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- POST /notes/add
- GET /notes/find
- GET /notes/get/{noteId}
- POST /notes/edit/{noteId}
- DELETE /notes/delete/{noteId}
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


class NotesResource:
    """Synchronous notes resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def add(self, note: dict[str, Any]) -> dict[str, Any]:
        """Create a new note.

        Endpoint: POST /notes/add

        Args:
            note: Note payload dict with required fields.

        Returns:
            Created note payload.
        """
        data = self._client.post_json(
            "/notes/add",
            data=build_module_payload(container_key="notes", object_key="note", obj=note),
        )
        return self._extract_note_payload(data)

    def find(
        self,
        params: dict[str, Any] | None = None,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[dict[str, Any]]:
        """Find/list notes.

        Endpoint: GET /notes/find

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
            params: Optional query parameters.

        Returns:
            List of raw note payload dicts.
        """
        if conditions is None and limit is None and page is None:
            data = self._client.get_json("/notes/find", params=params)
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = self._client.post_json(
                "/notes/find",
                data={"notes": {"parameters": parameters}},
                params=params,
            )
        payloads = extract_object_list_payloads(data=data, container_key="notes", object_key="note")
        return [dict(payload) for payload in payloads]

    def get(self, note_id: int) -> dict[str, Any]:
        """Get note by ID.

        Endpoint: GET /notes/get/{noteId}

        Args:
            note_id: Note identifier.

        Returns:
            Raw note payload dict.
        """
        data = self._client.get_json(f"/notes/get/{note_id}")
        return self._extract_note_payload(data)

    def edit(self, note_id: int, note: dict[str, Any]) -> dict[str, Any]:
        """Update an existing note.

        Endpoint: POST /notes/edit/{noteId}

        Args:
            note_id: Note identifier.
            note: Note payload dict with updated fields.

        Returns:
            Updated note payload.
        """
        data = self._client.post_json(
            f"/notes/edit/{note_id}",
            data=build_module_payload(container_key="notes", object_key="note", obj=note),
        )
        return self._extract_note_payload(data)

    def delete(self, note_id: int) -> dict[str, Any]:
        """Delete a note.

        Endpoint: DELETE /notes/delete/{noteId}

        Args:
            note_id: Note identifier.

        Returns:
            Response dict.
        """
        return self._client.delete_json(f"/notes/delete/{note_id}")

    @staticmethod
    def _extract_note_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract note payload from response."""
        return extract_single_object_payload(data=data, container_key="notes", object_key="note")
