"""Tests for OAuth2 error handling (async auth module)."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import OAuth2Auth
from wfirma.auth.common import MemoryTokenStore
from wfirma.config import Environment
from wfirma.exceptions import AuthenticationError


class TestOAuth2ErrorMappingAsync:
    # AICOMPLETE: OAuth2 error mapping (async) - ready for review

    @respx.mock
    async def test_exchange_code_maps_http_error_to_authentication_error(self) -> None:
        respx.post("https://api2.wfirma.pl/oauth2/token").mock(
            return_value=httpx.Response(401, json={"error": "invalid_client"}),
        )
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=MemoryTokenStore(),
        )

        with pytest.raises(AuthenticationError):
            await auth.exchange_code("code-123")
