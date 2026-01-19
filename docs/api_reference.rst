Invoices Resource
=================

This page documents the high-level Python resource wrappers for wFirma invoices.

Synchronous
-----------

.. code-block:: python

   from wfirma.sync.auth import APIKeyAuth
   from wfirma.sync.client import WFirmaClient


   auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
   client = WFirmaClient(auth=auth, company_id=123)

   invoice = client.invoices.get(invoice_id=456)
   invoices = client.invoices.find()


Asynchronous
------------

.. code-block:: python

   import asyncio

   from wfirma.async_.auth import APIKeyAuth
   from wfirma.async_.client import WFirmaClient


   async def main() -> None:
       auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
       async with WFirmaClient(auth=auth, company_id=123) as client:
           invoice = await client.invoices.get(invoice_id=456)
           invoices = await client.invoices.find()


   asyncio.run(main())


Endpoints
---------

The wrapper currently supports the following endpoints (JSON mode):

- ``GET /invoices/get/{invoiceId}``
- ``GET /invoices/find``
- ``POST /invoices/add``
- ``POST /invoices/edit/{invoiceId}``
- ``DELETE /invoices/delete/{invoiceId}``


Payments Resource
=================

This page documents the high-level Python resource wrappers for wFirma payments.

Synchronous
-----------

.. code-block:: python

   from wfirma.sync.auth import APIKeyAuth
   from wfirma.sync.client import WFirmaClient


   auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
   client = WFirmaClient(auth=auth, company_id=123)

   payment = client.payments.get(payment_id=456)
   payments = client.payments.find()

   created = client.payments.add(payment={"object_name": "invoice", "object_id": 1000})
   updated = client.payments.edit(created.id, payment={"description": "Updated"})
   client.payments.delete(payment_id=created.id)


Asynchronous
------------

.. code-block:: python

   import asyncio

   from wfirma.async_.auth import APIKeyAuth
   from wfirma.async_.client import WFirmaClient


   async def main() -> None:
       auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="app")
       async with WFirmaClient(auth=auth, company_id=123) as client:
           payment = await client.payments.get(payment_id=456)
           payments = await client.payments.find()

           created = await client.payments.add(payment={"object_name": "invoice", "object_id": 1000})
           updated = await client.payments.edit(created.id, payment={"description": "Updated"})
           await client.payments.delete(payment_id=created.id)


   asyncio.run(main())


Endpoints
---------

The wrapper currently supports the following endpoints (JSON mode):

- ``GET /payments/get/{paymentId}``
- ``GET /payments/find``
- ``POST /payments/add``
- ``POST /payments/edit/{paymentId}``
- ``DELETE /payments/delete/{paymentId}``
