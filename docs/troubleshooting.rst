Troubleshooting
===============

Common Issues and Solutions
----------------------------

Authentication Errors
~~~~~~~~~~~~~~~~~~~~~

**Problem**: ``AuthenticationError: Invalid credentials``

**Solution**:

1. Verify your app key and secret
2. Check that you're using the correct environment (sandbox/production)
3. Ensure credentials haven't expired
4. Try regenerating your API credentials in wFirma settings

**Problem**: ``AuthenticationError`` when exchanging an OAuth2 authorization code

**Solution**: This library maps HTTP errors from the OAuth2 token endpoint (for example 401/400)
into ``AuthenticationError`` for a consistent public API.

1. Verify your ``client_id`` and ``client_secret``
2. Verify you used the correct ``redirect_uri`` (must match the one configured in wFirma)
3. Ensure the authorization ``code`` was not already used and did not expire

**Problem**: ``ConnectionError`` / ``TimeoutError`` during OAuth2 token exchange

**Solution**: Transport-level errors (DNS, connection failures, timeouts) raised by ``httpx`` are
mapped to ``wfirma.exceptions.ConnectionError`` and ``wfirma.exceptions.TimeoutError``.

If you need extra details (URL, underlying exception), enable debug logging on the auth helper::

    auth = OAuth2Auth(
        client_id="...",
        client_secret="...",
        redirect_uri="...",
        environment=Environment.PRODUCTION,
        debug=True,
    )

The ``debug`` flag logs exception details via the standard ``logging`` module.

**Problem**: ``TokenExpiredError``

**Solution**: The library should handle this automatically. If you see this error repeatedly:

1. Check your system clock is correct
2. Verify network connectivity
3. Check for proxy/firewall issues

Network Errors
~~~~~~~~~~~~~~

**Problem**: ``ConnectionError`` or ``TimeoutError``

**Solution**:

1. Check internet connectivity
2. Verify wFirma API status
3. Increase timeout setting::

    from wfirma.sync import APIKeyAuth, WFirmaClient

    auth = APIKeyAuth(access_key="...", secret_key="...", app_key="...")
    client = WFirmaClient(auth=auth, timeout=60)

4. Check firewall/proxy settings

Validation Errors
~~~~~~~~~~~~~~~~~

**Problem**: ``ValidationError: Invalid field value``

**Solution**:

1. Check API documentation for field requirements
2. Verify data types match model specifications
3. Check for required fields
4. Review field constraints (min/max values, patterns)

Rate Limiting
~~~~~~~~~~~~~

**Problem**: ``RateLimitError: Too many requests``

**Solution**:

1. ``python-wfirma`` raises ``RateLimitError`` but does not retry automatically in ``1.0b1``
2. If the exception includes ``retry_after``, wait that many seconds before retrying
3. Reduce request frequency
4. Contact wFirma support if your integration needs a higher limit

Data Issues
~~~~~~~~~~~

**Problem**: ``ResourceNotFoundError``

**Solution**:

1. Verify the resource ID is correct
2. Check if resource was deleted
3. Ensure you have permission to access the resource
4. Verify you're accessing the correct company

**Problem**: Unexpected data in responses

**Solution**:

1. Check API version compatibility
2. Verify model definitions are up to date
3. Report issue on GitHub with example

Debugging
---------

Enable Detailed Logging
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import logging

    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('wfirma')
    logger.setLevel(logging.DEBUG)

Inspect Structured API Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from wfirma.exceptions import APIError

    try:
        client.get_json("/invoices/find")
    except APIError as exc:
        print(exc.to_dict())

Test Connectivity
~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        company = client.company.get()
        print("Connection successful!")
    except Exception as e:
        print(f"Connection failed: {e}")

Performance Issues
------------------

Slow Requests
~~~~~~~~~~~~~

1. Check network latency
2. Use async client for concurrent requests
3. Implement caching (future feature)
4. Use pagination with appropriate page sizes

Memory Issues
~~~~~~~~~~~~~

1. Use pagination for large datasets
2. Process results in batches
3. Use generators/iterators instead of loading all data

Getting Help
------------

If you can't resolve your issue:

1. Check the `GitHub Issues <https://github.com/dekoza/python-wfirma/issues>`_
2. Search existing discussions
3. Open a new issue with:

   * Python version
   * Library version
   * Minimal reproducible example
   * Full error traceback
   * Environment details

4. For security issues, email directly (see README)

Known Issues
------------

See `NOAI_PROBLEMS_REPORT.md` for current known issues with NOAI-protected tests.

Frequently Asked Questions
--------------------------

**Q: Can I use this library in production?**

A: ``1.0b1`` is a beta release. ``WFirmaClient`` support is limited to API Key and OAuth2 in this release, while OAuth1 remains helper-only. Use it only if you validate your exact flows first and accept API churn before ``1.0.0``.

**Q: Does this library support Python 3.11?**

A: Currently requires Python 3.12+. Python 3.11 support may be added based on demand.

**Q: How do I handle multi-company scenarios?**

A: Create the client with the target ``company_id``. If you need a different company, create another client configured for that company. For company lookups specifically, you can also call ``client.company.get(company_id=...)``.

**Q: Can I use this with Django/Flask?**

A: Yes. The client is framework-agnostic and can be used anywhere you can manage credentials and HTTP request lifecycles. Framework-specific examples are not bundled yet.

**Q: Is async mode required?**

A: No, both sync and async modes are fully supported. Choose based on your needs.
