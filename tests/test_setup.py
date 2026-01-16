"""
Basic sanity tests to verify project setup.
"""


def test_project_setup():
    """Test that basic project setup is working."""
    import wfirma

    assert wfirma.__version__ == "0.1.0"


def test_fixture_availability(mock_wfirma_credentials):
    """Test that pytest fixtures are available."""
    assert mock_wfirma_credentials["app_key"] == "test_app_key"
    assert mock_wfirma_credentials["secret"] == "test_secret"
    assert mock_wfirma_credentials["environment"] == "sandbox"

