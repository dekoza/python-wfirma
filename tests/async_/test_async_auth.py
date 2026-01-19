"""Tests for asynchronous authentication helpers.

These tests cover pure token logic only (no HTTP).
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError
from datetime import datetime, timedelta
from urllib.parse import parse_qs, urlparse

import httpx
import pytest
import respx

from wfirma.async_.auth import OAuth1Auth, OAuth2Auth, OAuthToken
from wfirma.auth.common import MemoryTokenStore
from wfirma.config import Environment
from wfirma.exceptions import MissingConfigurationError, TokenExpiredError, ValidationError


class TestOAuthToken:
    # AICOMPLETE: OAuth token model (async) - ready for review

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


class TestOAuth2Auth:
    # AICOMPLETE: OAuth2 async flow (exchange, reuse, refresh) - ready for review

    def setup_method(self) -> None:
        self.store = MemoryTokenStore()

    @respx.mock
    async def test_exchange_code_stores_token(self) -> None:
        route = respx.post("https://api2.wfirma.pl/oauth2/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "acc", "refresh_token": "ref", "expires_in": 1200},
            )
        )
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        token = await auth.exchange_code("code-123")

        assert token.access_token == "acc"
        assert token.refresh_token == "ref"
        assert token.expires_at is not None
        assert self.store.get("default") == token
        assert route.called

    @respx.mock
    async def test_get_token_returns_cached_when_valid(self) -> None:
        expires_at = datetime.now() + timedelta(minutes=5)
        cached = OAuthToken(access_token="cached", refresh_token="ref", expires_at=expires_at)
        self.store.set("default", cached)
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        token = await auth.get_token()

        assert token == cached

    @respx.mock
    async def test_get_token_refreshes_when_expired(self) -> None:
        expired = OAuthToken(
            access_token="old",
            refresh_token="refresh-me",
            expires_at=datetime.now() - timedelta(seconds=1),
        )
        self.store.set("default", expired)
        route = respx.post("https://api2.wfirma.pl/oauth2/token").mock(
            return_value=httpx.Response(
                200,
                json={"access_token": "new", "refresh_token": "new-ref", "expires_in": 600},
            )
        )
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        token = await auth.get_token()

        assert token.access_token == "new"
        assert token.refresh_token == "new-ref"
        assert token.expires_at is not None
        assert self.store.get("default") == token
        assert route.called

    async def test_get_token_raises_when_missing(self) -> None:
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        with pytest.raises(MissingConfigurationError):
            await auth.get_token()

    async def test_get_token_raises_when_expired_without_refresh(self) -> None:
        expired = OAuthToken(access_token="old", refresh_token=None, expires_at=datetime.now())
        self.store.set("default", expired)
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        with pytest.raises(TokenExpiredError):
            await auth.get_token()

    @respx.mock
    async def test_custom_store_key_is_used(self) -> None:
        route = respx.post("https://api2.wfirma.pl/oauth2/token").mock(
            return_value=httpx.Response(200, json={"access_token": "a", "refresh_token": None}),
        )
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
            store_key="company-123",
        )

        await auth.exchange_code("code-123")

        assert self.store.get("company-123").access_token == "a"
        assert route.called

    async def test_sandbox_environment_uses_sandbox_base_url(self) -> None:
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.SANDBOX,
            token_store=self.store,
        )

        assert auth.token_url == "https://sandbox-api2.wfirma.pl/oauth2/token"

    # AICOMPLETE: OAuth2 authorization URL builder (async module) - ready for review
    def test_build_authorization_url_builds_expected_query_params(self) -> None:
        auth = OAuth2Auth(
            client_id="cid-123",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        url = auth.build_authorization_url(scope="invoices-read", state="state-1")

        parsed = urlparse(url)
        assert parsed.scheme == "https"
        assert parsed.netloc == "wfirma.pl"
        assert parsed.path == "/oauth2/auth"

        qs = parse_qs(parsed.query)
        assert qs["response_type"] == ["code"]
        assert qs["client_id"] == ["cid-123"]
        assert qs["redirect_uri"] == ["https://app.local/callback"]
        assert qs["scope"] == ["invoices-read"]
        assert qs["state"] == ["state-1"]

    def test_build_authorization_url_omits_optional_params_when_not_provided(self) -> None:
        auth = OAuth2Auth(
            client_id="cid-123",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        url = auth.build_authorization_url()

        parsed = urlparse(url)
        qs = parse_qs(parsed.query)
        assert qs["response_type"] == ["code"]
        assert qs["client_id"] == ["cid-123"]
        assert qs["redirect_uri"] == ["https://app.local/callback"]
        assert "scope" not in qs
        assert "state" not in qs

    def test_build_authorization_url_encodes_redirect_uri(self) -> None:
        auth = OAuth2Auth(
            client_id="cid-123",
            client_secret="csecret",
            redirect_uri="https://app.local/callback?x=1&y=hello world",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        url = auth.build_authorization_url(scope="invoices-read")

        qs = parse_qs(urlparse(url).query)
        assert qs["redirect_uri"] == ["https://app.local/callback?x=1&y=hello world"]

    def test_build_authorization_url_accepts_scope_as_list(self) -> None:
        auth = OAuth2Auth(
            client_id="cid-123",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        url = auth.build_authorization_url(scope=["invoices-read", "payments-read"])

        qs = parse_qs(urlparse(url).query)
        assert qs["scope"] == ["invoices-read payments-read"]

    @pytest.mark.parametrize("scope", ["", [], [""], [" "]])
    def test_build_authorization_url_rejects_invalid_scope(self, scope) -> None:
        auth = OAuth2Auth(
            client_id="cid-123",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=self.store,
        )

        with pytest.raises(ValidationError):
            auth.build_authorization_url(scope=scope)


class TestOAuth1Auth:
    # AICOMPLETE: OAuth1 async flow (request/access token) - ready for review

    def setup_method(self) -> None:
        self.store = MemoryTokenStore()

    @respx.mock
    async def test_request_and_access_token_flow(self) -> None:
        request_route = respx.get("https://wfirma.pl/oauth/requestToken").mock(
            return_value=httpx.Response(200, text="oauth_token=req&oauth_token_secret=reqsec"),
        )
        access_route = respx.get("https://wfirma.pl/oauth/accessToken").mock(
            return_value=httpx.Response(200, text="oauth_token=acc&oauth_token_secret=accsec"),
        )
        auth = OAuth1Auth(
            consumer_key="ck",
            consumer_secret="cs",
            scope="invoices-read",
            callback_url="https://app.local/callback",
            token_store=self.store,
        )

        request_token = await auth.fetch_request_token()
        authorize_url = auth.build_authorization_url(request_token)
        access_token = await auth.fetch_access_token(
            oauth_token=request_token.access_token,
            oauth_token_secret=request_token.refresh_token or "",
            oauth_verifier="verifier-123",
        )

        assert request_route.called
        assert access_route.called
        assert request_token.access_token == "req"
        assert request_token.refresh_token == "reqsec"
        assert "oauth_token=req" in authorize_url
        assert access_token.access_token == "acc"
        assert access_token.refresh_token == "accsec"
        assert self.store.get("default") == access_token

    def test_parse_qs_matches_helper_used_by_auth(self) -> None:
        parsed = parse_qs("oauth_token=a&oauth_token_secret=b")
        assert parsed["oauth_token"] == ["a"]
        assert parsed["oauth_token_secret"] == ["b"]

    async def test_get_token_raises_when_missing(self) -> None:
        auth = OAuth1Auth(
            consumer_key="ck",
            consumer_secret="cs",
            scope="invoices-read",
            callback_url=None,
            token_store=self.store,
        )

        with pytest.raises(MissingConfigurationError):
            await auth.get_token()

    async def test_fetch_request_token_raises_on_invalid_payload(self) -> None:
        auth = OAuth1Auth(
            consumer_key="ck",
            consumer_secret="cs",
            scope="invoices-read",
            callback_url=None,
            token_store=self.store,
        )

        with pytest.raises(ValidationError):
            auth._parse_oauth1_response("invalid=true")
