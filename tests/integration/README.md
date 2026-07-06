# Integration Tests

This directory contains optional live tests against the public wFirma docs and the production API.

## Scope for `1.0.0`

The release candidate claims live coverage for:

- public Postman collection availability via `WFirmaAPIScraper`
- API Key sync client reading company details from production
- API Key async client reading company details from production
- OAuth2 sync client reading company details from production
- OAuth2 async client reading company details from production

The suite is intentionally read-only. It does not create, edit, or delete production data.

## How to Run

Integration tests are marked with `@pytest.mark.integration` and are skipped by default.

Run the full live suite:

```bash
pytest -m integration
```

Or opt in with an environment flag:

```bash
WFIRMA_RUN_INTEGRATION=1 pytest
```

Run a specific file:

```bash
pytest tests/integration/test_live_readonly_smoke.py -m integration
```

## Required Environment Variables

### API Key smoke tests

```bash
WFIRMA_APP_KEY=your_app_key
WFIRMA_ACCESS_KEY=your_access_key
WFIRMA_SECRET_KEY=your_secret_key
WFIRMA_COMPANY_ID=123456
```

### OAuth2 smoke tests

```bash
WFIRMA_OAUTH2_CLIENT_ID=your_client_id
WFIRMA_OAUTH2_CLIENT_SECRET=your_client_secret
WFIRMA_OAUTH2_REDIRECT_URI=https://your.app/callback
WFIRMA_OAUTH2_ACCESS_TOKEN=your_access_token
```

OAuth2 smoke tests assume the provided bearer token is already valid for the target production company.

## Notes

- These tests are not run in CI by default.
- They make real network calls.
- They are release-gating evidence, not unit tests.
- If a required variable is missing, the corresponding test skips instead of failing noisily.
