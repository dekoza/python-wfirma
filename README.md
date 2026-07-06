# python-wfirma

Python client for the [wFirma](https://wfirma.pl/) accounting API. Supports both synchronous and asynchronous usage.

> **Status**: Stable (`1.0.0`). `WFirmaClient` supports API Key, OAuth 2.0, and OAuth 1.0a in this release.

## Installation

```bash
pip install python-wfirma
```

Or with [uv](https://github.com/astral-sh/uv):

```bash
uv add python-wfirma
```

## Usage

### Safe Read-Only Start

```python
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient

auth = APIKeyAuth(
    access_key="your_access_key",
    secret_key="your_secret_key",
    app_key="your_app_key",
)

with WFirmaClient(auth=auth, company_id=123) as client:
    company = client.company.get()
    terms = client.terms.find()

print(company.name)
print(len(terms))
```

### CLI Read-Only Verification

```bash
wfirma company show
wfirma tags list
wfirma terms list
wfirma warehouses list
```

### Write Operations

These examples mutate real production data. Do not run them casually.

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

The library has two different environment-driven helpers:

- `APIKeyAuth.from_env()` reads API key credentials for `WFirmaClient`
- `get_config()` / `WFirmaConfig.from_env()` read shared application settings

API key authentication from environment:

```bash
# .env
WFIRMA_APP_KEY=your_app_key
WFIRMA_ACCESS_KEY=your_access_key
WFIRMA_SECRET_KEY=your_secret_key
WFIRMA_ENVIRONMENT=production
WFIRMA_COMPANY_ID=123
```

```python
from wfirma.sync.auth import APIKeyAuth

auth = APIKeyAuth.from_env()
```

Shared configuration helper:

```bash
# .env
WFIRMA_APP_KEY=your_app_key
WFIRMA_APP_SECRET=your_app_secret
WFIRMA_ENVIRONMENT=production
WFIRMA_COMPANY_ID=123
```

```python
from wfirma import get_config

config = get_config()
print(config.base_url)  # https://api2.wfirma.pl
```

Custom API base URL override (useful for local simulators):

```bash
# .env
WFIRMA_BASE_URL=http://localhost:18088
```

```python
from wfirma.sync.auth import APIKeyAuth
from wfirma.sync.client import WFirmaClient


auth = APIKeyAuth(
    access_key="your_access_key",
    secret_key="your_secret_key",
    app_key="your_app_key",
)

with WFirmaClient(
    auth=auth,
    company_id=123,
    base_url="http://localhost:18088",
) as client:
    company = client.company.get()
```

## Choosing Auth Mode

- `APIKeyAuth`: best for service integrations and manual CLI verification
- `OAuth2Auth`: best when you need upstream read/write scope control and user authorization flows
- `OAuth1Auth`: supported for upstream compatibility, but use it only when the target workflow requires it

## Handling API Errors

```python
from wfirma.exceptions import APIError

try:
    with WFirmaClient(auth=auth, company_id=123) as client:
        company = client.company.get()
except APIError as exc:
    print(exc.to_dict())
```

## Production Use Checklist

- use least-privilege credentials
- prefer read-only verification first (`company`, `tags`, `terms`, `warehouses`)
- treat write examples as production mutations
- run the CLI after install, not only from the repository checkout
- follow `RELEASING.md` before tagging or publishing

## Stability Policy

- `1.0rc1` started the API freeze, and `1.0.0` ships within that contract
- the freeze covers import paths, auth constructors, exception semantics, client defaults, and CLI command names and flags

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
uv run pytest -m integration                      # opt-in live integration tests
```

## CLI

The package now ships a small read-only CLI for manual API verification.

Required environment variables:

```bash
export WFIRMA_APP_KEY='...'
export WFIRMA_ACCESS_KEY='...'
export WFIRMA_SECRET_KEY='...'
export WFIRMA_COMPANY_ID='123'
```

Examples:

```bash
wfirma company show
wfirma company show --json
wfirma tags list
wfirma terms list
wfirma term-groups list --json
wfirma warehouses list
wfirma vat-codes list
```

Default list output uses `ID` and `Label`. `company show` uses `ID` and `Name`.

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
