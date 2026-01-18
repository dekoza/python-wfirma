"""
Pytest configuration and shared fixtures.
"""

import pytest


@pytest.fixture
def mock_wfirma_credentials():
    """Provide mock wFirma API credentials for testing."""
    return {
        "app_key": "test_app_key",
        "secret": "test_secret",
        "environment": "sandbox",
    }
