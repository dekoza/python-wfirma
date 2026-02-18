"""Tests for sync client.warehouses property."""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.warehouses import WarehousesResource


class TestSyncClientWarehousesProperty:
    """Tests for WFirmaClient.warehouses property."""

    def test_warehouses_returns_resource(self) -> None:
        """Test client.warehouses returns WarehousesResource instance."""
        auth = MagicMock()
        client = WFirmaClient(auth=auth)
        resource = client.warehouses

        assert isinstance(resource, WarehousesResource)

    def test_warehouses_is_cached(self) -> None:
        """Test client.warehouses is cached (returns same instance)."""
        auth = MagicMock()
        client = WFirmaClient(auth=auth)
        first = client.warehouses
        second = client.warehouses

        assert first is second
