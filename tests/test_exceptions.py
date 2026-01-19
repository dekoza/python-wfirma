"""
Tests for wFirma exception hierarchy.
"""

from wfirma.exceptions import (
    # API errors
    APIError,
    # Authentication errors
    AuthenticationError,
    BadRequestError,
    # Configuration errors
    ConfigurationError,
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
    TokenExpiredError,
    # Validation errors
    ValidationError,
    WFirmaException,
)
from wfirma.exceptions import (
    ConnectionError as WFirmaConnectionError,
)
from wfirma.exceptions import (
    TimeoutError as WFirmaTimeoutError,
)


class TestExceptionInheritance:
    """Test that exception hierarchy is correctly defined."""

    def test_base_exception_is_exception_subclass(self):
        """WFirmaException should inherit from Exception."""
        assert issubclass(WFirmaException, Exception)

    def test_authentication_errors_inherit_from_base(self):
        """All authentication errors should inherit from AuthenticationError."""
        assert issubclass(AuthenticationError, WFirmaException)
        assert issubclass(InvalidCredentialsError, AuthenticationError)
        assert issubclass(TokenExpiredError, AuthenticationError)
        assert issubclass(InsufficientPermissionsError, AuthenticationError)

    def test_validation_errors_inherit_from_base(self):
        """All validation errors should inherit from ValidationError."""
        assert issubclass(ValidationError, WFirmaException)
        assert issubclass(InvalidFieldError, ValidationError)
        assert issubclass(MissingRequiredFieldError, ValidationError)

    def test_api_errors_inherit_from_base(self):
        """All API errors should inherit from APIError."""
        assert issubclass(APIError, WFirmaException)
        assert issubclass(RateLimitError, APIError)
        assert issubclass(ServerError, APIError)
        assert issubclass(BadRequestError, APIError)
        assert issubclass(ServiceUnavailableError, APIError)

    def test_resource_errors_inherit_from_base(self):
        """All resource errors should inherit from ResourceError."""
        assert issubclass(ResourceError, WFirmaException)
        assert issubclass(ResourceNotFoundError, ResourceError)
        assert issubclass(ResourceAlreadyExistsError, ResourceError)
        assert issubclass(ResourceConflictError, ResourceError)

    def test_network_errors_inherit_from_base(self):
        """All network errors should inherit from NetworkError."""
        assert issubclass(NetworkError, WFirmaException)
        assert issubclass(WFirmaConnectionError, NetworkError)
        assert issubclass(WFirmaTimeoutError, NetworkError)

    def test_configuration_errors_inherit_from_base(self):
        """All configuration errors should inherit from ConfigurationError."""
        assert issubclass(ConfigurationError, WFirmaException)
        assert issubclass(MissingConfigurationError, ConfigurationError)
        assert issubclass(InvalidConfigurationError, ConfigurationError)


class TestExceptionMessageFormatting:
    """Test exception message formatting."""

    def test_base_exception_with_message(self):
        """Base exception should accept and store message."""
        exc = WFirmaException("Test error message")
        assert str(exc) == "Test error message"
        assert exc.message == "Test error message"

    def test_base_exception_without_message(self):
        """Base exception should work without message."""
        exc = WFirmaException()
        assert exc.message == ""

    def test_exception_with_error_code(self):
        """Exceptions should support error codes."""
        exc = APIError("Server error", error_code="FATAL")
        assert exc.error_code == "FATAL"
        assert exc.message == "Server error"

    def test_exception_with_status_code(self):
        """API exceptions should support HTTP status codes."""
        exc = APIError("Bad request", status_code=400)
        assert exc.status_code == 400

    def test_exception_with_all_attributes(self):
        """Exception should handle all attributes."""
        exc = APIError(
            "Rate limit exceeded",
            error_code="TOTAL_REQUESTS_LIMIT_EXCEEDED",
            status_code=429,
        )
        assert exc.message == "Rate limit exceeded"
        assert exc.error_code == "TOTAL_REQUESTS_LIMIT_EXCEEDED"
        assert exc.status_code == 429


