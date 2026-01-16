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

    client = WFirmaClient(..., timeout=60)

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

1. The library implements automatic retry with backoff
2. Reduce request frequency
3. Use bulk operations where available
4. Contact wFirma support to increase rate limits

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

Inspect Raw Responses
~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    # Access raw response data
    response = client.invoices._client.last_response
    print(response.status_code)
    print(response.json())

Test Connectivity
~~~~~~~~~~~~~~~~~

.. code-block:: python

    try:
        company = client.company.get_info()
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

1. Check the `GitHub Issues <https://github.com/yourusername/python-wfirma/issues>`_
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

A: Version 0.1.x is in development. Wait for 1.0.0 for production use, or thoroughly test in your environment.

**Q: Does this library support Python 3.11?**

A: Currently requires Python 3.12+. Python 3.11 support may be added based on demand.

**Q: How do I handle multi-company scenarios?**

A: Specify ``company_id`` when creating the client, or use ``client.company.switch(company_id)``.

**Q: Can I use this with Django/Flask?**

A: Yes! See examples in ``examples/flask_integration`` and ``examples/fastapi_integration``.

**Q: Is async mode required?**

A: No, both sync and async modes are fully supported. Choose based on your needs.

