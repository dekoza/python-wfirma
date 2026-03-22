"""Configuration management for the production wFirma API client."""

import os
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from dotenv import dotenv_values

from wfirma.exceptions import InvalidConfigurationError, MissingConfigurationError


class Environment(Enum):
    """API environment enumeration."""

    PRODUCTION = "production"

    @property
    def base_url(self) -> str:
        """
        Return the base URL for this environment.

        Returns:
            The API base URL for the environment.
        """
        return "https://api2.wfirma.pl"


def _parse_environment(value: str | Environment) -> Environment:
    """
    Parse environment value to Environment enum.

    Args:
        value: Environment as string or enum.

    Returns:
        Environment enum value.

    Raises:
        InvalidConfigurationError: If the value is not a valid environment.
    """
    if isinstance(value, Environment):
        return value

    value_lower = value.lower().strip()
    try:
        return Environment(value_lower)
    except ValueError as err:
        valid_values = [e.value for e in Environment]
        raise InvalidConfigurationError(
            f"Invalid environment value: {value!r}. Valid values are: {valid_values}"
        ) from err


@dataclass(frozen=True)
class WFirmaConfig:
    """
    Configuration for wFirma API client.

    This class holds all configuration needed to connect to the wFirma API.
    It supports loading from environment variables, .env files, or direct
    instantiation.

    The class is immutable (frozen) to prevent accidental modifications
    after creation.

    Attributes:
        app_key: Application key for API authentication.
        app_secret: Application secret for API authentication.
        environment: API environment.
        company_id: Default company ID for API requests.
        timeout: Request timeout in seconds.

    Example:
        >>> config = WFirmaConfig(
        ...     app_key="your_app_key",
        ...     app_secret="your_secret",
        ... )
        >>> config.is_production
        True
    """

    app_key: str
    app_secret: str
    environment: Environment = field(default=Environment.PRODUCTION)
    company_id: str | None = field(default=None)
    timeout: float = field(default=30.0)

    def __post_init__(self) -> None:
        """Validate configuration after initialization."""
        # Validate required fields
        if not self.app_key:
            raise MissingConfigurationError(
                "Configuration field 'app_key' is required but was empty or None."
            )
        if not self.app_secret:
            raise MissingConfigurationError(
                "Configuration field 'app_secret' is required but was empty or None."
            )

        # Convert environment string to enum if needed
        if isinstance(self.environment, str):
            # Use object.__setattr__ because the class is frozen
            object.__setattr__(self, "environment", _parse_environment(self.environment))

        # Validate timeout
        if self.timeout <= 0:
            raise InvalidConfigurationError(
                f"Configuration field 'timeout' must be positive, got: {self.timeout}"
            )

    @property
    def base_url(self) -> str:
        """
        Return the API base URL for the configured environment.

        Returns:
            The base URL string.
        """
        return self.environment.base_url

    @property
    def is_production(self) -> bool:
        """
        Check if the configuration is for production environment.

        Returns:
            True if production environment, False otherwise.
        """
        return self.environment == Environment.PRODUCTION

    @classmethod
    def from_env(
        cls,
        *,
        app_key: str | None = None,
        app_secret: str | None = None,
        environment: str | Environment | None = None,
        company_id: str | None = None,
        timeout: float | None = None,
    ) -> "WFirmaConfig":
        """
        Create configuration from environment variables.

        Environment variables used:
            - WFIRMA_APP_KEY
            - WFIRMA_APP_SECRET
            - WFIRMA_ENVIRONMENT
            - WFIRMA_COMPANY_ID
            - WFIRMA_TIMEOUT

        Explicit arguments override environment variables.

        Args:
            app_key: Override for WFIRMA_APP_KEY.
            app_secret: Override for WFIRMA_APP_SECRET.
            environment: Override for WFIRMA_ENVIRONMENT.
            company_id: Override for WFIRMA_COMPANY_ID.
            timeout: Override for WFIRMA_TIMEOUT.

        Returns:
            WFirmaConfig instance.

        Raises:
            MissingConfigurationError: If required fields are missing.
            InvalidConfigurationError: If configuration values are invalid.
        """
        # Get values from environment with explicit overrides
        resolved_app_key = app_key or os.environ.get("WFIRMA_APP_KEY", "")
        resolved_app_secret = app_secret or os.environ.get("WFIRMA_APP_SECRET", "")

        # Check for missing required environment variables
        if not resolved_app_key:
            raise MissingConfigurationError(
                "Environment variable 'WFIRMA_APP_KEY' is required but not set."
            )
        if not resolved_app_secret:
            raise MissingConfigurationError(
                "Environment variable 'WFIRMA_APP_SECRET' is required but not set."
            )

        # Handle environment
        if environment is not None:
            resolved_environment = _parse_environment(environment)
        else:
            env_str = os.environ.get("WFIRMA_ENVIRONMENT", "production")
            resolved_environment = _parse_environment(env_str)

        # Handle company_id
        resolved_company_id = company_id or os.environ.get("WFIRMA_COMPANY_ID") or None

        # Handle timeout
        if timeout is not None:
            resolved_timeout = timeout
        else:
            timeout_str = os.environ.get("WFIRMA_TIMEOUT")
            resolved_timeout = float(timeout_str) if timeout_str else 30.0

        return cls(
            app_key=resolved_app_key,
            app_secret=resolved_app_secret,
            environment=resolved_environment,
            company_id=resolved_company_id,
            timeout=resolved_timeout,
        )

    @classmethod
    def from_dotenv(
        cls,
        dotenv_path: str | Path,
        *,
        app_key: str | None = None,
        app_secret: str | None = None,
        environment: str | Environment | None = None,
        company_id: str | None = None,
        timeout: float | None = None,
    ) -> "WFirmaConfig":
        """
        Create configuration from a .env file.

        Args:
            dotenv_path: Path to the .env file.
            app_key: Override for WFIRMA_APP_KEY.
            app_secret: Override for WFIRMA_APP_SECRET.
            environment: Override for WFIRMA_ENVIRONMENT.
            company_id: Override for WFIRMA_COMPANY_ID.
            timeout: Override for WFIRMA_TIMEOUT.

        Returns:
            WFirmaConfig instance.

        Raises:
            InvalidConfigurationError: If the .env file does not exist.
            MissingConfigurationError: If required fields are missing.
        """
        path = Path(dotenv_path)
        if not path.exists():
            raise InvalidConfigurationError(f"Configuration file not found: {path}")

        # Load values from .env file
        env_values = dotenv_values(path)

        # Get values from file with explicit overrides
        resolved_app_key = app_key or env_values.get("WFIRMA_APP_KEY", "")
        resolved_app_secret = app_secret or env_values.get("WFIRMA_APP_SECRET", "")

        if not resolved_app_key:
            raise MissingConfigurationError(
                "Configuration field 'WFIRMA_APP_KEY' is required in .env file but not set."
            )
        if not resolved_app_secret:
            raise MissingConfigurationError(
                "Configuration field 'WFIRMA_APP_SECRET' is required in .env file but not set."
            )

        # Handle environment
        if environment is not None:
            resolved_environment = _parse_environment(environment)
        else:
            env_str = env_values.get("WFIRMA_ENVIRONMENT", "production")
            resolved_environment = _parse_environment(env_str or "production")

        # Handle company_id
        resolved_company_id = company_id or env_values.get("WFIRMA_COMPANY_ID") or None

        # Handle timeout
        if timeout is not None:
            resolved_timeout = timeout
        else:
            timeout_str = env_values.get("WFIRMA_TIMEOUT")
            resolved_timeout = float(timeout_str) if timeout_str else 30.0

        return cls(
            app_key=resolved_app_key,
            app_secret=resolved_app_secret,
            environment=resolved_environment,
            company_id=resolved_company_id,
            timeout=resolved_timeout,
        )

    def to_dict(self, *, include_secrets: bool = False) -> dict[str, Any]:
        """
        Convert configuration to dictionary.

        By default, sensitive data (app_secret) is excluded for safe logging.

        Args:
            include_secrets: If True, include sensitive data.

        Returns:
            Dictionary representation of the configuration.
        """
        result: dict[str, Any] = {
            "app_key": self.app_key,
            "environment": self.environment.value,
            "company_id": self.company_id,
            "timeout": self.timeout,
            "base_url": self.base_url,
        }
        if include_secrets:
            result["app_secret"] = self.app_secret
        return result

    def __repr__(self) -> str:
        """
        Return string representation without exposing secrets.

        Returns:
            Safe string representation.
        """
        return (
            f"WFirmaConfig("
            f"app_key={self.app_key!r}, "
            f"app_secret='***HIDDEN***', "
            f"environment={self.environment.value!r}, "
            f"company_id={self.company_id!r}, "
            f"timeout={self.timeout})"
        )


