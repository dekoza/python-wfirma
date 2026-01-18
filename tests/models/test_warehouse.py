"""
Tests for warehouse document Pydantic models.

These tests verify warehouse document models for wFirma API:
- WarehouseDocument - Main warehouse document model
- WarehouseDocumentContent - Warehouse document line item model
- WarehouseDocumentType - Enum for document types (PW, PZ, RW, WZ, etc.)

Based on wFirma API structure from:
- /warehouse_document_p_w/add, /warehouse_document_p_w/find, /warehouse_document_p_w/get, etc.
- /warehouse_document_p_z/add, /warehouse_document_p_z/find, etc.
- /warehouse_document_r/add, /warehouse_document_r/find, etc.
- /warehouse_document_r_w/add, /warehouse_document_r_w/find, etc.
- /warehouse_document_w_z/add, /warehouse_document_w_z/find, etc.
- /warehouse_document_z_d/add, /warehouse_document_z_d/find, etc.
- /warehouse_document_z_p_d/add, /warehouse_document_z_p_d/find, etc.

Warehouse document types in Polish accounting:
- PW (Przyjęcie Wewnętrzne) - Internal receipt
- PZ (Przyjęcie Zewnętrzne) - External receipt (from supplier)
- R (Rozchód) - Issue/disbursement
- RW (Rozchód Wewnętrzny) - Internal issue
- WZ (Wydanie Zewnętrzne) - External issue (to customer)
- ZD (Zwrot do Dostawcy) - Return to supplier
- ZPD (Zwrot Przyjętych Dostaw) - Return of received deliveries

Warehouse document fields from API documentation:
- id, fullnumber, date
- type (document type)
- warehouse_document_contents (line items)
- contractor_id (for external documents)
- company_id
- created, modified
"""

from datetime import datetime
from decimal import Decimal

import pytest
from pydantic import ValidationError

from wfirma.models.warehouse import (
    WarehouseDocument,
    WarehouseDocumentContent,
    WarehouseDocumentType,
)


class TestWarehouseDocumentType:
    """Tests for WarehouseDocumentType enum."""

    # AICOMPLETE: WarehouseDocumentType enum tests - ready for review

    def test_warehouse_document_type_values(self) -> None:
        """Test WarehouseDocumentType enum has expected values."""
        assert WarehouseDocumentType.PW.value == "p_w"
        assert WarehouseDocumentType.PZ.value == "p_z"
        assert WarehouseDocumentType.R.value == "r"
        assert WarehouseDocumentType.RW.value == "r_w"
        assert WarehouseDocumentType.WZ.value == "w_z"
        assert WarehouseDocumentType.ZD.value == "z_d"
        assert WarehouseDocumentType.ZPD.value == "z_p_d"

    def test_warehouse_document_type_from_string(self) -> None:
        """Test creating WarehouseDocumentType from string value."""
        assert WarehouseDocumentType("p_w") == WarehouseDocumentType.PW
        assert WarehouseDocumentType("p_z") == WarehouseDocumentType.PZ
        assert WarehouseDocumentType("r") == WarehouseDocumentType.R
        assert WarehouseDocumentType("r_w") == WarehouseDocumentType.RW
        assert WarehouseDocumentType("w_z") == WarehouseDocumentType.WZ
        assert WarehouseDocumentType("z_d") == WarehouseDocumentType.ZD
        assert WarehouseDocumentType("z_p_d") == WarehouseDocumentType.ZPD

    def test_warehouse_document_type_invalid(self) -> None:
        """Test WarehouseDocumentType raises error for invalid value."""
        with pytest.raises(ValueError):
            WarehouseDocumentType("invalid")


