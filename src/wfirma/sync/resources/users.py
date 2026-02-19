"""Users-related resource endpoints (synchronous).

This module provides thin wrappers around the base HTTP client for endpoints
from the "users" group.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.
"""

from __future__ import annotations

from wfirma._payloads import extract_single_object_payload
from wfirma.models.employee import User
from wfirma.sync.client import WFirmaClient


class UsersResource:
    """Synchronous users resource.

    Args:
        client: A configured synchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    def get(self, user_id: int) -> User:
        """Get user details.

        Endpoint: GET /users/get/{userCompanyId}

        Args:
            user_id: User identifier.

        Returns:
            Parsed user model.
        """
        data = self._client.get_json(f"/users/get/{user_id}")
        payload = extract_single_object_payload(data=data, container_key="users", object_key="user")
        return User.model_validate(payload)


__all__ = [
    "UsersResource",
]
