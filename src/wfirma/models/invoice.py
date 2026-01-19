"""
Invoice models for wFirma API.

This module provides invoice-related model classes used in wFirma API:
- Invoice - Main invoice model
- InvoiceContent - Invoice line item model
- InvoiceType - Enum for invoice types (normal, proforma, correction, etc.)
- PaymentMethod - Enum for payment methods (cash, transfer, card, etc.)
- PaymentState - Enum for payment states (paid, unpaid, partial)
- DisposalDateFormat - Enum for disposal date format (date, month)

Invoices are core business documents for sales and purchases.
They contain header information, line items (invoicecontents),
and related information like contractor and company details.

Example:
    >>> from wfirma.models.invoice import Invoice, InvoiceType, PaymentMethod
    >>> invoice = Invoice(
    ...     id=1207242,
    ...     fullnumber="FV 1/2024",
    ...     type=InvoiceType.NORMAL,
    ...     paymentmethod=PaymentMethod.TRANSFER,
    ...     netto=Decimal("970.00"),
    ...     brutto=Decimal("1193.10"),
    ... )
    >>> invoice.fullnumber
    'FV 1/2024'
"""

from decimal import Decimal
from enum import Enum

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, OptionalDateTimeField


class InvoiceType(str, Enum):
    """
    Enum for invoice types.

    Attributes:
        NORMAL: Standard VAT invoice.
        PROFORMA: Proforma invoice (not a VAT document).
        CORRECTION: Corrective invoice (adjustment to previous invoice).
        RECEIPT: Receipt (paragon) invoice.
        FINAL: Final invoice (after proforma).
    """

    NORMAL = "normal"
    PROFORMA = "proforma"
    CORRECTION = "correction"
    RECEIPT = "receipt"
    FINAL = "final"


class PaymentMethod(str, Enum):
    """
    Enum for payment methods.

    Attributes:
        CASH: Cash payment.
        TRANSFER: Bank transfer.
        CARD: Card payment.
        COMPENSATION: Compensation/barter.
        ADVANCE: Advance payment.
        CHECK: Check payment.
    """

    CASH = "cash"
    TRANSFER = "transfer"
    CARD = "card"
    COMPENSATION = "compensation"
    ADVANCE = "advance"
    CHECK = "check"


class PaymentState(str, Enum):
    """
    Enum for payment states.

    Attributes:
        PAID: Invoice fully paid.
        UNPAID: Invoice not paid.
        PARTIAL: Invoice partially paid.
    """

    PAID = "paid"
    UNPAID = "unpaid"
    PARTIAL = "partial"


class DisposalDateFormat(str, Enum):
    """
    Enum for disposal date format on invoice.

    The disposal date can be shown as exact date or just month.

    Attributes:
        DATE: Show full date (YYYY-MM-DD).
        MONTH: Show only month (YYYY-MM).
    """

    DATE = "date"
    MONTH = "month"


class InvoiceContent(BaseXMLModel, tag="invoicecontent"):
    """
    Invoice line item model.

    This model matches the `invoicecontent` structure used by wFirma API
    within invoices. Each invoice can have multiple invoice contents
    representing individual line items.

    Attributes:
        id: Line item ID.
        name: Product/service name on invoice.
        classification: PKWiU or other classification code.
        unit: Unit of measure (szt., kg, h, etc.).
        count: Quantity.
        price: Unit price (net).
        price_modified: Whether price was manually modified.
        discount: Whether discount is applied.
        discount_percent: Discount percentage.
        netto: Net total for this line item.
        brutto: Gross total for this line item.
        vat: VAT rate (23, 8, 5, 0, zw, np, oo).
        lumpcode: Lump sum tax code.
        good_id: Reference to Good model.
        invoice_id: Reference to parent Invoice.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> content = InvoiceContent(
        ...     id=3187305,
        ...     name="Widget",
        ...     unit="szt.",
        ...     count=Decimal("10.0000"),
        ...     price=Decimal("100.00"),
        ...     vat="23",
        ... )
    """

    # Required fields
    id: int = element()
    name: str = element()

    # Classification
    classification: str | None = element(default=None)

    # Quantity and pricing
    unit: str | None = element(default=None)
    count: Decimal | None = element(default=None)
    price: Decimal | None = element(default=None)
    price_modified: bool | None = element(default=None)
    unit_count: Decimal | None = element(default=None)

    # Discounts
    discount: bool | None = element(default=None)
    discount_percent: Decimal | None = element(default=None)

    # Totals (calculated by API)
    netto: Decimal | None = element(default=None)
    brutto: Decimal | None = element(default=None)

    # Tax fields
    vat: str | None = element(default=None)
    lumpcode: str | None = element(default=None)

    # Foreign key references (stored as IDs, not nested objects)
    good_id: int | None = element(default=None)
    invoice_id: int | None = element(default=None)
    tangiblefixedasset_id: int | None = element(default=None)
    equipment_id: int | None = element(default=None)
    vehicle_id: int | None = element(default=None)

    # Timestamps
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


