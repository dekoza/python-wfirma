"""
Base Pydantic models for wFirma API data structures.

This module provides base model classes with XML and JSON serialization
support for all wFirma API entities. Uses pydantic-xml for seamless
XML handling alongside standard JSON serialization.

Note:
    This library uses standard library `datetime` instead of `pendulum`
    for better compatibility with pydantic-xml.

Example:
    >>> from wfirma.models.base import BaseXMLModel
    >>> from pydantic_xml import element
    >>> class Invoice(BaseXMLModel, tag="invoice"):
    ...     id: int = element()
    ...     date: str = element()
    >>> invoice = Invoice(id=123, date="2024-01-15")
    >>> xml_bytes = invoice.to_xml()
    >>> restored = Invoice.from_xml(xml_bytes)
"""

from datetime import datetime
from typing import Annotated

from pydantic import BeforeValidator, ConfigDict, PlainSerializer
from pydantic_xml import BaseXmlModel, element

# ============================================================================
# DateTime Parsing and Formatting Functions
# ============================================================================

WFIRMA_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WFIRMA_NULL_DATETIME = "0000-00-00 00:00:00"


def parse_wfirma_datetime(value: str | datetime | None) -> datetime | None:
    """
    Parse datetime value from wFirma API format.

    Handles various datetime formats:
    - wFirma format: "YYYY-MM-DD HH:MM:SS"
    - Null datetime: "0000-00-00 00:00:00" (returns None)
    - Empty string (returns None)
    - None (returns None)
    - datetime object (returns as-is)

    Args:
        value: Datetime value to parse.

    Returns:
        datetime instance or None for null/empty values.

    Raises:
        ValueError: If the datetime format is invalid.

    Example:
        >>> parse_wfirma_datetime("2024-01-15 10:30:45")
        datetime.datetime(2024, 1, 15, 10, 30, 45)
        >>> parse_wfirma_datetime("0000-00-00 00:00:00")
        None
    """
    if value is None:
        return None

    if isinstance(value, datetime):
        return value

    if isinstance(value, str):
        # Handle empty string
        if not value.strip():
            return None

        # Handle wFirma null datetime
        if value == WFIRMA_NULL_DATETIME:
            return None

        # Parse standard wFirma format
        try:
            return datetime.strptime(value, WFIRMA_DATETIME_FORMAT)
        except ValueError as err:
            raise ValueError(f"Invalid datetime format: {value}") from err

    raise ValueError(f"Expected datetime string or datetime object, got {type(value)}")


def format_wfirma_datetime(dt: datetime | None) -> str | None:
    """
    Format datetime to wFirma format.

    Args:
        dt: datetime instance or None.

    Returns:
        Datetime string in "YYYY-MM-DD HH:MM:SS" format or None.

    Example:
        >>> from datetime import datetime
        >>> format_wfirma_datetime(datetime(2024, 1, 15, 10, 30, 45))
        '2024-01-15 10:30:45'
        >>> format_wfirma_datetime(None)
        None
    """
    if dt is None:
        return None
    return dt.strftime(WFIRMA_DATETIME_FORMAT)


# Type alias for datetime fields with automatic parsing and serialization
DateTimeField = Annotated[
    datetime,
    BeforeValidator(parse_wfirma_datetime),
    PlainSerializer(format_wfirma_datetime, return_type=str),
]

# Type alias for optional datetime fields (handles null/empty values from API)
OptionalDateTimeField = Annotated[
    datetime | None,
    BeforeValidator(parse_wfirma_datetime),
    PlainSerializer(format_wfirma_datetime, return_type=str | None),
]


# ============================================================================
# Base Model Classes
# ============================================================================


class WFirmaBaseModel(BaseXmlModel, search_mode="unordered"):
    """
    Base model for all wFirma data structures.

    Provides common configuration for Pydantic models used in the
    wFirma library. Features:
    - Immutable instances (frozen)
    - Extra XML elements ignored during parsing (API may add new fields)
    - Validation of assignments
    - Unordered XML search mode (elements can appear in any order)

    Example:
        >>> from pydantic_xml import element
        >>> class Contractor(WFirmaBaseModel):
        ...     name: str = element()
        ...     nip: str | None = element(default=None)
        >>> contractor = Contractor(name="ACME Corp")
    """

    model_config = ConfigDict(
        frozen=True,  # Immutable instances
        validate_assignment=True,  # Validate on assignment (for non-frozen subclasses)
        populate_by_name=True,  # Allow using field names or aliases
        str_strip_whitespace=True,  # Strip whitespace from strings
    )


class BaseXMLModel(WFirmaBaseModel):
    """
    Base model with XML serialization support.

    Extends WFirmaBaseModel with convenient methods for XML
    serialization and deserialization using pydantic-xml.

    The `tag` class parameter must be specified when subclassing
    to define the XML root element name.

    Example:
        >>> from pydantic_xml import element
        >>> class Invoice(BaseXMLModel, tag="invoice"):
        ...     id: int = element()
        ...     date: str = element()
        >>> invoice = Invoice(id=123, date="2024-01-15")
        >>> xml_bytes = invoice.to_xml()
        >>> print(xml_bytes.decode())
        <invoice><id>123</id><date>2024-01-15</date></invoice>
    """

    pass  # Inherits all XML functionality from pydantic-xml


# ============================================================================
# Response Models
# ============================================================================


class ResponseStatus(BaseXMLModel, tag="status"):
    """
    API response status model.

    Represents the status element in wFirma API responses.
    Common status codes:
    - OK: Request successful
    - ERROR: Validation error
    - AUTH: Authentication required
    - NOT FOUND: Resource not found
    - ACCESS DENIED: Permission denied

    Attributes:
        code: Status code string.

    Example:
        >>> status = ResponseStatus(code="OK")
        >>> status.is_success
        True
    """

    code: str = element()

    @property
    def is_success(self) -> bool:
        """
        Check if status indicates success.

        Returns:
            True if status code is "OK", False otherwise.
        """
        return self.code == "OK"


class ResponseParameters(BaseXMLModel, tag="parameters"):
    """
    API response pagination parameters.

    Contains pagination information returned by find operations.

    Attributes:
        limit: Number of items per page.
        page: Current page number (1-based).
        total: Total number of items.

    Example:
        >>> params = ResponseParameters(limit=20, page=1, total=100)
        >>> params.total_pages
        5
        >>> params.has_more_pages
        True
    """

    limit: int = element()
    page: int = element()
    total: int = element()

    @property
    def has_more_pages(self) -> bool:
        """
        Check if there are more pages available.

        Returns:
            True if current page is not the last page.
        """
        return self.page < self.total_pages

    @property
    def total_pages(self) -> int:
        """
        Calculate total number of pages.

        Returns:
            Total number of pages based on limit and total.
        """
        if self.total == 0 or self.limit == 0:
            return 0
        return (self.total + self.limit - 1) // self.limit


__all__ = [
    "BaseXMLModel",
    "DateTimeField",
    "OptionalDateTimeField",
    "ResponseParameters",
    "ResponseStatus",
    "WFirmaBaseModel",
    "format_wfirma_datetime",
    "parse_wfirma_datetime",
]