class TestExceptionAttributes:
    """Test exception-specific attributes."""

    def test_validation_error_with_field_info(self):
        """ValidationError should store field information."""
        exc = InvalidFieldError(
            "Invalid date format",
            field="date",
            value="not-a-date",
        )
        assert exc.field == "date"
        assert exc.value == "not-a-date"
        assert exc.message == "Invalid date format"

    def test_missing_required_field_error(self):
        """MissingRequiredFieldError should store field name."""
        exc = MissingRequiredFieldError("Field is required", field="name")
        assert exc.field == "name"

    def test_resource_not_found_with_resource_info(self):
        """ResourceNotFoundError should store resource information."""
        exc = ResourceNotFoundError(
            "Invoice not found",
            resource_type="invoice",
            resource_id="12345",
        )
        assert exc.resource_type == "invoice"
        assert exc.resource_id == "12345"

    def test_rate_limit_error_with_retry_after(self):
        """RateLimitError should store retry information."""
        exc = RateLimitError(
            "Rate limit exceeded",
            retry_after=300,
        )
        assert exc.retry_after == 300


class TestAPIErrorCodeMapping:
    """Test mapping of wFirma API error codes to exceptions."""

    def test_api_error_code_property(self):
        """APIError should expose API error codes."""
        # Error codes from wFirma API documentation
        error_codes = [
            "ACCESS_DENIED",
            "ACTION_NOT_FOUND",
            "AUTH",
            "AUTH_FAILED_LIMIT_WAIT_5_MINUTES",
            "COMPANY_ID_REQUIRED",
            "DENIED_SCOPE_REQUESTED",
            "ERROR",
            "FATAL",
            "INPUT_ERROR",
            "NOT_FOUND",
            "OUT_OF_SERVICE",
            "SNAPSHOT_LOCK",
            "TOTAL_REQUESTS_LIMIT_EXCEEDED",
            "TOTAL_EXECUTION_TIME_LIMIT_EXCEEDED",
        ]
        for code in error_codes:
            exc = APIError(f"Error: {code}", error_code=code)
            assert exc.error_code == code


class TestExceptionSerialization:
    """Test exception serialization for logging."""

    def test_exception_to_dict(self):
        """Exception should be convertible to dictionary for logging."""
        exc = APIError(
            "Server error",
            error_code="FATAL",
            status_code=500,
        )
        exc_dict = exc.to_dict()
        assert exc_dict["message"] == "Server error"
        assert exc_dict["error_code"] == "FATAL"
        assert exc_dict["status_code"] == 500
        assert exc_dict["type"] == "APIError"

    def test_validation_error_to_dict(self):
        """Validation error should include field info in dict."""
        exc = InvalidFieldError(
            "Invalid value",
            field="amount",
            value="-100",
        )
        exc_dict = exc.to_dict()
        assert exc_dict["field"] == "amount"
        assert exc_dict["value"] == "-100"

    def test_resource_error_to_dict(self):
        """Resource error should include resource info in dict."""
        exc = ResourceNotFoundError(
            "Not found",
            resource_type="contractor",
            resource_id="999",
        )
        exc_dict = exc.to_dict()
        assert exc_dict["resource_type"] == "contractor"
        assert exc_dict["resource_id"] == "999"

    def test_missing_required_field_error_to_dict(self):
        """MissingRequiredFieldError should include field in dict."""
        exc = MissingRequiredFieldError(
            "Field is required",
            field="name",
        )
        exc_dict = exc.to_dict()
        assert exc_dict["field"] == "name"
        assert exc_dict["type"] == "MissingRequiredFieldError"

    def test_rate_limit_error_to_dict(self):
        """RateLimitError should include retry_after in dict."""
        exc = RateLimitError(
            "Rate limit exceeded",
            retry_after=60,
            status_code=429,
        )
        exc_dict = exc.to_dict()
        assert exc_dict["retry_after"] == 60
        assert exc_dict["status_code"] == 429
        assert exc_dict["type"] == "RateLimitError"

    def test_base_exception_repr(self):
        """Exception should have informative repr."""
        exc = WFirmaException("Test error")
        assert "WFirmaException" in repr(exc)
        assert "Test error" in repr(exc)


class TestExceptionChaining:
    """Test exception cause chaining."""

    def test_exception_with_cause(self):
        """Exception should support cause chaining."""
        original = ValueError("Original error")
        exc = NetworkError("Connection failed", cause=original)
        assert exc.__cause__ is original

    def test_exception_from_httpx_error(self):
        """NetworkError should wrap httpx exceptions."""
        # Simulating an httpx error
        original = Exception("Connection refused")
        exc = WFirmaConnectionError(
            "Failed to connect to API",
            cause=original,
        )
        assert exc.__cause__ is original
        assert "Failed to connect" in str(exc)


# AICOMPLETE: Exception hierarchy tests - ready for review
