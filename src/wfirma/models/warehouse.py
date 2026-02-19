"""
Warehouse document models for wFirma API.

This module provides warehouse document-related model classes used in wFirma API:
- WarehouseDocument - Main warehouse document model
- WarehouseDocumentContent - Warehouse document line item model
- WarehouseDocumentType - Enum for document types

Warehouse document types in Polish accounting:
- PW (Przyjęcie Wewnętrzne) - Internal receipt
- PZ (Przyjęcie Zewnętrzne) - External receipt (from supplier)
- R (Rozchód) - Issue/disbursement
- RW (Rozchód Wewnętrzny) - Internal issue
- WZ (Wydanie Zewnętrzne) - External issue (to customer)
- ZD (Zwrot do Dostawcy) - Return to supplier
- ZPD (Zwrot Przyjętych Dostaw) - Return of received deliveries

Warehouse documents track inventory movements in the warehouse.
External documents (PZ, WZ, ZD, ZPD) are linked to contractors.
Internal documents (PW, RW, R) do not require a contractor.

Example:
    >>> from wfirma.models.warehouse import (
    ...     WarehouseDocument,
    ...     WarehouseDocumentContent,
    ...     WarehouseDocumentType,
    ... )
    >>> from decimal import Decimal
    >>> doc = WarehouseDocument(
    ...     id=53487196,
    ...     fullnumber="PZ 1/2024",
    ...     date="2024-01-15",
    ...     type=WarehouseDocumentType.PZ,
    ...     contractor_id=12345,
    ... )
    >>> doc.type
    WarehouseDocumentType.PZ
"""

from decimal import Decimal
from enum import Enum

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, TimestampedFieldsMixin


class WarehouseDocumentType(str, Enum):
    """
    Enum for warehouse document types.

    Defines the type of warehouse document. Each type corresponds
    to a different API endpoint in wFirma.

    Internal documents (no contractor required):
    - PW: Przyjęcie Wewnętrzne (Internal receipt)
    - RW: Rozchód Wewnętrzny (Internal issue)
    - R: Rozchód (Issue/disbursement)

    External documents (contractor required):
    - PZ: Przyjęcie Zewnętrzne (External receipt from supplier)
    - WZ: Wydanie Zewnętrzne (External issue to customer)
    - ZD: Zwrot do Dostawcy (Return to supplier)
    - ZPD: Zwrot Przyjętych Dostaw (Return of received deliveries)
    - ZPM: Zwrot Przyjętych Materiałów (Return of received materials)

    Attributes:
        PW: Internal receipt (Przyjęcie Wewnętrzne).
        PZ: External receipt (Przyjęcie Zewnętrzne).
        R: Issue/disbursement (Rozchód).
        RW: Internal issue (Rozchód Wewnętrzny).
        WZ: External issue (Wydanie Zewnętrzne).
        ZD: Return to supplier (Zwrot do Dostawcy).
        ZPD: Return of received deliveries (Zwrot Przyjętych Dostaw).
        ZPM: Return of received materials (Zwrot Przyjętych Materiałów).
    """

    PW = "p_w"
    PZ = "p_z"
    R = "r"
    RW = "r_w"
    WZ = "w_z"
    ZD = "z_d"
    ZPD = "z_p_d"
    ZPM = "z_p_m"


class WarehouseDocumentContent(
    TimestampedFieldsMixin, BaseXMLModel, tag="warehouse_document_content"
):
    """
    Warehouse document line item model.

    This model matches the `warehouse_document_content` structure used by
    wFirma API within warehouse documents. Each warehouse document can have
    multiple contents representing individual line items (products).

    Attributes:
        id: Line item ID.
        name: Product name on document.
        unit: Unit of measure (szt., kg, m, etc.).
        unit_count: Quantity.
        price: Unit price.
        good_id: Reference to Good model (product catalog).
        warehouse_document_id: Reference to parent WarehouseDocument.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> from decimal import Decimal
        >>> content = WarehouseDocumentContent(
        ...     id=1,
        ...     name="Widget Pro",
        ...     unit="szt.",
        ...     unit_count=Decimal("10.0000"),
        ...     price=Decimal("100.00"),
        ...     good_id=17895634,
        ... )
        >>> content.unit_count
        Decimal('10.0000')
    """

    # Required fields
    id: int = element()
    name: str = element()

    # Quantity and pricing
    unit: str | None = element(default=None)
    unit_count: Decimal | None = element(default=None)
    price: Decimal | None = element(default=None)

    # Foreign key references
    good_id: int | None = element(default=None)
    warehouse_document_id: int | None = element(default=None)

    # Timestamps provided by TimestampedFieldsMixin


class WarehouseDocument(TimestampedFieldsMixin, BaseXMLModel, tag="warehouse_document"):
    """
    Warehouse document model representing inventory movement.

    This model matches the `warehouse_document` structure used by wFirma API
    endpoints for various document types:
    - /warehouse_document_p_w/* (PW - internal receipt)
    - /warehouse_document_p_z/* (PZ - external receipt)
    - /warehouse_document_r/* (R - issue)
    - /warehouse_document_r_w/* (RW - internal issue)
    - /warehouse_document_w_z/* (WZ - external issue)
    - /warehouse_document_z_d/* (ZD - return to supplier)
    - /warehouse_document_z_p_d/* (ZPD - return of received deliveries)

    Attributes:
        id: Document ID.
        fullnumber: Full document number (e.g., "PZ 1/2024").
        date: Document date (YYYY-MM-DD).
        type: Document type (PW, PZ, RW, WZ, etc.).
        description: Document description.
        notes: Internal notes.
        tags: Tags for categorization.
        contractor_id: Reference to Contractor (for external documents).
        company_id: Reference to Company.
        series_id: Reference to document series.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> doc = WarehouseDocument(
        ...     id=53487196,
        ...     fullnumber="PZ 1/2024",
        ...     date="2024-01-15",
        ...     type=WarehouseDocumentType.PZ,
        ...     contractor_id=12345,
        ... )
        >>> doc.fullnumber
        'PZ 1/2024'
    """

    # Required fields
    id: int = element()

    # Document number fields
    fullnumber: str | None = element(default=None)

    # Date field (stored as string in wFirma format YYYY-MM-DD)
    date: str | None = element(default=None)

    # Document type
    type: WarehouseDocumentType | None = element(default=None)

    # Metadata
    description: str | None = element(default=None)
    notes: str | None = element(default=None)
    tags: str | None = element(default=None)

    # Foreign key references
    contractor_id: int | None = element(default=None)
    company_id: int | None = element(default=None)
    series_id: int | None = element(default=None)

    # Timestamps provided by TimestampedFieldsMixin


__all__ = [
    "WarehouseDocument",
    "WarehouseDocumentContent",
    "WarehouseDocumentType",
]
