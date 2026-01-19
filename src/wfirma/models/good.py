"""
Good models for wFirma API.

This module provides good/product-related model classes used in wFirma API:
- Good - Main product/service model
- GoodType - Enum for good types (good, service)
- WarehouseType - Enum for warehouse inventory tracking types

Goods represent products or services that can be sold or purchased.
They are used in invoices, warehouse documents, and price lists.

Example:
    >>> from wfirma.models.good import Good, GoodType
    >>> good = Good(
    ...     id=123,
    ...     name="Premium Widget",
    ...     type=GoodType.GOOD,
    ...     unit="szt.",
    ...     netto=Decimal("99.99"),
    ... )
    >>> good.name
    'Premium Widget'
"""

from decimal import Decimal
from enum import Enum

from pydantic_xml import element

from wfirma.models.base import BaseXMLModel, OptionalDateTimeField


class GoodType(str, Enum):
    """
    Enum for good/product types.

    Attributes:
        GOOD: Physical product/merchandise.
        SERVICE: Service (non-physical).
    """

    GOOD = "good"
    SERVICE = "service"


class WarehouseType(str, Enum):
    """
    Enum for warehouse inventory tracking types.

    Attributes:
        SIMPLE: Simple inventory tracking (no detailed locations).
        DETAILED: Detailed inventory tracking with locations/batches.
    """

    SIMPLE = "simple"
    DETAILED = "detailed"


class Good(BaseXMLModel, tag="good"):
    """
    Good model representing a product or service.

    This model matches the `good` structure used by wFirma API
    endpoints: /goods/add, /goods/find, /goods/get, /goods/edit, etc.

    Attributes:
        id: Good ID.
        name: Product/service name.
        unit: Unit of measure (szt., kg, h, etc.).
        netto: Net price (without VAT).
        type: Type of good (good or service).
        warehouse_type: Warehouse inventory tracking type.
        count: Current stock count.
        vat: VAT rate (23, 8, 5, 0, zw, np, oo).
        vat_code_id: ID of VAT code in wFirma system.
        lumpcode: Lump sum tax code.
        classification: PKWiU or other classification code.
        description: Product description.
        code: Product code/SKU.
        tags: Tags/labels for categorization.
        created: Creation timestamp.
        modified: Last modification timestamp.

    Example:
        >>> good = Good(
        ...     id=12345,
        ...     name="Premium Widget",
        ...     unit="szt.",
        ...     netto=Decimal("99.99"),
        ...     type=GoodType.GOOD,
        ... )
    """

    # Required fields
    id: int = element()
    name: str = element()

    # Pricing fields
    unit: str | None = element(default=None)
    netto: Decimal | None = element(default=None)

    # Type fields
    type: GoodType | None = element(default=None)
    warehouse_type: WarehouseType | None = element(default=None)

    # Inventory fields
    count: Decimal | None = element(default=None)

    # Tax fields
    vat: str | None = element(default=None)
    vat_code_id: int | None = element(default=None)
    lumpcode: str | None = element(default=None)

    # Classification
    classification: str | None = element(default=None)

    # Metadata
    description: str | None = element(default=None)
    code: str | None = element(default=None)
    tags: str | None = element(default=None)

    # Timestamps
    created: OptionalDateTimeField = element(default=None)
    modified: OptionalDateTimeField = element(default=None)


__all__ = [
    "Good",
    "GoodType",
    "WarehouseType",
]
