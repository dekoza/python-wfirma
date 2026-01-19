"""Tests for synchronous file-based token store implementation."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from wfirma.exceptions import ConfigurationError, ValidationError
from wfirma.sync.auth import FileTokenStore, OAuthToken


# AICOMPLETE: Sync file token store behavior tested (persist, overwrite, corruption) - ready for review
class TestFileTokenStore:
    def test_get_returns_none_when_file_missing(self, tmp_path: Path) -> None:
        store = FileTokenStore(tmp_path / "tokens.json")
        assert store.get("missing") is None

    def test_set_then_get_persists_to_disk(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        store = FileTokenStore(path)
        token = OAuthToken(access_token="access", refresh_token="refresh")

        store.set("default", token)

        assert path.exists()
        assert store.get("default") == token

        store_2 = FileTokenStore(path)
        assert store_2.get("default") == token

    def test_set_overwrites_existing_key(self, tmp_path: Path) -> None:
        store = FileTokenStore(tmp_path / "tokens.json")
        store.set("default", OAuthToken(access_token="a"))

        store.set("default", OAuthToken(access_token="b"))

        assert store.get("default") == OAuthToken(access_token="b")

    def test_delete_removes_token_and_persists(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        store = FileTokenStore(path)
        store.set("default", OAuthToken(access_token="a"))

        store.delete("default")

        assert store.get("default") is None
        raw = json.loads(path.read_text(encoding="utf-8"))
        assert raw == {}

    def test_clear_removes_all_tokens_and_persists(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        store = FileTokenStore(path)
        store.set("one", OAuthToken(access_token="a"))
        store.set("two", OAuthToken(access_token="b"))

        store.clear()

        assert store.get("one") is None
        assert store.get("two") is None
        assert json.loads(path.read_text(encoding="utf-8")) == {}

    def test_token_with_expires_at_roundtrip(self, tmp_path: Path) -> None:
        store = FileTokenStore(tmp_path / "tokens.json")
        expires_at = datetime(2030, 1, 1, 12, 0, 0)
        token = OAuthToken(access_token="a", expires_at=expires_at)

        store.set("default", token)

        assert store.get("default") == token

    def test_get_raises_type_error_for_non_str_key(self, tmp_path: Path) -> None:
        store = FileTokenStore(tmp_path / "tokens.json")

        with pytest.raises(TypeError):
            store.get(123)  # type: ignore[arg-type]

    def test_corrupt_json_raises_validation_error(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        path.write_text("{not-json", encoding="utf-8")
        store = FileTokenStore(path)

        with pytest.raises(ValidationError):
            store.get("default")

    def test_non_mapping_json_raises_validation_error(self, tmp_path: Path) -> None:
        path = tmp_path / "tokens.json"
        path.write_text("[]", encoding="utf-8")
        store = FileTokenStore(path)

        with pytest.raises(ValidationError):
            store.get("default")

    def test_write_error_raises_configuration_error(self, tmp_path: Path) -> None:
        # Using a directory path as a file should consistently fail when writing.
        store = FileTokenStore(tmp_path)

        with pytest.raises(ConfigurationError):
            store.set("default", OAuthToken(access_token="a"))
