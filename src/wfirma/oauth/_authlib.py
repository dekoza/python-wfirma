"""Authlib-based OAuth adapters.

This module is an internal integration layer between Authlib and the public
`synchronous`/`asynchronous` auth helpers.

We keep our own `TokenStore` abstraction to control persistence and keep a stable,
well-tested storage format.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from authlib.integrations.httpx_client import AsyncOAuth2Client, OAuth2Client

from wfirma.auth.common import OAuthToken, TokenStore
from wfirma.exceptions import ValidationError


def _raise_as_http_status_error(err: Exception) -> None:
    """Convert an Authlib OAuth error into an httpx.HTTPStatusError.

    Note:
        Authlib's OAuthError raised for 4xx token responses does not include the
        underlying httpx.Response instance. Higher layers should map it directly
        to wfirma AuthenticationError.
    """
    raise err


def _persist_token_sync(*, store: TokenStore, key: str, token: dict[str, Any]) -> None:
    store.set(key, _authlib_dict_to_token(token))


async def _persist_token_async(
    *, store: TokenStore, key: str, token: dict[str, Any], **_: Any
) -> None:
    store.set(key, _authlib_dict_to_token(token))


def _token_to_authlib_dict(token: OAuthToken) -> dict[str, Any]:
    """Convert our token model to an Authlib-compatible token dictionary."""

    payload: dict[str, Any] = {"access_token": token.access_token}
    if token.refresh_token is not None:
        payload["refresh_token"] = token.refresh_token

    if token.expires_at is not None:
        # Authlib uses `expires_at` as UNIX timestamp (seconds).
        payload["expires_at"] = int(token.expires_at.timestamp())

    return payload


def _authlib_dict_to_token(data: dict[str, Any]) -> OAuthToken:
    """Convert Authlib token dictionary to our `OAuthToken` model."""

    return OAuthToken.from_oauth2_response(data)


@dataclass(slots=True)
class SyncOAuth2Backend:
    """Small adapter around Authlib `OAuth2Client` for wFirma OAuth2."""

    client_id: str
    client_secret: str
    token_url: str
    redirect_uri: str
    token_store: TokenStore
    store_key: str

    def _client(self):
        token = self.token_store.get(self.store_key)
        token_dict = _token_to_authlib_dict(token) if token is not None else None

        return OAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=token_dict,
            redirect_uri=self.redirect_uri,
            update_token=lambda t, **_: _persist_token_sync(
                store=self.token_store, key=self.store_key, token=t
            ),
        )

    def exchange_code(self, *, code: str) -> OAuthToken:
        if not isinstance(code, str) or not code:
            raise ValidationError("Field 'code' must be a non-empty string.")

        try:
            with self._client() as client:
                token = client.fetch_token(
                    url=self.token_url,
                    grant_type="authorization_code",
                    code=code,
                    redirect_uri=self.redirect_uri,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
        except Exception:
            # Authlib raises OAuthError (without httpx.Response) for 4xx responses.
            raise

        return _authlib_dict_to_token(token)

    def refresh(self, *, refresh_token: str) -> OAuthToken:
        if not isinstance(refresh_token, str) or not refresh_token:
            raise ValidationError("Field 'refresh_token' must be a non-empty string.")

        try:
            with self._client() as client:
                token = client.refresh_token(
                    url=self.token_url,
                    refresh_token=refresh_token,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
        except Exception as err:
            if err.__class__.__name__ == "OAuthError":
                _raise_as_http_status_error(err)
            raise

        return _authlib_dict_to_token(token)


@dataclass(slots=True)
class AsyncOAuth2Backend:
    """Small adapter around Authlib `AsyncOAuth2Client` for wFirma OAuth2."""

    client_id: str
    client_secret: str
    token_url: str
    redirect_uri: str
    token_store: TokenStore
    store_key: str

    async def _client(self):
        token = self.token_store.get(self.store_key)
        token_dict = _token_to_authlib_dict(token) if token is not None else None

        async def _update_token(token_data: dict[str, Any], **kwargs: Any) -> None:
            await _persist_token_async(
                store=self.token_store,
                key=self.store_key,
                token=token_data,
                **kwargs,
            )

        return AsyncOAuth2Client(
            client_id=self.client_id,
            client_secret=self.client_secret,
            token=token_dict,
            redirect_uri=self.redirect_uri,
            update_token=_update_token,
        )

    async def exchange_code(self, *, code: str) -> OAuthToken:
        if not isinstance(code, str) or not code:
            raise ValidationError("Field 'code' must be a non-empty string.")

        client = await self._client()
        try:
            async with client:
                token = await client.fetch_token(
                    url=self.token_url,
                    grant_type="authorization_code",
                    code=code,
                    redirect_uri=self.redirect_uri,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
        except Exception as err:
            if err.__class__.__name__ == "OAuthError":
                _raise_as_http_status_error(err)
            raise

        return _authlib_dict_to_token(token)

    async def refresh(self, *, refresh_token: str) -> OAuthToken:
        if not isinstance(refresh_token, str) or not refresh_token:
            raise ValidationError("Field 'refresh_token' must be a non-empty string.")

        client = await self._client()
        try:
            async with client:
                token = await client.refresh_token(
                    url=self.token_url,
                    refresh_token=refresh_token,
                    client_id=self.client_id,
                    client_secret=self.client_secret,
                )
        except Exception as err:
            if err.__class__.__name__ == "OAuthError":
                _raise_as_http_status_error(err)
            raise

        return _authlib_dict_to_token(token)
