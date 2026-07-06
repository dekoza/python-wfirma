# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

Work toward `1.0.0`.

## [1.0rc3] - 2026-07-07

### Added
- KSeF read fields on invoice models
- `price_type` support for invoices
- Filtered `find` for invoices

### Changed
- Version metadata now targets `1.0rc3`

## [1.0rc2] - 2026-05-04

### Added
- Explicit `base_url` overrides for `WFirmaConfig`, `get_config()`, and the sync/async `WFirmaClient`
- `WFIRMA_BASE_URL` environment variable support for local simulators and custom API endpoints
- Stable `1.0.0` go/no-go checklist in `RELEASING.md`

### Changed
- Version metadata now targets `1.0rc2`
- README, troubleshooting, authentication, and integration docs now describe the current release candidate
- Roadmap now records `1.0rc2` as the latest shipped release candidate before `1.0.0`

## [1.0rc1] - 2026-03-23

### Added
- Migration guide covering beta-to-RC changes and the public freeze scope
- Release candidate documentation for the frozen public API surface

### Changed
- Version metadata now targets `1.0rc1`
- README and authentication docs now describe the release candidate contract
- Roadmap now targets `1.0.0` as the next milestone after the RC cut

### Fixed
- Release checklist now verifies the installed CLI via `python -m wfirma.cli --help`
- CLI company display now falls back to alternate company name fields when needed
- CLI environment parsing now reports invalid `WFIRMA_COMPANY_ID` values clearly
- OAuth2 auth helpers and HTTP clients now have stronger coverage for error-wrapping edge cases

## [1.0b2] - 2026-03-23

### Added
- Packaged `wfirma` CLI for read-only API inspection
- Formal release checklist and blocker policy in `RELEASING.md`

### Changed
- README now prioritizes safe read-only production usage before mutating examples
- Roadmap now targets `1.0b2` hardening instead of the already-shipped beta
- Contributor docs now point to the release workflow
- Version metadata now targets `1.0b2`

## [1.0b1] - 2026-03-23

### Added
- Project setup: pyproject.toml with hatchling, uv for dependency management
- Development tooling: ruff, mypy, pytest, pre-commit
- OAuth 2.0 authentication (sync and async) via authlib
- API key authentication (sync and async)
- Base HTTP client built on httpx (sync and async variants)
- Configuration management with environment variable and .env file support
- Pydantic models with pydantic-xml for XML request/response handling
- Resource implementations for 40+ wFirma API endpoints (invoices, contractors, goods, payments, warehouse documents, etc.)
- Test suite with respx-based HTTP mocking
- Packaged `WFirmaAPIScraper` utility under `wfirma.tools`

### Changed
- Version metadata now targets `1.0b1`
- Development status is now beta instead of alpha

### Fixed
- Sync and async clients now default to the documented production API base URL
- `WFirmaClient` now supports `OAuth1Auth` as a first-class auth mode
- HTTP and XML error handling is hardened for non-JSON and binary responses

[Unreleased]: https://github.com/dekoza/python-wfirma/compare/v1.0rc3...HEAD
[1.0rc3]: https://github.com/dekoza/python-wfirma/releases/tag/v1.0rc3
[1.0rc2]: https://github.com/dekoza/python-wfirma/releases/tag/v1.0rc2
[1.0rc1]: https://github.com/dekoza/python-wfirma/releases/tag/v1.0rc1
[1.0b2]: https://github.com/dekoza/python-wfirma/releases/tag/v1.0b2
[1.0b1]: https://github.com/dekoza/python-wfirma/releases/tag/v1.0b1
