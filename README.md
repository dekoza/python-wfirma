# python-wfirma

Python client for the [wFirma](https://wfirma.pl/) accounting API. Supports both synchronous and asynchronous usage.

> **Status**: Alpha (v0.1.0). The API surface may change before 1.0.

## Installation

```bash
pip install python-wfirma
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add python-wfirma
```

## Usage

### API Key Authentication

```python
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient

auth = APIKeyAuth(
    access_key="your_access_key",
    secret_key="your_secret_key",
    app_key="your_app_key",
)

with WFirmaClient(auth=auth, company_id=123) as client:
    contractor = client.contractors.add(name="ACME Sp. z o.o.", nip="1234567890")

    invoice = client.invoices.add(
        invoice={
            "contractor_id": contractor.id,
            "type": "normal",
            "paid": "0",
        }
    )

    invoices = client.invoices.find()
```

### Async

```python
import asyncio
from wfirma.async_.auth import APIKeyAuth
from wfirma.async_.client import WFirmaClient


async def main() -> None:
    auth = APIKeyAuth(
        access_key="your_access_key",
        secret_key="your_secret_key",
        app_key="your_app_key",
    )

    async with WFirmaClient(auth=auth, company_id=123) as client:
        contractor = await client.contractors.add(
            name="ACME Sp. z o.o.", nip="1234567890"
        )
        invoices = await client.invoices.find()


asyncio.run(main())
```

### OAuth 2.0

```python
from wfirma.sync.auth import OAuth2Auth
from wfirma.sync.client import WFirmaClient
from wfirma.config import Environment

oauth = OAuth2Auth(
    client_id="your_client_id",
    client_secret="your_client_secret",
    redirect_uri="https://yourapp.example.com/callback",
    environment=Environment.PRODUCTION,
)

# Step 1: redirect user to authorization URL
url = oauth.build_authorization_url(scope="invoices-read")

# Step 2: exchange the code from callback
token = oauth.exchange_code(code="authorization_code_from_callback")

# Step 3: use the client
with WFirmaClient(auth=oauth, company_id=123) as client:
    invoices = client.invoices.find()
```

## Configuration

The library reads credentials from environment variables when using `from_env()` class methods:

```bash
# .env
WFIRMA_APP_KEY=your_app_key
WFIRMA_APP_SECRET=your_app_secret
WFIRMA_ENVIRONMENT=sandbox  # or production
WFIRMA_COMPANY_ID=123
```

```python
from wfirma import get_config

config = get_config()
print(config.base_url)  # https://sandbox-api2.wfirma.pl
```

## Supported Resources

The client exposes the following wFirma API resources. Each resource provides methods matching the upstream API (typically `add`, `find`, `get`, `edit`, `delete`):

**Core**: invoices, contractors, goods, payments, expenses, documents

**Company**: company, company_accounts, company_packs

**Declarations**: declaration_countries, declaration_body_jpkvat, declaration_body_pit

**Warehouse**: warehouses, warehouse documents (PW, PZ, R, RW, WZ, ZD, ZPD, ZPM)

**Reference data**: tags, series, terms, term_groups, vat_codes, translation_languages, taxregisters, interests, ledger_accountant_years, ledger_operation_schemas

**Users & misc**: users, user_companies, vehicles, vehicle_run_rates, payment_cashboxes, invoice_deliveries, invoice_descriptions, notes, webhooks

## Development

Requires Python 3.12+. The project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
git clone https://github.com/dekoza/python-wfirma.git
cd python-wfirma
uv venv && uv sync --extra dev
uv run pre-commit install
```

### Tests

```bash
uv run pytest                                     # all tests
uv run pytest --cov=wfirma --cov-report=html      # with coverage
uv run pytest -n auto                             # parallel
```

### Linting & type-checking

```bash
uv run ruff format src tests
uv run ruff check --fix src tests
uv run mypy src
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).

---

This library is not affiliated with wFirma. It is an independent project.
Built on [httpx](https://www.python-httpx.org/), [Pydantic](https://docs.pydantic.dev/), and [authlib](https://docs.authlib.org/).

