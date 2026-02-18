"""Tests for async VehicleRunRatesResource."""

from __future__ import annotations

from typing import Any

import pytest

from wfirma.async_.resources.vehicle_run_rates import VehicleRunRatesResource


@pytest.fixture
def mock_client() -> Any:
    """Create a mock client for testing."""
    from unittest.mock import AsyncMock, MagicMock

    client = MagicMock()
    client.company_id = 123
    client.get_json = AsyncMock()
    return client


class TestAsyncVehicleRunRatesResource:
    """Test suite for async VehicleRunRatesResource."""

    @pytest.mark.asyncio
    async def test_find_returns_list_of_vehicle_run_rates(self, mock_client: Any) -> None:
        """Test that find() returns a list of vehicle_run_rates dicts."""
        resource = VehicleRunRatesResource(mock_client)

        response_data = {
            "status": {"code": "OK"},
            "vehicle_run_rates": {
                "0": {"vehicle_run_rate": {"id": "1", "name": "Rate 1"}},
                "1": {"vehicle_run_rate": {"id": "2", "name": "Rate 2"}},
            },
        }
        mock_client.get_json.return_value = response_data

        result = await resource.find()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {"id": "1", "name": "Rate 1"}
        assert result[1] == {"id": "2", "name": "Rate 2"}
        mock_client.get_json.assert_called_once_with("/vehicle_run_rates/find")

    @pytest.mark.asyncio
    async def test_find_returns_empty_list_when_container_is_empty(self, mock_client: Any) -> None:
        """Test that find() returns empty list when container is empty dict."""
        resource = VehicleRunRatesResource(mock_client)

        response_data = {
            "status": {"code": "OK"},
            "vehicle_run_rates": {},
        }
        mock_client.get_json.return_value = response_data

        result = await resource.find()

        assert isinstance(result, list)
        assert len(result) == 0
        mock_client.get_json.assert_called_once_with("/vehicle_run_rates/find")
