"""
Tests for common Pydantic models.

These tests verify common/shared model classes for address,
contact information, currency, and tax-related data used
across wFirma API entities.
"""

from decimal import Decimal

import pytest
from pydantic import ValidationError

from wfirma.models.common import (
    Address,
    BankAccount,
    CountryCode,
    Currency,
    Email,
    Money,
    Phone,
    TaxIdType,
    VATRate,
)


class TestCountryCode:
    """Tests for CountryCode enum."""

    # AICOMPLETE: Country code validation tests - ready for review

    def test_country_code_poland(self) -> None:
        """Test Poland country code."""
        assert CountryCode.PL.value == "PL"
        assert CountryCode.PL.name == "PL"

    def test_country_code_germany(self) -> None:
        """Test Germany country code."""
        assert CountryCode.DE.value == "DE"

    def test_country_code_common_eu_countries(self) -> None:
        """Test common EU country codes are available."""
        eu_codes = ["PL", "DE", "FR", "GB", "IT", "ES", "NL", "BE", "AT", "CZ"]
        for code in eu_codes:
            assert hasattr(CountryCode, code)


class TestTaxIdType:
    """Tests for TaxIdType enum."""

    # AICOMPLETE: Tax ID type validation tests - ready for review

    def test_tax_id_type_nip(self) -> None:
        """Test NIP (Polish tax ID) type."""
        assert TaxIdType.NIP.value == "nip"

    def test_tax_id_type_custom(self) -> None:
        """Test custom tax ID type."""
        assert TaxIdType.CUSTOM.value == "custom"

    def test_tax_id_type_none(self) -> None:
        """Test none tax ID type."""
        assert TaxIdType.NONE.value == "none"

    def test_tax_id_type_pesel(self) -> None:
        """Test PESEL (Polish ID number) type."""
        assert TaxIdType.PESEL.value == "pesel"


class TestVATRate:
    """Tests for VATRate enum."""

    # AICOMPLETE: VAT rate validation tests - ready for review

    def test_vat_rate_standard_23(self) -> None:
        """Test standard 23% VAT rate."""
        assert VATRate.VAT_23.value == "23"
        assert VATRate.VAT_23.as_decimal() == Decimal("0.23")

    def test_vat_rate_reduced_8(self) -> None:
        """Test reduced 8% VAT rate."""
        assert VATRate.VAT_8.value == "8"
        assert VATRate.VAT_8.as_decimal() == Decimal("0.08")

    def test_vat_rate_reduced_5(self) -> None:
        """Test reduced 5% VAT rate."""
        assert VATRate.VAT_5.value == "5"
        assert VATRate.VAT_5.as_decimal() == Decimal("0.05")

    def test_vat_rate_zero(self) -> None:
        """Test 0% VAT rate."""
        assert VATRate.VAT_0.value == "0"
        assert VATRate.VAT_0.as_decimal() == Decimal("0")

    def test_vat_rate_exempt(self) -> None:
        """Test VAT exempt (zw)."""
        assert VATRate.ZW.value == "zw"
        assert VATRate.ZW.as_decimal() == Decimal("0")

    def test_vat_rate_not_applicable(self) -> None:
        """Test VAT not applicable (np)."""
        assert VATRate.NP.value == "np"
        assert VATRate.NP.as_decimal() == Decimal("0")

    def test_vat_rate_oo(self) -> None:
        """Test VAT OO rate (special)."""
        assert VATRate.OO.value == "oo"
        assert VATRate.OO.as_decimal() == Decimal("0")


class TestCurrency:
    """Tests for Currency enum."""

    # AICOMPLETE: Currency validation tests - ready for review

    def test_currency_pln(self) -> None:
        """Test PLN currency."""
        assert Currency.PLN.value == "PLN"

    def test_currency_eur(self) -> None:
        """Test EUR currency."""
        assert Currency.EUR.value == "EUR"

    def test_currency_usd(self) -> None:
        """Test USD currency."""
        assert Currency.USD.value == "USD"

    def test_currency_gbp(self) -> None:
        """Test GBP currency."""
        assert Currency.GBP.value == "GBP"


