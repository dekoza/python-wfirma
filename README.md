# Python wFirma API Library

[![PyPI version](https://badge.fury.io/py/python-wfirma.svg)](https://badge.fury.io/py/python-wfirma)
[![Python Versions](https://img.shields.io/pypi/pyversions/python-wfirma.svg)](https://pypi.org/project/python-wfirma/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://github.com/yourusername/python-wfirma/workflows/Tests/badge.svg)](https://github.com/yourusername/python-wfirma/actions)
[![Coverage](https://codecov.io/gh/yourusername/python-wfirma/branch/main/graph/badge.svg)](https://codecov.io/gh/yourusername/python-wfirma)

A modern, fully-typed Python library for interacting with the [wFirma](https://www.wfirma.pl/) accounting API. Supports both synchronous and asynchronous operations.

## Features

- 🔄 **Dual Mode**: Full support for both synchronous and asynchronous operations
- 🎯 **Type-Safe**: Complete type hints for better IDE support and fewer bugs
- ✅ **Validated**: Automatic request/response validation using Pydantic models
- 📦 **Format Agnostic**: Seamless handling of both JSON and XML via pydantic-xml
- 🔐 **OAuth Ready**: Built-in OAuth authentication with automatic token management
- 🧪 **Well Tested**: Comprehensive test coverage (>90%) following TDD principles
- 📚 **Documented**: Full API documentation and usage examples

## Installation

Using pip:
```bash
pip install python-wfirma
```

Using [uv](https://github.com/astral-sh/uv) (recommended for faster installation):
```bash
uv pip install python-wfirma
```

For development:
```bash
uv pip install python-wfirma[dev]
```

## Quick Start

### Synchronous Usage

```python
from wfirma import WFirmaClient
from wfirma.models import Invoice, Contractor

# Initialize client
client = WFirmaClient(
    app_key="your_app_key",
    secret="your_secret",
    environment="sandbox"  # or "production"
)

# Create a contractor
contractor = Contractor(
    name="Example Company Ltd.",
    tax_id="1234567890",
    email="contact@example.com"
)
created_contractor = client.contractors.create(contractor)

# Create an invoice
invoice = Invoice(
    contractor_id=created_contractor.id,
    issue_date="2026-01-16",
    # ... other fields
)
created_invoice = client.invoices.create(invoice)

# List invoices
invoices = client.invoices.list(limit=10)
for invoice in invoices:
    print(f"Invoice {invoice.number}: {invoice.total}")
```

### Asynchronous Usage

```python
import asyncio
from wfirma import AsyncWFirmaClient
from wfirma.models import Invoice, Contractor

async def main():
    # Initialize async client
    async with AsyncWFirmaClient(
        app_key="your_app_key",
        secret="your_secret",
        environment="sandbox"
    ) as client:
        # Create a contractor
        contractor = Contractor(
            name="Example Company Ltd.",
            tax_id="1234567890",
            email="contact@example.com"
        )
        created_contractor = await client.contractors.create(contractor)

        # Create an invoice
        invoice = Invoice(
            contractor_id=created_contractor.id,
            issue_date="2026-01-16",
            # ... other fields
        )
        created_invoice = await client.invoices.create(invoice)

        # List invoices
        invoices = await client.invoices.list(limit=10)
        async for invoice in invoices:
            print(f"Invoice {invoice.number}: {invoice.total}")

asyncio.run(main())
```

## Supported Resources

- ✅ **Invoices**: Create, read, update, delete, and manage invoices (including proforma and corrections)
- ✅ **Contractors**: Manage business partners and customers
- ✅ **Goods**: Product and service catalog management
- ✅ **Payments**: Track invoice payments
- ✅ **Warehouse**: Inventory management and stock documents
- ✅ **Employees**: User and permission management
- ✅ **Company**: Company information and settings

## Configuration

The library can be configured via environment variables or directly in code:

```bash
# .env file
WFIRMA_APP_KEY=your_app_key_here
WFIRMA_SECRET=your_secret_here
WFIRMA_ENVIRONMENT=sandbox  # or production
WFIRMA_TIMEOUT=30
WFIRMA_MAX_RETRIES=3
```

```python
from wfirma import WFirmaClient

# Configuration via code
client = WFirmaClient(
    app_key="your_app_key",
    secret="your_secret",
    environment="production",
    timeout=30,
    max_retries=3
)
```

## Documentation

Full documentation is available at [https://python-wfirma.readthedocs.io](https://python-wfirma.readthedocs.io)

- [Installation Guide](https://python-wfirma.readthedocs.io/en/latest/installation.html)
- [Authentication Setup](https://python-wfirma.readthedocs.io/en/latest/authentication.html)
- [Quick Start Tutorial](https://python-wfirma.readthedocs.io/en/latest/quickstart.html)
- [API Reference](https://python-wfirma.readthedocs.io/en/latest/api/)
- [Examples](https://github.com/yourusername/python-wfirma/tree/main/examples)

## Development

### Setup Development Environment

```bash
# Clone repository
git clone https://github.com/yourusername/python-wfirma.git
cd python-wfirma

# Create virtual environment and install dependencies using uv
uv venv
uv pip install -e ".[dev,docs,examples]"

# Install pre-commit hooks
uv run pre-commit install
```

### Running Tests

```bash
# All tests
uv run pytest

# With coverage
uv run pytest --cov=wfirma --cov-report=html

# Specific test file
uv run pytest tests/sync/test_client.py

# Parallel execution
uv run pytest -n auto
```

### Using Tox

```bash
# Run tests across all environments
uv run tox

# Run specific environment
uv run tox -e py312
uv run tox -e lint
uv run tox -e type
uv run tox -e docs
```

### Code Quality

```bash
# Format code
uv run ruff format src tests examples

# Lint and fix
uv run ruff check --fix src tests examples

# Type check
uv run mypy src
```

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### For Core Maintainers & AI Agents

Internal implementation documentation is in [`_aidocs/`](_aidocs/) directory. Start with [`_aidocs/README.md`](_aidocs/README.md).

### Quick Start for Contributors

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Write tests for your changes (TDD approach)
4. Implement your changes
5. Ensure all tests pass (`uv run pytest`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

This project follows **Test-Driven Development (TDD)** with comprehensive test coverage (>90%).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history.

## Support

- 📫 [Issue Tracker](https://github.com/yourusername/python-wfirma/issues)
- 📖 [Documentation](https://python-wfirma.readthedocs.io)
- 💬 [Discussions](https://github.com/yourusername/python-wfirma/discussions)

## Acknowledgments

- [wFirma API Documentation](https://doc.wfirma.pl/)
- Built with [httpx](https://www.python-httpx.org/), [Pydantic](https://docs.pydantic.dev/), and [anyio](https://anyio.readthedocs.io/)

---

**Note**: This library is not officially affiliated with wFirma. It is a community-maintained project.

