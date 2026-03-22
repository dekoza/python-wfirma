# Roadmap

Current target version: **1.0b1**.
Last updated: 2026-03-22.

## 1.0b1 — Current beta target

Honest beta for the supported client surface.

**Done:**
- Project setup (pyproject.toml, uv, ruff, mypy, pytest, pre-commit, CI)
- Configuration management with environment variable support
- Exception hierarchy mapped to wFirma API status codes
- API Key authentication (sync & async)
- OAuth 2.0 authentication (sync & async)
- OAuth 1.0a authentication (sync & async, including `WFirmaClient`)
- HTTP client (sync & async) with JSON/XML support
- 40+ resource implementations (invoices, contractors, goods, payments, warehouse documents, etc.)
- Production-aligned client defaults and hardened HTTP error handling

## 1.0b2 — Beta hardening

- Optional live read-only production checks with least-privilege credentials
- Broader packaging and compatibility validation

## 1.0rc1 — Release candidate

- Freeze the public API for `1.0.0`
- Finish documentation, examples, and release notes
- Re-run packaging and compatibility validation

## 1.0.0 — Stable release

- Publish only after RC validation is clean
- Stable public API with semver guarantees
- Comprehensive documentation and migration guidance for post-beta users
