# Quick Start Guide

Welcome to **python-wfirma** - a Python library for the wFirma accounting API!

## 🚀 Getting Started

### Installation

```bash
pip install python-wfirma
```

Or with uv (faster):
```bash
uv pip install python-wfirma
```

### Basic Usage

```python
from wfirma import WFirmaClient

# Initialize client
client = WFirmaClient(
    app_key="your_app_key",
    secret="your_secret",
    environment="sandbox"
)

# List invoices
invoices = client.invoices.list(limit=10)
for invoice in invoices:
    print(f"Invoice {invoice.number}: {invoice.total}")
```

### Async Usage

```python
import asyncio
from wfirma import AsyncWFirmaClient

async def main():
    async with AsyncWFirmaClient(
        app_key="your_app_key",
        secret="your_secret"
    ) as client:
        invoices = await client.invoices.list(limit=10)
        async for invoice in invoices:
            print(f"Invoice {invoice.number}: {invoice.total}")

asyncio.run(main())
```

## 📚 Next Steps

- **Documentation**: [https://python-wfirma.readthedocs.io](https://python-wfirma.readthedocs.io)
- **Examples**: Check the `/examples` directory
- **API Reference**: Full documentation at [docs.wfirma.pl](https://doc.wfirma.pl/)

## 🤝 Contributing

Want to contribute? Great! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

---

**Note:** This library is currently in development (v0.1.0-dev). Check [CHANGELOG.md](CHANGELOG.md) for latest updates and [ROADMAP.md](ROADMAP.md) for planned features.