def get_config(
    *,
    app_key: str | None = None,
    app_secret: str | None = None,
    environment: str | Environment | None = None,
    company_id: str | None = None,
    timeout: float | None = None,
) -> WFirmaConfig:
    """
    Get wFirma configuration.

    This is a convenience function that creates a WFirmaConfig instance.
    If no arguments are provided, it attempts to load from environment
    variables.

    Args:
        app_key: Application key for API authentication.
        app_secret: Application secret for API authentication.
        environment: API environment.
        company_id: Default company ID for API requests.
        timeout: Request timeout in seconds.

    Returns:
        WFirmaConfig instance.

    Raises:
        MissingConfigurationError: If required configuration is missing.
        InvalidConfigurationError: If configuration values are invalid.

    Example:
        >>> # Load from environment
        >>> config = get_config()
        >>>
        >>> # Or provide explicit values
        >>> config = get_config(
        ...     app_key="your_key",
        ...     app_secret="your_secret",
        ... )
    """
    # If explicit credentials provided, use them
    if app_key is not None and app_secret is not None:
        env = environment if environment is not None else Environment.PRODUCTION
        return WFirmaConfig(
            app_key=app_key,
            app_secret=app_secret,
            environment=env if isinstance(env, Environment) else _parse_environment(env),
            company_id=company_id,
            timeout=timeout or 30.0,
        )

    # Otherwise, load from environment
    return WFirmaConfig.from_env(
        app_key=app_key,
        app_secret=app_secret,
        environment=environment,
        company_id=company_id,
        timeout=timeout,
    )
