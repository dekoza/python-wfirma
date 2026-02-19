"""Note-related resource endpoints (asynchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "notes" group.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).

The wFirma API reference lists these endpoints:
- POST /notes/add
- GET /notes/find
- GET /notes/get/{noteId}
- PUT /notes/edit/{noteId}
- DELETE /notes/delete/{noteId}

Note: The spec has a typo listing /goods/notes/{noteId} for edit, but
the actual endpoint is /notes/edit/{noteId} (same pattern as Tags resource).
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import extract_object_list_payloads, extract_single_object_payload
from wfirma.async_.client import WFirmaClient


class NotesResource:
    """Asynchronous notes resource."""

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def add(self, note: dict[str, Any]) -> dict[str, Any]:
        """Create a new note.

        Endpoint: POST /notes/add

        Args:
            note: Note payload dict with required fields.

        Returns:
            Created note payload.
        """
        data = await self._client.post_json("/notes/add", data={"note": note})
        return self._extract_note_payload(data)

    async def find(self, params: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        """Find/list notes.

        Endpoint: GET /notes/find

        Args:
            params: Optional query parameters.

        Returns:
            List of raw note payload dicts.
        """
        data = await self._client.get_json("/notes/find", params=params)
        payloads = extract_object_list_payloads(data=data, container_key="notes", object_key="note")
        return [dict(payload) for payload in payloads]

    async def get(self, note_id: int) -> dict[str, Any]:
        """Get note by ID.

        Endpoint: GET /notes/get/{noteId}

        Args:
            note_id: Note identifier.

        Returns:
            Raw note payload dict.
        """
        data = await self._client.get_json(f"/notes/get/{note_id}")
        return self._extract_note_payload(data)

    async def edit(self, note_id: int, note: dict[str, Any]) -> dict[str, Any]:
        """Update an existing note.

        Endpoint: PUT /notes/edit/{noteId}

        Args:
            note_id: Note identifier.
            note: Note payload dict with updated fields.

        Returns:
            Updated note payload.
        """
        data = await self._client.put_json(f"/notes/edit/{note_id}", data={"note": note})
        return self._extract_note_payload(data)

    async def delete(self, note_id: int) -> dict[str, Any]:
        """Delete a note.

        Endpoint: DELETE /notes/delete/{noteId}

        Args:
            note_id: Note identifier.

        Returns:
            Response dict.
        """
        return await self._client.delete_json(f"/notes/delete/{note_id}")

    @staticmethod
    def _extract_note_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract note payload from response."""
        return extract_single_object_payload(data=data, container_key="notes", object_key="note")
