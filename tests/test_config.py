"""
Tests for wFirma configuration management.
"""

import os
from pathlib import Path
from unittest.mock import patch

import pytest

from wfirma.config import (
    Environment,
    WFirmaConfig,
    get_config,
)
from wfirma.exceptions import (
    InvalidConfigurationError,
    MissingConfigurationError,
)


class TestEnvironmentEnum:
    """Test Environment enum values."""

    def test_production_environment_value(self):
        """Production environment should have correct value."""
        assert Environment.PRODUCTION.value == "production"

    def test_production_base_url(self):
        """Production environment should return production API URL."""
        assert Environment.PRODUCTION.base_url == "https://api2.wfirma.pl"

    def test_environment_from_string(self):
        """Environment should be parseable from string."""
        from wfirma.config import _parse_environment

        assert _parse_environment("production") == Environment.PRODUCTION
        assert _parse_environment("PRODUCTION") == Environment.PRODUCTION

    def test_environment_from_enum_returns_same(self):
        """Parsing Environment enum should return the same enum."""
        from wfirma.config import _parse_environment

        assert _parse_environment(Environment.PRODUCTION) is Environment.PRODUCTION


class TestWFirmaConfigCreation:
    """Test WFirmaConfig creation and validation."""

    def test_create_config_with_required_fields(self):
        """Config should be created with required fields."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
        )
        assert config.app_key == "test_app_key"
        assert config.app_secret == "test_secret"

    def test_default_environment_is_production(self):
        """Default environment should be production."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
        )
        assert config.environment == Environment.PRODUCTION

    def test_create_config_with_production_environment(self):
        """Config should accept production environment."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            environment=Environment.PRODUCTION,
        )
        assert config.environment == Environment.PRODUCTION

    def test_create_config_with_environment_string(self):
        """Config should accept environment as string."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            environment="production",
        )
        assert config.environment == Environment.PRODUCTION

    def test_create_config_with_company_id(self):
        """Config should accept optional company_id."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            company_id="12345",
        )
        assert config.company_id == "12345"

    def test_default_company_id_is_none(self):
        """Default company_id should be None."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
        )
        assert config.company_id is None

    def test_create_config_with_timeout(self):
        """Config should accept custom timeout."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            timeout=60.0,
        )
        assert config.timeout == 60.0

    def test_default_timeout_is_30_seconds(self):
        """Default timeout should be 30 seconds."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
        )
        assert config.timeout == 30.0


