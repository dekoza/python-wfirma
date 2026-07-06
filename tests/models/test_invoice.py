"""
Tests for invoice Pydantic models.

These tests verify invoice models for wFirma API:
- Invoice - Main invoice model
- InvoiceContent - Invoice line item model
- InvoiceType - Enum for invoice types (normal, proforma, correction, etc.)
- PaymentMethod - Enum for payment methods

Based on wFirma API structure from /invoices/add, /invoices/find, /invoices/get, etc.

Invoice fields from API documentation:
- id, fullnumber, number, date, paymentdate
- paymentmethod (cash, transfer, etc.)
- type (normal, proforma, correction, etc.)
- netto, brutto, paid, remaining
- currency, currency_exchange, currency_date
- description, notes, tags
- contractor (embedded or reference)
- invoicecontents (line items)
- company_detail (seller info)
- created, modified
"""

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from wfirma.models.invoice import (
    DisposalDateFormat,
    Invoice,
    InvoiceContent,
    InvoiceType,
    PaymentMethod,
    PaymentState,
    PriceType,
)


class TestInvoiceType:
    """Tests for InvoiceType enum."""

    # AICOMPLETE: InvoiceType enum tests - ready for review

    def test_invoice_type_values(self) -> None:
        """Test InvoiceType enum has expected values."""
        assert InvoiceType.NORMAL.value == "normal"
        assert InvoiceType.PROFORMA.value == "proforma"
        assert InvoiceType.CORRECTION.value == "correction"
        assert InvoiceType.RECEIPT.value == "receipt"
        assert InvoiceType.FINAL.value == "final"

    def test_invoice_type_from_string(self) -> None:
        """Test creating InvoiceType from string value."""
        assert InvoiceType("normal") == InvoiceType.NORMAL
        assert InvoiceType("proforma") == InvoiceType.PROFORMA
        assert InvoiceType("correction") == InvoiceType.CORRECTION

    def test_invoice_type_invalid(self) -> None:
        """Test InvoiceType raises error for invalid value."""
        with pytest.raises(ValueError):
            InvoiceType("invalid")


class TestPaymentMethod:
    """Tests for PaymentMethod enum."""

    # AICOMPLETE: PaymentMethod enum tests - ready for review

    def test_payment_method_values(self) -> None:
        """Test PaymentMethod enum has expected values."""
        assert PaymentMethod.CASH.value == "cash"
        assert PaymentMethod.TRANSFER.value == "transfer"
        assert PaymentMethod.CARD.value == "card"
        assert PaymentMethod.COMPENSATION.value == "compensation"

    def test_payment_method_from_string(self) -> None:
        """Test creating PaymentMethod from string value."""
        assert PaymentMethod("cash") == PaymentMethod.CASH
        assert PaymentMethod("transfer") == PaymentMethod.TRANSFER
        assert PaymentMethod("card") == PaymentMethod.CARD

    def test_payment_method_invalid(self) -> None:
        """Test PaymentMethod raises error for invalid value."""
        with pytest.raises(ValueError):
            PaymentMethod("invalid")


class TestPaymentState:
    """Tests for PaymentState enum."""

    # AICOMPLETE: PaymentState enum tests - ready for review

    def test_payment_state_values(self) -> None:
        """Test PaymentState enum has expected values."""
        assert PaymentState.PAID.value == "paid"
        assert PaymentState.UNPAID.value == "unpaid"
        assert PaymentState.PARTIAL.value == "partial"

    def test_payment_state_from_string(self) -> None:
        """Test creating PaymentState from string value."""
        assert PaymentState("paid") == PaymentState.PAID
        assert PaymentState("unpaid") == PaymentState.UNPAID
        assert PaymentState("partial") == PaymentState.PARTIAL

    def test_payment_state_invalid(self) -> None:
        """Test PaymentState raises error for invalid value."""
        with pytest.raises(ValueError):
            PaymentState("invalid")