class TestWarehouseDocumentContent:
    """Tests for WarehouseDocumentContent model."""

    # AICOMPLETE: WarehouseDocumentContent validation tests - ready for review

    def test_warehouse_document_content_minimal(self) -> None:
        """Test WarehouseDocumentContent with minimal required fields."""
        content = WarehouseDocumentContent(
            id=1,
            name="Test Product",
        )
        assert content.id == 1
        assert content.name == "Test Product"
        assert content.unit is None
        assert content.unit_count is None
        assert content.price is None

    def test_warehouse_document_content_full(self) -> None:
        """Test WarehouseDocumentContent with all fields."""
        content = WarehouseDocumentContent(
            id=12345,
            name="Widget Pro",
            unit="szt.",
            unit_count=Decimal("10.0000"),
            price=Decimal("100.00"),
            good_id=17895634,
            warehouse_document_id=98765,
            created=datetime(2024, 1, 15, 10, 30, 45),
            modified=datetime(2024, 1, 16, 11, 0, 0),
        )
        assert content.id == 12345
        assert content.name == "Widget Pro"
        assert content.unit == "szt."
        assert content.unit_count == Decimal("10.0000")
        assert content.price == Decimal("100.00")
        assert content.good_id == 17895634
        assert content.warehouse_document_id == 98765
        assert content.created == datetime(2024, 1, 15, 10, 30, 45)
        assert content.modified == datetime(2024, 1, 16, 11, 0, 0)

    def test_warehouse_document_content_decimal_precision(self) -> None:
        """Test WarehouseDocumentContent preserves decimal precision."""
        content = WarehouseDocumentContent(
            id=1,
            name="Test",
            unit_count=Decimal("12.3456"),
            price=Decimal("99.99"),
        )
        assert content.unit_count == Decimal("12.3456")
        assert content.price == Decimal("99.99")

    def test_warehouse_document_content_immutable(self) -> None:
        """Test WarehouseDocumentContent is immutable (frozen)."""
        content = WarehouseDocumentContent(
            id=1,
            name="Test Product",
        )
        with pytest.raises(ValidationError):
            content.name = "Modified Name"  # type: ignore[misc]

    def test_warehouse_document_content_xml_serialization(self) -> None:
        """Test WarehouseDocumentContent XML serialization."""
        content = WarehouseDocumentContent(
            id=1,
            name="Test",
            unit="szt.",
            unit_count=Decimal("5"),
            price=Decimal("10.50"),
        )
        xml_bytes = content.to_xml()
        assert b"<warehouse_document_content>" in xml_bytes
        assert b"<id>1</id>" in xml_bytes
        assert b"<name>Test</name>" in xml_bytes
        assert b"<unit>szt.</unit>" in xml_bytes

    def test_warehouse_document_content_xml_parsing(self) -> None:
        """Test WarehouseDocumentContent XML parsing."""
        xml_data = b"""<?xml version="1.0" encoding="UTF-8"?>
        <warehouse_document_content>
            <id>1</id>
            <name>Produkt testowy</name>
            <unit>szt.</unit>
            <unit_count>10.0000</unit_count>
            <price>100</price>
            <good_id>17895634</good_id>
        </warehouse_document_content>"""
        content = WarehouseDocumentContent.from_xml(xml_data)
        assert content.id == 1
        assert content.name == "Produkt testowy"
        assert content.unit == "szt."
        assert content.unit_count == Decimal("10.0000")
        assert content.price == Decimal("100")
        assert content.good_id == 17895634

    def test_warehouse_document_content_optional_good_reference(self) -> None:
        """Test WarehouseDocumentContent with good reference."""
        content_with_good = WarehouseDocumentContent(
            id=1,
            name="Linked Product",
            good_id=12345,
        )
        assert content_with_good.good_id == 12345

        content_without_good = WarehouseDocumentContent(
            id=2,
            name="Unlinked Product",
        )
        assert content_without_good.good_id is None


