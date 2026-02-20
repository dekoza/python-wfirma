# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/dekoza/python-wfirma/compare/main...HEAD