class TestDisposalDateFormat:
    """Tests for DisposalDateFormat enum."""

    # AICOMPLETE: DisposalDateFormat enum tests - ready for review

    def test_disposal_date_format_values(self) -> None:
        """Test DisposalDateFormat enum has expected values."""
        assert DisposalDateFormat.DATE.value == "date"
        assert DisposalDateFormat.MONTH.value == "month"

    def test_disposal_date_format_from_string(self) -> None:
        """Test creating DisposalDateFormat from string value."""
        assert DisposalDateFormat("date") == DisposalDateFormat.DATE
        assert DisposalDateFormat("month") == DisposalDateFormat.MONTH

    def test_disposal_date_format_invalid(self) -> None:
        """Test DisposalDateFormat raises error for invalid value."""
        with pytest.raises(ValueError):
            DisposalDateFormat("invalid")


class TestInvoiceContent:
    """Tests for InvoiceContent model."""

    # AICOMPLETE: InvoiceContent validation tests - ready for review

    def test_invoice_content_minimal(self) -> None:
        """Test InvoiceContent with minimal required fields."""
        content = InvoiceContent(
            id=1,
            name="Test Product",
        )
        assert content.id == 1
        assert content.name == "Test Product"
        assert content.unit is None
        assert content.count is None
        assert content.price is None

    def test_invoice_content_full(self) -> None:
        """Test InvoiceContent with all fields."""
        content = InvoiceContent(
            id=3187305,
            name="makulatura 2011",
            classification="PKWiU 38.11.19.0",
            unit="kg",
            count=Decimal("4850.0000"),
            price=Decimal("0.20"),
            price_modified=False,
            discount=True,
            discount_percent=Decimal("0.00"),
            netto=Decimal("970.00"),
            brutto=Decimal("1193.10"),
            vat="23",
            lumpcode="20",
            good_id=123,
            invoice_id=1207242,
            created="2011-12-22 11:23:12",
            modified="2011-12-22 11:23:12",
        )
        assert content.id == 3187305
        assert content.name == "makulatura 2011"
        assert content.classification == "PKWiU 38.11.19.0"
        assert content.unit == "kg"
        assert content.count == Decimal("4850.0000")
        assert content.price == Decimal("0.20")
        assert content.price_modified is False
        assert content.discount is True
        assert content.discount_percent == Decimal("0.00")
        assert content.netto == Decimal("970.00")
        assert content.brutto == Decimal("1193.10")
        assert content.vat == "23"
        assert content.lumpcode == "20"
        assert content.good_id == 123
        assert content.invoice_id == 1207242
        assert content.created == datetime(2011, 12, 22, 11, 23, 12)
        assert content.modified == datetime(2011, 12, 22, 11, 23, 12)

    def test_invoice_content_calculation_example(self) -> None:
        """Test InvoiceContent represents a typical calculation."""
        # 1 unit at 100 PLN with 23% VAT
        content = InvoiceContent(
            id=1,
            name="Test Product",
            unit="szt.",
            count=Decimal("1.0000"),
            price=Decimal("100.00"),
            netto=Decimal("100.00"),
            brutto=Decimal("123.00"),
            vat="23",
        )
        assert content.count == Decimal("1.0000")
        assert content.price == Decimal("100.00")
        assert content.netto == Decimal("100.00")
        assert content.brutto == Decimal("123.00")
        assert content.vat == "23"

    def test_invoice_content_datetime_parsing(self) -> None:
        """Test InvoiceContent parses datetime from string."""
        content = InvoiceContent(
            id=1,
            name="Test",
            created="2024-01-15 10:30:45",
        )
        assert content.created == datetime(2024, 1, 15, 10, 30, 45)

    def test_invoice_content_null_datetime(self) -> None:
        """Test InvoiceContent handles null datetime format."""
        content = InvoiceContent(
            id=1,
            name="Test",
            created="0000-00-00 00:00:00",
        )
        assert content.created is None

    def test_invoice_content_immutable(self) -> None:
        """Test InvoiceContent is immutable (frozen)."""
        content = InvoiceContent(id=1, name="Test")
        with pytest.raises(ValidationError):
            content.name = "Changed"  # type: ignore[misc]

    def test_invoice_content_xml_serialization(self) -> None:
        """Test InvoiceContent XML serialization."""
        content = InvoiceContent(
            id=1,
            name="Test Product",
            unit="szt.",
            count=Decimal("1.0000"),
            price=Decimal("100.00"),
            vat="23",
        )
        xml_bytes = content.to_xml()
        assert b"<invoicecontent>" in xml_bytes
        assert b"<name>Test Product</name>" in xml_bytes
        assert b"<vat>23</vat>" in xml_bytes

    def test_invoice_content_xml_deserialization(self) -> None:
        """Test InvoiceContent XML deserialization."""
        xml_data = b"""
        <invoicecontent>
            <id>1</id>
            <name>Test Product</name>
            <unit>szt.</unit>
            <count>1.0000</count>
            <price>100.00</price>
            <vat>23</vat>
        </invoicecontent>
        """
        content = InvoiceContent.from_xml(xml_data)
        assert content.id == 1
        assert content.name == "Test Product"
        assert content.unit == "szt."
        assert content.count == Decimal("1.0000")
        assert content.price == Decimal("100.00")
        assert content.vat == "23"

    def test_invoice_content_with_discount(self) -> None:
        """Test InvoiceContent with discount applied."""
        content = InvoiceContent(
            id=1,
            name="Discounted Product",
            unit="szt.",
            count=Decimal("2.0000"),
            price=Decimal("100.00"),
            discount=True,
            discount_percent=Decimal("10.00"),
            netto=Decimal("180.00"),  # 200 - 10%
            brutto=Decimal("221.40"),  # 180 * 1.23
            vat="23",
        )
        assert content.discount is True
        assert content.discount_percent == Decimal("10.00")


