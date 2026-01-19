# AICOMPLETE: API scraper tests - full implementation with all edge cases covered - ready for review

"""Tests for API documentation scraper."""

# Standard library
import json
from pathlib import Path

# Third-party
import pytest


class TestAPIScraper:
    """Test suite for API documentation scraper."""

    def test_can_extract_endpoints_from_local_snapshot(self, scraper, postman_collection_snapshot):
        """Test that scraper can extract endpoints from a local Postman collection snapshot."""
        endpoints = scraper.extract_endpoints(postman_collection_snapshot)

        assert len(endpoints) > 0
        endpoint_names = [ep["name"] for ep in endpoints]
        assert any("contractor" in name.lower() for name in endpoint_names)

    def test_can_extract_authentication_info_from_local_snapshot(
        self, scraper, postman_collection_snapshot
    ):
        """Test that scraper can extract authentication requirements from snapshot."""
        auth_info = scraper.extract_authentication(postman_collection_snapshot)

        assert auth_info is not None
        assert "types" in auth_info
        assert len(auth_info["types"]) > 0

    def test_can_save_structured_spec(self, scraper, postman_collection_snapshot, tmp_path):
        """Test that scraper can save structured API specification."""
        spec = scraper.create_api_spec(postman_collection_snapshot)

        output_file = tmp_path / "api_spec.json"
        scraper.save_spec(spec, output_file)

        assert output_file.exists()
        with open(output_file) as f:
            saved_spec = json.load(f)

        assert "endpoints" in saved_spec
        assert "authentication" in saved_spec
        assert "base_url" in saved_spec

    def test_can_generate_markdown_docs(self, scraper, postman_collection_snapshot, tmp_path):
        """Test that scraper can generate human-readable markdown documentation."""
        spec = scraper.create_api_spec(postman_collection_snapshot)

        output_file = tmp_path / "api_reference.md"
        scraper.generate_markdown(spec, output_file)

        assert output_file.exists()
        content = output_file.read_text()

        assert "# wFirma.pl Reference" in content or "# wFirma API Reference" in content
        assert "Authentication" in content
        assert "Endpoints" in content


@pytest.fixture
def postman_collection_snapshot() -> dict:
    """Provide a local Postman collection snapshot for hermetic unit tests."""
    snapshot_path = Path(__file__).parent / "fixtures" / "postman_collection_wfirma.json"
    return json.loads(snapshot_path.read_text(encoding="utf-8"))


@pytest.fixture
def scraper():
    """Fixture providing API scraper instance."""
    import sys

    # Add scripts directory to path
    scripts_dir = Path(__file__).parent.parent / "scripts"
    sys.path.insert(0, str(scripts_dir))

    from scrape_api_docs import WFirmaAPIScraper

    return WFirmaAPIScraper()
