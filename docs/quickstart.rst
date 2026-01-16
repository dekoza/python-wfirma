Quick Start
===========

This guide will help you make your first API call in just a few minutes.

Prerequisites
-------------

* Python 3.12+ installed
* wFirma API credentials (see :doc:`authentication`)
* python-wfirma installed (see :doc:`installation`)

Your First API Call
-------------------

Synchronous Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wfirma import WFirmaClient

    # Initialize the client
    client = WFirmaClient(
        app_key="your_app_key",
        secret="your_secret",
        environment="sandbox"
    )

    # List invoices
    invoices = client.invoices.list(limit=10)
    for invoice in invoices:
        print(f"Invoice {invoice.number}: {invoice.total} PLN")

Asynchronous Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio
    from wfirma import AsyncWFirmaClient

    async def main():
        # Initialize the async client
        async with AsyncWFirmaClient(
            app_key="your_app_key",
            secret="your_secret",
            environment="sandbox"
        ) as client:
            # List invoices
            invoices = await client.invoices.list(limit=10)
            async for invoice in invoices:
                print(f"Invoice {invoice.number}: {invoice.total} PLN")

    asyncio.run(main())

Common Operations
-----------------

Creating a Contractor
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wfirma.models import Contractor

    contractor = Contractor(
        name="Example Company Ltd.",
        tax_id="1234567890",
        email="contact@example.com",
        address="123 Main Street",
        city="Warsaw",
        postal_code="00-001",
        country="PL"
    )

    created = client.contractors.create(contractor)
    print(f"Created contractor with ID: {created.id}")

Creating an Invoice
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wfirma.models import Invoice, InvoicePosition
    from datetime import date

    invoice = Invoice(
        contractor_id=contractor_id,
        issue_date=date.today(),
        sale_date=date.today(),
        payment_date=date.today(),
        positions=[
            InvoicePosition(
                name="Consulting Services",
                quantity=1,
                unit_price=1000.00,
                vat_rate=23
            )
        ]
    )

    created = client.invoices.create(invoice)
    print(f"Created invoice: {created.number}")

Retrieving a Single Resource
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Get invoice by ID
    invoice = client.invoices.get(invoice_id)

    # Get contractor by ID
    contractor = client.contractors.get(contractor_id)

Updating a Resource
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Fetch the invoice
    invoice = client.invoices.get(invoice_id)

    # Modify it
    invoice.payment_date = date.today() + timedelta(days=14)

    # Update
    updated = client.invoices.update(invoice_id, invoice)

Deleting a Resource
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Delete invoice
    client.invoices.delete(invoice_id)

    # Delete contractor
    client.contractors.delete(contractor_id)

Filtering and Pagination
~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from datetime import date, timedelta

    # Filter invoices by date range
    start_date = date.today() - timedelta(days=30)
    end_date = date.today()

    invoices = client.invoices.list(
        start_date=start_date,
        end_date=end_date,
        limit=50
    )

    # Paginate through results
    for invoice in invoices:
        print(invoice.number)

Error Handling
--------------

Always handle potential errors:

.. code-block:: python

    from wfirma.exceptions import (
        AuthenticationError,
        ValidationError,
        ResourceNotFoundError
    )

    try:
        invoice = client.invoices.get(invoice_id)
    except AuthenticationError:
        print("Invalid credentials")
    except ResourceNotFoundError:
        print("Invoice not found")
    except ValidationError as e:
        print(f"Validation error: {e}")

Using Context Managers
----------------------

For automatic resource cleanup:

.. code-block:: python

    # Synchronous
    with WFirmaClient(app_key="...", secret="...") as client:
        invoices = client.invoices.list()

    # Asynchronous
    async with AsyncWFirmaClient(app_key="...", secret="...") as client:
        invoices = await client.invoices.list()

Next Steps
----------

* :doc:`guides/invoices` - Detailed invoice management guide
* :doc:`guides/contractors` - Managing contractors
* :doc:`guides/error_handling` - Comprehensive error handling
* :doc:`guides/async_usage` - Advanced async patterns
* :doc:`api_reference` - Full API documentation

