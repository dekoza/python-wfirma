Authentication
==============

wFirma API uses OAuth for authentication. This guide will help you set up authentication.

Getting API Credentials
------------------------

1. Log in to your wFirma account
2. Navigate to **Settings** → **API**
3. Generate a new application key and secret
4. Save these credentials securely

Configuration Methods
---------------------

Environment Variables
~~~~~~~~~~~~~~~~~~~~~

The recommended method for production::

    export WFIRMA_APP_KEY=your_app_key
    export WFIRMA_SECRET=your_secret
    export WFIRMA_ENVIRONMENT=sandbox  # or production

Or create a ``.env`` file::

    WFIRMA_APP_KEY=your_app_key
    WFIRMA_SECRET=your_secret
    WFIRMA_ENVIRONMENT=sandbox

Direct Configuration
~~~~~~~~~~~~~~~~~~~~

Pass credentials directly when creating the client::

    from wfirma import WFirmaClient

    client = WFirmaClient(
        app_key="your_app_key",
        secret="your_secret",
        environment="sandbox"
    )

Environments
------------

Sandbox Environment
~~~~~~~~~~~~~~~~~~~

Use sandbox for testing::

    client = WFirmaClient(
        app_key="your_sandbox_key",
        secret="your_sandbox_secret",
        environment="sandbox"
    )

Production Environment
~~~~~~~~~~~~~~~~~~~~~~

Use production for live data::

    client = WFirmaClient(
        app_key="your_production_key",
        secret="your_production_secret",
        environment="production"
    )

.. warning::
   Always test your integration in the sandbox environment before using production credentials.

Token Management
----------------

The library handles token management automatically:

* Tokens are obtained on first API call
* Tokens are cached during the session
* Expired tokens are automatically renewed
* No manual token handling required

Multi-Company Support
---------------------

If you have access to multiple companies::

    client = WFirmaClient(
        app_key="your_app_key",
        secret="your_secret",
        company_id="specific_company_id"
    )

Security Best Practices
-----------------------

1. **Never commit credentials** to version control
2. **Use environment variables** in production
3. **Rotate credentials** regularly
4. **Use sandbox** for development and testing
5. **Limit API key permissions** to minimum required

Next Steps
----------

* :doc:`quickstart` - Make your first API call
* :doc:`guides/error_handling` - Handle authentication errors

