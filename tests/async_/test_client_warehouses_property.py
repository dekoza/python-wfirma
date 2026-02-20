"""Tests for async client.warehouses property."""

from __future__ import annotations

from unittest.mock import MagicMock

from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.warehouses import WarehousesResource


class TestAsyncClientWarehousesProperty:
    """Tests for async WFirmaClient.warehouses property."""

    def test_warehouses_returns_resource(self) -> None:
        """Test async client.warehouses returns WarehousesResource instance."""
        auth = MagicMock()
        client = WFirmaClient(auth=auth)
        resource = client.warehouses

        assert isinstance(resource, WarehousesResource)

    def test_warehouses_is_cached(self) -> None:
        """Test async client.warehouses is cached (returns same instance)."""
        auth = MagicMock()
        client = WFirmaClient(auth=auth)
        first = client.warehouses
        second = client.warehouses

        assert first is second
