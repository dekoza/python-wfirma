"""
Tests for goods Pydantic models.

These tests verify goods models for wFirma API:
- Good - Main product/service model
- GoodType - Enum for good types (good, service)
- WarehouseType - Enum for warehouse types

Based on wFirma API structure from /goods/add, /goods/find, /goods/get, etc.

Good fields from API:
- id, name, unit, netto, type, warehouse_type, count
- vat (VAT rate), vat_code_id, lumpcode, classification
- description, code (SKU/product code)
- created, modified
"""

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from wfirma.models.good import (
    Good,
    GoodType,
    WarehouseType,
)


class TestGoodType:
    """Tests for GoodType enum."""

    # AICOMPLETE: GoodType enum tests - ready for review

    def test_good_type_values(self) -> None:
        """Test GoodType enum has expected values."""
        assert GoodType.GOOD.value == "good"
        assert GoodType.SERVICE.value == "service"

    def test_good_type_from_string(self) -> None:
        """Test creating GoodType from string value."""
        assert GoodType("good") == GoodType.GOOD
        assert GoodType("service") == GoodType.SERVICE

    def test_good_type_invalid(self) -> None:
        """Test GoodType raises error for invalid value."""
        with pytest.raises(ValueError):
            GoodType("invalid")


class TestWarehouseType:
    """Tests for WarehouseType enum."""

    # AICOMPLETE: WarehouseType enum tests - ready for review

    def test_warehouse_type_values(self) -> None:
        """Test WarehouseType enum has expected values."""
        assert WarehouseType.SIMPLE.value == "simple"
        assert WarehouseType.DETAILED.value == "detailed"

    def test_warehouse_type_from_string(self) -> None:
        """Test creating WarehouseType from string value."""
        assert WarehouseType("simple") == WarehouseType.SIMPLE
        assert WarehouseType("detailed") == WarehouseType.DETAILED

    def test_warehouse_type_invalid(self) -> None:
        """Test WarehouseType raises error for invalid value."""
        with pytest.raises(ValueError):
            WarehouseType("invalid")


