"""Contractor-related resource endpoints (asynchronous).

This module provides thin wrappers around the async HTTP client for endpoints
from the "contractors" group.

The resource layer maps API payloads into Pydantic models from ``wfirma.models``.
"""

from __future__ import annotations

from typing import Any

from wfirma._payloads import build_find_parameters, build_module_payload
from wfirma.async_.client import WFirmaClient
from wfirma.models.contractor import Contractor


class ContractorResource:
    """Asynchronous contractor resource.

    Args:
        client: A configured asynchronous wFirma HTTP client.

    Notes:
        wFirma payload shapes differ between endpoints and formats.
        This resource currently expects JSON responses (``outputFormat=json``).

    Example:
        >>> from wfirma.async_.client import WFirmaClient
        >>> from wfirma.async_.auth import APIKeyAuth
        >>> from wfirma.async_.resources.contractors import ContractorResource
        >>> auth = APIKeyAuth(access_key="...", secret_key="...", app_key="...")
        >>> async with WFirmaClient(auth=auth, company_id=123) as client:
        ...     contractors = ContractorResource(client)
        ...     contractor = await contractors.get(contractor_id=456)
        ...     print(contractor.name)
    """

    def __init__(self, client: WFirmaClient) -> None:
        self._client = client

    async def get(self, contractor_id: int) -> Contractor:
        """Get contractor by ID.

        Endpoint: GET /contractors/get/{contractorId}

        Args:
            contractor_id: Contractor identifier.

        Returns:
            Parsed contractor model.
        """
        data = await self._client.get_json(f"/contractors/get/{contractor_id}")
        payload = self._extract_contractor_payload(data)
        return Contractor.model_validate(payload)

    async def find(
        self,
        *,
        conditions: list[dict[str, Any]] | None = None,
        limit: int | None = None,
        page: int | None = None,
    ) -> list[Contractor]:
        """Find/list contractors.

        Endpoint: GET /contractors/find

        Returns:
            List of parsed contractor models.

        Args:
            conditions: Condition dicts with ``field``/``operator``/``value`` keys.
            limit: Page size.
            page: Page number.
        """
        if conditions is None and limit is None and page is None:
            data = await self._client.get_json("/contractors/find")
        else:
            parameters = build_find_parameters(conditions, limit=limit, page=page)
            data = await self._client.post_json(
                "/contractors/find",
                data={"contractors": {"parameters": parameters}},
            )
        return self._extract_contractor_list(data)

    async def add(
        self,
        name: str,
        *,
        altname: str | None = None,
        nip: str | None = None,
        regon: str | None = None,
        pesel: str | None = None,
        tax_id_type: str | None = None,
        street: str | None = None,
        building_number: str | None = None,
        flat_number: str | None = None,
        zip: str | None = None,
        city: str | None = None,
        country: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        fax: str | None = None,
        url: str | None = None,
        notes: str | None = None,
        tags: str | None = None,
        buyer: bool | None = None,
        seller: bool | None = None,
        remind: bool | None = None,
    ) -> Contractor:
        """Create a new contractor.

        Endpoint: POST /contractors/add

        Args:
            name: Full company/person name (required).
            altname: Short/alternative name.
            nip: Polish tax identification number (NIP).
            regon: Polish business registry number (REGON).
            pesel: Polish personal identification number (PESEL).
            tax_id_type: Type of tax ID (nip, pesel, custom, none).
            street: Street name.
            building_number: Building/house number.
            flat_number: Flat/apartment number.
            zip: Postal code.
            city: City name.
            country: Country code (ISO 3166-1 alpha-2).
            email: Email address.
            phone: Phone number.
            fax: Fax number.
            url: Website URL.
            notes: Internal notes.
            tags: Tags/labels for categorization.
            buyer: Is this contractor a buyer/customer.
            seller: Is this contractor a seller/supplier.
            remind: Send payment reminders to this contractor.

        Returns:
            Created contractor model with assigned ID.
        """
        payload = self._build_contractor_payload(
            name=name,
            altname=altname,
            nip=nip,
            regon=regon,
            pesel=pesel,
            tax_id_type=tax_id_type,
            street=street,
            building_number=building_number,
            flat_number=flat_number,
            zip=zip,
            city=city,
            country=country,
            email=email,
            phone=phone,
            fax=fax,
            url=url,
            notes=notes,
            tags=tags,
            buyer=buyer,
            seller=seller,
            remind=remind,
        )
        data = await self._client.post_json("/contractors/add", data=payload)
        result_payload = self._extract_contractor_payload(data)
        return Contractor.model_validate(result_payload)

    async def edit(
        self,
        contractor_id: int,
        *,
        name: str | None = None,
        altname: str | None = None,
        nip: str | None = None,
        regon: str | None = None,
        pesel: str | None = None,
        tax_id_type: str | None = None,
        street: str | None = None,
        building_number: str | None = None,
        flat_number: str | None = None,
        zip: str | None = None,
        city: str | None = None,
        country: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        fax: str | None = None,
        url: str | None = None,
        notes: str | None = None,
        tags: str | None = None,
        buyer: bool | None = None,
        seller: bool | None = None,
        remind: bool | None = None,
    ) -> Contractor:
        """Update an existing contractor.

        Endpoint: POST /contractors/edit/{contractorId}

        Args:
            contractor_id: Contractor identifier (required).
            name: Full company/person name.
            altname: Short/alternative name.
            nip: Polish tax identification number (NIP).
            regon: Polish business registry number (REGON).
            pesel: Polish personal identification number (PESEL).
            tax_id_type: Type of tax ID (nip, pesel, custom, none).
            street: Street name.
            building_number: Building/house number.
            flat_number: Flat/apartment number.
            zip: Postal code.
            city: City name.
            country: Country code (ISO 3166-1 alpha-2).
            email: Email address.
            phone: Phone number.
            fax: Fax number.
            url: Website URL.
            notes: Internal notes.
            tags: Tags/labels for categorization.
            buyer: Is this contractor a buyer/customer.
            seller: Is this contractor a seller/supplier.
            remind: Send payment reminders to this contractor.

        Returns:
            Updated contractor model.
        """
        payload = self._build_contractor_payload(
            name=name,
            altname=altname,
            nip=nip,
            regon=regon,
            pesel=pesel,
            tax_id_type=tax_id_type,
            street=street,
            building_number=building_number,
            flat_number=flat_number,
            zip=zip,
            city=city,
            country=country,
            email=email,
            phone=phone,
            fax=fax,
            url=url,
            notes=notes,
            tags=tags,
            buyer=buyer,
            seller=seller,
            remind=remind,
        )
        data = await self._client.post_json(f"/contractors/edit/{contractor_id}", data=payload)
        result_payload = self._extract_contractor_payload(data)
        return Contractor.model_validate(result_payload)

    async def delete(self, contractor_id: int) -> bool:
        """Delete a contractor.

        Endpoint: DELETE /contractors/delete/{contractorId}

        Args:
            contractor_id: Contractor identifier.

        Returns:
            True if deletion was successful.

        Raises:
            ResourceNotFoundError: If contractor not found.
        """
        await self._client.delete_json(f"/contractors/delete/{contractor_id}")
        return True

    @staticmethod
    def _extract_contractor_payload(data: dict[str, Any]) -> dict[str, Any]:
        """Extract Contractor payload from a wFirma JSON response."""
        container = data.get("contractors")
        if isinstance(container, dict):
            # Usually indexed dict: {"0": {"contractor": {...}}}
            first_item = next(iter(container.values()), None)
            if isinstance(first_item, dict):
                inner = first_item.get("contractor")
                if isinstance(inner, dict):
                    return inner
            # Direct structure
            if "contractor" in container and isinstance(container["contractor"], dict):
                return container["contractor"]

        raise KeyError("Unable to locate contractor payload in response.")

    @staticmethod
    def _extract_contractor_list(data: dict[str, Any]) -> list[Contractor]:
        """Extract list of Contractors from a wFirma JSON response."""
        container = data.get("contractors")
        if not isinstance(container, dict):
            return []

        contractors: list[Contractor] = []
        # Container is usually indexed dict: {"0": {"contractor": {...}}, "1": {...}}
        for key, item in container.items():
            # Skip non-numeric keys (sometimes meta info)
            if not key.isdigit():
                continue
            if isinstance(item, dict):
                inner = item.get("contractor")
                if isinstance(inner, dict):
                    contractors.append(Contractor.model_validate(inner))

        return contractors

    @staticmethod
    def _build_contractor_payload(**kwargs: Any) -> dict[str, Any]:
        """Build contractor payload for API request.

        Filters out None values and wraps in expected API structure.
        """
        contractor_data = {k: v for k, v in kwargs.items() if v is not None}
        return build_module_payload(
            container_key="contractors", object_key="contractor", obj=contractor_data
        )
