"""
Tests for company Pydantic models.

These tests verify company models for wFirma API:
- CompanyDetail - Company information/details (name, NIP, address, bank info)
- CompanyAccount - Company bank account
- CompanyAddress - Company address entry
- UserCompany - User-company relationship

Based on wFirma API structure from /companies/get, /company_accounts/*, etc.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from wfirma.models.company import (
    CompanyAccount,
    CompanyAddress,
    CompanyDetail,
    UserCompany,
)


class TestCompanyDetail:
    """Tests for CompanyDetail model."""

    # AICOMPLETE: Company detail validation tests - ready for review

    def test_company_detail_minimal(self) -> None:
        """Test CompanyDetail with minimal required fields."""
        company = CompanyDetail(
            id=123,
            name="Test Company",
        )
        assert company.id == 123
        assert company.name == "Test Company"
        assert company.altname is None
        assert company.nip is None

    def test_company_detail_full(self) -> None:
        """Test CompanyDetail with all fields."""
        company = CompanyDetail(
            id=702218,
            name="PPHU Komputery-Kowalski",
            altname="Komputery-Kowalski",
            nip="8982073475",
            street="Legnicka",
            building_number="33",
            flat_number="12",
            zip="54-162",
            post="Wrocław",
            city="Wrocław",
            bank_name="BZWBK",
            bank_account="59 1111 2222 3333 4444 5555 6666",
            bank_swift="WBKPPLPP",
            bank_address="ul. Bankowa 1, Wrocław",
            created="2011-12-22 11:23:12",
            modified="2011-12-22 11:23:12",
        )
        assert company.id == 702218
        assert company.name == "PPHU Komputery-Kowalski"
        assert company.altname == "Komputery-Kowalski"
        assert company.nip == "8982073475"
        assert company.street == "Legnicka"
        assert company.building_number == "33"
        assert company.flat_number == "12"
        assert company.zip == "54-162"
        assert company.post == "Wrocław"
        assert company.city == "Wrocław"
        assert company.bank_name == "BZWBK"
        assert company.bank_account == "59 1111 2222 3333 4444 5555 6666"
        assert company.bank_swift == "WBKPPLPP"
        assert company.bank_address == "ul. Bankowa 1, Wrocław"
        assert company.created == datetime(2011, 12, 22, 11, 23, 12)
        assert company.modified == datetime(2011, 12, 22, 11, 23, 12)

    def test_company_detail_datetime_parsing(self) -> None:
        """Test CompanyDetail parses datetime from string."""
        company = CompanyDetail(
            id=1,
            name="Test",
            created="2024-01-15 10:30:45",
        )
        assert company.created == datetime(2024, 1, 15, 10, 30, 45)

    def test_company_detail_null_datetime(self) -> None:
        """Test CompanyDetail handles null datetime format."""
        company = CompanyDetail(
            id=1,
            name="Test",
            created="0000-00-00 00:00:00",
        )
        assert company.created is None

    def test_company_detail_xml_serialization(self) -> None:
        """Test CompanyDetail XML serialization."""
        company = CompanyDetail(
            id=123,
            name="Test Company",
            nip="1234567890",
            city="Warsaw",
        )
        xml_bytes = company.to_xml()
        assert b"<company_detail>" in xml_bytes
        assert b"<id>123</id>" in xml_bytes
        assert b"<name>Test Company</name>" in xml_bytes
        assert b"<nip>1234567890</nip>" in xml_bytes
        assert b"<city>Warsaw</city>" in xml_bytes

    def test_company_detail_xml_deserialization(self) -> None:
        """Test CompanyDetail XML deserialization."""
        xml_data = b"""<company_detail>
            <id>456</id>
            <name>Deserialized Company</name>
            <nip>9876543210</nip>
            <street>Main Street</street>
            <building_number>1</building_number>
            <zip>00-001</zip>
            <city>Krakow</city>
        </company_detail>"""
        company = CompanyDetail.from_xml(xml_data)
        assert company.id == 456
        assert company.name == "Deserialized Company"
        assert company.nip == "9876543210"
        assert company.street == "Main Street"
        assert company.building_number == "1"
        assert company.zip == "00-001"
        assert company.city == "Krakow"

    def test_company_detail_immutable(self) -> None:
        """Test CompanyDetail is immutable (frozen)."""
        company = CompanyDetail(id=1, name="Test")
        with pytest.raises(ValidationError):
            company.name = "Modified"

    def test_company_detail_id_required(self) -> None:
        """Test CompanyDetail requires id field."""
        with pytest.raises(ValidationError) as exc_info:
            CompanyDetail(name="Test")
        assert "id" in str(exc_info.value)

    def test_company_detail_name_required(self) -> None:
        """Test CompanyDetail requires name field."""
        with pytest.raises(ValidationError) as exc_info:
            CompanyDetail(id=1)
        assert "name" in str(exc_info.value)


class TestCompanyAccount:
    """Tests for CompanyAccount model."""

    # AICOMPLETE: Company account validation tests - ready for review

    def test_company_account_minimal(self) -> None:
        """Test CompanyAccount with minimal required fields."""
        account = CompanyAccount(
            id=1,
            account_number="59 1111 2222 3333 4444 5555 6666",
        )
        assert account.id == 1
        assert account.account_number == "59 1111 2222 3333 4444 5555 6666"

    def test_company_account_full(self) -> None:
        """Test CompanyAccount with all fields."""
        account = CompanyAccount(
            id=100,
            account_number="PL59111122223333444455556666",
            bank_name="PKO BP",
            swift="BPKOPLPW",
            is_default=True,
            created="2024-01-15 10:30:45",
            modified="2024-01-16 12:00:00",
        )
        assert account.id == 100
        assert account.account_number == "PL59111122223333444455556666"
        assert account.bank_name == "PKO BP"
        assert account.swift == "BPKOPLPW"
        assert account.is_default is True
        assert account.created == datetime(2024, 1, 15, 10, 30, 45)
        assert account.modified == datetime(2024, 1, 16, 12, 0, 0)

    def test_company_account_xml_serialization(self) -> None:
        """Test CompanyAccount XML serialization."""
        account = CompanyAccount(
            id=50,
            account_number="1234567890",
            bank_name="Test Bank",
        )
        xml_bytes = account.to_xml()
        assert b"<company_account>" in xml_bytes
        assert b"<id>50</id>" in xml_bytes
        assert b"<bank_name>Test Bank</bank_name>" in xml_bytes

    def test_company_account_xml_deserialization(self) -> None:
        """Test CompanyAccount XML deserialization."""
        xml_data = b"""<company_account>
            <id>75</id>
            <account_number>PL12345678901234567890123456</account_number>
            <bank_name>mBank</bank_name>
            <swift>BREXPLPW</swift>
        </company_account>"""
        account = CompanyAccount.from_xml(xml_data)
        assert account.id == 75
        assert account.account_number == "PL12345678901234567890123456"
        assert account.bank_name == "mBank"
        assert account.swift == "BREXPLPW"

    def test_company_account_immutable(self) -> None:
        """Test CompanyAccount is immutable (frozen)."""
        account = CompanyAccount(id=1, account_number="123")
        with pytest.raises(ValidationError):
            account.bank_name = "New Bank"


class TestCompanyAddress:
    """Tests for CompanyAddress model."""

    # AICOMPLETE: Company address validation tests - ready for review

    def test_company_address_minimal(self) -> None:
        """Test CompanyAddress with minimal required fields."""
        address = CompanyAddress(
            id=1,
            street="Test Street",
            building_number="1",
            zip="00-001",
            city="Warsaw",
        )
        assert address.id == 1
        assert address.street == "Test Street"
        assert address.building_number == "1"
        assert address.zip == "00-001"
        assert address.city == "Warsaw"

    def test_company_address_full(self) -> None:
        """Test CompanyAddress with all fields."""
        address = CompanyAddress(
            id=200,
            street="Długa",
            building_number="15",
            flat_number="3A",
            zip="31-147",
            post="Kraków",
            city="Kraków",
            country="PL",
            is_main=True,
            created="2024-02-01 08:00:00",
            modified="2024-02-02 09:30:00",
        )
        assert address.id == 200
        assert address.street == "Długa"
        assert address.building_number == "15"
        assert address.flat_number == "3A"
        assert address.zip == "31-147"
        assert address.post == "Kraków"
        assert address.city == "Kraków"
        assert address.country == "PL"
        assert address.is_main is True

    def test_company_address_xml_serialization(self) -> None:
        """Test CompanyAddress XML serialization."""
        address = CompanyAddress(
            id=10,
            street="Test",
            building_number="5",
            zip="12-345",
            city="Gdańsk",
        )
        xml_bytes = address.to_xml()
        assert b"<company_address>" in xml_bytes
        assert b"<id>10</id>" in xml_bytes
        assert b"<street>Test</street>" in xml_bytes

    def test_company_address_xml_deserialization(self) -> None:
        """Test CompanyAddress XML deserialization."""
        xml_data = b"""<company_address>
            <id>25</id>
            <street>Nowa</street>
            <building_number>99</building_number>
            <zip>80-001</zip>
            <city>Gdynia</city>
            <country>PL</country>
        </company_address>"""
        address = CompanyAddress.from_xml(xml_data)
        assert address.id == 25
        assert address.street == "Nowa"
        assert address.building_number == "99"
        assert address.zip == "80-001"
        assert address.city == "Gdynia"
        assert address.country == "PL"

    def test_company_address_immutable(self) -> None:
        """Test CompanyAddress is immutable (frozen)."""
        address = CompanyAddress(
            id=1, street="Test", building_number="1", zip="00-001", city="Test"
        )
        with pytest.raises(ValidationError):
            address.city = "Modified"


class TestUserCompany:
    """Tests for UserCompany model (user-company relationship)."""

    # AICOMPLETE: User-company relationship tests - ready for review

    def test_user_company_minimal(self) -> None:
        """Test UserCompany with minimal required fields."""
        user_company = UserCompany(
            id=1,
            company_id=100,
        )
        assert user_company.id == 1
        assert user_company.company_id == 100

    def test_user_company_full(self) -> None:
        """Test UserCompany with all fields."""
        user_company = UserCompany(
            id=50,
            company_id=200,
            company_name="Test Company Sp. z o.o.",
            role="admin",
            is_active=True,
            created="2024-03-01 14:00:00",
        )
        assert user_company.id == 50
        assert user_company.company_id == 200
        assert user_company.company_name == "Test Company Sp. z o.o."
        assert user_company.role == "admin"
        assert user_company.is_active is True
        assert user_company.created == datetime(2024, 3, 1, 14, 0, 0)

    def test_user_company_xml_serialization(self) -> None:
        """Test UserCompany XML serialization."""
        user_company = UserCompany(
            id=5,
            company_id=10,
            company_name="Test",
        )
        xml_bytes = user_company.to_xml()
        assert b"<user_company>" in xml_bytes
        assert b"<id>5</id>" in xml_bytes
        assert b"<company_id>10</company_id>" in xml_bytes

    def test_user_company_xml_deserialization(self) -> None:
        """Test UserCompany XML deserialization."""
        xml_data = b"""<user_company>
            <id>15</id>
            <company_id>300</company_id>
            <company_name>Deserialized Corp</company_name>
            <role>user</role>
        </user_company>"""
        user_company = UserCompany.from_xml(xml_data)
        assert user_company.id == 15
        assert user_company.company_id == 300
        assert user_company.company_name == "Deserialized Corp"
        assert user_company.role == "user"

    def test_user_company_immutable(self) -> None:
        """Test UserCompany is immutable (frozen)."""
        user_company = UserCompany(id=1, company_id=1)
        with pytest.raises(ValidationError):
            user_company.company_id = 999