class TestWFirmaConfigValidation:
    """Test WFirmaConfig validation."""

    def test_missing_app_key_raises_error(self):
        """Missing app_key should raise MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError) as exc_info:
            WFirmaConfig(
                app_key="",
                app_secret="test_secret",
            )
        assert "app_key" in str(exc_info.value)

    def test_missing_app_secret_raises_error(self):
        """Missing app_secret should raise MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError) as exc_info:
            WFirmaConfig(
                app_key="test_app_key",
                app_secret="",
            )
        assert "app_secret" in str(exc_info.value)

    def test_none_app_key_raises_error(self):
        """None app_key should raise MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError):
            WFirmaConfig(
                app_key=None,  # type: ignore[arg-type]
                app_secret="test_secret",
            )

    def test_none_app_secret_raises_error(self):
        """None app_secret should raise MissingConfigurationError."""
        with pytest.raises(MissingConfigurationError):
            WFirmaConfig(
                app_key="test_app_key",
                app_secret=None,  # type: ignore[arg-type]
            )

    def test_invalid_environment_raises_error(self):
        """Invalid environment should raise InvalidConfigurationError."""
        with pytest.raises(InvalidConfigurationError) as exc_info:
            WFirmaConfig(
                app_key="test_app_key",
                app_secret="test_secret",
                environment="invalid_env",  # type: ignore[arg-type]
            )
        assert "environment" in str(exc_info.value)

    def test_negative_timeout_raises_error(self):
        """Negative timeout should raise InvalidConfigurationError."""
        with pytest.raises(InvalidConfigurationError) as exc_info:
            WFirmaConfig(
                app_key="test_app_key",
                app_secret="test_secret",
                timeout=-1.0,
            )
        assert "timeout" in str(exc_info.value)

    def test_zero_timeout_raises_error(self):
        """Zero timeout should raise InvalidConfigurationError."""
        with pytest.raises(InvalidConfigurationError) as exc_info:
            WFirmaConfig(
                app_key="test_app_key",
                app_secret="test_secret",
                timeout=0.0,
            )
        assert "timeout" in str(exc_info.value)


class TestWFirmaConfigProperties:
    """Test WFirmaConfig computed properties."""

    def test_base_url_for_production(self):
        """Config should return correct base_url for production."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            environment=Environment.PRODUCTION,
        )
        assert config.base_url == "https://api2.wfirma.pl"

    def test_is_production_property(self):
        """Config should correctly identify production environment."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            environment=Environment.PRODUCTION,
        )
        assert config.is_production is True


class TestWFirmaConfigFromEnvironment:
    """Test loading configuration from environment variables."""

    def test_load_from_environment_variables(self):
        """Config should load from environment variables."""
        env_vars = {
            "WFIRMA_APP_KEY": "env_app_key",
            "WFIRMA_APP_SECRET": "env_app_secret",
            "WFIRMA_ENVIRONMENT": "production",
            "WFIRMA_COMPANY_ID": "99999",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            config = WFirmaConfig.from_env()

        assert config.app_key == "env_app_key"
        assert config.app_secret == "env_app_secret"
        assert config.environment == Environment.PRODUCTION
        assert config.company_id == "99999"

    def test_load_from_environment_with_defaults(self):
        """Config should use defaults for optional env vars."""
        env_vars = {
            "WFIRMA_APP_KEY": "env_app_key",
            "WFIRMA_APP_SECRET": "env_app_secret",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            config = WFirmaConfig.from_env()

        assert config.app_key == "env_app_key"
        assert config.app_secret == "env_app_secret"
        assert config.environment == Environment.PRODUCTION
        assert config.company_id is None

    def test_missing_required_env_var_raises_error(self):
        """Missing required env var should raise MissingConfigurationError."""
        env_vars = {
            "WFIRMA_APP_KEY": "env_app_key",
            # Missing WFIRMA_APP_SECRET
        }
        with (
            patch.dict(os.environ, env_vars, clear=True),
            pytest.raises(MissingConfigurationError) as exc_info,
        ):
            WFirmaConfig.from_env()

        assert "WFIRMA_APP_SECRET" in str(exc_info.value)

    def test_load_timeout_from_environment(self):
        """Config should load timeout from environment."""
        env_vars = {
            "WFIRMA_APP_KEY": "env_app_key",
            "WFIRMA_APP_SECRET": "env_app_secret",
            "WFIRMA_TIMEOUT": "60",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            config = WFirmaConfig.from_env()

        assert config.timeout == 60.0

    def test_explicit_values_override_env_vars(self):
        """Explicit values should override environment variables."""
        env_vars = {
            "WFIRMA_APP_KEY": "env_app_key",
            "WFIRMA_APP_SECRET": "env_app_secret",
            "WFIRMA_ENVIRONMENT": "production",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            config = WFirmaConfig.from_env(
                app_key="override_key",
                environment=Environment.PRODUCTION,
            )

        assert config.app_key == "override_key"
        assert config.app_secret == "env_app_secret"
        assert config.environment == Environment.PRODUCTION


class TestWFirmaConfigFromDotenv:
    """Test loading configuration from .env file."""

    def test_load_from_dotenv_file(self, tmp_path: Path):
        """Config should load from .env file."""
        dotenv_file = tmp_path / ".env"
        dotenv_file.write_text(
            "WFIRMA_APP_KEY=dotenv_app_key\n"
            "WFIRMA_APP_SECRET=dotenv_secret\n"
            "WFIRMA_ENVIRONMENT=production\n"
        )

        # Clear environment to ensure we're loading from file
        with patch.dict(os.environ, {}, clear=True):
            config = WFirmaConfig.from_dotenv(dotenv_file)

        assert config.app_key == "dotenv_app_key"
        assert config.app_secret == "dotenv_secret"
        assert config.environment == Environment.PRODUCTION

    def test_missing_dotenv_file_raises_error(self, tmp_path: Path):
        """Missing .env file should raise InvalidConfigurationError."""
        non_existent = tmp_path / "nonexistent.env"

        with pytest.raises(InvalidConfigurationError) as exc_info:
            WFirmaConfig.from_dotenv(non_existent)

        assert ".env" in str(exc_info.value) or "nonexistent" in str(exc_info.value)

    def test_load_from_dotenv_with_overrides(self, tmp_path: Path):
        """Config should allow overriding .env values."""
        dotenv_file = tmp_path / ".env"
        dotenv_file.write_text(
            "WFIRMA_APP_KEY=dotenv_app_key\n"
            "WFIRMA_APP_SECRET=dotenv_secret\n"
            "WFIRMA_ENVIRONMENT=production\n"
            "WFIRMA_COMPANY_ID=file_company\n"
            "WFIRMA_TIMEOUT=10\n"
        )

        with patch.dict(os.environ, {}, clear=True):
            config = WFirmaConfig.from_dotenv(
                dotenv_file,
                app_key="override_key",
                app_secret="override_secret",
                environment=Environment.PRODUCTION,
                company_id="override_company",
                timeout=99.0,
            )

        assert config.app_key == "override_key"
        assert config.app_secret == "override_secret"
        assert config.environment == Environment.PRODUCTION
        assert config.company_id == "override_company"
        assert config.timeout == 99.0

    def test_load_from_dotenv_with_timeout(self, tmp_path: Path):
        """Config should load timeout from .env file."""
        dotenv_file = tmp_path / ".env"
        dotenv_file.write_text(
            "WFIRMA_APP_KEY=dotenv_app_key\nWFIRMA_APP_SECRET=dotenv_secret\nWFIRMA_TIMEOUT=45\n"
        )

        with patch.dict(os.environ, {}, clear=True):
            config = WFirmaConfig.from_dotenv(dotenv_file)

        assert config.timeout == 45.0

    def test_load_from_dotenv_with_company_id(self, tmp_path: Path):
        """Config should load company_id from .env file."""
        dotenv_file = tmp_path / ".env"
        dotenv_file.write_text(
            "WFIRMA_APP_KEY=dotenv_app_key\n"
            "WFIRMA_APP_SECRET=dotenv_secret\n"
            "WFIRMA_COMPANY_ID=12345\n"
        )

        with patch.dict(os.environ, {}, clear=True):
            config = WFirmaConfig.from_dotenv(dotenv_file)

        assert config.company_id == "12345"


class TestWFirmaConfigSerialization:
    """Test configuration serialization."""

    def test_to_dict_excludes_secrets(self):
        """to_dict should exclude sensitive data."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            environment=Environment.PRODUCTION,
            company_id="12345",
        )

        config_dict = config.to_dict()

        assert "app_secret" not in config_dict
        assert config_dict["app_key"] == "test_app_key"
        assert config_dict["environment"] == "production"
        assert config_dict["company_id"] == "12345"

    def test_to_dict_includes_all_non_secret_fields(self):
        """to_dict should include all non-secret configuration."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
            environment=Environment.PRODUCTION,
            company_id="12345",
            timeout=45.0,
        )

        config_dict = config.to_dict()

        assert "app_key" in config_dict
        assert "environment" in config_dict
        assert "company_id" in config_dict
        assert "timeout" in config_dict
        assert "base_url" in config_dict

    def test_to_dict_full_includes_secrets_when_specified(self):
        """to_dict_full should include secrets when requested."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
        )

        config_dict = config.to_dict(include_secrets=True)

        assert config_dict["app_secret"] == "test_secret"

    def test_repr_does_not_expose_secrets(self):
        """String representation should not expose secrets."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="super_secret_value",
        )

        repr_str = repr(config)

        assert "super_secret_value" not in repr_str
        assert "***" in repr_str or "HIDDEN" in repr_str.upper()


class TestGetConfigFunction:
    """Test the get_config convenience function."""

    def test_get_config_returns_config_instance(self):
        """get_config should return WFirmaConfig instance."""
        config = get_config(
            app_key="test_key",
            app_secret="test_secret",
        )

        assert isinstance(config, WFirmaConfig)
        assert config.app_key == "test_key"

    def test_get_config_from_env_when_no_args(self):
        """get_config should load from env when no args provided."""
        env_vars = {
            "WFIRMA_APP_KEY": "env_key",
            "WFIRMA_APP_SECRET": "env_secret",
        }
        with patch.dict(os.environ, env_vars, clear=True):
            config = get_config()

        assert config.app_key == "env_key"
        assert config.app_secret == "env_secret"


class TestConfigImmutability:
    """Test that config is immutable after creation."""

    def test_config_is_frozen(self):
        """Config should be frozen after creation."""
        config = WFirmaConfig(
            app_key="test_app_key",
            app_secret="test_secret",
        )

        # Attempting to modify should raise an error
        with pytest.raises((AttributeError, TypeError)):
            config.app_key = "new_key"  # type: ignore[misc]


# AICOMPLETE: Configuration management tests - ready for review