class TestWarehouseDocument:
    """Tests for WarehouseDocument model."""

    # AICOMPLETE: WarehouseDocument validation tests - ready for review

    def test_warehouse_document_minimal(self) -> None:
        """Test WarehouseDocument with minimal required fields."""
        doc = WarehouseDocument(id=1)
        assert doc.id == 1
        assert doc.fullnumber is None
        assert doc.date is None
        assert doc.type is None
        assert doc.contractor_id is None

    def test_warehouse_document_full(self) -> None:
        """Test WarehouseDocument with all fields."""
        doc = WarehouseDocument(
            id=53487196,
            fullnumber="PZ 1/2024",
            date="2024-01-15",
            type=WarehouseDocumentType.PZ,
            description="Test warehouse receipt",
            notes="Internal notes",
            tags="warehouse,test",
            contractor_id=12345,
            company_id=99999,
            series_id=5,
            created=datetime(2024, 1, 15, 10, 30, 45),
            modified=datetime(2024, 1, 16, 11, 0, 0),
        )
        assert doc.id == 53487196
        assert doc.fullnumber == "PZ 1/2024"
        assert doc.date == "2024-01-15"
        assert doc.type == WarehouseDocumentType.PZ
        assert doc.description == "Test warehouse receipt"
        assert doc.notes == "Internal notes"
        assert doc.tags == "warehouse,test"
        assert doc.contractor_id == 12345
        assert doc.company_id == 99999
        assert doc.series_id == 5
        assert doc.created == datetime(2024, 1, 15, 10, 30, 45)
        assert doc.modified == datetime(2024, 1, 16, 11, 0, 0)

    def test_warehouse_document_all_types(self) -> None:
        """Test WarehouseDocument with each document type."""
        types_to_test = [
            WarehouseDocumentType.PW,
            WarehouseDocumentType.PZ,
            WarehouseDocumentType.R,
            WarehouseDocumentType.RW,
            WarehouseDocumentType.WZ,
            WarehouseDocumentType.ZD,
            WarehouseDocumentType.ZPD,
        ]
        for doc_type in types_to_test:
            doc = WarehouseDocument(id=1, type=doc_type)
            assert doc.type == doc_type

    def test_warehouse_document_internal_types(self) -> None:
        """Test WarehouseDocument internal types (PW, RW - no contractor)."""
        # Internal receipt - no external contractor
        pw_doc = WarehouseDocument(
            id=1,
            type=WarehouseDocumentType.PW,
            fullnumber="PW 1/2024",
        )
        assert pw_doc.type == WarehouseDocumentType.PW
        assert pw_doc.contractor_id is None

        # Internal issue - no external contractor
        rw_doc = WarehouseDocument(
            id=2,
            type=WarehouseDocumentType.RW,
            fullnumber="RW 1/2024",
        )
        assert rw_doc.type == WarehouseDocumentType.RW
        assert rw_doc.contractor_id is None

    def test_warehouse_document_external_types(self) -> None:
        """Test WarehouseDocument external types (PZ, WZ - with contractor)."""
        # External receipt from supplier
        pz_doc = WarehouseDocument(
            id=1,
            type=WarehouseDocumentType.PZ,
            fullnumber="PZ 1/2024",
            contractor_id=12345,
        )
        assert pz_doc.type == WarehouseDocumentType.PZ
        assert pz_doc.contractor_id == 12345

        # External issue to customer
        wz_doc = WarehouseDocument(
            id=2,
            type=WarehouseDocumentType.WZ,
            fullnumber="WZ 1/2024",
            contractor_id=67890,
        )
        assert wz_doc.type == WarehouseDocumentType.WZ
        assert wz_doc.contractor_id == 67890

    def test_warehouse_document_immutable(self) -> None:
        """Test WarehouseDocument is immutable (frozen)."""
        doc = WarehouseDocument(id=1)
        with pytest.raises(ValidationError):
            doc.id = 2  # type: ignore[misc]

    def test_warehouse_document_xml_serialization(self) -> None:
        """Test WarehouseDocument XML serialization."""
        doc = WarehouseDocument(
            id=1,
            fullnumber="PW 1/2024",
            date="2024-01-15",
            type=WarehouseDocumentType.PW,
        )
        xml_bytes = doc.to_xml()
        assert b"<warehouse_document>" in xml_bytes
        assert b"<id>1</id>" in xml_bytes
        assert b"<fullnumber>PW 1/2024</fullnumber>" in xml_bytes
        assert b"<date>2024-01-15</date>" in xml_bytes
        assert b"<type>p_w</type>" in xml_bytes

    def test_warehouse_document_xml_parsing(self) -> None:
        """Test WarehouseDocument XML parsing."""
        xml_data = b"""<?xml version="1.0" encoding="UTF-8"?>
        <warehouse_document>
            <id>53487196</id>
            <fullnumber>PZ 5/2024</fullnumber>
            <date>2024-06-30</date>
            <type>p_z</type>
            <contractor_id>12345</contractor_id>
        </warehouse_document>"""
        doc = WarehouseDocument.from_xml(xml_data)
        assert doc.id == 53487196
        assert doc.fullnumber == "PZ 5/2024"
        assert doc.date == "2024-06-30"
        assert doc.type == WarehouseDocumentType.PZ
        assert doc.contractor_id == 12345

    def test_warehouse_document_xml_parsing_unordered_elements(self) -> None:
        """Test WarehouseDocument XML parsing with unordered elements."""
        xml_data = b"""<?xml version="1.0" encoding="UTF-8"?>
        <warehouse_document>
            <type>w_z</type>
            <fullnumber>WZ 10/2024</fullnumber>
            <id>99999</id>
            <contractor_id>54321</contractor_id>
            <date>2024-12-01</date>
        </warehouse_document>"""
        doc = WarehouseDocument.from_xml(xml_data)
        assert doc.id == 99999
        assert doc.fullnumber == "WZ 10/2024"
        assert doc.date == "2024-12-01"
        assert doc.type == WarehouseDocumentType.WZ
        assert doc.contractor_id == 54321

    def test_warehouse_document_datetime_handling(self) -> None:
        """Test WarehouseDocument datetime field handling."""
        # Test with datetime objects
        doc = WarehouseDocument(
            id=1,
            created=datetime(2024, 1, 15, 10, 30, 45),
            modified=datetime(2024, 1, 16, 11, 0, 0),
        )
        assert doc.created == datetime(2024, 1, 15, 10, 30, 45)
        assert doc.modified == datetime(2024, 1, 16, 11, 0, 0)

    def test_warehouse_document_datetime_from_string(self) -> None:
        """Test WarehouseDocument datetime parsing from string."""
        doc = WarehouseDocument(
            id=1,
            created="2024-01-15 10:30:45",
            modified="2024-01-16 11:00:00",
        )
        assert doc.created == datetime(2024, 1, 15, 10, 30, 45)
        assert doc.modified == datetime(2024, 1, 16, 11, 0, 0)

    def test_warehouse_document_null_datetime_handling(self) -> None:
        """Test WarehouseDocument handles null datetime values."""
        doc = WarehouseDocument(
            id=1,
            created="0000-00-00 00:00:00",
        )
        assert doc.created is None

    def test_warehouse_document_with_series_reference(self) -> None:
        """Test WarehouseDocument with series reference."""
        doc = WarehouseDocument(
            id=1,
            series_id=5,
            fullnumber="PW 1/2024",
        )
        assert doc.series_id == 5


class TestWarehouseModelsExport:
    """Tests for warehouse model exports from wfirma.models."""

    # AICOMPLETE: Warehouse models export tests - ready for review

    def test_models_importable_from_package(self) -> None:
        """Test all warehouse models are importable from wfirma.models."""
        from wfirma.models import (
            WarehouseDocument,
            WarehouseDocumentContent,
            WarehouseDocumentType,
        )
        assert WarehouseDocument is not None
        assert WarehouseDocumentContent is not None
        assert WarehouseDocumentType is not None

    def test_models_in_all_list(self) -> None:
        """Test all warehouse models are in __all__ list."""
        from wfirma import models
        assert "WarehouseDocument" in models.__all__
        assert "WarehouseDocumentContent" in models.__all__
        assert "WarehouseDocumentType" in models.__all__


