"""Tests for asynchronous HTTP client.

This module contains unit tests for the async base HTTP client that communicates
with the wFirma API.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth, OAuth2Auth, OAuthToken
from wfirma.config import Environment
from wfirma.exceptions import (
    AuthenticationError,
    BadRequestError,
    ConnectionError,
    RateLimitError,
    ResourceNotFoundError,
    ServerError,
    ServiceUnavailableError,
    TimeoutError,
    ValidationError,
)


class TestWFirmaClientInitialization:
    # AICOMPLETE: Client initialization tests - ready for review

    @pytest.mark.asyncio
    async def test_client_initializes_with_api_key_auth(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth)

        assert client.auth is auth
        assert client.environment == Environment.PRODUCTION
        assert client.company_id is None

    @pytest.mark.asyncio
    async def test_client_initializes_with_oauth2_auth(self) -> None:
        from wfirma.async_.client import WFirmaClient
        from wfirma.auth.common import MemoryTokenStore

        store = MemoryTokenStore()
        store.set("default", OAuthToken(access_token="token123"))
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=store,
        )
        client = WFirmaClient(auth=auth)

        assert client.auth is auth
        assert client.environment == Environment.PRODUCTION

    @pytest.mark.asyncio
    async def test_client_uses_sandbox_environment(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, environment=Environment.SANDBOX)

        assert client.environment == Environment.SANDBOX
        assert "sandbox" in client.base_url

    @pytest.mark.asyncio
    async def test_client_uses_production_environment_by_default(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth)

        assert client.environment == Environment.PRODUCTION
        assert client.base_url == "https://api2.wfirma.pl"

    @pytest.mark.asyncio
    async def test_client_accepts_company_id(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, company_id=12345)

        assert client.company_id == 12345

    @pytest.mark.asyncio
    async def test_client_accepts_timeout_setting(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, timeout=60.0)

        assert client.timeout == 60.0

    @pytest.mark.asyncio
    async def test_client_uses_default_timeout(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth)

        assert client.timeout == 30.0


class TestWFirmaClientHTTPMethods:
    # AICOMPLETE: HTTP method tests - ready for review

    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        from wfirma.async_.client import WFirmaClient

        self.auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        self.client = WFirmaClient(auth=self.auth)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_request_sends_authentication_headers(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={
                    "users": {"0": {"user": {"id": "123", "login": "test@example.com"}}},
                    "status": {"code": "OK"},
                },
            )
        )

        await self.client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert request.headers["accessKey"] == "ak"
        assert request.headers["secretKey"] == "sk"
        assert request.headers["appKey"] == "appk"

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_request_returns_response_data(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={
                    "users": {"0": {"user": {"id": "123", "login": "test@example.com"}}},
                    "status": {"code": "OK"},
                },
            )
        )

        result = await self.client.get("/users/get/123")

        assert result["status"]["code"] == "OK"
        assert result["users"]["0"]["user"]["id"] == "123"

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_request_sends_json_body(self) -> None:
        route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                json={
                    "contractors": {"0": {"contractor": {"id": "456", "name": "Test"}}},
                    "status": {"code": "OK"},
                },
            )
        )

        data = {
            "contractors": {
                "0": {
                    "contractor": {
                        "name": "Test",
                        "zip": "12-345",
                        "country": "PL",
                    }
                }
            }
        }
        await self.client.post("/contractors/add", json=data)

        assert route.called
        request = route.calls.last.request
        assert "contractors" in request.content.decode()

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_request_sends_xml_body(self) -> None:
        route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                text="""<?xml version="1.0" encoding="UTF-8"?>
                <api>
                    <contractors>
                        <contractor><id>456</id></contractor>
                    </contractors>
                    <status><code>OK</code></status>
                </api>""",
            )
        )

        xml_data = """<?xml version="1.0" encoding="UTF-8"?>
        <api>
            <contractors>
                <contractor><name>Test</name></contractor>
            </contractors>
        </api>"""
        await self.client.post("/contractors/add", content=xml_data, content_type="application/xml")

        assert route.called
        request = route.calls.last.request
        assert request.headers["Content-Type"] == "application/xml"

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_request_adds_company_id_parameter(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OK"}},
            )
        )

        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, company_id=999)

        await client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "company_id=999" in str(request.url)


    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_returns_bytes(self) -> None:
        binary_content = b"PDF content here"
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(200, content=binary_content)
        )

        result = await self.client.get_binary("/invoices/download/123")

        assert isinstance(result, bytes)
        assert result == binary_content

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_returns_bytes(self) -> None:
        binary_content = b"PDF file data"
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(200, content=binary_content)
        )

        result = await self.client.post_binary(
            "/documents/generate",
            data={"document_id": "123"},
        )

        assert isinstance(result, bytes)
        assert result == binary_content

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_raises_on_429(self) -> None:
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(429)
        )

        with pytest.raises(RateLimitError):
            await self.client.get_binary("/invoices/download/123")

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_raises_on_503(self) -> None:
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(503)
        )

        with pytest.raises(ServiceUnavailableError):
            await self.client.get_binary("/invoices/download/123")

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_raises_on_500(self) -> None:
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(500)
        )

        with pytest.raises(ServerError):
            await self.client.get_binary("/invoices/download/123")

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_raises_on_429(self) -> None:
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(429)
        )

        with pytest.raises(RateLimitError):
            await self.client.post_binary("/documents/generate", data={"doc_id": "1"})

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_raises_on_503(self) -> None:
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(503)
        )

        with pytest.raises(ServiceUnavailableError):
            await self.client.post_binary("/documents/generate", data={"doc_id": "1"})

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_raises_on_500(self) -> None:
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(500)
        )

        with pytest.raises(ServerError):
            await self.client.post_binary("/documents/generate", data={"doc_id": "1"})


    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_returns_bytes(self) -> None:
        binary_content = b"PDF content here"
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(200, content=binary_content)
        )

        result = await self.client.get_binary("/invoices/download/123")

        assert isinstance(result, bytes)
        assert result == binary_content

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_returns_bytes(self) -> None:
        binary_content = b"PDF file data"
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(200, content=binary_content)
        )

        result = await self.client.post_binary(
            "/documents/generate",
            data={"document_id": "123"},
        )

        assert isinstance(result, bytes)
        assert result == binary_content

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_raises_on_429(self) -> None:
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(429)
        )

        with pytest.raises(RateLimitError):
            await self.client.get_binary("/invoices/download/123")

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_raises_on_503(self) -> None:
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(503)
        )

        with pytest.raises(ServiceUnavailableError):
            await self.client.get_binary("/invoices/download/123")

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_binary_raises_on_500(self) -> None:
        respx.get("https://api2.wfirma.pl/invoices/download/123").mock(
            return_value=httpx.Response(500)
        )

        with pytest.raises(ServerError):
            await self.client.get_binary("/invoices/download/123")

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_raises_on_429(self) -> None:
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(429)
        )

        with pytest.raises(RateLimitError):
            await self.client.post_binary("/documents/generate", data={"doc_id": "1"})

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_raises_on_503(self) -> None:
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(503)
        )

        with pytest.raises(ServiceUnavailableError):
            await self.client.post_binary("/documents/generate", data={"doc_id": "1"})

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_binary_raises_on_500(self) -> None:
        respx.post("https://api2.wfirma.pl/documents/generate").mock(
            return_value=httpx.Response(500)
        )

        with pytest.raises(ServerError):
            await self.client.post_binary("/documents/generate", data={"doc_id": "1"})


class TestWFirmaClientErrorHandling:
    # AICOMPLETE: Error handling tests - ready for review

    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        from wfirma.async_.client import WFirmaClient

        self.auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        self.client = WFirmaClient(auth=self.auth)

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_authentication_error_auth(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "AUTH"}},
            )
        )

        with pytest.raises(AuthenticationError, match="Authentication failed"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_authentication_error_limit(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "AUTH FAILED LIMIT WAIT 5 MINUTES"}},
            )
        )

        with pytest.raises(AuthenticationError, match="Authentication failed"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_denied_scope_requested(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "DENIED SCOPE REQUESTED"}},
            )
        )

        with pytest.raises(AuthenticationError, match="Access denied"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_access_denied(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "ACCESS DENIED"}},
            )
        )

        with pytest.raises(AuthenticationError, match="Access denied"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_not_found(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "NOT FOUND"}},
            )
        )

        with pytest.raises(ResourceNotFoundError, match="Resource not found"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_action_not_found(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "ACTION NOT FOUND"}},
            )
        )

        with pytest.raises(ResourceNotFoundError, match="Action not found"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_input_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "INPUT ERROR"}},
            )
        )

        with pytest.raises(BadRequestError, match="Invalid input"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_validation_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "ERROR"}},
            )
        )

        with pytest.raises(ValidationError, match="Validation error"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_fatal_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "FATAL"}},
            )
        )

        with pytest.raises(ServerError, match="Internal server error"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_out_of_service(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OUT OF SERVICE"}},
            )
        )

        with pytest.raises(ServiceUnavailableError, match="Service unavailable"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_snapshot_lock(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "SNAPSHOT LOCK"}},
            )
        )

        with pytest.raises(ServiceUnavailableError, match="Service locked"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_rate_limit_exceeded(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "TOTAL REQUESTS LIMIT EXCEEDED"}},
            )
        )

        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_http_429_rate_limit(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(return_value=httpx.Response(429))

        with pytest.raises(RateLimitError, match="Rate limit exceeded"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_http_500_server_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(return_value=httpx.Response(500))

        with pytest.raises(ServerError, match="Server error"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_http_503_service_unavailable(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(return_value=httpx.Response(503))

        with pytest.raises(ServiceUnavailableError, match="Service unavailable"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_timeout_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(side_effect=httpx.TimeoutException("Timeout"))

        with pytest.raises(TimeoutError, match="Request timed out"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_connection_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            side_effect=httpx.ConnectError("Connection failed")
        )

        with pytest.raises(ConnectionError, match="Failed to connect"):
            await self.client.get("/test")

    @pytest.mark.asyncio
    @respx.mock
    async def test_handles_generic_request_error(self) -> None:
        respx.get("https://api2.wfirma.pl/test").mock(
            side_effect=httpx.RequestError("Network error")
        )

        with pytest.raises(ConnectionError, match="Network error"):
            await self.client.get("/test")


class TestWFirmaClientFormatHandling:
    # AICOMPLETE: Format handling tests - ready for review

    @pytest.fixture(autouse=True)
    def setup_method(self) -> None:
        from wfirma.async_.client import WFirmaClient

        self.auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        self.client = WFirmaClient(auth=self.auth)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_json_adds_output_format_parameter(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OK"}, "users": {}},
            )
        )

        await self.client.get_json("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "outputFormat=json" in str(request.url)

    @pytest.mark.asyncio
    @respx.mock
    async def test_get_xml_adds_output_format_parameter(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                text="""<?xml version="1.0" encoding="UTF-8"?>
                <api><status><code>OK</code></status></api>""",
            )
        )

        result = await self.client.get_xml("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "outputFormat=xml" in str(request.url)
        assert "<?xml" in result

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_json_adds_format_parameters(self) -> None:
        route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OK"}},
            )
        )

        await self.client.post_json("/contractors/add", data={"test": "data"})

        assert route.called
        request = route.calls.last.request
        assert "inputFormat=json" in str(request.url)
        assert "outputFormat=json" in str(request.url)

    @pytest.mark.asyncio
    @respx.mock
    async def test_post_xml_adds_format_parameters(self) -> None:
        route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                text="""<?xml version="1.0" encoding="UTF-8"?>
                <api><status><code>OK</code></status></api>""",
            )
        )

        result = await self.client.post_xml("/contractors/add", data="<api></api>")

        assert route.called
        request = route.calls.last.request
        assert "inputFormat=xml" in str(request.url)
        assert "outputFormat=xml" in str(request.url)
        assert "<?xml" in result


class TestWFirmaClientContextManager:
    # AICOMPLETE: Context manager tests - ready for review

    @pytest.mark.asyncio
    async def test_client_can_be_used_as_async_context_manager(self) -> None:
        from wfirma.async_.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

        async with WFirmaClient(auth=auth) as client:
            assert client.auth is auth
            assert client._http_client is not None

    @pytest.mark.asyncio
    @respx.mock
    async def test_client_closes_http_client_on_exit(self) -> None:
        from wfirma.async_.client import WFirmaClient

        respx.get("https://api2.wfirma.pl/test").mock(
            return_value=httpx.Response(200, json={"status": {"code": "OK"}})
        )

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

        async with WFirmaClient(auth=auth) as client:
            await client.get("/test")
            assert not client._http_client.is_closed

        assert client._http_client.is_closed


class TestWFirmaClientOAuth2Integration:
    # AICOMPLETE: OAuth2 integration tests - ready for review

    @pytest.mark.asyncio
    @respx.mock
    async def test_oauth2_auth_adds_bearer_token_header(self) -> None:
        from wfirma.async_.client import WFirmaClient
        from wfirma.auth.common import MemoryTokenStore

        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OK"}},
            )
        )

        store = MemoryTokenStore()
        store.set("default", OAuthToken(access_token="test_token_abc123"))
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=store,
        )

        async with WFirmaClient(auth=auth) as client:
            await client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert request.headers["Authorization"] == "Bearer test_token_abc123"

    @pytest.mark.asyncio
    @respx.mock
    async def test_oauth2_auth_adds_oauth_version_parameter(self) -> None:
        from wfirma.async_.client import WFirmaClient
        from wfirma.auth.common import MemoryTokenStore

        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OK"}},
            )
        )

        store = MemoryTokenStore()
        store.set("default", OAuthToken(access_token="test_token"))
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=store,
        )

        async with WFirmaClient(auth=auth) as client:
            await client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "oauth_version=2" in str(request.url)
