"""
Tests for payment Pydantic models.

These tests verify payment models for wFirma API:
- Payment - Main payment model
- PaymentCashbox - Payment cashbox (kasa) model
- PaymentObjectType - Enum for payment object types (invoice, expense, etc.)
- PaymentType - Enum for payment types (income, expense)

Based on wFirma API structure from /payments/add, /payments/find, /payments/get, etc.

Payment fields from API documentation:
- id, value, date
- object_name - type of related document (invoice, expense, etc.)
- object_id - ID of related document
- payment_cashbox (reference to cashbox)
- created, modified
"""

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from wfirma.models.payment import (
    Payment,
    PaymentCashbox,
    PaymentObjectType,
    PaymentType,
)


class TestPaymentObjectType:
    """Tests for PaymentObjectType enum."""

    # AICOMPLETE: PaymentObjectType enum tests - ready for review

    def test_payment_object_type_values(self) -> None:
        """Test PaymentObjectType enum has expected values."""
        assert PaymentObjectType.INVOICE.value == "invoice"
        assert PaymentObjectType.EXPENSE.value == "expense"
        assert PaymentObjectType.INVOICE_RECURRING.value == "invoicerecurring"
        assert PaymentObjectType.EXPENSE_RECURRING.value == "expenserecurring"

    def test_payment_object_type_from_string(self) -> None:
        """Test creating PaymentObjectType from string value."""
        assert PaymentObjectType("invoice") == PaymentObjectType.INVOICE
        assert PaymentObjectType("expense") == PaymentObjectType.EXPENSE
        assert PaymentObjectType("invoicerecurring") == PaymentObjectType.INVOICE_RECURRING

    def test_payment_object_type_invalid(self) -> None:
        """Test PaymentObjectType raises error for invalid value."""
        with pytest.raises(ValueError):
            PaymentObjectType("invalid")


class TestPaymentType:
    """Tests for PaymentType enum."""

    # AICOMPLETE: PaymentType enum tests - ready for review

    def test_payment_type_values(self) -> None:
        """Test PaymentType enum has expected values."""
        assert PaymentType.INCOME.value == "income"
        assert PaymentType.EXPENSE.value == "expense"

    def test_payment_type_from_string(self) -> None:
        """Test creating PaymentType from string value."""
        assert PaymentType("income") == PaymentType.INCOME
        assert PaymentType("expense") == PaymentType.EXPENSE

    def test_payment_type_invalid(self) -> None:
        """Test PaymentType raises error for invalid value."""
        with pytest.raises(ValueError):
            PaymentType("invalid")


