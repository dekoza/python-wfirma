"""
Contractor models for wFirma API.

This module provides contractor-related model classes used in wFirma API:
- Contractor - Main contractor model (customer/supplier)
- ContractorDetail - Contractor detail info (embedded in invoices)

Contractors represent customers, suppliers, or other business partners.
They are used in invoices, payments, and other business documents.

Example:
    >>> from wfirma.models.contractor import Contractor
    >>> contractor = Contractor(
    ...     id=123,
    ...     name="ACME Corp",
    ...     nip="1234567890",
    ...     city="Warsaw",
    ...     country="PL",
    ...     tax_id_type="nip",
    ... )
    >>> contractor.name
    'ACME Corp'
"""

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, TimestampedFieldsMixin


class Contractor(TimestampedFieldsMixin, BaseXMLModel, tag="contractor"):
    """
    Contractor model representing a customer/supplier.

    This model matches the `contractor` structure used by wFirma API
    endpoints: /contractors/add, /contractors/find, /contractors/get, etc.

    Attributes:
        id: Contractor ID.
        name: Full company/person name.
        altname: Short/alternative name.
        nip: Polish tax identification number (NIP).
        regon: Polish business registry number (REGON).
        pesel: Polish personal identification number (PESEL).
        street: Street name.
        building_number: Building/house number.
        flat_number: Flat/apartment number.
        zip: Postal code.
        post: Post office name.
        city: City name.
        country: Country code (ISO 3166-1 alpha-2).
        tax_id_type: Type of tax ID (nip, pesel, custom, none).
        contact_name: Contact person name.
        contact_street: Contact address street.
        contact_building_number: Contact address building number.
        contact_flat_number: Contact address flat number.
        contact_zip: Contact address postal code.
        contact_post: Contact address post office.
        contact_city: Contact address city.
        contact_country: Contact address country.
        buyer: Is this contractor a buyer/customer.
        seller: Is this contractor a seller/supplier.
        remind: Send payment reminders to this contractor.
        phone: Phone number.
        fax: Fax number.
        email: Email address.
        url: Website URL.
        notes: Internal notes.
        tags: Tags/labels for categorization.
        reference_company_id: Reference to parent company.
        translation_language_id: Language for translated documents.
        company_account_id: Default bank account for payments.
        good_price_group_id: Price group for goods.
        invoice_description_id: Default invoice description.
        shop_buyer_id: E-commerce buyer ID.
        source: Source of contractor (manual, import, etc.).
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> contractor = Contractor(
        ...     id=12345,
        ...     name="Test Company Sp. z o.o.",
        ...     nip="1234567890",
        ...     city="Warsaw",
        ...     country="PL",
        ...     tax_id_type="nip",
        ...     buyer=True,
        ... )
    """

    # Required fields
    id: int = element()
    name: str = element()

    # Optional identification fields
    altname: str | None = element(default=None)
    nip: str | None = element(default=None)
    regon: str | None = element(default=None)
    pesel: str | None = element(default=None)
    tax_id_type: str | None = element(default=None)

    # Main address fields
    street: str | None = element(default=None)
    building_number: str | None = element(default=None)
    flat_number: str | None = element(default=None)
    zip: str | None = element(default=None)
    post: str | None = element(default=None)
    city: str | None = element(default=None)
    country: str | None = element(default=None)

    # Contact address fields (may differ from main address)
    contact_name: str | None = element(default=None)
    contact_street: str | None = element(default=None)
    contact_building_number: str | None = element(default=None)
    contact_flat_number: str | None = element(default=None)
    contact_zip: str | None = element(default=None)
    contact_post: str | None = element(default=None)
    contact_city: str | None = element(default=None)
    contact_country: str | None = element(default=None)

    # Relationship flags
    buyer: bool | None = element(default=None)
    seller: bool | None = element(default=None)
    remind: bool | None = element(default=None)

    # Contact information
    phone: str | None = element(default=None)
    fax: str | None = element(default=None)
    email: str | None = element(default=None)
    url: str | None = element(default=None)

    # Metadata
    notes: str | None = element(default=None)
    tags: str | None = element(default=None)
    source: str | None = element(default=None)

    # Foreign key references
    reference_company_id: int | None = element(default=None)
    translation_language_id: int | None = element(default=None)
    company_account_id: int | None = element(default=None)
    good_price_group_id: int | None = element(default=None)
    invoice_description_id: int | None = element(default=None)
    shop_buyer_id: int | None = element(default=None)


class ContractorDetail(TimestampedFieldsMixin, BaseXMLModel, tag="contractor_detail"):
    """
    Contractor detail model for embedded contractor info.

    This model matches the `contractor_detail` structure returned by wFirma API
    when contractor info is embedded in other entities (e.g., invoices).
    It contains a subset of Contractor fields typically needed for display.

    Attributes:
        id: Contractor ID.
        name: Full company/person name.
        altname: Short/alternative name.
        nip: Polish tax identification number (NIP).
        street: Street name.
        building_number: Building/house number.
        flat_number: Flat/apartment number.
        zip: Postal code.
        post: Post office name.
        city: City name.
        country: Country code (ISO 3166-1 alpha-2).
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> detail = ContractorDetail(
        ...     id=702218,
        ...     name="PPHU Komputery-Kowalski",
        ...     nip="8982073475",
        ...     city="Wrocław",
        ... )
    """

    # Required fields
    id: int = element()
    name: str = element()

    # Optional identification fields
    altname: str | None = element(default=None)
    nip: str | None = element(default=None)

    # Address fields
    street: str | None = element(default=None)
    building_number: str | None = element(default=None)
    flat_number: str | None = element(default=None)
    zip: str | None = element(default=None)
    post: str | None = element(default=None)
    city: str | None = element(default=None)
    country: str | None = element(default=None)


__all__ = [
    "Contractor",
    "ContractorDetail",
]
