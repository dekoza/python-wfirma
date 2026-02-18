"""Tests for WFirmaClient.translation_languages property (async).

These tests verify that the client property returns the correct resource
instance and maintains proper caching.
"""

from __future__ import annotations

import pytest

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.translation_languages import TranslationLanguagesResource

pytestmark = pytest.mark.aicomplete


class TestClientTranslationLanguagesProperty:
    """Tests for WFirmaClient.translation_languages property."""

    async def test_translation_languages_returns_resource(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            resource = client.translation_languages

            assert isinstance(resource, TranslationLanguagesResource)

    async def test_translation_languages_is_cached(self) -> None:
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        async with WFirmaClient(auth=auth, company_id=123) as client:
            first = client.translation_languages
            second = client.translation_languages

            assert first is second
