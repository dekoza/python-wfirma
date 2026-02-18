"""Tests for WFirmaClient.translation_languages property (sync).

These tests verify that the client property returns the correct resource
instance and maintains proper caching.
"""

from __future__ import annotations

import pytest

from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.translation_languages import TranslationLanguagesResource

pytestmark = pytest.mark.aicomplete


class TestClientTranslationLanguagesProperty:
    """Tests for WFirmaClient.translation_languages property."""

    def test_translation_languages_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        resource = client.translation_languages

        client.close()

        assert isinstance(resource, TranslationLanguagesResource)

    def test_translation_languages_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)

        first = client.translation_languages
        second = client.translation_languages

        client.close()

        assert first is second
