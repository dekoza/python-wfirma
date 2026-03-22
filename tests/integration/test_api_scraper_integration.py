"""Live integration tests for the public API scraper."""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.integration


def test_fetch_collection_returns_live_postman_payload(live_api_scraper) -> None:
    """The public Postman collection should stay fetchable."""
    collection = live_api_scraper.fetch_collection()

    assert collection["info"]["name"].lower().startswith("wfirma")
    assert isinstance(collection["item"], list)
    assert collection["item"]


def test_create_api_spec_detects_supported_auth_types(live_api_scraper) -> None:
    """The live docs should still advertise all upstream auth modes."""
    spec = live_api_scraper.create_api_spec(live_api_scraper.fetch_collection())

    assert {"apikey", "oauth1", "oauth2"}.issubset(spec["authentication"]["types"])
