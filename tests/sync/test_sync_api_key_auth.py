"""Tests for API Key authentication.

These tests cover the API Key authentication mechanism used with wFirma API.
API Key authentication requires 3 keys: accessKey, secretKey, and appKey,
which are sent as HTTP headers with each request.
"""

from __future__ import annotations

import pytest

from wfirma.exceptions import MissingConfigurationError, ValidationError
from wfirma.sync.auth import APIKeyAuth


class TestAPIKeyAuth:
    """Tests for APIKeyAuth class."""

    # AICOMPLETE: API Key authentication - ready for review

    def test_init_with_all_keys(self) -> None:
        """Test initialization with all required keys."""
        auth = APIKeyAuth(
            access_key="my_access_key",
            secret_key="my_secret_key",
            app_key="my_app_key",
        )
        assert auth.access_key == "my_access_key"
        assert auth.secret_key == "my_secret_key"
        assert auth.app_key == "my_app_key"

    def test_init_missing_access_key_raises_error(self) -> None:
        """Test that missing access_key raises MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError) as exc_info:
            APIKeyAuth(
                access_key="",
                secret_key="my_secret_key",
                app_key="my_app_key",
            )
        assert "access_key" in str(exc_info.value)

    def test_init_missing_secret_key_raises_error(self) -> None:
        """Test that missing secret_key raises MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError) as exc_info:
            APIKeyAuth(
                access_key="my_access_key",
                secret_key="",
                app_key="my_app_key",
            )
        assert "secret_key" in str(exc_info.value)

    def test_init_missing_app_key_raises_error(self) -> None:
        """Test that missing app_key raises MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError) as exc_info:
            APIKeyAuth(
                access_key="my_access_key",
                secret_key="my_secret_key",
                app_key="",
            )
        assert "app_key" in str(exc_info.value)

    def test_init_none_access_key_raises_error(self) -> None:
        """Test that None access_key raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            APIKeyAuth(
                access_key=None,  # type: ignore[arg-type]
                secret_key="my_secret_key",
                app_key="my_app_key",
            )
        assert "access_key" in str(exc_info.value)

    def test_init_none_secret_key_raises_error(self) -> None:
        """Test that None secret_key raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            APIKeyAuth(
                access_key="my_access_key",
                secret_key=None,  # type: ignore[arg-type]
                app_key="my_app_key",
            )
        assert "secret_key" in str(exc_info.value)

    def test_init_none_app_key_raises_error(self) -> None:
        """Test that None app_key raises ValidationError."""
        with pytest.raises(ValidationError) as exc_info:
            APIKeyAuth(
                access_key="my_access_key",
                secret_key="my_secret_key",
                app_key=None,  # type: ignore[arg-type]
            )
        assert "app_key" in str(exc_info.value)

    def test_get_headers_returns_correct_headers(self) -> None:
        """Test that get_headers returns the correct authentication headers."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        headers = auth.get_headers()
        assert headers == {
            "accessKey": "test_access",
            "secretKey": "test_secret",
            "appKey": "test_app",
        }

    def test_get_headers_returns_new_dict_each_time(self) -> None:
        """Test that get_headers returns a new dictionary each time."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        headers1 = auth.get_headers()
        headers2 = auth.get_headers()
        assert headers1 is not headers2
        assert headers1 == headers2

    def test_is_immutable(self) -> None:
        """Test that APIKeyAuth instance is immutable (frozen dataclass)."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        with pytest.raises(AttributeError):
            auth.access_key = "new_value"  # type: ignore[misc]

    def test_repr_hides_secrets(self) -> None:
        """Test that __repr__ does not expose secret values."""
        auth = APIKeyAuth(
            access_key="real_access_key",
            secret_key="real_secret_key",
            app_key="real_app_key",
        )
        repr_str = repr(auth)
        assert "real_secret_key" not in repr_str
        assert "***" in repr_str or "HIDDEN" in repr_str

    def test_equality(self) -> None:
        """Test that two APIKeyAuth instances with same values are equal."""
        auth1 = APIKeyAuth(
            access_key="key1",
            secret_key="key2",
            app_key="key3",
        )
        auth2 = APIKeyAuth(
            access_key="key1",
            secret_key="key2",
            app_key="key3",
        )
        assert auth1 == auth2

    def test_hash(self) -> None:
        """Test that APIKeyAuth is hashable."""
        auth = APIKeyAuth(
            access_key="key1",
            secret_key="key2",
            app_key="key3",
        )
        # Should not raise
        hash_value = hash(auth)
        assert isinstance(hash_value, int)

    def test_to_dict_excludes_secrets_by_default(self) -> None:
        """Test that to_dict excludes secret_key by default."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        data = auth.to_dict()
        assert data["access_key"] == "test_access"
        assert data["app_key"] == "test_app"
        assert "secret_key" not in data

    def test_to_dict_includes_secrets_when_requested(self) -> None:
        """Test that to_dict includes secret_key when include_secrets=True."""
        auth = APIKeyAuth(
            access_key="test_access",
            secret_key="test_secret",
            app_key="test_app",
        )
        data = auth.to_dict(include_secrets=True)
        assert data["access_key"] == "test_access"
        assert data["secret_key"] == "test_secret"
        assert data["app_key"] == "test_app"

    def test_whitespace_only_access_key_raises_error(self) -> None:
        """Test that whitespace-only access_key raises error."""
        with pytest.raises(MissingConfigurationError):
            APIKeyAuth(
                access_key="   ",
                secret_key="my_secret_key",
                app_key="my_app_key",
            )

    def test_whitespace_only_secret_key_raises_error(self) -> None:
        """Test that whitespace-only secret_key raises error."""
        with pytest.raises(MissingConfigurationError):
            APIKeyAuth(
                access_key="my_access_key",
                secret_key="   ",
                app_key="my_app_key",
            )

    def test_whitespace_only_app_key_raises_error(self) -> None:
        """Test that whitespace-only app_key raises error."""
        with pytest.raises(MissingConfigurationError):
            APIKeyAuth(
                access_key="my_access_key",
                secret_key="my_secret_key",
                app_key="   ",
            )


class TestAPIKeyAuthFromEnv:
    """Tests for APIKeyAuth.from_env class method."""

    # AICOMPLETE: API Key authentication from environment - ready for review

    def test_from_env_loads_all_variables(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test loading configuration from environment variables."""
        monkeypatch.setenv("WFIRMA_ACCESS_KEY", "env_access")
        monkeypatch.setenv("WFIRMA_SECRET_KEY", "env_secret")
        monkeypatch.setenv("WFIRMA_APP_KEY", "env_app")

        auth = APIKeyAuth.from_env()
        assert auth.access_key == "env_access"
        assert auth.secret_key == "env_secret"
        assert auth.app_key == "env_app"

    def test_from_env_missing_access_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that missing WFIRMA_ACCESS_KEY raises MissingConfigurationError."""
        monkeypatch.delenv("WFIRMA_ACCESS_KEY", raising=False)
        monkeypatch.setenv("WFIRMA_SECRET_KEY", "env_secret")
        monkeypatch.setenv("WFIRMA_APP_KEY", "env_app")

        with pytest.raises(MissingConfigurationError) as exc_info:
            APIKeyAuth.from_env()
        assert "WFIRMA_ACCESS_KEY" in str(exc_info.value)

    def test_from_env_missing_secret_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that missing WFIRMA_SECRET_KEY raises MissingConfigurationError."""
        monkeypatch.setenv("WFIRMA_ACCESS_KEY", "env_access")
        monkeypatch.delenv("WFIRMA_SECRET_KEY", raising=False)
        monkeypatch.setenv("WFIRMA_APP_KEY", "env_app")

        with pytest.raises(MissingConfigurationError) as exc_info:
            APIKeyAuth.from_env()
        assert "WFIRMA_SECRET_KEY" in str(exc_info.value)

    def test_from_env_missing_app_key(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that missing WFIRMA_APP_KEY raises MissingConfigurationError."""
        monkeypatch.setenv("WFIRMA_ACCESS_KEY", "env_access")
        monkeypatch.setenv("WFIRMA_SECRET_KEY", "env_secret")
        monkeypatch.delenv("WFIRMA_APP_KEY", raising=False)

        with pytest.raises(MissingConfigurationError) as exc_info:
            APIKeyAuth.from_env()
        assert "WFIRMA_APP_KEY" in str(exc_info.value)

    def test_from_env_explicit_overrides_environment(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test that explicit arguments override environment variables."""
        monkeypatch.setenv("WFIRMA_ACCESS_KEY", "env_access")
        monkeypatch.setenv("WFIRMA_SECRET_KEY", "env_secret")
        monkeypatch.setenv("WFIRMA_APP_KEY", "env_app")

        auth = APIKeyAuth.from_env(
            access_key="override_access",
            secret_key="override_secret",
            app_key="override_app",
        )
        assert auth.access_key == "override_access"
        assert auth.secret_key == "override_secret"
        assert auth.app_key == "override_app"

    def test_from_env_partial_override(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Test partial override - some from env, some explicit."""
        monkeypatch.setenv("WFIRMA_ACCESS_KEY", "env_access")
        monkeypatch.setenv("WFIRMA_SECRET_KEY", "env_secret")
        monkeypatch.setenv("WFIRMA_APP_KEY", "env_app")

        auth = APIKeyAuth.from_env(access_key="override_access")
        assert auth.access_key == "override_access"
        assert auth.secret_key == "env_secret"
        assert auth.app_key == "env_app"
