"""Shared token utilities for wFirma authentication.

Provides minimal storage primitives and token container shared by sync and async auth layers.
"""

from __future__ import annotations

import json
import os
import tempfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Protocol

from wfirma.exceptions import ConfigurationError, ValidationError
from wfirma.models import format_wfirma_datetime, parse_wfirma_datetime


class TokenStore(Protocol):
    """A minimal storage interface for OAuth tokens."""

    def get(self, key: str) -> "OAuthToken | None":
        """Retrieve token for a given key."""

    def set(self, key: str, token: "OAuthToken") -> None:
        """Store token under a given key."""

    def delete(self, key: str) -> None:
        """Delete token for a given key if present."""

    def clear(self) -> None:
        """Remove all stored tokens."""


@dataclass(slots=True)
class MemoryTokenStore:
    """In-memory token storage (not persistent, not thread-safe)."""

    _tokens: dict[str, "OAuthToken"]

    def __init__(self) -> None:
        self._tokens = {}

    def get(self, key: str) -> "OAuthToken | None":
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        return self._tokens.get(key)

    def set(self, key: str, token: "OAuthToken") -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        self._tokens[key] = token

    def delete(self, key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        self._tokens.pop(key, None)

    def clear(self) -> None:
        self._tokens.clear()


@dataclass(slots=True)
class FileTokenStore:
    """File-based token storage (JSON mapping {key: token_dict})."""

    path: Path

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)

    def get(self, key: str) -> "OAuthToken | None":
        self._validate_key(key)
        payload = self._read_payload()
        token_payload = payload.get(key)
        if token_payload is None:
            return None
        if not isinstance(token_payload, dict):
            raise ValidationError("Stored token payload must be a dictionary.")
        return OAuthToken.from_dict(token_payload)

    def set(self, key: str, token: "OAuthToken") -> None:
        self._validate_key(key)
        payload = self._read_payload()
        payload[key] = token.to_dict()
        self._write_payload(payload)

    def delete(self, key: str) -> None:
        self._validate_key(key)
        payload = self._read_payload()
        payload.pop(key, None)
        self._write_payload(payload)

    def clear(self) -> None:
        self._write_payload({})

    @staticmethod
    def _validate_key(key: str) -> None:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")

    def _read_payload(self) -> dict[str, Any]:
        if not self.path.exists():
            return {}

        if not self.path.is_file():
            raise ConfigurationError("Token store path must point to a file.")

        try:
            raw = self.path.read_text(encoding="utf-8")
            data = json.loads(raw) if raw.strip() else {}
        except (OSError, json.JSONDecodeError) as err:
            raise ValidationError("Token store file contains invalid JSON.") from err

        if not isinstance(data, dict):
            raise ValidationError("Token store JSON must be an object mapping keys to tokens.")

        return data

    def _write_payload(self, payload: dict[str, Any]) -> None:
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)

            with tempfile.NamedTemporaryFile(
                "w",
                encoding="utf-8",
                dir=str(self.path.parent),
                delete=False,
            ) as tmp:
                tmp_path = Path(tmp.name)
                tmp.write(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2))

            tmp_path.replace(self.path)
        except OSError as err:
            raise ConfigurationError("Failed to write token store file.") from err
        finally:
            try:
                if "tmp_path" in locals() and tmp_path.exists():
                    tmp_path.unlink(missing_ok=True)
            except OSError:
                # Best-effort cleanup.
                pass


@dataclass(frozen=True, slots=True)
class OAuthToken:
    """OAuth token container."""

    access_token: str
    refresh_token: str | None = None
    expires_at: datetime | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.access_token, str) or not self.access_token:
            raise ValidationError("Field 'access_token' must be a non-empty string.")

        if self.refresh_token is not None and (
            not isinstance(self.refresh_token, str) or not self.refresh_token
        ):
            raise ValidationError("Field 'refresh_token' must be a non-empty string when provided.")

        if self.expires_at is not None and not isinstance(self.expires_at, datetime):
            raise ValidationError("Field 'expires_at' must be a datetime instance when provided.")

    def is_expired(self, *, at: datetime | None = None) -> bool:
        if self.expires_at is None:
            return False

        now = at or datetime.now()
        return self.expires_at <= now

    def to_dict(self) -> dict[str, Any]:
        return {
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_at": format_wfirma_datetime(self.expires_at),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "OAuthToken":
        if not isinstance(data, dict):
            raise ValidationError("Token payload must be a dictionary.")

        access_token: str = data.get("access_token", "")
        refresh_token: str | None = data.get("refresh_token")

        expires_at_raw = data.get("expires_at")
        try:
            expires_at = parse_wfirma_datetime(expires_at_raw)
        except ValueError as err:
            raise ValidationError(
                "Field 'expires_at' must be a datetime or wFirma datetime string."
            ) from err

        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at=expires_at,
        )


__all__ = [
    "TokenStore",
    "MemoryTokenStore",
    "FileTokenStore",
    "OAuthToken",
]
