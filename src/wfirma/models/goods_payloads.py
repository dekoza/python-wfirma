"""Pydantic models for goods request payloads.

These models are used to validate and serialize request payloads sent to the wFirma API.
They intentionally support only the subset of fields exposed by the current resource
methods.

Notes:
    The wFirma API expects wrapped payloads with numbered record branches
    (doc.wfirma.pl, "Format wymiany danych")::

        {"goods": {"0": {"good": {...}}}}

    which matches how other resources in this library structure requests.
"""

from __future__ import annotations

from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from wfirma.models.good import GoodType, WarehouseType


class GoodUpsertData(BaseModel):
    """Data accepted by /goods/add and /goods/edit endpoints."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = None
    code: str | None = None
    unit: str | None = None
    netto: Decimal | None = None
    vat: str | None = None
    description: str | None = None
    tags: str | None = None

    type: GoodType | None = None
    warehouse_type: WarehouseType | None = None


class GoodsUpsertRequest(BaseModel):
    """Wrapped request payload for goods endpoints."""

    model_config = ConfigDict(extra="forbid")

    goods: dict[str, dict[str, GoodUpsertData]]

    @classmethod
    def from_good_data(cls, good: GoodUpsertData) -> GoodsUpsertRequest:
        return cls(goods={"0": {"good": good}})


__all__ = [
    "GoodsUpsertRequest",
    "GoodUpsertData",
]
