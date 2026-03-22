"""Tests for asynchronous contractor resource.

These tests verify that resource wrappers call the expected endpoints and
forward parameters through the async HTTP client.
"""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.contractors import ContractorResource
from wfirma.models.contractor import Contractor


class TestContractorResourceGet:
    """Tests for async ContractorResource.get() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource GET returns Contractor model - ready for review
    async def test_get_calls_expected_endpoint_and_returns_model(self) -> None:
        """Should call /contractors/get/{contractorId} and return Contractor."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/contractors/get/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "contractors": {
                                "0": {
                                    "contractor": {
                                        "id": 456,
                                        "name": "ACME Corp",
                                        "nip": "1234567890",
                                        "city": "Warsaw",
                                        "country": "PL",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.get(contractor_id=456)

        assert route.called
        assert isinstance(result, Contractor)
        assert result.id == 456
        assert result.name == "ACME Corp"
        assert result.nip == "1234567890"
        assert result.city == "Warsaw"


class TestContractorResourceFind:
    """Tests for async ContractorResource.find() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource FIND returns list of Contractors - ready for review
    async def test_find_calls_expected_endpoint_and_returns_list(self) -> None:
        """Should call /contractors/find and return list of Contractors."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/contractors/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "contractors": {
                                "0": {
                                    "contractor": {
                                        "id": 100,
                                        "name": "Company A",
                                    }
                                },
                                "1": {
                                    "contractor": {
                                        "id": 101,
                                        "name": "Company B",
                                    }
                                },
                            },
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 2,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 2
        assert all(isinstance(c, Contractor) for c in result)
        assert result[0].id == 100
        assert result[0].name == "Company A"
        assert result[1].id == 101
        assert result[1].name == "Company B"

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource FIND handles empty result - ready for review
    async def test_find_handles_empty_result(self) -> None:
        """Should return empty list when no contractors found."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.get(
                    "https://sandbox-api2.wfirma.pl/contractors/find",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "contractors": {},
                            "parameters": {
                                "page": 1,
                                "limit": 20,
                                "total": 0,
                            },
                        },
                    )
                )

                result = await resource.find()

        assert route.called
        assert isinstance(result, list)
        assert len(result) == 0


class TestContractorResourceAdd:
    """Tests for async ContractorResource.add() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource ADD creates and returns Contractor - ready for review
    async def test_add_calls_expected_endpoint_and_returns_model(self) -> None:
        """Should call POST /contractors/add and return created Contractor."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/contractors/add",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "contractors": {
                                "0": {
                                    "contractor": {
                                        "id": 789,
                                        "name": "New Company",
                                        "nip": "9876543210",
                                        "city": "Krakow",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.add(
                    name="New Company",
                    nip="9876543210",
                    city="Krakow",
                )

        assert route.called
        assert isinstance(result, Contractor)
        assert result.id == 789
        assert result.name == "New Company"
        assert result.nip == "9876543210"

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource ADD with all fields - ready for review
    async def test_add_with_full_data(self) -> None:
        """Should create contractor with all available fields."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/contractors/add",
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "contractors": {
                                "0": {
                                    "contractor": {
                                        "id": 999,
                                        "name": "Full Company",
                                        "altname": "FC",
                                        "nip": "1111111111",
                                        "street": "Main Street",
                                        "building_number": "10",
                                        "flat_number": "5",
                                        "zip": "00-001",
                                        "city": "Warsaw",
                                        "country": "PL",
                                        "email": "contact@fullcompany.pl",
                                        "phone": "+48123456789",
                                        "buyer": True,
                                        "seller": False,
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.add(
                    name="Full Company",
                    altname="FC",
                    nip="1111111111",
                    street="Main Street",
                    building_number="10",
                    flat_number="5",
                    zip="00-001",
                    city="Warsaw",
                    country="PL",
                    email="contact@fullcompany.pl",
                    phone="+48123456789",
                    buyer=True,
                    seller=False,
                )

        assert route.called
        assert isinstance(result, Contractor)
        assert result.id == 999
        assert result.altname == "FC"
        assert result.email == "contact@fullcompany.pl"
        assert result.buyer is True


class TestContractorResourceEdit:
    """Tests for async ContractorResource.edit() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource EDIT updates and returns Contractor - ready for review
    async def test_edit_calls_expected_endpoint_and_returns_model(self) -> None:
        """Should call POST /contractors/edit/{contractorId} and return updated Contractor."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.post(
                    "https://sandbox-api2.wfirma.pl/contractors/edit/456",
                    params={
                        "inputFormat": "json",
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                            "contractors": {
                                "0": {
                                    "contractor": {
                                        "id": 456,
                                        "name": "Updated Company",
                                        "city": "Gdansk",
                                    }
                                }
                            },
                        },
                    )
                )

                result = await resource.edit(
                    contractor_id=456,
                    name="Updated Company",
                    city="Gdansk",
                )

        assert route.called
        assert isinstance(result, Contractor)
        assert result.id == 456
        assert result.name == "Updated Company"
        assert result.city == "Gdansk"


class TestContractorResourceDelete:
    """Tests for async ContractorResource.delete() method."""

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource DELETE removes contractor - ready for review
    async def test_delete_calls_expected_endpoint(self) -> None:
        """Should call DELETE /contractors/delete/{contractorId}."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://sandbox-api2.wfirma.pl/contractors/delete/456",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "OK"},
                        },
                    )
                )

                result = await resource.delete(contractor_id=456)

        assert route.called
        assert result is True

    @pytest.mark.asyncio
    # AICOMPLETE: Async contractor resource DELETE raises on NOT FOUND - ready for review
    async def test_delete_raises_on_not_found(self) -> None:
        """Should raise ResourceNotFoundError when contractor not found."""
        auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
        client = WFirmaClient(auth=auth, company_id=123)
        resource = ContractorResource(client)

        async with client:
            with respx.mock:
                route = respx.delete(
                    "https://sandbox-api2.wfirma.pl/contractors/delete/999",
                    params={
                        "outputFormat": "json",
                        "company_id": "123",
                    },
                ).mock(
                    return_value=httpx.Response(
                        200,
                        json={
                            "status": {"code": "NOT FOUND"},
                        },
                    )
                )

                from wfirma.exceptions import ResourceNotFoundError

                with pytest.raises(ResourceNotFoundError):
                    await resource.delete(contractor_id=999)

        assert route.called
