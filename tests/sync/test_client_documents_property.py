import pytest

from wfirma.sync.client import WFirmaClient
from wfirma.sync.resources.documents import DocumentsResource


@pytest.fixture
def auth():
    from wfirma.sync.auth import APIKeyAuth

    return APIKeyAuth(
        access_key="test_access",
        secret_key="test_secret",
        app_key="test_app",
    )


@pytest.fixture
def client(auth):
    return WFirmaClient(auth=auth, company_id=1)


def test_documents_property_returns_resource_instance(client):
    resource = client.documents
    assert isinstance(resource, DocumentsResource)


def test_documents_property_is_cached(client):
    first = client.documents
    second = client.documents
    assert first is second