class TestInvoice:
    """Tests for Invoice model."""

    # AICOMPLETE: Invoice validation tests - ready for review

    def test_invoice_minimal(self) -> None:
        """Test Invoice with minimal required fields."""
        invoice = Invoice(
            id=1207242,
        )
        assert invoice.id == 1207242
        assert invoice.type is None
        assert invoice.date is None

    def test_invoice_with_basic_fields(self) -> None:
        """Test Invoice with basic fields."""
        invoice = Invoice(
            id=1207242,
            fullnumber="FV 1/2024",
            number=1,
            date="2024-01-15",
            type=InvoiceType.NORMAL,
            paymentmethod=PaymentMethod.TRANSFER,
            paymentdate="2024-01-29",
        )
        assert invoice.id == 1207242
        assert invoice.fullnumber == "FV 1/2024"
        assert invoice.number == 1
        assert invoice.date == "2024-01-15"
        assert invoice.type == InvoiceType.NORMAL
        assert invoice.paymentmethod == PaymentMethod.TRANSFER
        assert invoice.paymentdate == "2024-01-29"

    def test_invoice_full(self) -> None:
        """Test Invoice with comprehensive fields."""
        invoice = Invoice(
            id=1207242,
            fullnumber="FV 1/2024",
            number=1,
            date="2024-01-15",
            disposaldate="2024-01-15",
            disposaldate_format=DisposalDateFormat.DATE,
            paymentmethod=PaymentMethod.TRANSFER,
            paymentdate="2024-01-29",
            paymentstate=PaymentState.UNPAID,
            type=InvoiceType.NORMAL,
            netto=Decimal("970.00"),
            brutto=Decimal("1193.10"),
            paid=Decimal("0.00"),
            remaining=Decimal("1193.10"),
            currency="PLN",
            currency_exchange=Decimal("1.0000"),
            currency_date="2024-01-15",
            description="Test invoice",
            notes="Internal notes",
            tags="test,invoice",
            contractor_id=702218,
            series_id=1,
            created="2024-01-15 10:30:45",
            modified="2024-01-15 10:35:00",
        )
        assert invoice.id == 1207242
        assert invoice.fullnumber == "FV 1/2024"
        assert invoice.number == 1
        assert invoice.date == "2024-01-15"
        assert invoice.disposaldate == "2024-01-15"
        assert invoice.disposaldate_format == DisposalDateFormat.DATE
        assert invoice.paymentmethod == PaymentMethod.TRANSFER
        assert invoice.paymentdate == "2024-01-29"
        assert invoice.paymentstate == PaymentState.UNPAID
        assert invoice.type == InvoiceType.NORMAL
        assert invoice.netto == Decimal("970.00")
        assert invoice.brutto == Decimal("1193.10")
        assert invoice.paid == Decimal("0.00")
        assert invoice.remaining == Decimal("1193.10")
        assert invoice.currency == "PLN"
        assert invoice.currency_exchange == Decimal("1.0000")
        assert invoice.currency_date == "2024-01-15"
        assert invoice.description == "Test invoice"
        assert invoice.notes == "Internal notes"
        assert invoice.tags == "test,invoice"
        assert invoice.contractor_id == 702218
        assert invoice.series_id == 1
        assert invoice.created == datetime(2024, 1, 15, 10, 30, 45)
        assert invoice.modified == datetime(2024, 1, 15, 10, 35, 0)

    def test_invoice_proforma_type(self) -> None:
        """Test Invoice with proforma type."""
        invoice = Invoice(
            id=1,
            type=InvoiceType.PROFORMA,
            fullnumber="FP 1/2024",
        )
        assert invoice.type == InvoiceType.PROFORMA
        assert invoice.fullnumber == "FP 1/2024"

    def test_invoice_correction_type(self) -> None:
        """Test Invoice with correction type."""
        invoice = Invoice(
            id=1,
            type=InvoiceType.CORRECTION,
            fullnumber="FKS 1/2024",
        )
        assert invoice.type == InvoiceType.CORRECTION

    def test_invoice_datetime_parsing(self) -> None:
        """Test Invoice parses datetime from string."""
        invoice = Invoice(
            id=1,
            created="2024-01-15 10:30:45",
        )
        assert invoice.created == datetime(2024, 1, 15, 10, 30, 45)

    def test_invoice_null_datetime(self) -> None:
        """Test Invoice handles null datetime format."""
        invoice = Invoice(
            id=1,
            created="0000-00-00 00:00:00",
        )
        assert invoice.created is None

    def test_invoice_immutable(self) -> None:
        """Test Invoice is immutable (frozen)."""
        invoice = Invoice(id=1)
        with pytest.raises(ValidationError):
            invoice.id = 2  # type: ignore[misc]

    def test_invoice_xml_serialization(self) -> None:
        """Test Invoice XML serialization."""
        invoice = Invoice(
            id=1207242,
            fullnumber="FV 1/2024",
            type=InvoiceType.NORMAL,
            paymentmethod=PaymentMethod.TRANSFER,
        )
        xml_bytes = invoice.to_xml()
        assert b"<invoice>" in xml_bytes
        assert b"<id>1207242</id>" in xml_bytes
        assert b"<fullnumber>FV 1/2024</fullnumber>" in xml_bytes
        assert b"<type>normal</type>" in xml_bytes
        assert b"<paymentmethod>transfer</paymentmethod>" in xml_bytes

    def test_invoice_xml_deserialization(self) -> None:
        """Test Invoice XML deserialization."""
        xml_data = b"""
        <invoice>
            <id>1207242</id>
            <fullnumber>FV 1/2024</fullnumber>
            <date>2024-01-15</date>
            <type>normal</type>
            <paymentmethod>transfer</paymentmethod>
            <netto>970.00</netto>
            <brutto>1193.10</brutto>
        </invoice>
        """
        invoice = Invoice.from_xml(xml_data)
        assert invoice.id == 1207242
        assert invoice.fullnumber == "FV 1/2024"
        assert invoice.date == "2024-01-15"
        assert invoice.type == InvoiceType.NORMAL
        assert invoice.paymentmethod == PaymentMethod.TRANSFER
        assert invoice.netto == Decimal("970.00")
        assert invoice.brutto == Decimal("1193.10")

    def test_invoice_foreign_currency(self) -> None:
        """Test Invoice with foreign currency."""
        invoice = Invoice(
            id=1,
            fullnumber="FV 1/2024",
            currency="EUR",
            currency_exchange=Decimal("4.5123"),
            currency_date="2024-01-15",
            currency_label=False,
            netto=Decimal("215.26"),
            brutto=Decimal("264.77"),
        )
        assert invoice.currency == "EUR"
        assert invoice.currency_exchange == Decimal("4.5123")
        assert invoice.currency_date == "2024-01-15"
        assert invoice.currency_label is False

    def test_invoice_with_type_of_sale(self) -> None:
        """Test Invoice with type_of_sale field for JPK."""
        invoice = Invoice(
            id=1,
            type=InvoiceType.NORMAL,
            type_of_sale="WSTO_EE",
        )
        assert invoice.type_of_sale == "WSTO_EE"

    def test_invoice_paid_status(self) -> None:
        """Test Invoice with payment tracking fields."""
        invoice = Invoice(
            id=1,
            brutto=Decimal("1000.00"),
            paid=Decimal("500.00"),
            remaining=Decimal("500.00"),
            paymentstate=PaymentState.PARTIAL,
        )
        assert invoice.brutto == Decimal("1000.00")
        assert invoice.paid == Decimal("500.00")
        assert invoice.remaining == Decimal("500.00")
        assert invoice.paymentstate == PaymentState.PARTIAL

    def test_invoice_fully_paid(self) -> None:
        """Test Invoice that is fully paid."""
        invoice = Invoice(
            id=1,
            brutto=Decimal("1000.00"),
            paid=Decimal("1000.00"),
            remaining=Decimal("0.00"),
            paymentstate=PaymentState.PAID,
        )
        assert invoice.paid == Decimal("1000.00")
        assert invoice.remaining == Decimal("0.00")
        assert invoice.paymentstate == PaymentState.PAID

    def test_invoice_with_totals(self) -> None:
        """Test Invoice with total fields (calculated by API)."""
        invoice = Invoice(
            id=1,
            netto=Decimal("1000.00"),
            brutto=Decimal("1230.00"),
            tax=Decimal("230.00"),
        )
        assert invoice.netto == Decimal("1000.00")
        assert invoice.brutto == Decimal("1230.00")
        assert invoice.tax == Decimal("230.00")

    def test_invoice_disposaldate_month_format(self) -> None:
        """Test Invoice with disposal date in month format."""
        invoice = Invoice(
            id=1,
            disposaldate="2024-01",
            disposaldate_format=DisposalDateFormat.MONTH,
        )
        assert invoice.disposaldate == "2024-01"
        assert invoice.disposaldate_format == DisposalDateFormat.MONTH

    def test_invoice_with_related_ids(self) -> None:
        """Test Invoice with foreign key IDs."""
        invoice = Invoice(
            id=1,
            contractor_id=702218,
            series_id=1,
            company_detail_id=123,
            user_company_id=456,
        )
        assert invoice.contractor_id == 702218
        assert invoice.series_id == 1
        assert invoice.company_detail_id == 123
        assert invoice.user_company_id == 456


