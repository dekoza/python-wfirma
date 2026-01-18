"""
Payment models for wFirma API.

This module provides payment-related model classes used in wFirma API:
- Payment - Main payment record model
- PaymentCashbox - Payment cashbox (kasa) model
- PaymentObjectType - Enum for payment object types (invoice, expense, etc.)
- PaymentType - Enum for payment types (income, expense)

Payments represent financial transactions linked to invoices, expenses,
or other documents. Each payment is associated with a cashbox (kasa).

Example:
    >>> from wfirma.models.payment import Payment, PaymentObjectType
    >>> from decimal import Decimal
    >>> payment = Payment(
    ...     id=12345,
    ...     object_name=PaymentObjectType.INVOICE,
    ...     object_id=68827818,
    ...     value=Decimal("100.00"),
    ...     date="2020-02-20",
    ... )
    >>> payment.object_name
    PaymentObjectType.INVOICE
"""

from decimal import Decimal
from enum import Enum

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, OptionalDateTimeField


class PaymentObjectType(str, Enum):
    """
    Enum for payment object types.

    Defines the type of document that the payment is linked to.

    Attributes:
        INVOICE: Payment for a sales invoice.
        EXPENSE: Payment for an expense.
        INVOICE_RECURRING: Payment for a recurring invoice.
        EXPENSE_RECURRING: Payment for a recurring expense.
    """

    INVOICE = "invoice"
    EXPENSE = "expense"
    INVOICE_RECURRING = "invoicerecurring"
    EXPENSE_RECURRING = "expenserecurring"


class PaymentType(str, Enum):
    """
    Enum for payment types.

    Attributes:
        INCOME: Incoming payment (receipt).
        EXPENSE: Outgoing payment.
    """

    INCOME = "income"
    EXPENSE = "expense"


class PaymentCashbox(BaseXMLModel, tag="payment_cashbox"):
    """
    Payment cashbox (kasa) model.

    Represents a cashbox/bank account where payments are recorded.
    Used for tracking cash flow and bank reconciliation.

    Attributes:
        id: Cashbox ID.
        name: Cashbox name.
        description: Cashbox description.
        balance: Current balance.
        bank_account: Bank account number (IBAN).
        bank_name: Bank name.
        is_default: Whether this is the default cashbox.
        company_id: Reference to company.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> cashbox = PaymentCashbox(
        ...     id=1,
        ...     name="Main cashbox",
        ...     balance=Decimal("5000.00"),
        ... )
    """

    # Required fields
    id: int = element()
    name: str = element()

    # Optional description
    description: str | None = element(default=None)

    # Balance
    balance: Decimal | None = element(default=None)

    # Bank info
    bank_account: str | None = element(default=None)
    bank_name: str | None = element(default=None)

    # Flags
    is_default: bool | None = element(default=None)

    # Foreign keys
    company_id: int | None = element(default=None)

    # Timestamps
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


class Payment(BaseXMLModel, tag="payment"):
    """
    Payment model representing a financial transaction.

    This model matches the `payment` structure used by wFirma API
    endpoints: /payments/add, /payments/find, /payments/get, etc.

    A payment is linked to a document (invoice, expense, etc.) and
    represents money received or paid. Payments can be partial,
    allowing for tracking of installments.

    Attributes:
        id: Payment ID.
        object_name: Type of linked document (invoice, expense, etc.).
        object_id: ID of the linked document.
        value: Payment amount (positive for income, negative for expense).
        date: Payment date (YYYY-MM-DD).
        type: Payment type (income/expense).
        description: Payment description/notes.
        payment_cashbox_id: Reference to PaymentCashbox.
        company_id: Reference to Company.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> from decimal import Decimal
        >>> payment = Payment(
        ...     id=12345,
        ...     object_name=PaymentObjectType.INVOICE,
        ...     object_id=68827818,
        ...     value=Decimal("100.00"),
        ...     date="2020-02-20",
        ... )
        >>> payment.value
        Decimal('100.00')
    """

    # Required fields
    id: int = element()

    # Link to document
    object_name: PaymentObjectType | None = element(default=None)
    object_id: int | None = element(default=None)

    # Payment details
    value: Decimal | None = element(default=None)
    date: str | None = element(default=None)
    type: PaymentType | None = element(default=None)

    # Metadata
    description: str | None = element(default=None)

    # Foreign keys
    payment_cashbox_id: int | None = element(default=None)
    company_id: int | None = element(default=None)

    # Timestamps
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


__all__ = [
    "Payment",
    "PaymentCashbox",
    "PaymentObjectType",
    "PaymentType",
]

