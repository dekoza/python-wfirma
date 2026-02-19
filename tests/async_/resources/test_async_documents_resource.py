"""Tests for DocumentsResource (asynchronous)."""

from __future__ import annotations

import httpx
import pytest
import respx

from wfirma.async_.client import WFirmaClient
from wfirma.async_.resources.documents import DocumentsResource


@pytest.fixture
def auth():
    """Mock authentication."""
    from wfirma.async_.auth import APIKeyAuth

    return APIKeyAuth(
        access_key="test_access",
        secret_key="test_secret",
        app_key="test_app",
    )


@pytest.fixture
def client(auth):
    """Create a test client."""
    return WFirmaClient(auth=auth, company_id=1)


@pytest.fixture
def resource(client):
    """Create a test resource."""
    return DocumentsResource(client)


class TestDocumentsResourceAdd:
    """Tests for add method."""

    @pytest.mark.asyncio
    async def test_add_calls_expected_endpoint(self, resource):
        """Verify add() makes POST request to correct endpoint."""
        with respx.mock:
            respx.post(
                "https://api2.wfirma.pl/documents/add",
                params={
                    "outputFormat": "json",
                    "inputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 1,
                                    "name": "test.pdf",
                                    "type": "pdf",
                                }
                            }
                        },
                    },
                )
            )

            payload = {
                "name": "test.pdf",
                "type": "pdf",
            }
            result = await resource.add(payload)

            assert isinstance(result, dict)
            assert result["id"] == 1
            assert result["name"] == "test.pdf"

    @pytest.mark.asyncio
    async def test_add_returns_extracted_payload(self, resource):
        """Verify add() returns unwrapped payload dict."""
        with respx.mock:
            respx.post(
                "https://api2.wfirma.pl/documents/add",
                params={
                    "outputFormat": "json",
                    "inputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 42,
                                    "name": "document.pdf",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.add({"name": "document.pdf"})

            assert result == {"id": 42, "name": "document.pdf"}


class TestDocumentsResourceFind:
    """Tests for find method."""

    @pytest.mark.asyncio
    async def test_find_calls_expected_endpoint(self, resource):
        """Verify find() makes GET request to correct endpoint."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/find",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 1,
                                    "name": "doc1.pdf",
                                }
                            },
                            "1": {
                                "document": {
                                    "id": 2,
                                    "name": "doc2.pdf",
                                }
                            },
                        },
                    },
                )
            )

            result = await resource.find()

            assert isinstance(result, list)
            assert len(result) == 2
            assert all(isinstance(item, dict) for item in result)

    @pytest.mark.asyncio
    async def test_find_with_params(self, resource):
        """Verify find() accepts optional parameters."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/find",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                    "some_filter": "value",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 1,
                                    "name": "doc1.pdf",
                                }
                            },
                        },
                    },
                )
            )

            result = await resource.find(params={"some_filter": "value"})

            assert len(result) == 1

    @pytest.mark.asyncio
    async def test_find_returns_empty_list_on_empty_container(self, resource):
        """Verify find() returns empty list when container is empty."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/find",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {},
                    },
                )
            )

            result = await resource.find()

            assert result == []


class TestDocumentsResourceGet:
    """Tests for get method."""

    @pytest.mark.asyncio
    async def test_get_calls_expected_endpoint(self, resource):
        """Verify get() makes GET request with ID in path."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/get/42",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 42,
                                    "name": "document.pdf",
                                    "type": "pdf",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(42)

            assert isinstance(result, dict)
            assert result["id"] == 42
            assert result["name"] == "document.pdf"

    @pytest.mark.asyncio
    async def test_get_returns_extracted_payload(self, resource):
        """Verify get() returns unwrapped payload dict."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/get/99",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 99,
                                    "name": "file.pdf",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.get(99)

            assert result == {"id": 99, "name": "file.pdf"}


class TestDocumentsResourceDownload:
    """Tests for download method."""

    @pytest.mark.asyncio
    async def test_download_calls_expected_endpoint(self, resource):
        """Verify download() makes GET request to correct endpoint."""
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/download/42",
                params={
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    content=b"%PDF-1.4\n%mock pdf content",
                )
            )

            result = await resource.download(42)

            assert isinstance(result, bytes)
            assert result == b"%PDF-1.4\n%mock pdf content"

    @pytest.mark.asyncio
    async def test_download_returns_bytes(self, resource):
        """Verify download() returns binary content."""
        pdf_content = b"%PDF-1.4\n%\xe4\xe5\xe6\xe7"
        with respx.mock:
            respx.get(
                "https://api2.wfirma.pl/documents/download/99",
                params={
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    content=pdf_content,
                )
            )

            result = await resource.download(99)

            assert isinstance(result, bytes)
            assert result == pdf_content


class TestDocumentsResourceDelete:
    """Tests for delete method."""

    @pytest.mark.asyncio
    async def test_delete_calls_expected_endpoint(self, resource):
        """Verify delete() makes DELETE request with ID in path."""
        with respx.mock:
            respx.delete(
                "https://api2.wfirma.pl/documents/delete/42",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 42,
                                    "deleted": True,
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.delete(42)

            assert isinstance(result, dict)
            assert result["id"] == 42

    @pytest.mark.asyncio
    async def test_delete_returns_extracted_payload(self, resource):
        """Verify delete() returns unwrapped payload dict."""
        with respx.mock:
            respx.delete(
                "https://api2.wfirma.pl/documents/delete/88",
                params={
                    "outputFormat": "json",
                    "company_id": "1",
                },
            ).mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "status": {"code": "OK"},
                        "documents": {
                            "0": {
                                "document": {
                                    "id": 88,
                                    "status": "deleted",
                                }
                            }
                        },
                    },
                )
            )

            result = await resource.delete(88)

            assert result == {"id": 88, "status": "deleted"}
