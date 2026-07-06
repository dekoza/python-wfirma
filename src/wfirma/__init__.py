"""
python-wfirma - Python library for wFirma API
"""

__version__ = "1.0.0"

# Configuration - public API
from wfirma.config import (
    Environment,
    WFirmaConfig,
    get_config,
)

# Exceptions - public API
from wfirma.exceptions import (
    # API errors
    APIError,
    # Authentication errors
    AuthenticationError,
    BadRequestError,
    # Configuration errors
    ConfigurationError,
    ConnectionError,
    InsufficientPermissionsError,
    InvalidConfigurationError,
    InvalidCredentialsError,
    InvalidFieldError,
    MissingConfigurationError,
    MissingRequiredFieldError,
    # Network errors
    NetworkError,
    RateLimitError,
    ResourceAlreadyExistsError,
    ResourceConflictError,
    # Resource errors
    ResourceError,
    ResourceNotFoundError,
    ServerError,
    ServiceUnavailableError,
    TimeoutError,
    TokenExpiredError,
    # Validation errors
    ValidationError,
    # Base exception
    WFirmaException,
)

__all__ = [
    "__version__",
    # Configuration
    "Environment",
    "WFirmaConfig",
    "get_config",
    # Exceptions
    "WFirmaException",
    "AuthenticationError",
    "InvalidCredentialsError",
    "TokenExpiredError",
    "InsufficientPermissionsError",
    "ValidationError",
    "InvalidFieldError",
    "MissingRequiredFieldError",
    "APIError",
    "RateLimitError",
    "ServerError",
    "BadRequestError",
    "ServiceUnavailableError",
    "ResourceError",
    "ResourceNotFoundError",
    "ResourceAlreadyExistsError",
    "ResourceConflictError",
    "NetworkError",
    "ConnectionError",
    "TimeoutError",
    "ConfigurationError",
    "MissingConfigurationError",
    "InvalidConfigurationError",
]
