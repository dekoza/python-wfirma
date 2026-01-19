"""
Tests for contractor Pydantic models.

These tests verify contractor models for wFirma API:
- Contractor - Main contractor model (customer/supplier)
- ContractorDetail - Contractor detail info (embedded in invoices)

Based on wFirma API structure from /contractors/add, /contractors/find, etc.

Contractor fields from API:
- id, name, altname, nip, regon, pesel
- street, building_number, flat_number, zip, post, city, country
- tax_id_type (nip, pesel, custom, none)
- contact_name, contact_street, contact_building_number, contact_flat_number
- contact_zip, contact_post, contact_city, contact_country
- buyer (bool), seller (bool), remind (bool)
- phone, fax, email, url
- notes, tags
- created, modified
"""

from datetime import datetime

import pytest
from pydantic import ValidationError

from wfirma.models.contractor import (
    Contractor,
    ContractorDetail,
)


class TestContractor:
    """Tests for Contractor model."""

    # AICOMPLETE: Contractor validation tests - ready for review

    def test_contractor_minimal(self) -> None:
        """Test Contractor with minimal required fields."""
        contractor = Contractor(
            id=1,
            name="ACME Corp",
        )
        assert contractor.id == 1
        assert contractor.name == "ACME Corp"
        assert contractor.nip is None
        assert contractor.buyer is None

    def test_contractor_full(self) -> None:
        """Test Contractor with all fields."""
        contractor = Contractor(
            id=12345,
            name="Test Company Sp. z o.o.",
            altname="TestCo",
            nip="1234567890",
            regon="123456789",
            pesel=None,
            street="Legnicka",
            building_number="33",
            flat_number="12",
            zip="54-162",
            post="Wrocław",
            city="Wrocław",
            country="PL",
            tax_id_type="nip",
            contact_name="Jan Kowalski",
            contact_street="Inna",
            contact_building_number="1",
            contact_flat_number=None,
            contact_zip="00-001",
            contact_post="Warszawa",
            contact_city="Warszawa",
            contact_country="PL",
            buyer=True,
            seller=False,
            remind=True,
            phone="+48123456789",
            fax="+48123456788",
            email="contact@testco.pl",
            url="https://testco.pl",
            notes="Important customer",
            tags="vip,priority",
            reference_company_id=100,
            translation_language_id=1,
            company_account_id=50,
            good_price_group_id=10,
            invoice_description_id=5,
            shop_buyer_id=None,
            source="manual",
            created="2024-01-15 10:30:45",
            modified="2024-01-16 12:00:00",
        )
        assert contractor.id == 12345
        assert contractor.name == "Test Company Sp. z o.o."
        assert contractor.altname == "TestCo"
        assert contractor.nip == "1234567890"
        assert contractor.regon == "123456789"
        assert contractor.street == "Legnicka"
        assert contractor.building_number == "33"
        assert contractor.flat_number == "12"
        assert contractor.zip == "54-162"
        assert contractor.city == "Wrocław"
        assert contractor.country == "PL"
        assert contractor.tax_id_type == "nip"
        assert contractor.contact_name == "Jan Kowalski"
        assert contractor.buyer is True
        assert contractor.seller is False
        assert contractor.remind is True
        assert contractor.phone == "+48123456789"
        assert contractor.email == "contact@testco.pl"
        assert contractor.url == "https://testco.pl"
        assert contractor.notes == "Important customer"
        assert contractor.created == datetime(2024, 1, 15, 10, 30, 45)
        assert contractor.modified == datetime(2024, 1, 16, 12, 0, 0)

    def test_contractor_datetime_parsing(self) -> None:
        """Test Contractor parses datetime from string."""
        contractor = Contractor(
            id=1,
            name="Test",
            created="2024-01-15 10:30:45",
        )
        assert contractor.created == datetime(2024, 1, 15, 10, 30, 45)

    def test_contractor_null_datetime(self) -> None:
        """Test Contractor handles null datetime format."""
        contractor = Contractor(
            id=1,
            name="Test",
            created="0000-00-00 00:00:00",
        )
        assert contractor.created is None

    def test_contractor_xml_serialization(self) -> None:
        """Test Contractor XML serialization."""
        contractor = Contractor(
            id=123,
            name="XML Test Company",
            nip="9876543210",
            city="Warsaw",
            country="PL",
            tax_id_type="nip",
        )
        xml_bytes = contractor.to_xml()
        assert b"<contractor>" in xml_bytes
        assert b"<id>123</id>" in xml_bytes
        assert b"<name>XML Test Company</name>" in xml_bytes
        assert b"<nip>9876543210</nip>" in xml_bytes
        assert b"<city>Warsaw</city>" in xml_bytes
        assert b"<tax_id_type>nip</tax_id_type>" in xml_bytes

    def test_contractor_xml_deserialization(self) -> None:
        """Test Contractor XML deserialization."""
        xml_data = b"""<contractor>
            <id>456</id>
            <name>Deserialized Company</name>
            <nip>1111111111</nip>
            <street>Main Street</street>
            <building_number>1</building_number>
            <zip>00-001</zip>
            <city>Krakow</city>
            <country>PL</country>
            <tax_id_type>nip</tax_id_type>
            <buyer>1</buyer>
            <seller>0</seller>
        </contractor>"""
        contractor = Contractor.from_xml(xml_data)
        assert contractor.id == 456
        assert contractor.name == "Deserialized Company"
        assert contractor.nip == "1111111111"
        assert contractor.street == "Main Street"
        assert contractor.building_number == "1"
        assert contractor.zip == "00-001"
        assert contractor.city == "Krakow"
        assert contractor.country == "PL"
        assert contractor.tax_id_type == "nip"
        assert contractor.buyer is True
        assert contractor.seller is False

    def test_contractor_immutable(self) -> None:
        """Test Contractor is immutable (frozen)."""
        contractor = Contractor(id=1, name="Test")
        with pytest.raises(ValidationError):
            contractor.name = "Modified"

    def test_contractor_id_required(self) -> None:
        """Test Contractor requires id field."""
        with pytest.raises(ValidationError) as exc_info:
            Contractor(name="Test")
        assert "id" in str(exc_info.value)

    def test_contractor_name_required(self) -> None:
        """Test Contractor requires name field."""
        with pytest.raises(ValidationError) as exc_info:
            Contractor(id=1)
        assert "name" in str(exc_info.value)

    def test_contractor_tax_id_types(self) -> None:
        """Test Contractor handles different tax_id_type values."""
        for tax_type in ["nip", "pesel", "custom", "none"]:
            contractor = Contractor(
                id=1,
                name="Test",
                tax_id_type=tax_type,
            )
            assert contractor.tax_id_type == tax_type

    def test_contractor_boolean_fields(self) -> None:
        """Test Contractor boolean fields accept various formats."""
        # True values
        contractor = Contractor(id=1, name="Test", buyer=True, seller=False)
        assert contractor.buyer is True
        assert contractor.seller is False

        # None values
        contractor2 = Contractor(id=2, name="Test2")
        assert contractor2.buyer is None
        assert contractor2.seller is None

    def test_contractor_contact_address(self) -> None:
        """Test Contractor with contact address different from main address."""
        contractor = Contractor(
            id=1,
            name="Test",
            street="Main Street",
            city="Warsaw",
            zip="00-001",
            contact_name="Contact Person",
            contact_street="Other Street",
            contact_city="Krakow",
            contact_zip="30-001",
        )
        assert contractor.street == "Main Street"
        assert contractor.city == "Warsaw"
        assert contractor.contact_name == "Contact Person"
        assert contractor.contact_street == "Other Street"
        assert contractor.contact_city == "Krakow"

    def test_contractor_foreign(self) -> None:
        """Test Contractor for foreign company."""
        contractor = Contractor(
            id=1,
            name="Foreign Inc.",
            country="US",
            tax_id_type="custom",
            nip="US12345678",
        )
        assert contractor.country == "US"
        assert contractor.tax_id_type == "custom"


