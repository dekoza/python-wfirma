"""Tests for OAuth2 network error handling (async auth module)."""

from __future__ import annotations

from unittest.mock import patch

import httpx
import pytest

from wfirma.async_.auth import OAuth2Auth
from wfirma.auth.common import MemoryTokenStore
from wfirma.config import Environment
from wfirma.exceptions import ConnectionError


class TestOAuth2NetworkErrorMappingAsync:
    # AICOMPLETE: OAuth2 network error mapping (async) - ready for review

    async def test_exchange_code_maps_request_error_to_connection_error(self) -> None:
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=MemoryTokenStore(),
        )

        async def raise_connect_error(*args, **kwargs) -> None:  # noqa: ANN002, ANN003
            request = httpx.Request("POST", auth.token_url)
            raise httpx.ConnectError("boom", request=request)

        with (
            patch.object(httpx.AsyncClient, "post", side_effect=raise_connect_error),
            pytest.raises(ConnectionError),
        ):
            await auth.exchange_code("code-123")