class TestGood:
    """Tests for Good model."""

    # AICOMPLETE: Good validation tests - ready for review

    def test_good_minimal(self) -> None:
        """Test Good with minimal required fields."""
        good = Good(
            id=1,
            name="Test Product",
        )
        assert good.id == 1
        assert good.name == "Test Product"
        assert good.unit is None
        assert good.netto is None

    def test_good_full(self) -> None:
        """Test Good with all fields."""
        good = Good(
            id=12345,
            name="Premium Widget",
            unit="szt.",
            netto=Decimal("99.99"),
            type=GoodType.GOOD,
            warehouse_type=WarehouseType.SIMPLE,
            count=Decimal("100.0000"),
            vat="23",
            vat_code_id=222,
            lumpcode="20",
            classification="PKWiU 26.51.12.0",
            description="A premium quality widget",
            code="WID-001",
            tags="electronics,premium",
            created="2024-01-15 10:30:45",
            modified="2024-01-16 12:00:00",
        )
        assert good.id == 12345
        assert good.name == "Premium Widget"
        assert good.unit == "szt."
        assert good.netto == Decimal("99.99")
        assert good.type == GoodType.GOOD
        assert good.warehouse_type == WarehouseType.SIMPLE
        assert good.count == Decimal("100.0000")
        assert good.vat == "23"
        assert good.vat_code_id == 222
        assert good.lumpcode == "20"
        assert good.classification == "PKWiU 26.51.12.0"
        assert good.description == "A premium quality widget"
        assert good.code == "WID-001"
        assert good.tags == "electronics,premium"
        assert good.created == datetime(2024, 1, 15, 10, 30, 45)
        assert good.modified == datetime(2024, 1, 16, 12, 0, 0)

    def test_good_service_type(self) -> None:
        """Test Good with service type."""
        good = Good(
            id=1,
            name="Consulting Service",
            type=GoodType.SERVICE,
            unit="h",
            netto=Decimal("200.00"),
        )
        assert good.type == GoodType.SERVICE
        assert good.unit == "h"
        assert good.netto == Decimal("200.00")

    def test_good_datetime_parsing(self) -> None:
        """Test Good parses datetime from string."""
        good = Good(
            id=1,
            name="Test",
            created="2024-01-15 10:30:45",
        )
        assert good.created == datetime(2024, 1, 15, 10, 30, 45)

    def test_good_null_datetime(self) -> None:
        """Test Good handles null datetime format."""
        good = Good(
            id=1,
            name="Test",
            created="0000-00-00 00:00:00",
        )
        assert good.created is None

    def test_good_decimal_netto(self) -> None:
        """Test Good accepts various netto formats."""
        # String input
        good1 = Good(id=1, name="Test", netto="10.50")
        assert good1.netto == Decimal("10.50")

        # Float input (converted to Decimal)
        good2 = Good(id=2, name="Test", netto=15.99)
        assert good2.netto == Decimal("15.99")

        # Decimal input
        good3 = Good(id=3, name="Test", netto=Decimal("20.00"))
        assert good3.netto == Decimal("20.00")

    def test_good_decimal_count(self) -> None:
        """Test Good accepts various count formats."""
        good = Good(id=1, name="Test", count="50.5000")
        assert good.count == Decimal("50.5000")

    def test_good_xml_serialization(self) -> None:
        """Test Good XML serialization."""
        good = Good(
            id=123,
            name="XML Test Product",
            unit="szt.",
            netto=Decimal("10.00"),
            type=GoodType.GOOD,
            warehouse_type=WarehouseType.SIMPLE,
        )
        xml_bytes = good.to_xml()
        assert b"<good>" in xml_bytes
        assert b"<id>123</id>" in xml_bytes
        assert b"<name>XML Test Product</name>" in xml_bytes
        assert b"<unit>szt.</unit>" in xml_bytes
        assert b"<netto>10.00</netto>" in xml_bytes
        assert b"<type>good</type>" in xml_bytes
        assert b"<warehouse_type>simple</warehouse_type>" in xml_bytes

    def test_good_xml_deserialization(self) -> None:
        """Test Good XML deserialization."""
        xml_data = b"""<good>
            <id>456</id>
            <name>Deserialized Product</name>
            <unit>kg</unit>
            <netto>25.50</netto>
            <type>good</type>
            <warehouse_type>simple</warehouse_type>
            <count>100.0000</count>
            <vat>23</vat>
        </good>"""
        good = Good.from_xml(xml_data)
        assert good.id == 456
        assert good.name == "Deserialized Product"
        assert good.unit == "kg"
        assert good.netto == Decimal("25.50")
        assert good.type == GoodType.GOOD
        assert good.warehouse_type == WarehouseType.SIMPLE
        assert good.count == Decimal("100.0000")
        assert good.vat == "23"

    def test_good_xml_deserialization_with_enums_as_strings(self) -> None:
        """Test Good XML deserialization handles string enum values."""
        xml_data = b"""<good>
            <id>789</id>
            <name>Service Item</name>
            <type>service</type>
            <warehouse_type>detailed</warehouse_type>
        </good>"""
        good = Good.from_xml(xml_data)
        assert good.id == 789
        assert good.name == "Service Item"
        assert good.type == GoodType.SERVICE
        assert good.warehouse_type == WarehouseType.DETAILED

    def test_good_immutable(self) -> None:
        """Test Good is immutable (frozen)."""
        good = Good(id=1, name="Test")
        with pytest.raises(ValidationError):
            good.name = "Modified"

    def test_good_id_required(self) -> None:
        """Test Good requires id field."""
        with pytest.raises(ValidationError) as exc_info:
            Good(name="Test")
        assert "id" in str(exc_info.value)

    def test_good_name_required(self) -> None:
        """Test Good requires name field."""
        with pytest.raises(ValidationError) as exc_info:
            Good(id=1)
        assert "name" in str(exc_info.value)

    def test_good_all_vat_rates(self) -> None:
        """Test Good handles different VAT rates."""
        vat_rates = ["23", "8", "5", "0", "zw", "np", "oo"]
        for vat in vat_rates:
            good = Good(id=1, name="Test", vat=vat)
            assert good.vat == vat

    def test_good_with_code(self) -> None:
        """Test Good with product code/SKU."""
        good = Good(
            id=1,
            name="Product with SKU",
            code="SKU-12345-XYZ",
        )
        assert good.code == "SKU-12345-XYZ"

    def test_good_with_description(self) -> None:
        """Test Good with description."""
        good = Good(
            id=1,
            name="Described Product",
            description="This is a detailed description of the product.",
        )
        assert good.description == "This is a detailed description of the product."