class TestPaymentCashbox:
    """Tests for PaymentCashbox model."""

    # AICOMPLETE: PaymentCashbox model tests - ready for review

    def test_cashbox_creation_minimal(self) -> None:
        """Test creating PaymentCashbox with minimal required fields."""
        cashbox = PaymentCashbox(id=1, name="Main cashbox")
        assert cashbox.id == 1
        assert cashbox.name == "Main cashbox"

    def test_cashbox_creation_full(self) -> None:
        """Test creating PaymentCashbox with all fields."""
        cashbox = PaymentCashbox(
            id=123,
            name="Main cashbox",
            description="Company main cashbox",
            balance=Decimal("5000.00"),
            bank_account="PL12345678901234567890123456",
            bank_name="PKO BP",
            is_default=True,
            company_id=456,
            created=datetime(2024, 1, 15, 10, 30, 45),
            modified=datetime(2024, 1, 20, 14, 0, 0),
        )
        assert cashbox.id == 123
        assert cashbox.name == "Main cashbox"
        assert cashbox.description == "Company main cashbox"
        assert cashbox.balance == Decimal("5000.00")
        assert cashbox.bank_account == "PL12345678901234567890123456"
        assert cashbox.bank_name == "PKO BP"
        assert cashbox.is_default is True
        assert cashbox.company_id == 456
        assert cashbox.created == datetime(2024, 1, 15, 10, 30, 45)
        assert cashbox.modified == datetime(2024, 1, 20, 14, 0, 0)

    def test_cashbox_optional_fields_default_none(self) -> None:
        """Test that optional fields default to None."""
        cashbox = PaymentCashbox(id=1, name="Test")
        assert cashbox.description is None
        assert cashbox.balance is None
        assert cashbox.bank_account is None
        assert cashbox.bank_name is None
        assert cashbox.is_default is None
        assert cashbox.company_id is None
        assert cashbox.created is None
        assert cashbox.modified is None

    def test_cashbox_xml_serialization(self) -> None:
        """Test PaymentCashbox XML serialization."""
        cashbox = PaymentCashbox(
            id=123,
            name="Main cashbox",
            balance=Decimal("1000.00"),
        )
        xml_bytes = cashbox.to_xml()
        assert b"<payment_cashbox" in xml_bytes
        assert b"<id>123</id>" in xml_bytes
        assert b"<name>Main cashbox</name>" in xml_bytes
        assert b"1000.00" in xml_bytes

    def test_cashbox_xml_deserialization(self) -> None:
        """Test PaymentCashbox XML deserialization."""
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <payment_cashbox>
            <id>456</id>
            <name>Test cashbox</name>
            <balance>2500.50</balance>
        </payment_cashbox>
        """
        cashbox = PaymentCashbox.from_xml(xml)
        assert cashbox.id == 456
        assert cashbox.name == "Test cashbox"
        assert cashbox.balance == Decimal("2500.50")

    def test_cashbox_immutable(self) -> None:
        """Test that PaymentCashbox is immutable."""
        cashbox = PaymentCashbox(id=1, name="Test")
        with pytest.raises(ValidationError):
            cashbox.id = 2


class TestPayment:
    """Tests for Payment model."""

    # AICOMPLETE: Payment model tests - ready for review

    def test_payment_creation_minimal(self) -> None:
        """Test creating Payment with minimal required fields."""
        payment = Payment(id=1)
        assert payment.id == 1

    def test_payment_creation_typical(self) -> None:
        """Test creating Payment with typical fields from API."""
        payment = Payment(
            id=12345,
            object_name=PaymentObjectType.INVOICE,
            object_id=68827818,
            value=Decimal("100.00"),
            date="2020-02-20",
        )
        assert payment.id == 12345
        assert payment.object_name == PaymentObjectType.INVOICE
        assert payment.object_id == 68827818
        assert payment.value == Decimal("100.00")
        assert payment.date == "2020-02-20"

    def test_payment_creation_full(self) -> None:
        """Test creating Payment with all fields."""
        payment = Payment(
            id=12345,
            object_name=PaymentObjectType.INVOICE,
            object_id=68827818,
            value=Decimal("100.00"),
            date="2020-02-20",
            type=PaymentType.INCOME,
            description="Payment for invoice FV 1/2024",
            payment_cashbox_id=789,
            company_id=456,
            created=datetime(2024, 1, 15, 10, 30, 45),
            modified=datetime(2024, 1, 20, 14, 0, 0),
        )
        assert payment.id == 12345
        assert payment.object_name == PaymentObjectType.INVOICE
        assert payment.object_id == 68827818
        assert payment.value == Decimal("100.00")
        assert payment.date == "2020-02-20"
        assert payment.type == PaymentType.INCOME
        assert payment.description == "Payment for invoice FV 1/2024"
        assert payment.payment_cashbox_id == 789
        assert payment.company_id == 456
        assert payment.created == datetime(2024, 1, 15, 10, 30, 45)
        assert payment.modified == datetime(2024, 1, 20, 14, 0, 0)

    def test_payment_optional_fields_default_none(self) -> None:
        """Test that optional fields default to None."""
        payment = Payment(id=1)
        assert payment.object_name is None
        assert payment.object_id is None
        assert payment.value is None
        assert payment.date is None
        assert payment.type is None
        assert payment.description is None
        assert payment.payment_cashbox_id is None
        assert payment.company_id is None
        assert payment.created is None
        assert payment.modified is None

    def test_payment_with_expense_object(self) -> None:
        """Test Payment linked to an expense."""
        payment = Payment(
            id=999,
            object_name=PaymentObjectType.EXPENSE,
            object_id=55555,
            value=Decimal("-250.00"),
            type=PaymentType.EXPENSE,
        )
        assert payment.object_name == PaymentObjectType.EXPENSE
        assert payment.type == PaymentType.EXPENSE
        assert payment.value == Decimal("-250.00")

    def test_payment_decimal_precision(self) -> None:
        """Test Payment handles decimal precision correctly."""
        payment = Payment(
            id=1,
            value=Decimal("1234.56789"),
        )
        assert payment.value == Decimal("1234.56789")

    def test_payment_xml_serialization(self) -> None:
        """Test Payment XML serialization for API request."""
        payment = Payment(
            id=12345,
            object_name=PaymentObjectType.INVOICE,
            object_id=68827818,
            value=Decimal("100.00"),
            date="2020-02-20",
        )
        xml_bytes = payment.to_xml()
        assert b"<payment" in xml_bytes
        assert b"<id>12345</id>" in xml_bytes
        assert b"<object_name>invoice</object_name>" in xml_bytes
        assert b"<object_id>68827818</object_id>" in xml_bytes
        assert b"<value>100.00</value>" in xml_bytes
        assert b"<date>2020-02-20</date>" in xml_bytes

    def test_payment_xml_deserialization(self) -> None:
        """Test Payment XML deserialization from API response."""
        xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <payment>
            <id>12345</id>
            <object_name>invoice</object_name>
            <object_id>68827818</object_id>
            <value>100.00</value>
            <date>2020-02-20</date>
            <created>2024-01-15 10:30:45</created>
        </payment>
        """
        payment = Payment.from_xml(xml)
        assert payment.id == 12345
        assert payment.object_name == PaymentObjectType.INVOICE
        assert payment.object_id == 68827818
        assert payment.value == Decimal("100.00")
        assert payment.date == "2020-02-20"
        assert payment.created == datetime(2024, 1, 15, 10, 30, 45)

    def test_payment_xml_roundtrip(self) -> None:
        """Test Payment XML serialization and deserialization roundtrip."""
        original = Payment(
            id=12345,
            object_name=PaymentObjectType.INVOICE,
            object_id=68827818,
            value=Decimal("100.00"),
            date="2020-02-20",
        )
        xml_bytes = original.to_xml()
        restored = Payment.from_xml(xml_bytes)

        assert restored.id == original.id
        assert restored.object_name == original.object_name
        assert restored.object_id == original.object_id
        assert restored.value == original.value
        assert restored.date == original.date

    def test_payment_immutable(self) -> None:
        """Test that Payment is immutable (frozen)."""
        payment = Payment(id=1)
        with pytest.raises(ValidationError):
            payment.id = 2

    def test_payment_with_recurring_invoice(self) -> None:
        """Test Payment linked to a recurring invoice."""
        payment = Payment(
            id=1,
            object_name=PaymentObjectType.INVOICE_RECURRING,
            object_id=111111,
            value=Decimal("500.00"),
        )
        assert payment.object_name == PaymentObjectType.INVOICE_RECURRING
        assert payment.object_id == 111111

    def test_payment_with_recurring_expense(self) -> None:
        """Test Payment linked to a recurring expense."""
        payment = Payment(
            id=2,
            object_name=PaymentObjectType.EXPENSE_RECURRING,
            object_id=222222,
            value=Decimal("-300.00"),
        )
        assert payment.object_name == PaymentObjectType.EXPENSE_RECURRING
        assert payment.object_id == 222222

    def test_payment_with_different_types(self) -> None:
        """Test Payment types work correctly."""
        income = Payment(id=1, type=PaymentType.INCOME, value=Decimal("100.00"))
        expense = Payment(id=2, type=PaymentType.EXPENSE, value=Decimal("-50.00"))

        assert income.type == PaymentType.INCOME
        assert expense.type == PaymentType.EXPENSE

    def test_payment_id_required(self) -> None:
        """Test that Payment requires id field."""
        with pytest.raises(ValidationError):
            Payment()


__all__ = [
    "TestPayment",
    "TestPaymentCashbox",
    "TestPaymentObjectType",
    "TestPaymentType",
]

