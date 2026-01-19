"""Tests for asynchronous token store implementations.

Even though the store itself is synchronous (in-memory data structure), we keep
separate async tests for symmetry with the async API surface.
"""

from __future__ import annotations

from datetime import datetime

import pytest

from wfirma.async_.auth import MemoryTokenStore, OAuthToken


# AICOMPLETE: Async token store behavior tested (CRUD, key separation) - ready for review
class TestMemoryTokenStore:
    def test_get_returns_none_for_missing_key(self) -> None:
        store = MemoryTokenStore()
        assert store.get("missing") is None

    def test_set_then_get_returns_same_token(self) -> None:
        store = MemoryTokenStore()
        token = OAuthToken(access_token="access", refresh_token="refresh")

        store.set("default", token)

        assert store.get("default") == token

    def test_delete_removes_token(self) -> None:
        store = MemoryTokenStore()
        token = OAuthToken(access_token="access")
        store.set("default", token)

        store.delete("default")

        assert store.get("default") is None

    def test_clear_removes_all_tokens(self) -> None:
        store = MemoryTokenStore()
        store.set("one", OAuthToken(access_token="a"))
        store.set("two", OAuthToken(access_token="b"))

        store.clear()

        assert store.get("one") is None
        assert store.get("two") is None

    def test_key_separation_multiple_keys(self) -> None:
        store = MemoryTokenStore()
        token_1 = OAuthToken(access_token="a")
        token_2 = OAuthToken(access_token="b")

        store.set("one", token_1)
        store.set("two", token_2)

        assert store.get("one") == token_1
        assert store.get("two") == token_2

    def test_set_overwrites_existing_key(self) -> None:
        store = MemoryTokenStore()
        store.set("default", OAuthToken(access_token="a"))
        store.set("default", OAuthToken(access_token="b"))

        assert store.get("default") == OAuthToken(access_token="b")

    def test_token_can_contain_expires_at(self) -> None:
        store = MemoryTokenStore()
        expires_at = datetime(2030, 1, 1, 12, 0, 0)
        token = OAuthToken(access_token="a", expires_at=expires_at)

        store.set("default", token)

        assert store.get("default") == token

    def test_get_raises_type_error_for_non_str_key(self) -> None:
        store = MemoryTokenStore()

        with pytest.raises(TypeError):
            store.get(123)  # type: ignore[arg-type]
