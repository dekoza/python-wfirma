Installation
============

Requirements
------------

* Python 3.12 or higher
* pip or uv (recommended)

Installing from PyPI
--------------------

The recommended way to install python-wfirma is from PyPI using uv::

    uv pip install python-wfirma

Or using pip::

    pip install python-wfirma

Installing from Source
----------------------

To install the latest development version::

    git clone https://github.com/yourusername/python-wfirma.git
    cd python-wfirma
    uv pip install -e .

Optional Dependencies
---------------------

Development Tools
~~~~~~~~~~~~~~~~~

For development work, install the development dependencies::

    uv pip install python-wfirma[dev]

This includes:

* pytest - Testing framework
* pytest-asyncio - Async test support
* pytest-cov - Code coverage
* respx - HTTP mocking
* ruff - Linting and formatting
* mypy - Type checking
* tox - Test automation

Documentation Tools
~~~~~~~~~~~~~~~~~~~

To build documentation locally::

    uv pip install python-wfirma[docs]

Examples and Integrations
~~~~~~~~~~~~~~~~~~~~~~~~~~

To run examples::

    uv pip install python-wfirma[examples]

All Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

To install everything::

    uv pip install python-wfirma[dev,docs,examples]

Verifying Installation
----------------------

Check that the package is installed correctly::

    python -c "import wfirma; print(wfirma.__version__)"

This should print the installed version number.

Next Steps
----------

* :doc:`authentication` - Set up API credentials
* :doc:`quickstart` - Your first API call

