# Roadmap

Current target version: **1.0.0**.
Last updated: 2026-05-04.

## 1.0b1 — Released

Released beta for the supported client surface.

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

## 1.0b2 — Released

Hardening release focused on process, docs, and manual verification.

**Done:**
- Added a formal release checklist and blocker policy
- Documented manual live read-only verification with the packaged CLI
- Rewrote docs around safe production-first usage
- Broadened packaging and compatibility validation

## 1.0rc1 — Released

Release candidate that freezes the public API for `1.0.0`.

**Done:**
- Froze the public API surface for `1.0.0`
- Added migration guidance for post-beta users
- Tightened release verification wording around installed CLI checks
- Expanded targeted coverage for CLI env parsing and auth/client edge cases

## 1.0rc2 — Released

Second release candidate focused on blocker-class fixes and stable-release evidence.

**Done:**
- Added an explicit `base_url` override for config helpers and sync/async clients
- Documented `WFIRMA_BASE_URL` for local simulators and custom API endpoints
- Added a stable `1.0.0` go/no-go checklist in `RELEASING.md`
- Refreshed release metadata and RC docs for `1.0rc2`

## 1.0.0 — Stable release

- Publish only after RC validation is clean
- Stable public API with semver guarantees
- Comprehensive documentation and migration guidance for post-beta users
