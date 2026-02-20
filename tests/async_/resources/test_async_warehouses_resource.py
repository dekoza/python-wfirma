"""Tests for async warehouses resource.

Tests verify:
- async get(warehouse_id) returns dict[str, Any]
- async find() returns list[dict[str, Any]]
- async find() returns [] when container is {}
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock

import pytest

from wfirma.async_.resources.warehouses import WarehousesResource


class TestAsyncWarehousesResourceGet:
    """Tests for async WarehousesResource.get()."""

    @pytest.mark.asyncio
    async def test_get_warehouse_returns_dict(self) -> None:
        """Test async get() returns single warehouse as dict."""
        client = MagicMock()
        client.get_json = AsyncMock(
            return_value={
                "warehouses": {
                    "0": {
                        "warehouse": {
                            "id": 123,
                            "name": "Main Warehouse",
                            "code": "MW",
                        }
                    }
                }
            }
        )
        resource = WarehousesResource(client)
        result = await resource.get(123)

        assert isinstance(result, dict)
        assert result["id"] == 123
        assert result["name"] == "Main Warehouse"
        assert result["code"] == "MW"
        client.get_json.assert_called_once_with("/warehouses/get/123")


class TestAsyncWarehousesResourceFind:
    """Tests for async WarehousesResource.find()."""

    @pytest.mark.asyncio
    async def test_find_warehouses_returns_list(self) -> None:
        """Test async find() returns list of warehouses as dicts."""
        client = MagicMock()
        client.get_json = AsyncMock(
            return_value={
                "warehouses": {
                    "0": {"warehouse": {"id": 1, "name": "Warehouse A"}},
                    "1": {"warehouse": {"id": 2, "name": "Warehouse B"}},
                }
            }
        )
        resource = WarehousesResource(client)
        result = await resource.find()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0]["id"] == 1
        assert result[0]["name"] == "Warehouse A"
        assert result[1]["id"] == 2
        assert result[1]["name"] == "Warehouse B"
        client.get_json.assert_called_once_with("/warehouses/find")

    @pytest.mark.asyncio
    async def test_find_warehouses_empty_container_returns_empty_list(self) -> None:
        """Test async find() returns [] when container is empty {}."""
        client = MagicMock()
        client.get_json = AsyncMock(return_value={"warehouses": {}})
        resource = WarehousesResource(client)
        result = await resource.find()

        assert isinstance(result, list)
        assert len(result) == 0
        client.get_json.assert_called_once_with("/warehouses/find")
