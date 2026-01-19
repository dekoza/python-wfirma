python-wfirma Documentation
===========================

Welcome to the documentation for **python-wfirma**, a modern Python library for the wFirma accounting API.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   authentication
   quickstart
   api_reference.rst
   troubleshooting

Features
--------

* 🔄 **Dual Mode**: Full support for both synchronous and asynchronous operations
* 🎯 **Type-Safe**: Complete type hints for better IDE support
* ✅ **Validated**: Automatic request/response validation using Pydantic
* 📦 **Format Agnostic**: Seamless JSON and XML handling
* 🔐 **OAuth Ready**: Built-in OAuth authentication

Quick Example
-------------

Synchronous usage::

    from wfirma.sync import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    with WFirmaClient(auth=auth, company_id=123) as client:
        # Low-level HTTP calls (dict payload)
        data = client.get_json("/users/get/123")

        # Higher-level typed resources (Pydantic models)
        company = client.company.get()
        address = client.company.find_main_address()

Asynchronous usage::

    from wfirma.async_ import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="ak", secret_key="sk", app_key="appk")

    async with WFirmaClient(auth=auth, company_id=123) as client:
        # Low-level HTTP calls (dict payload)
        data = await client.get_json("/users/get/123")

        # Higher-level typed resources (Pydantic models)
        company = await client.company.get()
        address = await client.company.find_main_address()

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
