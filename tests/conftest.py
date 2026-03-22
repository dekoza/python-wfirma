"""Pytest configuration and shared fixtures."""

from __future__ import annotations

import os

import pytest

from wfirma.async_.auth import APIKeyAuth as AsyncAPIKeyAuth
from wfirma.async_.auth import OAuth2Auth as AsyncOAuth2Auth
from wfirma.async_.client import WFirmaClient as AsyncWFirmaClient
from wfirma.auth.common import MemoryTokenStore, OAuthToken
from wfirma.config import Environment
from wfirma.sync.auth import APIKeyAuth as SyncAPIKeyAuth
from wfirma.sync.auth import OAuth2Auth as SyncOAuth2Auth
from wfirma.sync.client import WFirmaClient as SyncWFirmaClient
from wfirma.tools import WFirmaAPIScraper


@pytest.fixture
def wfirma_config_data() -> dict[str, str]:
    """Provide sample configuration values as strings (as they come from env vars)."""
    return {
        "app_key": "test_app_key",
        "app_secret": "test_app_secret",
        "environment": "sandbox",
    }


@pytest.fixture
def api_key_auth_data() -> dict[str, str]:
    """Provide sample API Key Authentication header values."""
    return {
        "access_key": "test_access_key",
        "secret_key": "test_secret_key",
        "app_key": "test_app_key",
    }


def _integration_enabled(config: pytest.Config) -> bool:
    mark_expression = config.getoption("markexpr") or ""
    return os.environ.get("WFIRMA_RUN_INTEGRATION") == "1" or "integration" in mark_expression


def pytest_collection_modifyitems(config: pytest.Config, items: list[pytest.Item]) -> None:
    """Skip live integration tests unless the user explicitly opts in."""
    if _integration_enabled(config):
        return

    skip_integration = pytest.mark.skip(
        reason=(
            "Integration tests are skipped by default. "
            "Use `pytest -m integration` or set WFIRMA_RUN_INTEGRATION=1 to enable them."
        )
    )
    for item in items:
        if "integration" in item.keywords:
            item.add_marker(skip_integration)


def _get_required_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        pytest.skip(f"Integration test requires environment variable {name}.")
    assert value is not None
    return value


@pytest.fixture
def live_api_scraper() -> WFirmaAPIScraper:
    """Provide the packaged scraper for live integration checks."""
    return WFirmaAPIScraper()


@pytest.fixture
def integration_company_id() -> int:
    """Provide the sandbox company ID used for read-only smoke tests."""
    company_id = _get_required_env("WFIRMA_COMPANY_ID")
    try:
        return int(company_id)
    except ValueError as err:
        raise ValueError("WFIRMA_COMPANY_ID must be an integer.") from err


@pytest.fixture
def live_api_key_sync_client(integration_company_id: int) -> SyncWFirmaClient:
    """Provide a sync client configured for sandbox API key auth."""
    auth = SyncAPIKeyAuth(
        access_key=_get_required_env("WFIRMA_ACCESS_KEY"),
        secret_key=_get_required_env("WFIRMA_SECRET_KEY"),
        app_key=_get_required_env("WFIRMA_APP_KEY"),
    )
    return SyncWFirmaClient(
        auth=auth,
        environment=Environment.SANDBOX,
        company_id=integration_company_id,
    )


@pytest.fixture
def live_api_key_async_client(integration_company_id: int) -> AsyncWFirmaClient:
    """Provide an async client configured for sandbox API key auth."""
    auth = AsyncAPIKeyAuth(
        access_key=_get_required_env("WFIRMA_ACCESS_KEY"),
        secret_key=_get_required_env("WFIRMA_SECRET_KEY"),
        app_key=_get_required_env("WFIRMA_APP_KEY"),
    )
    return AsyncWFirmaClient(
        auth=auth,
        environment=Environment.SANDBOX,
        company_id=integration_company_id,
    )


def _oauth2_token_store() -> MemoryTokenStore:
    store = MemoryTokenStore()
    store.set(
        "integration", OAuthToken(access_token=_get_required_env("WFIRMA_OAUTH2_ACCESS_TOKEN"))
    )
    return store


@pytest.fixture
def live_oauth2_sync_client(integration_company_id: int) -> SyncWFirmaClient:
    """Provide a sync client configured for sandbox OAuth2 bearer auth."""
    auth = SyncOAuth2Auth(
        client_id=_get_required_env("WFIRMA_OAUTH2_CLIENT_ID"),
        client_secret=_get_required_env("WFIRMA_OAUTH2_CLIENT_SECRET"),
        redirect_uri=_get_required_env("WFIRMA_OAUTH2_REDIRECT_URI"),
        environment=Environment.SANDBOX,
        token_store=_oauth2_token_store(),
        store_key="integration",
    )
    return SyncWFirmaClient(
        auth=auth,
        environment=Environment.SANDBOX,
        company_id=integration_company_id,
    )


@pytest.fixture
def live_oauth2_async_client(integration_company_id: int) -> AsyncWFirmaClient:
    """Provide an async client configured for sandbox OAuth2 bearer auth."""
    auth = AsyncOAuth2Auth(
        client_id=_get_required_env("WFIRMA_OAUTH2_CLIENT_ID"),
        client_secret=_get_required_env("WFIRMA_OAUTH2_CLIENT_SECRET"),
        redirect_uri=_get_required_env("WFIRMA_OAUTH2_REDIRECT_URI"),
        environment=Environment.SANDBOX,
        token_store=_oauth2_token_store(),
        store_key="integration",
    )
    return AsyncWFirmaClient(
        auth=auth,
        environment=Environment.SANDBOX,
        company_id=integration_company_id,
    )
