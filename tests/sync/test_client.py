"""Tests for synchronous HTTP client.

This module contains unit tests for the base HTTP client that communicates
with the wFirma API.
"""

from __future__ import annotations

import httpx
import pytest
import respx

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
from wfirma.sync.auth import APIKeyAuth, OAuth2Auth, OAuthToken


@pytest.mark.aicomplete
class TestWFirmaClientInitialization:
    def test_client_initializes_with_api_key_auth(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth)

        assert client.auth is auth
        assert client.environment == Environment.PRODUCTION
        assert client.company_id is None

    def test_client_initializes_with_oauth2_auth(self) -> None:
        from wfirma.auth.common import MemoryTokenStore
        from wfirma.sync.client import WFirmaClient

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

    def test_client_uses_sandbox_environment(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, environment=Environment.SANDBOX)

        assert client.environment == Environment.SANDBOX
        assert "sandbox" in client.base_url

    def test_client_uses_production_environment_by_default(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth)

        assert client.environment == Environment.PRODUCTION
        assert client.base_url == "https://api2.wfirma.pl"

    def test_client_accepts_company_id(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, company_id=12345)

        assert client.company_id == 12345

    def test_client_accepts_timeout_setting(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth, timeout=60.0)

        assert client.timeout == 60.0

    def test_client_uses_default_timeout(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        client = WFirmaClient(auth=auth)

        assert client.timeout == 30.0


class TestWFirmaClientHTTPMethods:
    # AICOMPLETE: HTTP method tests - ready for review

    def setup_method(self) -> None:
        from wfirma.sync.client import WFirmaClient

        self.auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        self.client = WFirmaClient(auth=self.auth)

    @respx.mock
    def test_get_request_sends_authentication_headers(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={
                    "users": {"0": {"user": {"id": "123", "login": "test@example.com"}}},
                    "status": {"code": "OK"},
                },
            )
        )

        self.client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert request.headers["accessKey"] == "ak"
        assert request.headers["secretKey"] == "sk"
        assert request.headers["appKey"] == "appk"

    @respx.mock
    def test_get_request_returns_response_data(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={
                    "users": {"0": {"user": {"id": "123", "login": "test@example.com"}}},
                    "status": {"code": "OK"},
                },
            )
        )

        result = self.client.get("/users/get/123")

        assert result["status"]["code"] == "OK"
        assert result["users"]["0"]["user"]["id"] == "123"

    @respx.mock
    def test_post_request_sends_json_body(self) -> None:
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
        self.client.post("/contractors/add", json=data)

        assert route.called
        request = route.calls.last.request
        assert "contractors" in request.content.decode()

    @respx.mock
    def test_post_request_sends_xml_body(self) -> None:
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
        self.client.post("/contractors/add", content=xml_data, content_type="application/xml")

        assert route.called
        request = route.calls.last.request
        assert b"<contractor>" in request.content

    @respx.mock
    def test_get_request_adds_query_params(self) -> None:
        route = respx.get("https://api2.wfirma.pl/invoices/find").mock(
            return_value=httpx.Response(
                200,
                json={"invoices": {}, "status": {"code": "OK"}},
            )
        )

        self.client.get("/invoices/find", params={"outputFormat": "json", "page": "1"})

        assert route.called
        request = route.calls.last.request
        assert "outputFormat=json" in str(request.url)
        assert "page=1" in str(request.url)

    @respx.mock
    def test_request_includes_company_id_when_set(self) -> None:
        from wfirma.sync.client import WFirmaClient

        client = WFirmaClient(auth=self.auth, company_id=999)
        route = respx.get("https://api2.wfirma.pl/invoices/find").mock(
            return_value=httpx.Response(
                200,
                json={"invoices": {}, "status": {"code": "OK"}},
            )
        )

        client.get("/invoices/find")

        assert route.called
        request = route.calls.last.request
        assert "company_id=999" in str(request.url)


