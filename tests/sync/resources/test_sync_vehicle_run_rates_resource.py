"""Tests for sync VehicleRunRatesResource."""

from __future__ import annotations

from typing import Any

import httpx
import pytest
import respx

from wfirma.sync.resources.vehicle_run_rates import VehicleRunRatesResource


@pytest.fixture
def mock_client() -> Any:
    """Create a mock client for testing."""
    from unittest.mock import MagicMock

    client = MagicMock()
    client.company_id = 123
    return client


class TestVehicleRunRatesResource:
    """Test suite for VehicleRunRatesResource."""

    def test_find_returns_list_of_vehicle_run_rates(self, mock_client: Any) -> None:
        """Test that find() returns a list of vehicle_run_rates dicts."""
        resource = VehicleRunRatesResource(mock_client)

        # Mock response data
        response_data = {
            "status": {"code": "OK"},
            "vehicle_run_rates": {
                "0": {"vehicle_run_rate": {"id": "1", "name": "Rate 1"}},
                "1": {"vehicle_run_rate": {"id": "2", "name": "Rate 2"}},
            },
        }
        mock_client.get_json.return_value = response_data

        result = resource.find()

        assert isinstance(result, list)
        assert len(result) == 2
        assert result[0] == {"id": "1", "name": "Rate 1"}
        assert result[1] == {"id": "2", "name": "Rate 2"}
        mock_client.get_json.assert_called_once_with("/vehicle_run_rates/find")

    def test_find_returns_empty_list_when_container_is_empty(self, mock_client: Any) -> None:
        """Test that find() returns empty list when container is empty dict."""
        resource = VehicleRunRatesResource(mock_client)

        # Mock response with empty container
        response_data = {
            "status": {"code": "OK"},
            "vehicle_run_rates": {},
        }
        mock_client.get_json.return_value = response_data

        result = resource.find()

        assert isinstance(result, list)
        assert len(result) == 0
        mock_client.get_json.assert_called_once_with("/vehicle_run_rates/find")
