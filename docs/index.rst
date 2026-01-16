python-wfirma Documentation
===========================

Welcome to the documentation for **python-wfirma**, a modern Python library for the wFirma accounting API.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   installation
   authentication
   quickstart
   api_reference
   guides/index
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

    from wfirma import WFirmaClient

    client = WFirmaClient(
        app_key="your_app_key",
        secret="your_secret"
    )

    invoices = client.invoices.list(limit=10)

Asynchronous usage::

    from wfirma import AsyncWFirmaClient

    async with AsyncWFirmaClient(
        app_key="your_app_key",
        secret="your_secret"
    ) as client:
        invoices = await client.invoices.list(limit=10)

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

