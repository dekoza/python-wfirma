"""Tests for OAuth2 error handling.

We intentionally test behaviour at the boundary between the auth helpers and httpx.
The library should raise wfirma-specific exceptions with clear messages.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.auth.common import MemoryTokenStore
from wfirma.config import Environment
from wfirma.exceptions import AuthenticationError
from wfirma.sync.auth import OAuth2Auth


class TestOAuth2ErrorMapping:
    # AICOMPLETE: OAuth2 error mapping - ready for review

    @respx.mock
    def test_exchange_code_maps_http_error_to_authentication_error(self) -> None:
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
            auth.exchange_code("code-123")
