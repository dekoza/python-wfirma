"""Tests for synchronous authentication helpers.

These tests cover pure token logic only (no HTTP).
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta

import pytest

from wfirma.exceptions import ValidationError
from wfirma.sync.auth import OAuthToken


class TestOAuthToken:
    # AICOMPLETE: OAuth token model (sync) - ready for review

    def test_is_expired_returns_false_when_expires_at_in_future(self) -> None:
        now = datetime.now()
        token = OAuthToken(access_token="a", expires_at=now + timedelta(seconds=60))
        assert token.is_expired(at=now) is False

    def test_is_expired_returns_true_when_expires_at_in_past(self) -> None:
        now = datetime.now()
        token = OAuthToken(access_token="a", expires_at=now - timedelta(seconds=1))
        assert token.is_expired(at=now) is True

    def test_is_expired_returns_true_when_expires_at_equals_at(self) -> None:
        now = datetime.now()
        token = OAuthToken(access_token="a", expires_at=now)
        assert token.is_expired(at=now) is True

    def test_is_expired_returns_false_when_no_expiry(self) -> None:
        token = OAuthToken(access_token="a", expires_at=None)
        assert token.is_expired(at=datetime.now()) is False

    def test_is_expired_uses_current_time_when_at_not_provided(self) -> None:
        now = datetime.now()

        expired_token = OAuthToken(access_token="a", expires_at=now - timedelta(seconds=1))
        assert expired_token.is_expired() is True

        valid_token = OAuthToken(access_token="a", expires_at=now + timedelta(seconds=60))
        assert valid_token.is_expired() is False

    def test_to_dict_from_dict_roundtrip(self) -> None:
        expires_at = datetime(2026, 1, 1, 12, 30, 0)
        token = OAuthToken(access_token="a", refresh_token="r", expires_at=expires_at)

        data = token.to_dict()
        restored = OAuthToken.from_dict(data)

        assert restored == token

    def test_to_dict_with_minimal_token(self) -> None:
        token = OAuthToken(access_token="a")
        assert token.to_dict() == {
            "access_token": "a",
            "refresh_token": None,
            "expires_at": None,
        }

    def test_to_dict_serializes_expires_at_as_wfirma_datetime_string(self) -> None:
        token = OAuthToken(
            access_token="a",
            refresh_token="r",
            expires_at=datetime(2026, 1, 1, 12, 30, 0),
        )

        data = token.to_dict()

        assert data["expires_at"] == "2026-01-01 12:30:00"

    def test_from_dict_accepts_expires_at_as_wfirma_datetime_string(self) -> None:
        token = OAuthToken.from_dict(
            {
                "access_token": "a",
                "refresh_token": "r",
                "expires_at": "2026-01-01 12:30:00",
            }
        )

        assert token.expires_at == datetime(2026, 1, 1, 12, 30, 0)

    def test_from_dict_accepts_expires_at_as_datetime(self) -> None:
        expires_at = datetime(2026, 1, 1, 12, 30, 0)
        token = OAuthToken.from_dict(
            {
                "access_token": "a",
                "refresh_token": "r",
                "expires_at": expires_at,
            }
        )

        assert token.expires_at == expires_at

    def test_from_dict_accepts_expires_at_as_none(self) -> None:
        token = OAuthToken.from_dict({"access_token": "a", "expires_at": None})
        assert token.expires_at is None

    @pytest.mark.parametrize(
        "payload",
        [
            {},
            {"access_token": ""},
            {"access_token": None},
            {"access_token": 123},
            {"access_token": []},
        ],
    )
    def test_from_dict_validates_access_token(self, payload) -> None:
        with pytest.raises(ValidationError):
            OAuthToken.from_dict(payload)

    @pytest.mark.parametrize(
        "refresh_token",
        [
            "",
            123,
            [],
        ],
    )
    def test_from_dict_validates_refresh_token_when_provided(self, refresh_token) -> None:
        with pytest.raises(ValidationError):
            OAuthToken.from_dict({"access_token": "a", "refresh_token": refresh_token})

    def test_from_dict_rejects_invalid_expires_at_format(self) -> None:
        with pytest.raises(ValidationError):
            OAuthToken.from_dict({"access_token": "a", "expires_at": "not-a-datetime"})

    @pytest.mark.parametrize("expires_at", [12345, [], {}])
    def test_from_dict_rejects_invalid_expires_at_type(self, expires_at) -> None:
        with pytest.raises(ValidationError):
            OAuthToken.from_dict({"access_token": "a", "expires_at": expires_at})

    def test_equality_compares_all_fields(self) -> None:
        expires_at = datetime(2026, 1, 1, 12, 30, 0)
        token1 = OAuthToken(access_token="a", refresh_token="r", expires_at=expires_at)
        token2 = OAuthToken(access_token="a", refresh_token="r", expires_at=expires_at)
        assert token1 == token2

    def test_inequality_when_fields_differ(self) -> None:
        expires_at = datetime(2026, 1, 1, 12, 30, 0)
        token1 = OAuthToken(access_token="a", refresh_token="r", expires_at=expires_at)
        token2 = OAuthToken(access_token="b", refresh_token="r", expires_at=expires_at)
        assert token1 != token2

    def test_token_is_immutable(self) -> None:
        token = OAuthToken(access_token="a")
        with pytest.raises(FrozenInstanceError):
            token.access_token = "b"  # type: ignore[misc]
