Installation
============

Requirements
------------

* Python 3.12 or higher
* `uv` (recommended)

Installing from PyPI
--------------------

End users can install the package from PyPI using pip::

    pip install python-wfirma

Development / contributing
--------------------------

This repository uses `uv` (see `uv.lock`). To set up a local development environment::

    git clone https://github.com/dekoza/python-wfirma.git
    cd python-wfirma
    uv sync --extra dev --group dev --extra docs

Optional Dependencies
---------------------

Development Tools
~~~~~~~~~~~~~~~~~

For development work, add the development dependency group::

    uv sync --group dev

Documentation Tools
~~~~~~~~~~~~~~~~~~~

To build documentation locally, add the docs extras::

    uv sync --extra docs

All Optional Dependencies
~~~~~~~~~~~~~~~~~~~~~~~~~~

To install everything::

    uv sync --extra dev --group dev --extra docs

Verifying Installation
----------------------

Check that the package is installed correctly::

    python -c "import wfirma; print(wfirma.__version__)"

This should print the installed version number.

Next Steps
----------

* :doc:`authentication` - Set up API credentials
* :doc:`quickstart` - Your first API call
