"""
Common Pydantic models for wFirma API data structures.

This module provides shared model classes used across wFirma API entities,
including address, contact information, currency, and tax-related data.

Example:
    >>> from wfirma.models.common import Address, Currency, Money
    >>> address = Address(
    ...     street="Legnicka",
    ...     building_number="33",
    ...     zip_code="54-162",
    ...     city="Wrocław",
    ... )
    >>> money = Money(amount="100.50", currency=Currency.PLN)
"""

import re
from decimal import ROUND_HALF_UP, Decimal
from enum import Enum
from typing import Annotated

from pydantic import BeforeValidator, EmailStr, field_validator
from pydantic_xml import element

from wfirma.models.base import BaseXMLModel

# ============================================================================
# Enumerations
# ============================================================================


class CountryCode(str, Enum):
    """
    ISO 3166-1 alpha-2 country codes.

    Contains common country codes used in wFirma API.
    This is not exhaustive - additional codes can be added as needed.

    Example:
        >>> CountryCode.PL.value
        'PL'
    """

    # EU countries
    AT = "AT"  # Austria
    BE = "BE"  # Belgium
    BG = "BG"  # Bulgaria
    CY = "CY"  # Cyprus
    CZ = "CZ"  # Czech Republic
    DE = "DE"  # Germany
    DK = "DK"  # Denmark
    EE = "EE"  # Estonia
    ES = "ES"  # Spain
    FI = "FI"  # Finland
    FR = "FR"  # France
    GB = "GB"  # United Kingdom
    GR = "GR"  # Greece
    HR = "HR"  # Croatia
    HU = "HU"  # Hungary
    IE = "IE"  # Ireland
    IT = "IT"  # Italy
    LT = "LT"  # Lithuania
    LU = "LU"  # Luxembourg
    LV = "LV"  # Latvia
    MT = "MT"  # Malta
    NL = "NL"  # Netherlands
    PL = "PL"  # Poland
    PT = "PT"  # Portugal
    RO = "RO"  # Romania
    SE = "SE"  # Sweden
    SI = "SI"  # Slovenia
    SK = "SK"  # Slovakia

    # Other common countries
    CH = "CH"  # Switzerland
    NO = "NO"  # Norway
    UA = "UA"  # Ukraine
    US = "US"  # United States
    CN = "CN"  # China
    JP = "JP"  # Japan
    RU = "RU"  # Russia


class TaxIdType(str, Enum):
    """
    Tax ID types supported by wFirma API.

    Attributes:
        NIP: Polish tax identification number.
        PESEL: Polish personal identification number.
        CUSTOM: Custom/foreign tax ID.
        NONE: No tax ID.

    Example:
        >>> TaxIdType.NIP.value
        'nip'
    """

    NIP = "nip"
    PESEL = "pesel"
    CUSTOM = "custom"
    NONE = "none"


class VATRate(str, Enum):
    """
    VAT rates supported by wFirma API.

    Polish VAT rates:
    - 23% - standard rate
    - 8% - reduced rate (e.g., food, medicines)
    - 5% - reduced rate (e.g., books, newspapers)
    - 0% - zero rate (e.g., exports)
    - zw - exempt (zwolniony)
    - np - not applicable (nie podlega)
    - oo - reverse charge (odwrotne obciążenie)

    Example:
        >>> VATRate.VAT_23.value
        '23'
        >>> VATRate.VAT_23.as_decimal()
        Decimal('0.23')
    """

    VAT_23 = "23"
    VAT_8 = "8"
    VAT_5 = "5"
    VAT_0 = "0"
    ZW = "zw"  # Exempt
    NP = "np"  # Not applicable
    OO = "oo"  # Reverse charge

    def as_decimal(self) -> Decimal:
        """
        Convert VAT rate to decimal multiplier.

        Returns:
            Decimal multiplier (e.g., 0.23 for 23%).
            Returns 0 for exempt, not applicable, and reverse charge.

        Example:
            >>> VATRate.VAT_23.as_decimal()
            Decimal('0.23')
        """
        if self.value in ("zw", "np", "oo"):
            return Decimal("0")
        return Decimal(self.value) / 100


class Currency(str, Enum):
    """
    Currency codes supported by wFirma API.

    Uses ISO 4217 currency codes.

    Example:
        >>> Currency.PLN.value
        'PLN'
    """

    PLN = "PLN"  # Polish Złoty
    EUR = "EUR"  # Euro
    USD = "USD"  # US Dollar
    GBP = "GBP"  # British Pound
    CHF = "CHF"  # Swiss Franc
    CZK = "CZK"  # Czech Koruna
    DKK = "DKK"  # Danish Krone
    SEK = "SEK"  # Swedish Krona
    NOK = "NOK"  # Norwegian Krone


# ============================================================================
# Validators
# ============================================================================


