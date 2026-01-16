# Integration Tests
Integration tests are planned for version 0.2.0 (see ROADMAP.md).

## Roadmap

```
    await async_client.invoices.delete(invoice.id)
    yield invoice
    invoice = await async_client.invoices.create(...)
async def test_invoice(async_client):
@pytest.fixture
```python

Use fixtures for reliable cleanup:

3. Clean up (delete created resources)
2. Perform operations
1. Create test data
Integration tests should clean up any data they create. Each test should:

## Test Data Cleanup

- They are **not run in CI** by default
- They may **modify data** in your sandbox account
- They require valid credentials
- They are **slower** than unit tests
- Integration tests make real API calls to wFirma sandbox

## Important Notes

```
pytest tests/integration/test_sandbox.py -m integration
# Run specific integration test

pytest -m ""
# Run all tests including integration

pytest -m integration
# Run only integration tests
```bash

To run integration tests:

Integration tests are marked with `@pytest.mark.integration` and are **skipped by default**.

## Running Integration Tests

   ```
   pip install -e ".[dev]"
   ```bash
2. Install test dependencies:

   ```
   WFIRMA_ENVIRONMENT=sandbox
   WFIRMA_SECRET=your_sandbox_secret
   WFIRMA_APP_KEY=your_sandbox_app_key
   ```bash
1. Create a `.env` file in the project root:

Integration tests are **optional** and require valid wFirma API credentials.

## Setup

This directory contains optional integration tests that run against the actual wFirma API sandbox.


