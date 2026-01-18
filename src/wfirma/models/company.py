"""
Company models for wFirma API.

This module provides company-related model classes used in wFirma API:
- CompanyDetail - Company information/details (name, NIP, address, bank info)
- CompanyAccount - Company bank account
- CompanyAddress - Company address entry
- UserCompany - User-company relationship

Example:
    >>> from wfirma.models.company import CompanyDetail
    >>> company = CompanyDetail(
    ...     id=123,
    ...     name="Test Company",
    ...     nip="1234567890",
    ...     city="Warsaw",
    ... )
    >>> company.name
    'Test Company'
"""

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, OptionalDateTimeField


class CompanyDetail(BaseXMLModel, tag="company_detail"):
    """
    Company detail model representing company information.

    This model matches the `company_detail` structure returned by wFirma API,
    typically nested within invoice and other entity responses.

    Attributes:
        id: Company ID.
        name: Full company name.
        altname: Short/alternative company name.
        nip: Tax identification number (NIP).
        street: Street name.
        building_number: Building/house number.
        flat_number: Flat/apartment number.
        zip: Postal code.
        post: Post office name.
        city: City name.
        bank_name: Bank name for payments.
        bank_account: Bank account number.
        bank_swift: SWIFT/BIC code.
        bank_address: Bank address.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> company = CompanyDetail(
        ...     id=702218,
        ...     name="PPHU Komputery-Kowalski",
        ...     nip="8982073475",
        ...     city="Wrocław",
        ... )
    """

    id: int = element()
    name: str = element()
    altname: str | None = element(default=None)
    nip: str | None = element(default=None)
    street: str | None = element(default=None)
    building_number: str | None = element(default=None)
    flat_number: str | None = element(default=None)
    zip: str | None = element(default=None)
    post: str | None = element(default=None)
    city: str | None = element(default=None)
    bank_name: str | None = element(default=None)
    bank_account: str | None = element(default=None)
    bank_swift: str | None = element(default=None)
    bank_address: str | None = element(default=None)
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


class CompanyAccount(BaseXMLModel, tag="company_account"):
    """
    Company bank account model.

    Represents a bank account associated with a company in wFirma.
    Used by endpoints: /company_accounts/find, /company_accounts/get

    Attributes:
        id: Account ID.
        account_number: Bank account number (IBAN or local format).
        bank_name: Name of the bank.
        swift: SWIFT/BIC code.
        is_default: Whether this is the default account.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> account = CompanyAccount(
        ...     id=1,
        ...     account_number="PL59111122223333444455556666",
        ...     bank_name="PKO BP",
        ... )
    """

    id: int = element()
    account_number: str = element()
    bank_name: str | None = element(default=None)
    swift: str | None = element(default=None)
    is_default: bool | None = element(default=None)
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


class CompanyAddress(BaseXMLModel, tag="company_address"):
    """
    Company address model.

    Represents an address associated with a company.
    Used by endpoints: /company_addresses/findMain

    Attributes:
        id: Address ID.
        street: Street name.
        building_number: Building/house number.
        flat_number: Flat/apartment number.
        zip: Postal code.
        post: Post office name.
        city: City name.
        country: Country code (ISO 3166-1 alpha-2).
        is_main: Whether this is the main address.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> address = CompanyAddress(
        ...     id=1,
        ...     street="Legnicka",
        ...     building_number="33",
        ...     zip="54-162",
        ...     city="Wrocław",
        ... )
    """

    id: int = element()
    street: str = element()
    building_number: str = element()
    flat_number: str | None = element(default=None)
    zip: str = element()
    post: str | None = element(default=None)
    city: str = element()
    country: str | None = element(default=None)
    is_main: bool | None = element(default=None)
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


class UserCompany(BaseXMLModel, tag="user_company"):
    """
    User-company relationship model.

    Represents the relationship between a user and a company in wFirma.
    Used by endpoints: /user_companies/find, /user_companies/get

    This is used when a user has access to multiple companies
    and needs to select which one to operate on.

    Attributes:
        id: Relationship ID (user_company_id).
        company_id: Company ID.
        company_name: Company name (for convenience).
        role: User's role in the company.
        is_active: Whether the relationship is active.
        created: Creation timestamp.

    Example:
        >>> user_company = UserCompany(
        ...     id=1,
        ...     company_id=100,
        ...     company_name="Test Company",
        ...     role="admin",
        ... )
    """

    id: int = element()
    company_id: int = element()
    company_name: str | None = element(default=None)
    role: str | None = element(default=None)
    is_active: bool | None = element(default=None)
    created: OptionalDateTimeField = element(default=None)


__all__ = [
    "CompanyAccount",
    "CompanyAddress",
    "CompanyDetail",
    "UserCompany",
]

