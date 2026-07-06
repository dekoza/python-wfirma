"""Good-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "goods" group.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.

Notes:
    wFirma payload shapes differ between endpoints and formats.
    This resource currently expects JSON responses (``outputFormat=json``).
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

from wfirma._payloads import (
    build_find_parameters,
    extract_object_list_payloads,
    extract_single_object_payload,
)
from wfirma.async_.client import WFirmaClient
from wfirma.models.good import Good
from wfirma.models.goods_payloads import GoodsUpsertRequest, GoodUpsertData


class GoodsResource:
    """Asynchronous goods resource.

    Args:
        client: A configured asynchronous wFirma HTTP client.
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, good_id: int) -> Good:
        """Get good by ID.

        Endpoint: GET /goods/get/{goodId}
        """
        data = await self._client.get_json(f"/goods/get/{good_id}")
        payload = self._extract_good_payload(data)
        return Good.model_validate(payload)

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[Good]:
        """Find/list goods.

        Endpoint: GET /goods/find

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/goods/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/goods/find",
                data={"goods": {"parameters": parameters}},
            )
        return self._extract_good_list(data)

    async def add(
        self,
        name: str,
        *,
        code: str | None = None,
        unit: str | None = None,
        netto: Decimal | None = None,
        vat: str | None = None,
        description: str | None = None,
        tags: str | None = None,
        type: str | None = None,
        warehouse_type: str | None = None,
    ) -> Good:
        """Create a new good.

        Endpoint: POST /goods/add

        Args:
            name: Product/service name (required).
            code: Product code/SKU.
            unit: Unit of measure.
            netto: Net price (without VAT).
            vat: VAT rate code.
            description: Product description.
            tags: Tags/labels for categorization.
            type: Good type ("good" or "service").
            warehouse_type: Warehouse tracking type ("simple" or "detailed").

        Returns:
            Created good model with assigned ID.
        """
        good_data = GoodUpsertData.model_validate(
            {
                "name": name,
                "code": code,
                "unit": unit,
                "netto": netto,
                "vat": vat,
                "description": description,
                "tags": tags,
                "type": type,
                "warehouse_type": warehouse_type,
            }
        )
        payload = GoodsUpsertRequest.from_good_data(good_data).model_dump(mode="json")
        data = await self._client.post_json("/goods/add", data=payload)
        result_payload = self._extract_good_payload(data)
        return Good.model_validate(result_payload)

    async def edit(
        self,
        good_id: int,
        *,
        name: str | None = None,
        code: str | None = None,
        unit: str | None = None,
        netto: Decimal | None = None,
        vat: str | None = None,
        description: str | None = None,
        tags: str | None = None,
        type: str | None = None,
        warehouse_type: str | None = None,
    ) -> Good:
        """Update an existing good.

        Endpoint: POST /goods/edit/{goodId}

        Args:
            good_id: Good identifier (required).
            name: Product/service name.
            code: Product code/SKU.
            unit: Unit of measure.
            netto: Net price (without VAT).
            vat: VAT rate code.
            description: Product description.
            tags: Tags/labels for categorization.
            type: Good type ("good" or "service").
            warehouse_type: Warehouse tracking type ("simple" or "detailed").

        Returns:
            Updated good model.
        """
        good_data = GoodUpsertData.model_validate(
            {
                "name": name,
                "code": code,
                "unit": unit,
                "netto": netto,
                "vat": vat,
                "description": description,
                "tags": tags,
                "type": type,
                "warehouse_type": warehouse_type,
            }
        )
        payload = GoodsUpsertRequest.from_good_data(good_data).model_dump(mode="json")
        data = await self._client.post_json(f"/goods/edit/{good_id}", data=payload)
        result_payload = self._extract_good_payload(data)
        return Good.model_validate(result_payload)

    async def delete(self, good_id: int) -> bool:
        """Delete a good.

        Endpoint: DELETE /goods/delete/{goodId}
        """
        await self._client.delete_json(f"/goods/delete/{good_id}")
        return True

    @staticmethod
    def _extract_good_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract Good payload from a wFirma JSON response."""
        return extract_single_object_payload(
            data=data,
            container_key="goods",
            object_key="good",
        )

    @staticmethod
    def _extract_good_list(data: dict[str, Any]) -> list[Good]:
        """Extract list of Goods from a wFirma JSON response."""
        payloads = extract_object_list_payloads(
            data,
            container_key="goods",
            object_key="good",
        )
        return [Good.model_validate(payload) for payload in payloads]

    @staticmethod
    def _build_good_payload(**kwargs: Any) -> dict[str, Any]:
        """Build good payload for API request.

        Filters out None values and wraps in expected API structure.

        Deprecated:
            This helper is kept for backward compatibility with earlier iterations.
            New code should prefer ``wfirma.models.goods_payloads``.
        """
        good_data = {k: v for k, v in kwargs.items() if v is not None}
        return {"goods": [{"good": good_data}]}


__all__ = [
    "GoodsResource",
]