class Invoice(BaseXMLModel, tag="invoice"):
    """
    Invoice model representing a sales/purchase invoice.

    This model matches the `invoice` structure used by wFirma API
    endpoints: /invoices/add, /invoices/find, /invoices/get, etc.

    Attributes:
        id: Invoice ID.
        fullnumber: Full invoice number (e.g., "FV 1/2024").
        number: Sequential invoice number.
        date: Issue date (YYYY-MM-DD).
        disposaldate: Disposal/delivery date.
        disposaldate_format: Format of disposal date (date or month).
        paymentmethod: Payment method (cash, transfer, etc.).
        paymentdate: Payment due date.
        paymentstate: Payment status (paid, unpaid, partial).
        type: Invoice type (normal, proforma, correction).
        type_of_sale: Type of sale for JPK purposes.
        netto: Net total.
        brutto: Gross total.
        tax: Total VAT amount.
        paid: Amount paid.
        remaining: Remaining amount to pay.
        currency: Currency code (PLN, EUR, etc.).
        currency_exchange: Exchange rate.
        currency_date: Exchange rate date.
        currency_label: Show currency label on invoice.
        description: Invoice description.
        notes: Internal notes.
        tags: Tags for categorization.
        contractor_id: Reference to Contractor.
        series_id: Reference to invoice series.
        company_detail_id: Reference to CompanyDetail.
        user_company_id: Reference to UserCompany.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> invoice = Invoice(
        ...     id=1207242,
        ...     fullnumber="FV 1/2024",
        ...     date="2024-01-15",
        ...     type=InvoiceType.NORMAL,
        ...     paymentmethod=PaymentMethod.TRANSFER,
        ...     netto=Decimal("970.00"),
        ...     brutto=Decimal("1193.10"),
        ... )
    """

    # Required fields
    id: int = element()

    # Invoice number fields
    fullnumber: str | None = element(default=None)
    number: int | None = element(default=None)

    # Date fields (stored as strings in wFirma format)
    date: str | None = element(default=None)
    disposaldate: str | None = element(default=None)
    disposaldate_format: DisposalDateFormat | None = element(default=None)

    # Payment fields
    paymentmethod: PaymentMethod | None = element(default=None)
    paymentdate: str | None = element(default=None)
    paymentstate: PaymentState | None = element(default=None)

    # Invoice type
    type: InvoiceType | None = element(default=None)
    type_of_sale: str | None = element(default=None)

    # Total amounts
    netto: Decimal | None = element(default=None)
    brutto: Decimal | None = element(default=None)
    tax: Decimal | None = element(default=None)
    paid: Decimal | None = element(default=None)
    remaining: Decimal | None = element(default=None)

    # Currency fields
    currency: str | None = element(default=None)
    currency_exchange: Decimal | None = element(default=None)
    currency_date: str | None = element(default=None)
    currency_label: bool | None = element(default=None)

    # Metadata
    description: str | None = element(default=None)
    notes: str | None = element(default=None)
    tags: str | None = element(default=None)

    # Boolean flags
    alreadysent: bool | None = element(default=None)
    alreadysent_printed: bool | None = element(default=None)
    fiscal: bool | None = element(default=None)
    template: str | None = element(default=None)

    # Split payment (MPP - mechanizm podzielonej płatności)
    split_payment: bool | None = element(default=None)

    # Foreign key references
    contractor_id: int | None = element(default=None)
    series_id: int | None = element(default=None)
    company_detail_id: int | None = element(default=None)
    user_company_id: int | None = element(default=None)
    translation_language_id: int | None = element(default=None)
    corrected_invoice_id: int | None = element(default=None)

    # Timestamps
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


__all__ = [
    "DisposalDateFormat",
    "Invoice",
    "InvoiceContent",
    "InvoiceType",
    "PaymentMethod",
    "PaymentState",
]
