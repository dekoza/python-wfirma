"""
Pytest configuration and shared fixtures.
"""

# Third-party
import pytest


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
