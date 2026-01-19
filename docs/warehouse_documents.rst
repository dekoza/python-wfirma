Warehouse documents (PW)
========================

This page documents the current support for warehouse documents in the library.

wFirma exposes separate endpoint groups for each warehouse document type.
At the moment, the library implements typed wrappers for **PW** documents
("Przyjęcie Wewnętrzne") via the ``warehouse_document_p_w`` endpoints.

Synchronous
-----------

Example::

    from wfirma.sync import APIKeyAuth, WFirmaClient
    from wfirma.sync.resources.warehouse_documents_pw import WarehouseDocumentPWResource

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    with WFirmaClient(auth=auth, company_id=123) as client:
        pw = WarehouseDocumentPWResource(client)
        doc = pw.get(warehouse_document_id=53487196)
        docs = pw.find()

Asynchronous
------------

Example::

    from wfirma.async_ import APIKeyAuth, WFirmaClient
    from wfirma.async_.resources.warehouse_documents_pw import WarehouseDocumentPWResource

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    async with WFirmaClient(auth=auth, company_id=123) as client:
        pw = WarehouseDocumentPWResource(client)
        doc = await pw.get(warehouse_document_id=53487196)
        docs = await pw.find()

Notes
-----

* These resource wrappers currently assume JSON input/output (``inputFormat=json`` and
  ``outputFormat=json``).
* Other warehouse document types (PZ, WZ, RW, etc.) are planned as future resources.

