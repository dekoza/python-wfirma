# Roadmap

Current version: **0.1.0** (in development).
Last updated: 2026-02-20.

## 0.1.0 — Current

Core library with sync/async clients covering all major wFirma API resources.

**Done:**
- Project setup (pyproject.toml, uv, ruff, mypy, pytest, pre-commit, CI)
- Configuration management with environment variable support
- Exception hierarchy mapped to wFirma API status codes
- API Key authentication (sync & async)
- OAuth 1.0a and OAuth 2.0 authentication (sync & async)
- HTTP client (sync & async) with JSON/XML support
- 40+ resource implementations (invoices, contractors, goods, payments, warehouse documents, etc.)

**In progress:**
- Pagination helpers
- Usage examples
- Sphinx documentation

## 0.2.0 — Integration & hardening

- Integration tests against wFirma sandbox
- Automatic retry with exponential backoff
- Response caching (pluggable backends)
- Bulk operations (batch create/update/delete)
- Webhook signature verification utilities

## 0.3.0 — Developer experience

- Query builder for filtering/sorting
- Request/response middleware (logging, timing)
- Rate limiting coordination

## 1.0.0 — Stable release

- Stable public API with semver guarantees
- Production hardening (connection pool tuning, load testing)
- Comprehensive documentation and migration guide from 0.x