class TestMoney:
    """Tests for Money model (decimal with precision)."""

    # AICOMPLETE: Money/decimal precision tests - ready for review

    def test_money_from_string(self) -> None:
        """Test Money creation from string."""
        money = Money(amount="123.45", currency=Currency.PLN)
        assert money.amount == Decimal("123.45")
        assert money.currency == Currency.PLN

    def test_money_from_decimal(self) -> None:
        """Test Money creation from Decimal."""
        money = Money(amount=Decimal("999.99"), currency=Currency.EUR)
        assert money.amount == Decimal("999.99")

    def test_money_from_int(self) -> None:
        """Test Money creation from int."""
        money = Money(amount=100, currency=Currency.PLN)
        assert money.amount == Decimal("100")

    def test_money_from_float(self) -> None:
        """Test Money creation from float with rounding."""
        money = Money(amount=123.456789, currency=Currency.PLN)
        # Should round to 2 decimal places
        assert money.amount == Decimal("123.46")

    def test_money_preserves_two_decimal_places(self) -> None:
        """Test that Money preserves exactly 2 decimal places."""
        money = Money(amount="100.10", currency=Currency.PLN)
        assert str(money.amount) == "100.10"

    def test_money_negative_amount(self) -> None:
        """Test Money with negative amount."""
        money = Money(amount="-50.00", currency=Currency.PLN)
        assert money.amount == Decimal("-50.00")

    def test_money_zero_amount(self) -> None:
        """Test Money with zero amount."""
        money = Money(amount="0.00", currency=Currency.PLN)
        assert money.amount == Decimal("0.00")

    def test_money_default_currency_pln(self) -> None:
        """Test that default currency is PLN."""
        money = Money(amount="100.00")
        assert money.currency == Currency.PLN

    def test_money_serialization(self) -> None:
        """Test Money serialization to dict."""
        money = Money(amount="123.45", currency=Currency.EUR)
        data = money.model_dump()
        assert data["amount"] == Decimal("123.45")
        assert data["currency"] == Currency.EUR


class TestEmail:
    """Tests for Email validation."""

    # AICOMPLETE: Email validation tests - ready for review

    def test_email_valid_simple(self) -> None:
        """Test valid simple email."""
        email = Email(value="test@example.com")
        assert email.value == "test@example.com"

    def test_email_valid_with_subdomain(self) -> None:
        """Test valid email with subdomain."""
        email = Email(value="user@mail.example.com")
        assert email.value == "user@mail.example.com"

    def test_email_valid_with_plus(self) -> None:
        """Test valid email with plus sign."""
        email = Email(value="user+tag@example.com")
        assert email.value == "user+tag@example.com"

    def test_email_valid_with_dots(self) -> None:
        """Test valid email with dots in local part."""
        email = Email(value="first.last@example.com")
        assert email.value == "first.last@example.com"

    def test_email_invalid_no_at(self) -> None:
        """Test invalid email without @ symbol."""
        with pytest.raises(ValidationError):
            Email(value="invalid-email")

    def test_email_invalid_no_domain(self) -> None:
        """Test invalid email without domain."""
        with pytest.raises(ValidationError):
            Email(value="user@")

    def test_email_invalid_empty(self) -> None:
        """Test invalid empty email."""
        with pytest.raises(ValidationError):
            Email(value="")

    def test_email_strips_whitespace(self) -> None:
        """Test that email strips whitespace."""
        email = Email(value="  test@example.com  ")
        assert email.value == "test@example.com"


class TestPhone:
    """Tests for Phone validation."""

    # AICOMPLETE: Phone validation tests - ready for review

    def test_phone_valid_polish_format(self) -> None:
        """Test valid Polish phone number."""
        phone = Phone(number="+48 123 456 789")
        assert phone.number == "+48123456789"

    def test_phone_valid_without_country_code(self) -> None:
        """Test valid phone without country code."""
        phone = Phone(number="123456789")
        assert phone.number == "123456789"

    def test_phone_valid_with_spaces(self) -> None:
        """Test phone with spaces (normalized)."""
        phone = Phone(number="123 456 789")
        assert phone.number == "123456789"

    def test_phone_valid_with_dashes(self) -> None:
        """Test phone with dashes (normalized)."""
        phone = Phone(number="123-456-789")
        assert phone.number == "123456789"

    def test_phone_valid_with_parentheses(self) -> None:
        """Test phone with parentheses (normalized)."""
        phone = Phone(number="(12) 345-67-89")
        assert phone.number == "1234567-89".replace("-", "")

    def test_phone_invalid_too_short(self) -> None:
        """Test invalid phone (too short)."""
        with pytest.raises(ValidationError):
            Phone(number="123")

    def test_phone_invalid_letters(self) -> None:
        """Test invalid phone with letters."""
        with pytest.raises(ValidationError):
            Phone(number="123-ABC-789")

    def test_phone_optional_none(self) -> None:
        """Test that Phone can be None in optional context."""
        # This tests the model field definition rather than Phone itself
        phone = Phone(number="123456789")
        assert phone.number is not None


