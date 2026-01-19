"""Unit tests for OAuth 1.0a signing primitives.

These helpers are shared between sync and async authentication layers.
"""

from __future__ import annotations

import pytest

from wfirma.auth.common import (
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