class TestContractorDetail:
    """Tests for ContractorDetail model (embedded in invoices)."""

    # AICOMPLETE: ContractorDetail validation tests - ready for review

    def test_contractor_detail_minimal(self) -> None:
        """Test ContractorDetail with minimal required fields."""
        detail = ContractorDetail(
            id=1,
            name="ACME Corp",
        )
        assert detail.id == 1
        assert detail.name == "ACME Corp"
        assert detail.nip is None

    def test_contractor_detail_full(self) -> None:
        """Test ContractorDetail with all fields."""
        detail = ContractorDetail(
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
            country="PL",
            created="2011-12-22 11:23:12",
            modified="2011-12-22 11:23:12",
        )
        assert detail.id == 702218
        assert detail.name == "PPHU Komputery-Kowalski"
        assert detail.altname == "Komputery-Kowalski"
        assert detail.nip == "8982073475"
        assert detail.street == "Legnicka"
        assert detail.building_number == "33"
        assert detail.flat_number == "12"
        assert detail.zip == "54-162"
        assert detail.post == "Wrocław"
        assert detail.city == "Wrocław"
        assert detail.country == "PL"
        assert detail.created == datetime(2011, 12, 22, 11, 23, 12)
        assert detail.modified == datetime(2011, 12, 22, 11, 23, 12)

    def test_contractor_detail_xml_serialization(self) -> None:
        """Test ContractorDetail XML serialization."""
        detail = ContractorDetail(
            id=123,
            name="Test Company",
            nip="1234567890",
            city="Warsaw",
        )
        xml_bytes = detail.to_xml()
        assert b"<contractor_detail>" in xml_bytes
        assert b"<id>123</id>" in xml_bytes
        assert b"<name>Test Company</name>" in xml_bytes
        assert b"<nip>1234567890</nip>" in xml_bytes

    def test_contractor_detail_xml_deserialization(self) -> None:
        """Test ContractorDetail XML deserialization."""
        xml_data = b"""<contractor_detail>
            <id>456</id>
            <name>Deserialized Company</name>
            <nip>9876543210</nip>
            <street>Main Street</street>
            <building_number>1</building_number>
            <zip>00-001</zip>
            <city>Krakow</city>
        </contractor_detail>"""
        detail = ContractorDetail.from_xml(xml_data)
        assert detail.id == 456
        assert detail.name == "Deserialized Company"
        assert detail.nip == "9876543210"
        assert detail.street == "Main Street"
        assert detail.city == "Krakow"

    def test_contractor_detail_immutable(self) -> None:
        """Test ContractorDetail is immutable (frozen)."""
        detail = ContractorDetail(id=1, name="Test")
        with pytest.raises(ValidationError):
            detail.name = "Modified"
