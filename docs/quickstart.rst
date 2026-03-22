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

    import respx
    import httpx

    from wfirma.sync import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    # The base HTTP client returns the parsed API payload (dict).
    # Below we mock the HTTP call to keep the example self-contained.
    with respx.mock:
        respx.get("https://sandbox-api2.wfirma.pl/users/get/123").mock(
            return_value=httpx.Response(
                200,
                json={
                    "users": {"0": {"user": {"id": "123", "login": "test@example.com"}}},
                    "status": {"code": "OK"},
                },
            )
        )

        with WFirmaClient(auth=auth) as client:
            data = client.get_json("/users/get/123")
            print(data["users"]["0"]["user"]["login"])

Asynchronous Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import asyncio

    import httpx
    import respx

    from wfirma.async_ import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")


    async def main() -> None:
        with respx.mock:
            respx.get("https://sandbox-api2.wfirma.pl/users/get/123").mock(
                return_value=httpx.Response(
                    200,
                    json={
                        "users": {"0": {"user": {"id": "123", "login": "test@example.com"}}},
                        "status": {"code": "OK"},
                    },
                )
            )

            async with WFirmaClient(auth=auth) as client:
                data = await client.get_json("/users/get/123")
                print(data["users"]["0"]["user"]["login"])


    asyncio.run(main())

Next Steps
----------

You can also use the higher-level resource wrappers (recommended for type-safe access):

Synchronous resources example::

    from wfirma.sync import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    with WFirmaClient(auth=auth, company_id=123) as client:
        company = client.company.get()  # CompanyDetail model
        address = client.company.find_main_address()  # CompanyAddress model

        # Goods (typed resource)
        goods = client.goods.find()  # list[Good] models
        updated = client.goods.edit(456, name="Updated name")  # Good model

        # Tags (resource returns raw dict payloads)
        tags = client.tags.find()  # list[dict[str, Any]]
        tag = client.tags.add(name="New tag", visibility="visible")

Asynchronous resources example::

    from wfirma.async_ import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    async with WFirmaClient(auth=auth, company_id=123) as client:
        company = await client.company.get()  # CompanyDetail model
        address = await client.company.find_main_address()  # CompanyAddress model

        # Goods (typed resource)
        goods = await client.goods.find()  # list[Good] models
        updated = await client.goods.edit(456, name="Updated name")  # Good model

        # Tags (resource returns raw dict payloads)
        tags = await client.tags.find()  # list[dict[str, Any]]
        tag = await client.tags.add(name="New tag", visibility="visible")

See :doc:`authentication` for supported authentication methods and :doc:`troubleshooting`
for common issues.