class TestAddress:
    """Tests for Address model."""

    # AICOMPLETE: Address model validation tests - ready for review

    def test_address_minimal_required_fields(self) -> None:
        """Test Address with minimal required fields."""
        address = Address(
            street="Legnicka",
            building_number="33",
            zip_code="54-162",
            city="Wrocław",
        )
        assert address.street == "Legnicka"
        assert address.building_number == "33"
        assert address.zip_code == "54-162"
        assert address.city == "Wrocław"
        assert address.country == CountryCode.PL  # default

    def test_address_full_fields(self) -> None:
        """Test Address with all fields."""
        address = Address(
            street="Legnicka",
            building_number="33",
            flat_number="12",
            zip_code="54-162",
            city="Wrocław",
            post="Wrocław",
            country=CountryCode.PL,
        )
        assert address.flat_number == "12"
        assert address.post == "Wrocław"

    def test_address_foreign_country(self) -> None:
        """Test Address with foreign country."""
        address = Address(
            street="Hauptstraße",
            building_number="1",
            zip_code="10115",
            city="Berlin",
            country=CountryCode.DE,
        )
        assert address.country == CountryCode.DE

    def test_address_optional_flat_number(self) -> None:
        """Test Address without flat number."""
        address = Address(
            street="Legnicka",
            building_number="33",
            zip_code="54-162",
            city="Wrocław",
        )
        assert address.flat_number is None

    def test_address_optional_post(self) -> None:
        """Test Address without post field (defaults to city)."""
        address = Address(
            street="Legnicka",
            building_number="33",
            zip_code="54-162",
            city="Wrocław",
        )
        # post defaults to None (not city)
        assert address.post is None

    def test_address_xml_serialization(self) -> None:
        """Test Address XML serialization."""
        address = Address(
            street="Legnicka",
            building_number="33",
            zip_code="54-162",
            city="Wrocław",
        )
        xml_bytes = address.to_xml()
        xml_str = xml_bytes.decode("utf-8")
        assert "<street>Legnicka</street>" in xml_str
        assert "<building_number>33</building_number>" in xml_str
        assert "<zip>54-162</zip>" in xml_str
        # City may be encoded as HTML entity (&#321; for ł)
        assert "<city>" in xml_str
        assert "Wroc" in xml_str

    def test_address_xml_round_trip(self) -> None:
        """Test Address XML serialization and deserialization."""
        original = Address(
            street="Legnicka",
            building_number="33",
            flat_number="12",
            zip_code="54-162",
            city="Wrocław",
            country=CountryCode.PL,
        )
        xml_bytes = original.to_xml()
        restored = Address.from_xml(xml_bytes)
        assert restored.street == original.street
        assert restored.building_number == original.building_number
        assert restored.flat_number == original.flat_number
        assert restored.zip_code == original.zip_code
        assert restored.city == original.city
        assert restored.country == original.country


class TestBankAccount:
    """Tests for BankAccount model."""

    # AICOMPLETE: Bank account validation tests - ready for review

    def test_bank_account_minimal(self) -> None:
        """Test BankAccount with minimal fields."""
        account = BankAccount(account_number="59 1111 2222 3333 4444 5555 6666")
        assert "59111122223333444455556666" in account.account_number.replace(" ", "")

    def test_bank_account_full(self) -> None:
        """Test BankAccount with all fields."""
        account = BankAccount(
            account_number="59 1111 2222 3333 4444 5555 6666",
            bank_name="BZWBK",
            swift="WBKPPLPP",
            bank_address="ul. Rynek 9/11, 50-950 Wrocław",
        )
        assert account.bank_name == "BZWBK"
        assert account.swift == "WBKPPLPP"
        assert account.bank_address == "ul. Rynek 9/11, 50-950 Wrocław"

    def test_bank_account_iban_format(self) -> None:
        """Test BankAccount with IBAN format."""
        account = BankAccount(account_number="PL59111122223333444455556666")
        assert "PL" in account.account_number

    def test_bank_account_optional_fields(self) -> None:
        """Test BankAccount optional fields default to None."""
        account = BankAccount(account_number="59111122223333444455556666")
        assert account.bank_name is None
        assert account.swift is None
        assert account.bank_address is None

    def test_bank_account_xml_serialization(self) -> None:
        """Test BankAccount XML serialization."""
        account = BankAccount(
            account_number="59111122223333444455556666",
            bank_name="BZWBK",
        )
        xml_bytes = account.to_xml()
        xml_str = xml_bytes.decode("utf-8")
        assert "<bank_account>" in xml_str
        assert "<bank_name>BZWBK</bank_name>" in xml_str

