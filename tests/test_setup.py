"""
Basic sanity tests to verify project setup.
"""


def test_project_setup():
    """Test that basic project setup is working."""
    import wfirma

    assert wfirma.__version__ == "0.1.0"


def test_fixture_availability(wfirma_config_data, api_key_auth_data):
    """Test that pytest fixtures are available."""
    assert wfirma_config_data["app_key"] == "test_app_key"
    assert wfirma_config_data["app_secret"] == "test_app_secret"
    assert wfirma_config_data["environment"] == "sandbox"

    assert api_key_auth_data["access_key"] == "test_access_key"
    assert api_key_auth_data["secret_key"] == "test_secret_key"
    assert api_key_auth_data["app_key"] == "test_app_key"