class TestWFirmaClientErrorHandling:
    # AICOMPLETE: Error handling tests - ready for review

    def setup_method(self) -> None:
        from wfirma.sync.client import WFirmaClient

        self.auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        self.client = WFirmaClient(auth=self.auth)

    @respx.mock
    def test_raises_authentication_error_on_auth_status(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "AUTH"}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            self.client.get("/users/get/123")

        assert "AUTH" in str(exc_info.value)

    @respx.mock
    def test_raises_authentication_error_on_denied_scope(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "DENIED SCOPE REQUESTED"}},
            )
        )

        with pytest.raises(AuthenticationError) as exc_info:
            self.client.get("/users/get/123")

        assert "DENIED SCOPE REQUESTED" in str(exc_info.value)

    @respx.mock
    def test_raises_resource_not_found_error_on_not_found_status(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/999").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "NOT FOUND"}},
            )
        )

        with pytest.raises(ResourceNotFoundError):
            self.client.get("/users/get/999")

    @respx.mock
    def test_raises_bad_request_error_on_input_error(self) -> None:
        respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "INPUT ERROR"}},
            )
        )

        with pytest.raises(BadRequestError):
            self.client.post("/contractors/add", json={})

    @respx.mock
    def test_raises_validation_error_on_error_status_with_errors(self) -> None:
        respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                json={
                    "contractors": {
                        "0": {
                            "contractor": {
                                "errors": {
                                    "0": {
                                        "error": {
                                            "field": "name",
                                            "message": "Field cannot be empty",
                                        }
                                    }
                                }
                            }
                        }
                    },
                    "status": {"code": "ERROR"},
                },
            )
        )

        with pytest.raises(ValidationError):
            self.client.post("/contractors/add", json={})

    @respx.mock
    def test_raises_server_error_on_fatal_status(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "FATAL"}},
            )
        )

        with pytest.raises(ServerError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_service_unavailable_on_out_of_service(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "OUT OF SERVICE"}},
            )
        )

        with pytest.raises(ServiceUnavailableError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_rate_limit_error_on_limit_exceeded(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "TOTAL REQUESTS LIMIT EXCEEDED"}},
            )
        )

        with pytest.raises(RateLimitError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_rate_limit_error_on_execution_time_exceeded(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"status": {"code": "TOTAL EXECUTION TIME LIMIT EXCEEDED"}},
            )
        )

        with pytest.raises(RateLimitError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_rate_limit_error_on_http_429(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(429, text="Too Many Requests")
        )

        with pytest.raises(RateLimitError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_server_error_on_http_500(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(500, text="Internal Server Error")
        )

        with pytest.raises(ServerError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_service_unavailable_on_http_503(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(503, text="Service Unavailable")
        )

        with pytest.raises(ServiceUnavailableError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_timeout_error_on_timeout(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            side_effect=httpx.TimeoutException("Connection timed out")
        )

        with pytest.raises(TimeoutError):
            self.client.get("/users/get/123")

    @respx.mock
    def test_raises_connection_error_on_network_error(self) -> None:
        respx.get("https://api2.wfirma.pl/users/get/123").mock(
            side_effect=httpx.ConnectError("Failed to connect")
        )

        with pytest.raises(ConnectionError):
            self.client.get("/users/get/123")


class TestWFirmaClientFormatHandling:
    # AICOMPLETE: Format handling tests - ready for review

    def setup_method(self) -> None:
        from wfirma.sync.client import WFirmaClient

        self.auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")
        self.client = WFirmaClient(auth=self.auth)

    @respx.mock
    def test_get_json_adds_output_format_param(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"users": {}, "status": {"code": "OK"}},
            )
        )

        self.client.get_json("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "outputFormat=json" in str(request.url)

    @respx.mock
    def test_get_xml_adds_output_format_param(self) -> None:
        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                text="""<?xml version="1.0"?>
                <api><users></users><status><code>OK</code></status></api>""",
            )
        )

        self.client.get_xml("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "outputFormat=xml" in str(request.url)

    @respx.mock
    def test_post_json_sets_format_params(self) -> None:
        route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                json={"contractors": {}, "status": {"code": "OK"}},
            )
        )

        self.client.post_json("/contractors/add", data={"test": "data"})

        assert route.called
        request = route.calls.last.request
        assert "inputFormat=json" in str(request.url)
        assert "outputFormat=json" in str(request.url)

    @respx.mock
    def test_post_xml_sets_format_params(self) -> None:
        route = respx.post("https://api2.wfirma.pl/contractors/add").mock(
            return_value=httpx.Response(
                200,
                text="""<?xml version="1.0"?>
                <api><contractors></contractors><status><code>OK</code></status></api>""",
            )
        )

        self.client.post_xml("/contractors/add", data="<api><test/></api>")

        assert route.called
        request = route.calls.last.request
        assert "inputFormat=xml" in str(request.url)
        assert "outputFormat=xml" in str(request.url)


class TestWFirmaClientContextManager:
    # AICOMPLETE: Context manager tests - ready for review

    def test_client_can_be_used_as_context_manager(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

        with WFirmaClient(auth=auth) as client:
            assert client is not None

    @respx.mock
    def test_client_closes_http_client_on_exit(self) -> None:
        from wfirma.sync.client import WFirmaClient

        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

        with WFirmaClient(auth=auth) as client:
            # Client should be usable inside context
            assert client._http_client is not None

        # After exit, the HTTP client should be closed
        assert client._http_client.is_closed


class TestWFirmaClientOAuth2Integration:
    # AICOMPLETE: OAuth2 integration tests - ready for review

    @respx.mock
    def test_oauth2_auth_sends_bearer_token(self) -> None:
        from wfirma.auth.common import MemoryTokenStore
        from wfirma.sync.client import WFirmaClient

        store = MemoryTokenStore()
        store.set("default", OAuthToken(access_token="my-oauth-token"))
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=store,
        )

        client = WFirmaClient(auth=auth)

        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"users": {}, "status": {"code": "OK"}},
            )
        )

        client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert request.headers["Authorization"] == "Bearer my-oauth-token"

    @respx.mock
    def test_oauth2_auth_adds_oauth_version_param(self) -> None:
        from wfirma.auth.common import MemoryTokenStore
        from wfirma.sync.client import WFirmaClient

        store = MemoryTokenStore()
        store.set("default", OAuthToken(access_token="my-oauth-token"))
        auth = OAuth2Auth(
            client_id="cid",
            client_secret="csecret",
            redirect_uri="https://app.local/callback",
            environment=Environment.PRODUCTION,
            token_store=store,
        )

        client = WFirmaClient(auth=auth)

        route = respx.get("https://api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={"users": {}, "status": {"code": "OK"}},
            )
        )

        client.get("/users/get/123")

        assert route.called
        request = route.calls.last.request
        assert "oauth_version=2" in str(request.url)