def _normalize_phone_number(value: str) -> str:
    """
    Normalize phone number by removing spaces, dashes, and parentheses.

    Keeps the plus sign for international format.

    Args:
        value: Raw phone number string.

    Returns:
        Normalized phone number string.
    """
    if not value:
        return value
    # Remove spaces, dashes, parentheses
    normalized = re.sub(r"[\s\-\(\)]", "", value)
    return normalized


def _validate_phone_number(value: str) -> str:
    """
    Validate and normalize phone number.

    Args:
        value: Phone number to validate.

    Returns:
        Normalized phone number.

    Raises:
        ValueError: If phone number is invalid.
    """
    normalized = _normalize_phone_number(value)

    # Check minimum length (at least 6 digits for short numbers)
    digits_only = re.sub(r"[^\d]", "", normalized)
    if len(digits_only) < 6:
        raise ValueError(f"Phone number too short: {value}")

    # Check for invalid characters (only digits and + allowed after normalization)
    if not re.match(r"^\+?\d+$", normalized):
        raise ValueError(f"Phone number contains invalid characters: {value}")

    return normalized


def _round_money(value: Decimal | float | int | str) -> Decimal:
    """
    Round money value to 2 decimal places.

    Args:
        value: Monetary amount to round.

    Returns:
        Decimal rounded to 2 decimal places.
    """
    decimal_value = value if isinstance(value, Decimal) else Decimal(str(value))
    return decimal_value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


# Type alias for phone number with validation
PhoneNumber = Annotated[str, BeforeValidator(_validate_phone_number)]


# ============================================================================
# Models
# ============================================================================


class Email(BaseXMLModel, tag="email"):
    """
    Email address model with validation.

    Uses Pydantic's EmailStr for validation.

    Attributes:
        value: Validated email address.

    Example:
        >>> email = Email(value="user@example.com")
        >>> email.value
        'user@example.com'
    """

    value: EmailStr = element()

    @field_validator("value", mode="before")
    @classmethod
    def strip_whitespace(cls, v: str) -> str:
        """Strip whitespace from email before validation."""
        if isinstance(v, str):
            return v.strip()
        return v


class Phone(BaseXMLModel, tag="phone"):
    """
    Phone number model with normalization.

    Normalizes phone numbers by removing spaces, dashes, and parentheses.
    Validates minimum length and character set.

    Attributes:
        number: Normalized phone number.

    Example:
        >>> phone = Phone(number="+48 123 456 789")
        >>> phone.number
        '+48123456789'
    """

    number: PhoneNumber = element()


class Money(BaseXMLModel, tag="money"):
    """
    Monetary amount model with currency.

    Automatically rounds amounts to 2 decimal places.
    Default currency is PLN.

    Attributes:
        amount: Decimal amount (2 decimal places).
        currency: Currency code (default PLN).

    Example:
        >>> money = Money(amount="123.456", currency=Currency.PLN)
        >>> money.amount
        Decimal('123.46')
    """

    amount: Annotated[Decimal, BeforeValidator(_round_money)] = element()
    currency: Currency = element(default=Currency.PLN)


class Address(BaseXMLModel, tag="address"):
    """
    Physical address model.

    Represents a physical address with fields matching wFirma API structure.
    Uses XML element names matching the API (e.g., 'zip' instead of 'zip_code').

    Attributes:
        street: Street name.
        building_number: Building/house number.
        flat_number: Flat/apartment number (optional).
        zip_code: Postal code (XML tag: 'zip').
        city: City name.
        post: Post office name (optional, may differ from city).
        country: Country code (default PL).

    Example:
        >>> address = Address(
        ...     street="Legnicka",
        ...     building_number="33",
        ...     zip_code="54-162",
        ...     city="Wrocław",
        ... )
    """

    street: str = element()
    building_number: str = element()
    flat_number: str | None = element(default=None)
    zip_code: str = element(tag="zip")
    city: str = element()
    post: str | None = element(default=None)
    country: CountryCode = element(default=CountryCode.PL)


class BankAccount(BaseXMLModel, tag="bank_account"):
    """
    Bank account model.

    Represents bank account information for payments.

    Attributes:
        account_number: Bank account number (IBAN or local format).
        bank_name: Name of the bank (optional).
        swift: SWIFT/BIC code (optional).
        bank_address: Bank branch address (optional).

    Example:
        >>> account = BankAccount(
        ...     account_number="59 1111 2222 3333 4444 5555 6666",
        ...     bank_name="BZWBK",
        ... )
    """

    account_number: str = element(tag="bank_account")
    bank_name: str | None = element(default=None)
    swift: str | None = element(tag="bank_swift", default=None)
    bank_address: str | None = element(default=None)


__all__ = [
    "Address",
    "BankAccount",
    "CountryCode",
    "Currency",
    "Email",
    "Money",
    "Phone",
    "PhoneNumber",
    "TaxIdType",
    "VATRate",
]

