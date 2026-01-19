"""Unit tests for OAuth 1.0a signing primitives.

These helpers are shared between sync and async authentication layers.
"""

from __future__ import annotations

import pytest

from wfirma.auth.common import (
    OAuthToken,
    build_oauth1_authorization_header,
    oauth_percent_encode,
    sign_oauth1_plaintext,
)
from wfirma.exceptions import ValidationError


class TestOAuthPercentEncode:
    # AICOMPLETE: OAuth percent encoding - ready for review

    def test_encodes_space_as_percent_20_not_plus(self) -> None:
        assert oauth_percent_encode("a b") == "a%20b"

    def test_encodes_tilde_as_literal(self) -> None:
        assert oauth_percent_encode("~") == "~"

    def test_encodes_reserved_characters(self) -> None:
        assert oauth_percent_encode("!*()'") == "%21%2A%28%29%27"

    @pytest.mark.parametrize("value", [None, 123, [], {}])
    def test_rejects_non_string(self, value) -> None:
        with pytest.raises(ValidationError):
            oauth_percent_encode(value)  # type: ignore[arg-type]


class TestOAuth1PlaintextSignature:
    # AICOMPLETE: OAuth1 PLAINTEXT signature - ready for review

    def test_signs_consumer_and_token_secrets(self) -> None:
        assert sign_oauth1_plaintext(consumer_secret="cs", token_secret="ts") == "cs&ts"

    def test_signs_consumer_only_when_no_token_secret(self) -> None:
        assert sign_oauth1_plaintext(consumer_secret="cs", token_secret=None) == "cs&"

    def test_percent_encodes_secrets(self) -> None:
        assert sign_oauth1_plaintext(consumer_secret="c s", token_secret="t/s") == "c%20s&t%2Fs"

    @pytest.mark.parametrize("value", ["", None, 123])
    def test_validates_consumer_secret(self, value) -> None:
        with pytest.raises(ValidationError):
            sign_oauth1_plaintext(consumer_secret=value, token_secret="ts")  # type: ignore[arg-type]

    @pytest.mark.parametrize("value", ["", 123, []])
    def test_validates_token_secret_when_provided(self, value) -> None:
        with pytest.raises(ValidationError):
            sign_oauth1_plaintext(consumer_secret="cs", token_secret=value)  # type: ignore[arg-type]


class TestOAuth1AuthorizationHeader:
    def test_builds_header_with_required_fields(self) -> None:
        token = OAuthToken(access_token="token", refresh_token="secret")
        header = build_oauth1_authorization_header(
            consumer_key="ck",
            consumer_secret="cs",
            token=token,
            nonce="nonce",
            timestamp=123,
        )

        assert header.startswith("OAuth ")
        assert 'oauth_consumer_key="ck"' in header
        assert 'oauth_token="token"' in header
        assert 'oauth_signature_method="PLAINTEXT"' in header
        assert 'oauth_signature="cs%26secret"' in header
        assert 'oauth_timestamp="123"' in header
        assert 'oauth_nonce="nonce"' in header
        assert 'oauth_version="1.0"' in header

    def test_generates_timestamp_when_missing(self) -> None:
        token = OAuthToken(access_token="token", refresh_token="secret")
        header = build_oauth1_authorization_header(
            consumer_key="ck",
            consumer_secret="cs",
            token=token,
            nonce="nonce",
            timestamp=None,
        )

        assert 'oauth_timestamp="' in header

    def test_percent_encodes_parameter_values(self) -> None:
        token = OAuthToken(access_token="t ok", refresh_token="s/cret")
        header = build_oauth1_authorization_header(
            consumer_key="c k",
            consumer_secret="c s",
            token=token,
            nonce="n n",
            timestamp=1,
        )

        assert 'oauth_consumer_key="c%20k"' in header
        assert 'oauth_token="t%20ok"' in header
        assert 'oauth_nonce="n%20n"' in header
        assert 'oauth_signature="c%20s%26s%2Fcret"' in header

    def test_allows_optional_realm(self) -> None:
        token = OAuthToken(access_token="token", refresh_token="secret")
        header = build_oauth1_authorization_header(
            consumer_key="ck",
            consumer_secret="cs",
            token=token,
            nonce="nonce",
            timestamp=1,
            realm="wfirma",
        )

        assert header.startswith('OAuth realm="wfirma", ')

    @pytest.mark.parametrize("value", ["", None, 123])
    def test_validates_consumer_key(self, value) -> None:
        token = OAuthToken(access_token="token", refresh_token="secret")
        with pytest.raises(ValidationError):
            build_oauth1_authorization_header(
                consumer_key=value,  # type: ignore[arg-type]
                consumer_secret="cs",
                token=token,
                nonce="nonce",
                timestamp=1,
            )

    def test_requires_token_secret(self) -> None:
        token = OAuthToken(access_token="token", refresh_token=None)
        with pytest.raises(ValidationError):
            build_oauth1_authorization_header(
                consumer_key="ck",
                consumer_secret="cs",
                token=token,
                nonce="nonce",
                timestamp=1,
            )

    @pytest.mark.parametrize("value", ["", "1", 1.1])
    def test_validates_timestamp(self, value) -> None:
        token = OAuthToken(access_token="token", refresh_token="secret")
        with pytest.raises(ValidationError):
            build_oauth1_authorization_header(
                consumer_key="ck",
                consumer_secret="cs",
                token=token,
                nonce="nonce",
                timestamp=value,  # type: ignore[arg-type]
            )