class TestInvoicePriceTypeAndKsef:
    """price_type and KSeF read-only fields, per doc.wfirma.pl (invoices module)."""

    def test_invoice_price_type_values(self) -> None:
        assert PriceType.NETTO == "netto"
        assert PriceType.BRUTTO == "brutto"

    def test_invoice_with_price_type_and_ksef_fields(self) -> None:
        invoice = Invoice(
            id=1,
            price_type=PriceType.BRUTTO,
            ksef_reference_number="5252248481-20260707-ABCDEF012345-01",
            ksef_status="sent",
            ksef_registration_date="2026-07-07 10:15:00",
        )
        assert invoice.price_type == PriceType.BRUTTO
        assert invoice.ksef_reference_number == "5252248481-20260707-ABCDEF012345-01"
        assert invoice.ksef_status == "sent"
        assert invoice.ksef_registration_date == "2026-07-07 10:15:00"

    def test_invoice_from_xml_parses_price_type_and_ksef(self) -> None:
        xml_data = (
            "<invoice>"
            "<id>1207242</id>"
            "<price_type>brutto</price_type>"
            "<ksef_reference_number>5252248481-20260707-ABCDEF012345-01</ksef_reference_number>"
            "<ksef_status>sent</ksef_status>"
            "<ksef_registration_date>2026-07-07 10:15:00</ksef_registration_date>"
            "</invoice>"
        )
        invoice = Invoice.from_xml(xml_data)
        assert invoice.price_type == PriceType.BRUTTO
        assert invoice.ksef_reference_number == "5252248481-20260707-ABCDEF012345-01"
        assert invoice.ksef_status == "sent"
        assert invoice.ksef_registration_date == "2026-07-07 10:15:00"

    def test_invoice_ksef_fields_default_to_none(self) -> None:
        invoice = Invoice(id=1)
        assert invoice.price_type is None
        assert invoice.ksef_reference_number is None
        assert invoice.ksef_status is None
        assert invoice.ksef_registration_date is None
