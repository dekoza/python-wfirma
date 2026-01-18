"""
Exception hierarchy for wFirma API client.

This module defines all exceptions that can be raised by the wFirma library.
The hierarchy is designed to allow for granular exception handling while
maintaining a common base class for catching all library-related errors.

Exception Hierarchy:
    WFirmaException (base)
    ├── AuthenticationError
    │   ├── InvalidCredentialsError
    │   ├── TokenExpiredError
    │   └── InsufficientPermissionsError
    ├── ValidationError
    │   ├── InvalidFieldError
    │   └── MissingRequiredFieldError
    ├── APIError
    │   ├── RateLimitError
    │   ├── ServerError
    │   ├── BadRequestError
    │   └── ServiceUnavailableError
    ├── ResourceError
    │   ├── ResourceNotFoundError
    │   ├── ResourceAlreadyExistsError
    │   └── ResourceConflictError
    ├── NetworkError
    │   ├── ConnectionError
    │   └── TimeoutError
    └── ConfigurationError
        ├── MissingConfigurationError
        └── InvalidConfigurationError
"""

from typing import Any


class WFirmaException(Exception):
    """
    Base exception for all wFirma library errors.

    All exceptions raised by the wFirma library inherit from this class,
    allowing for easy catching of all library-related errors.

    Attributes:
        message: Human-readable error message.
    """

    def __init__(self, message: str = "", *, cause: Exception | None = None) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            cause: Original exception that caused this error.
        """
        self.message = message
        super().__init__(message)
        if cause is not None:
            self.__cause__ = cause

    def __repr__(self) -> str:
        """Return a detailed string representation of the exception."""
        return f"{self.__class__.__name__}({self.message!r})"

    def to_dict(self) -> dict[str, Any]:
        """
        Convert exception to dictionary for logging/serialization.

        Returns:
            Dictionary containing exception details.
        """
        return {
            "type": self.__class__.__name__,
            "message": self.message,
        }


# =============================================================================
# Authentication Errors
# =============================================================================


class AuthenticationError(WFirmaException):
    """
    Base class for authentication-related errors.

    Raised when there are issues with OAuth authentication,
    credentials, or permissions.
    """

    pass


class InvalidCredentialsError(AuthenticationError):
    """
    Raised when provided credentials are invalid.

    This includes wrong API keys, client IDs, or secrets.
    """

    pass


class TokenExpiredError(AuthenticationError):
    """
    Raised when the OAuth access token has expired.

    The client should attempt to refresh the token or re-authenticate.
    """

    pass


class InsufficientPermissionsError(AuthenticationError):
    """
    Raised when the authenticated user lacks required permissions.

    This occurs when trying to access resources or perform actions
    that require additional scopes or permissions.
    """

    pass


# =============================================================================
# Validation Errors
# =============================================================================


class ValidationError(WFirmaException):
    """
    Base class for data validation errors.

    Raised when input data fails validation before being sent to the API
    or when API returns validation errors.
    """

    pass


class InvalidFieldError(ValidationError):
    """
    Raised when a field value is invalid.

    Attributes:
        field: Name of the field that failed validation.
        value: The invalid value that was provided.
    """

    def __init__(
        self,
        message: str = "",
        *,
        field: str | None = None,
        value: Any = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            field: Name of the field that failed validation.
            value: The invalid value that was provided.
            cause: Original exception that caused this error.
        """
        super().__init__(message, cause=cause)
        self.field = field
        self.value = value

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/serialization."""
        result = super().to_dict()
        result["field"] = self.field
        result["value"] = self.value
        return result


class MissingRequiredFieldError(ValidationError):
    """
    Raised when a required field is missing.

    Attributes:
        field: Name of the missing required field.
    """

    def __init__(
        self,
        message: str = "",
        *,
        field: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            field: Name of the missing required field.
            cause: Original exception that caused this error.
        """
        super().__init__(message, cause=cause)
        self.field = field

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/serialization."""
        result = super().to_dict()
        result["field"] = self.field
        return result


# =============================================================================
# API Errors
# =============================================================================


class APIError(WFirmaException):
    """
    Base class for API-related errors.

    Raised when the wFirma API returns an error response.

    Attributes:
        error_code: wFirma API error code (e.g., 'FATAL', 'NOT_FOUND').
        status_code: HTTP status code from the API response.
    """

    def __init__(
        self,
        message: str = "",
        *,
        error_code: str | None = None,
        status_code: int | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            error_code: wFirma API error code.
            status_code: HTTP status code from the API response.
            cause: Original exception that caused this error.
        """
        super().__init__(message, cause=cause)
        self.error_code = error_code
        self.status_code = status_code

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/serialization."""
        result = super().to_dict()
        result["error_code"] = self.error_code
        result["status_code"] = self.status_code
        return result


class RateLimitError(APIError):
    """
    Raised when API rate limits are exceeded.

    Corresponds to wFirma error codes:
    - TOTAL_REQUESTS_LIMIT_EXCEEDED
    - TOTAL_EXECUTION_TIME_LIMIT_EXCEEDED

    Attributes:
        retry_after: Number of seconds to wait before retrying.
    """

    def __init__(
        self,
        message: str = "",
        *,
        error_code: str | None = None,
        status_code: int | None = None,
        retry_after: int | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            error_code: wFirma API error code.
            status_code: HTTP status code from the API response.
            retry_after: Number of seconds to wait before retrying.
            cause: Original exception that caused this error.
        """
        super().__init__(message, error_code=error_code, status_code=status_code, cause=cause)
        self.retry_after = retry_after

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/serialization."""
        result = super().to_dict()
        result["retry_after"] = self.retry_after
        return result


class ServerError(APIError):
    """
    Raised when the API encounters an internal server error.

    Corresponds to HTTP 5xx status codes.
    """

    pass


class BadRequestError(APIError):
    """
    Raised when the request is malformed or invalid.

    Corresponds to HTTP 400 status code.
    """

    pass


class ServiceUnavailableError(APIError):
    """
    Raised when the wFirma API service is unavailable.

    Corresponds to wFirma error code OUT_OF_SERVICE or HTTP 503.
    """

    pass


# =============================================================================
# Resource Errors
# =============================================================================


class ResourceError(WFirmaException):
    """
    Base class for resource-related errors.

    Raised when operations on specific resources fail.
    """

    pass


class ResourceNotFoundError(ResourceError):
    """
    Raised when a requested resource does not exist.

    Corresponds to wFirma error code NOT_FOUND or HTTP 404.

    Attributes:
        resource_type: Type of resource (e.g., 'invoice', 'contractor').
        resource_id: Identifier of the resource that was not found.
    """

    def __init__(
        self,
        message: str = "",
        *,
        resource_type: str | None = None,
        resource_id: str | None = None,
        cause: Exception | None = None,
    ) -> None:
        """
        Initialize the exception.

        Args:
            message: Human-readable error message.
            resource_type: Type of resource (e.g., 'invoice', 'contractor').
            resource_id: Identifier of the resource that was not found.
            cause: Original exception that caused this error.
        """
        super().__init__(message, cause=cause)
        self.resource_type = resource_type
        self.resource_id = resource_id

    def to_dict(self) -> dict[str, Any]:
        """Convert exception to dictionary for logging/serialization."""
        result = super().to_dict()
        result["resource_type"] = self.resource_type
        result["resource_id"] = self.resource_id
        return result


class ResourceAlreadyExistsError(ResourceError):
    """
    Raised when trying to create a resource that already exists.

    May occur when creating resources with unique constraints.
    """

    pass


class ResourceConflictError(ResourceError):
    """
    Raised when there is a conflict with the current resource state.

    May occur during concurrent modifications or when the resource
    is locked (e.g., wFirma SNAPSHOT_LOCK error).
    """

    pass


# =============================================================================
# Network Errors
# =============================================================================


class NetworkError(WFirmaException):
    """
    Base class for network-related errors.

    Raised when there are issues with network communication.
    """

    pass


class ConnectionError(NetworkError):  # noqa: A001
    """
    Raised when unable to establish a connection to the API.

    Note: This shadows the built-in ConnectionError intentionally.
    Import as `from wfirma.exceptions import ConnectionError as WFirmaConnectionError`
    to avoid confusion.
    """

    pass


class TimeoutError(NetworkError):  # noqa: A001
    """
    Raised when a request times out.

    Note: This shadows the built-in TimeoutError intentionally.
    Import as `from wfirma.exceptions import TimeoutError as WFirmaTimeoutError`
    to avoid confusion.
    """

    pass


# =============================================================================
# Configuration Errors
# =============================================================================


class ConfigurationError(WFirmaException):
    """
    Base class for configuration-related errors.

    Raised when there are issues with library configuration.
    """

    pass


class MissingConfigurationError(ConfigurationError):
    """
    Raised when required configuration is missing.

    This includes missing API credentials, base URLs, or other
    required settings.
    """

    pass


class InvalidConfigurationError(ConfigurationError):
    """
    Raised when configuration values are invalid.

    This includes malformed URLs, invalid credential formats, or
    incompatible configuration combinations.
    """

    pass


__all__ = [
    # Base exception
    "WFirmaException",
    # Authentication errors
    "AuthenticationError",
    "InvalidCredentialsError",
    "TokenExpiredError",
    "InsufficientPermissionsError",
    # Validation errors
    "ValidationError",
    "InvalidFieldError",
    "MissingRequiredFieldError",
    # API errors
    "APIError",
    "RateLimitError",
    "ServerError",
    "BadRequestError",
    "ServiceUnavailableError",
    # Resource errors
    "ResourceError",
    "ResourceNotFoundError",
    "ResourceAlreadyExistsError",
    "ResourceConflictError",
    # Network errors
    "NetworkError",
    "ConnectionError",
    "TimeoutError",
    # Configuration errors
    "ConfigurationError",
    "MissingConfigurationError",
    "InvalidConfigurationError",
]

