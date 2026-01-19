# Python wFirma API Library - Implementation Plan

**Project:** python-wfirma  
**Version:** 0.1.0  
**Python:** >=3.12  
**Methodology:** Test-Driven Development (TDD)  
**Date:** 2026-01-16

---

## Executive Summary

This document outlines the complete implementation plan for a professional Python library providing both synchronous and asynchronous access to the wFirma accounting API. The library follows TDD methodology with pure separation architecture, comprehensive test coverage, and strict quality standards.

---

## 1. Architecture Overview

### 1.1 Design Principles

- **Pure Separation**: Complete separation between sync and async code paths
- **Type Safety**: Gradual typing with mypy, strict for public API
- **Data Validation**: Pydantic models with pydantic-xml for unified XML/JSON handling
- **Test-Driven**: No implementation without failing tests first
- **Immutability**: Tests marked NOAI are protected from AI modifications

### 1.2 Project Structure

```
python-wfirma/
├── src/
│   └── wfirma/
│       ├── __init__.py              # Public API exports
│       ├── exceptions.py            # Exception hierarchy
│       ├── config.py                # Configuration management
│       ├── models/                  # Pydantic data models
│       │   ├── __init__.py
│       │   ├── base.py             # Base model classes
│       │   ├── invoice.py          # Invoice models
│       │   ├── contractor.py       # Contractor models
│       │   ├── good.py             # Goods models
│       │   ├── warehouse.py        # Warehouse document models
│       │   ├── payment.py          # Payment models
│       │   ├── employee.py         # Employee models
│       │   ├── company.py          # Company/settings models
│       │   └── common.py           # Shared types (Address, etc.)
│       ├── sync/                    # Synchronous implementation
│       │   ├── __init__.py
│       │   ├── auth.py             # OAuth authentication
│       │   ├── client.py           # Base HTTP client
│       │   └── resources/          # Resource endpoints
│       │       ├── __init__.py
│       │       ├── invoices.py
│       │       ├── contractors.py
│       │       ├── goods.py
│       │       ├── warehouse.py
│       │       ├── payments.py
│       │       ├── employees.py
│       │       └── company.py
│       └── async_/                  # Asynchronous implementation
│           ├── __init__.py
│           ├── auth.py
│           ├── client.py
│           └── resources/
│               ├── __init__.py
│               ├── invoices.py
│               ├── contractors.py
│               ├── goods.py
│               ├── warehouse.py
│               ├── payments.py
│               ├── employees.py
│               └── company.py
├── tests/
│   ├── conftest.py                  # Pytest configuration & fixtures
│   ├── test_config.py
│   ├── test_exceptions.py
│   ├── models/                      # Model validation tests
│   │   ├── test_invoice.py
│   │   ├── test_contractor.py
│   │   ├── test_good.py
│   │   ├── test_warehouse.py
│   │   ├── test_payment.py
│   │   ├── test_employee.py
│   │   └── test_company.py
│   ├── sync/                        # Sync implementation tests
│   │   ├── test_auth.py
│   │   ├── test_client.py
│   │   └── resources/
│   │       ├── test_invoices.py
│   │       ├── test_contractors.py
│   │       ├── test_goods.py
│   │       ├── test_warehouse.py
│   │       ├── test_payments.py
│   │       ├── test_employees.py
│   │       └── test_company.py
│   ├── async_/                      # Async implementation tests
│   │   ├── test_auth.py
│   │   ├── test_client.py
│   │   └── resources/
│   │       ├── test_invoices.py
│   │       ├── test_contractors.py
│   │       ├── test_goods.py
│   │       ├── test_warehouse.py
│   │       ├── test_payments.py
│   │       ├── test_employees.py
│   │       └── test_company.py
│   └── integration/                 # Optional integration tests (roadmap)
│       ├── README.md
│       └── test_sandbox.py
├── examples/
│   ├── basic_sync.py
│   ├── basic_async.py
│   ├── invoices_management.py
│   ├── contractors_management.py
│   ├── cli_tool/
│   │   ├── __main__.py
│   │   └── commands/
│   ├── flask_integration/
│   │   └── app.py
│   ├── fastapi_integration/
│   │   └── app.py
│   └── notebooks/
│       ├── 01_getting_started.ipynb
│       ├── 02_invoices.ipynb
│       └── 03_advanced_usage.ipynb
├── docs/
│   ├── conf.py                      # Sphinx configuration
│   ├── index.rst
│   ├── installation.rst
│   ├── authentication.rst
│   ├── quickstart.rst
│   ├── api_reference.md             # Scraped API documentation
│   ├── api/                         # Auto-generated API docs
│   ├── guides/
│   │   ├── invoices.rst
│   │   ├── contractors.rst
│   │   ├── error_handling.rst
│   │   └── async_usage.rst
│   └── troubleshooting.rst
├── .github/
│   └── workflows/
│       ├── ci.yml                   # CI/CD pipeline
│       └── docs.yml                 # Documentation deployment
├── _skills/                         # Optional AI skills (agentskills.io)
├── pyproject.toml
├── tox.ini
├── .pre-commit-config.yaml
├── .gitignore
├── README.md
├── LICENSE
├── CHANGELOG.md
├── CONTRIBUTING.md
├── NOAI_PROBLEMS_REPORT.md         # NOAI conflicts tracker
└── ROADMAP.md                       # Future enhancements
```

---

## 2. Dependencies

### 2.1 Core Dependencies

```toml
dependencies = [
    "httpx[http2]>=0.27.0",      # HTTP client (sync/async)
    "anyio>=4.0.0",               # Async abstraction layer
    "pydantic>=2.0.0",            # Data validation
    "pydantic-xml>=2.0.0",        # XML serialization/deserialization
    "python-dotenv>=1.0.0",       # Environment configuration
]
```

### 2.2 Development Dependencies

```toml
[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0",
    "respx>=0.21.0",              # HTTP mocking for httpx
    "tox>=4.0.0",
    "ruff>=0.2.0",                # Linting & formatting
    "mypy>=1.8.0",                # Type checking
    "pre-commit>=3.6.0",
]

docs = [
    "sphinx>=7.2.0",
    "sphinx-rtd-theme>=2.0.0",
    "sphinx-autodoc-typehints>=1.25.0",
    "myst-parser>=2.0.0",         # Markdown support in Sphinx
]

examples = [
    "click>=8.1.0",               # CLI tool
    "flask>=3.0.0",               # Flask example
    "fastapi>=0.109.0",           # FastAPI example
    "uvicorn>=0.27.0",            # ASGI server
    "jupyter>=1.0.0",             # Notebooks
    "ipython>=8.20.0",
]

scraping = [
    "beautifulsoup4>=4.12.0",     # Web scraping
    "lxml>=5.1.0",                # XML parser
    "requests>=2.31.0",           # HTTP for scraper
]
```

---

## 3. Exception Hierarchy

```
WFirmaException (base)
├── AuthenticationError
│   ├── InvalidCredentialsError
│   ├── TokenExpiredError
│   └── InsufficientPermissionsError
├── ValidationError
│   ├── InvalidFieldError
│   └── MissingRequiredFieldError
├── APIError
│   ├── RateLimitError
│   ├── ServerError
│   ├── BadRequestError
│   └── ServiceUnavailableError
├── ResourceError
│   ├── ResourceNotFoundError
│   ├── ResourceAlreadyExistsError
│   └── ResourceConflictError
├── NetworkError
│   ├── ConnectionError
│   └── TimeoutError
└── ConfigurationError
    ├── MissingConfigurationError
    └── InvalidConfigurationError
```

---

## 4. Implementation Phases

### Phase 0: Project Setup (Foundation)
**Goal:** Establish development environment and tooling

**Status:** ✅ **COMPLETED** (2026-01-16)

**Tasks:**
1. ✅ Configure `pyproject.toml` with all dependencies
2. ✅ Create folder structure
3. ✅ Setup `tox.ini` for multi-environment testing
4. ✅ Configure ruff (in `pyproject.toml`)
5. ✅ Configure mypy (in `pyproject.toml`)
6. ✅ Setup pre-commit hooks
7. ✅ Create `.gitignore`
8. ✅ Initialize `README.md` with project overview
9. ✅ Create `NOAI_PROBLEMS_REPORT.md` with template sections
10. ✅ Create `ROADMAP.md` with future enhancements
11. ✅ Setup uv for dependency management
12. ✅ Create basic test to verify setup

**Deliverables:**
- ✅ Working development environment
- ✅ Runnable test suite (2 tests passing)
- ✅ Linting and type checking configured
- ✅ All documentation files created

---

### Phase 1: API Documentation Scraping
**Goal:** Extract complete API specification from wFirma documentation

**Tasks:**
1. Create web scraper in `scripts/scrape_api_docs.py`
2. Extract all endpoints (paths, methods, parameters)
3. Extract authentication requirements
4. Extract request/response schemas
5. Extract error codes and meanings
6. Extract pagination patterns
7. Document findings in `docs/api_reference.md`
8. Create structured data file (`docs/api_spec.json`)

**Test Strategy:**
- Unit tests for scraper functions
- Validation of extracted data structure
- Comparison with manual documentation review

**Deliverables:**
- Complete API endpoint inventory
- Structured API specification
- Human-readable documentation

---

### Phase 2: Core Infrastructure (TDD)
**Goal:** Build exception hierarchy and configuration system

#### 2.1 Exception Classes

**Test File:** `tests/test_exceptions.py`

**Test Cases:**
- Test exception inheritance hierarchy
- Test exception message formatting
- Test exception attributes (status codes, error codes)
- Test exception serialization for logging

**Implementation:** `src/wfirma/exceptions.py`

#### 2.2 Configuration Management

**Test File:** `tests/test_config.py`

**Test Cases:**
- Load configuration from environment variables
- Load configuration from .env file
- Override defaults with explicit values
- Validate required configuration fields
- Test multi-environment support (sandbox/production)
- Test configuration serialization (excluding secrets)

**Implementation:** `src/wfirma/config.py`

**Tag Strategy:** Mark with `AICOMPLETE` when configuration supports all planned features

---

### Phase 3: Data Models (TDD)
**Goal:** Create Pydantic models for all API entities with pydantic-xml support

**Priority:** High (required by all other phases)

#### 3.1 Base Models

**Test File:** `tests/models/test_base.py`

**Test Cases:**
- Test base model XML/JSON serialization
- Test base model deserialization
- Test field validation
- Test optional vs required fields
- Test default values
- Test custom validators

**Implementation:** `src/wfirma/models/base.py`

#### 3.2 Common Models

**Test File:** `tests/models/test_common.py`

**Test Cases:**
- Address model validation
- Phone number validation
- Email validation
- Date/datetime handling
- Currency and decimal precision
- Tax rates (VAT types)

**Implementation:** `src/wfirma/models/common.py`

#### 3.3 Company Models

**Test File:** `tests/models/test_company.py`

**Test Cases:**
- Company information structure
- Company settings validation
- Multi-company support structures

**Implementation:** `src/wfirma/models/company.py`

#### 3.4 Contractor Models

**Test File:** `tests/models/test_contractor.py`

**Test Cases:**
- Contractor creation with required fields
- Contractor with optional fields
- Address handling (multiple addresses)
- Tax ID validation (NIP, REGON)
- Foreign contractor handling
- Contact information validation

**Implementation:** `src/wfirma/models/contractor.py`

#### 3.5 Good Models

**Test File:** `tests/models/test_good.py`

**Test Cases:**
- Product/service definitions
- Pricing structures
- Tax classification
- Unit of measure
- Inventory tracking fields

**Implementation:** `src/wfirma/models/good.py`

#### 3.6 Invoice Models

**Test File:** `tests/models/test_invoice.py`

**Test Cases:**
- Invoice header information
- Invoice line items
- Invoice totals calculation
- Different invoice types (standard, proforma, correction)
- Payment terms
- Invoice status transitions
- Tax calculations (gross/net)

**Implementation:** `src/wfirma/models/invoice.py`

#### 3.7 Payment Models

**Test File:** `tests/models/test_payment.py`

**Test Cases:**
- Payment creation
- Payment methods
- Payment status
- Multi-currency payments
- Partial payments

**Implementation:** `src/wfirma/models/payment.py`

#### 3.8 Warehouse Models

**Test File:** `tests/models/test_warehouse.py`

**Test Cases:**
- Warehouse document types
- Stock movements
- Document positions
- Warehouse locations

**Implementation:** `src/wfirma/models/warehouse.py`

#### 3.9 Employee Models

**Test File:** `tests/models/test_employee.py`

**Test Cases:**
- Employee information
- Permissions and roles
- Employment details

**Implementation:** `src/wfirma/models/employee.py`

**Tag Strategy:** Each model test marked `AICOMPLETE` after full validation coverage

---

### Phase 4: Authentication Layer (TDD)
**Goal:** Implement OAuth authentication for both sync and async

#### 4.1 Synchronous Authentication

**Test File:** `tests/sync/test_auth.py`

**Test Cases:**
- Initialize authenticator with credentials
- Authenticate and retrieve access token
- Store token securely
- Automatic token renewal on expiry
- Handle authentication failures
- Multi-company token management
- Token serialization/deserialization

**Implementation:** `src/wfirma/sync/auth.py`

**Mocking Strategy:** Use respx to mock OAuth endpoints

#### 4.2 Asynchronous Authentication

**Test File:** `tests/async_/test_auth.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/auth.py`

#### 4.3 OAuth Migration to Authlib (TDD)

**Goal:** Replace the in-house OAuth implementation with an Authlib-based one.

**Internal Spec:** `_aidocs/PHASE_4.3_OAUTH_MIGRATION_PLAN.md`

**Work Items:**
- Introduce Authlib adapters for OAuth2 and OAuth1 (PLAINTEXT)
- Integrate Authlib into sync and async auth helpers
- Wire Authlib-based auth into `WFirmaClient` authentication flow
- Replace legacy OAuth code paths and update docs

**Testing:**
- Add unit tests for token modeling and persistence adapters
- Add mocked integration tests (`respx`) for OAuth2 code exchange and refresh
- Add deterministic tests for OAuth1 PLAINTEXT Authorization header

**Quality Gates:**
- `tox -e lint,type` passes
- Full pytest suite passes

---

### Phase 5: Base HTTP Client (TDD)
**Goal:** Build foundation for API communication

#### 5.1 Synchronous Client

**Test File:** `tests/sync/test_client.py`

**Test Cases:**
- Initialize client with configuration
- Make GET request with authentication
- Make POST request with JSON body
- Make POST request with XML body
- Handle rate limiting (429 responses)
- Handle server errors (5xx)
- Handle network timeouts
- Retry logic with exponential backoff
- Request/response logging
- Custom headers handling
- Parse XML responses to models
- Parse JSON responses to models

**Implementation:** `src/wfirma/sync/client.py`

#### 5.2 Asynchronous Client

**Test File:** `tests/async_/test_client.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/client.py`

**Tag Strategy:** Mark `AICOMPLETE` when client handles all HTTP scenarios

---

### Phase 6: Company/Settings Resource (TDD)
**Goal:** Access company information (needed for context)

#### 6.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_company.py`

**Test Cases:**
- Get current company information
- List accessible companies
- Switch active company context
- Get company settings
- Update company settings

**Implementation:** `src/wfirma/sync/resources/company.py`

#### 6.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_company.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/company.py`

---

### Phase 7: Contractors Resource (TDD)
**Goal:** Manage business partners (required by invoices)

#### 7.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_contractors.py`

**Test Cases:**
- Create contractor with minimal data
- Create contractor with full data
- Get contractor by ID
- List contractors with pagination
- Filter contractors by various criteria
- Update contractor information
- Delete contractor
- Search contractors by name
- Search contractors by tax ID
- Handle duplicate tax ID error
- Validate address fields

**Implementation:** `src/wfirma/sync/resources/contractors.py`

#### 7.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_contractors.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/contractors.py`

**Tag Strategy:** Mark `AICOMPLETE` when all CRUD + search operations tested

---

### Phase 8: Goods Resource (TDD)
**Goal:** Manage products/services catalog (required by invoices)

#### 8.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_goods.py`

**Test Cases:**
- Create good/service
- Get good by ID
- List goods with pagination
- Filter by type (product/service)
- Update good information
- Update pricing
- Delete good
- Handle inventory-tracked goods
- Validate tax classification

**Implementation:** `src/wfirma/sync/resources/goods.py`

#### 8.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_goods.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/goods.py`

---

### Phase 9: Invoices Resource (TDD)
**Goal:** Core invoicing functionality (most complex)

#### 9.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_invoices.py`

**Test Cases:**
- Create simple invoice
- Create invoice with multiple line items
- Create invoice with discounts
- Create proforma invoice
- Convert proforma to final invoice
- Create corrective invoice
- Get invoice by ID
- Get invoice as PDF
- List invoices with pagination
- Filter by date range
- Filter by contractor
- Filter by status
- Update invoice (if in draft)
- Delete invoice (if in draft)
- Mark invoice as sent
- Send invoice via email
- Generate recurring invoice
- Calculate totals correctly
- Handle different tax rates
- Handle foreign currency invoices
- Validate payment terms

**Implementation:** `src/wfirma/sync/resources/invoices.py`

#### 9.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_invoices.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/invoices.py`

**Tag Strategy:** Most complex resource - multiple `AICOMPLETE` candidates for sub-features

---

### Phase 10: Payments Resource (TDD)
**Goal:** Track invoice payments

#### 10.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_payments.py`

**Test Cases:**
- Register payment for invoice
- Register partial payment
- List payments for invoice
- List all payments with pagination
- Update payment
- Delete payment
- Handle multi-currency payments
- Link payment to multiple invoices

**Implementation:** `src/wfirma/sync/resources/payments.py`

#### 10.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_payments.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/payments.py`

---

### Phase 11: Warehouse Resource (TDD)
**Goal:** Inventory management

#### 11.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_warehouse.py`

**Test Cases:**
- Create warehouse document
- Get document by ID
- List documents with pagination
- Filter by document type
- Document positions handling
- Stock level updates
- Warehouse transfers

**Implementation:** `src/wfirma/sync/resources/warehouse.py`

#### 11.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_warehouse.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/warehouse.py`

---

### Phase 12: Employees Resource (TDD)
**Goal:** User management (less commonly used)

#### 12.1 Synchronous Implementation

**Test File:** `tests/sync/resources/test_employees.py`

**Test Cases:**
- Get employee information
- List employees
- Update employee permissions
- Employee role management

**Implementation:** `src/wfirma/sync/resources/employees.py`

#### 12.2 Asynchronous Implementation

**Test File:** `tests/async_/resources/test_employees.py`

**Test Cases:** (Same as sync)

**Implementation:** `src/wfirma/async_/resources/employees.py`

---

### Phase 13: Public API & Convenience Features
**Goal:** User-facing API and developer experience

**Tasks:**
1. Design main client class exposing all resources
2. Implement context manager support
3. Add pagination helpers (iterators)
4. Add bulk operation utilities
5. Create comprehensive examples
6. Write API documentation strings
7. Setup `__init__.py` exports

**Test Files:**
- `tests/test_main_client.py`
- `tests/test_pagination.py`
- `tests/test_bulk_operations.py`

**Deliverables:**
- Clean, intuitive public API
- Working examples for all major use cases

---

### Phase 14: Documentation (Sphinx)
**Goal:** Professional documentation website

**Tasks:**
1. Configure Sphinx in `docs/conf.py`
2. Write installation guide
3. Write authentication setup guide
4. Write quickstart tutorial
5. Write resource-specific guides
6. Generate API reference from docstrings
7. Write error handling guide
8. Write async usage guide
9. Write troubleshooting guide
10. Add code examples throughout
11. Setup documentation builds in CI

**Deliverables:**
- Comprehensive documentation
- Deployed to ReadTheDocs or GitHub Pages

---

### Phase 15: Examples & Integrations
**Goal:** Demonstrate real-world usage

#### 15.1 CLI Tool

**Location:** `examples/cli_tool/`

**Features:**
- List invoices
- Create invoice from JSON/YAML
- Export invoice as PDF
- Search contractors
- Check payment status

**Tests:** Integration-style tests in `tests/examples/test_cli.py`

#### 15.2 Flask Integration

**Location:** `examples/flask_integration/`

**Features:**
- REST API wrapper around wFirma
- Invoice creation endpoint
- Contractor management
- Webhook handling (if supported by wFirma)

#### 15.3 FastAPI Integration

**Location:** `examples/fastapi_integration/`

**Features:**
- Async REST API
- OpenAPI documentation
- Background tasks for long operations

#### 15.4 Jupyter Notebooks

**Location:** `examples/notebooks/`

**Notebooks:**
1. Getting Started
2. Invoice Management Workflow
3. Advanced Queries and Reporting

---

### Phase 16: CI/CD Pipeline
**Goal:** Automated quality assurance

#### 16.1 GitHub Actions Workflows

**File:** `.github/workflows/ci.yml`

**Jobs:**
- Lint (ruff)
- Type check (mypy)
- Test (pytest across Python 3.12, 3.13)
- Coverage report (pytest-cov, upload to Codecov)
- Build package
- Test package installation

**File:** `.github/workflows/docs.yml`

**Jobs:**
- Build Sphinx documentation
- Deploy to GitHub Pages

#### 16.2 Pre-commit Hooks

**File:** `.pre-commit-config.yaml`

**Hooks:**
- ruff format
- ruff check
- mypy
- trailing whitespace removal
- YAML validation

#### 16.3 Tox Configuration

**File:** `tox.ini`

**Environments:**
- py312, py313
- lint
- type
- docs
- examples

---

## 5. NOAI Protection System

### 5.1 NOAI Tag Usage

Tests reach their final form when:
1. All test cases for a feature are implemented
2. Feature implementation is complete and passing
3. Edge cases are covered
4. User has verified correctness

**Process:**
1. AI marks test with `AICOMPLETE` tag in comment
2. User reviews and decides whether to promote to `NOAI`
3. Once `NOAI`, test is immutable to AI

**Example:**
```python
# NOAI: Contractor creation with full validation - verified 2026-01-16
def test_create_contractor_full():
    ...
```

### 5.2 NOAI Problems Report

**File:** `NOAI_PROBLEMS_REPORT.md`

**Template Sections:**
- Authentication Issues
- Client Communication Issues
- Model Validation Issues
- Resource Operations Issues (per resource)
- Integration Issues
- Configuration Issues

**Entry Format:**
```markdown
### [YYYY-MM-DD HH:MM] Issue in test_file.py::test_name

**Problem:** Brief description
**Test Tagged NOAI:** Yes/No
**Attempted Change:** What AI tried to do
**Reason Blocked:** Why NOAI prevented it
**Recommendation:** Suggested fix for human
**Priority:** Low/Medium/High/Critical
```

---

## 6. Development Workflow

### 6.1 TDD Cycle (per feature)

1. **Write Test(s):** Create failing test(s) for new feature
2. **Run Test:** Verify test fails (`pytest -k test_name`)
3. **Implement:** Write minimal code to pass test
4. **Run Test:** Verify test passes
5. **Refactor:** Improve code quality without breaking test
6. **Repeat:** Continue until feature complete
7. **Tag AICOMPLETE:** When feature fully implemented
8. **User Review:** Human verifies correctness
9. **Tag NOAI:** If approved, protect test

### 6.2 Quality Gates

Before marking `AICOMPLETE`:
- ✅ All test cases pass
- ✅ Code coverage ≥ 90% for module
- ✅ No mypy errors (gradual typing applied)
- ✅ No ruff violations
- ✅ Docstrings present for public API
- ✅ Examples work correctly

### 6.3 Terminal Command Fallback

If terminal hangs or is unresponsive:
```bash
command > /tmp/wfirma_output.txt 2>&1
# Then read /tmp/wfirma_output.txt with read_file tool
```

---

## 7. Roadmap (Future Enhancements)

### 7.1 Version 0.2.0
- Integration tests against wFirma sandbox (Phase 3.C implementation)
- Response caching layer
- Bulk operations optimization
- Webhook support (if available in API)

### 7.2 Version 0.3.0
- Rate limiting intelligence (adaptive backoff)
- Request/response middleware system
- Plugin architecture for extensions
- GraphQL-style query building (if beneficial)

### 7.3 Version 1.0.0
- API versioning support (if wFirma introduces versions)
- Comprehensive performance benchmarks
- Production stability guarantees
- Long-term support commitment

---

## 8. Success Criteria

### 8.1 Functional Requirements
- ✅ All documented endpoints accessible
- ✅ Both sync and async fully functional
- ✅ XML and JSON handling via pydantic/pydantic-xml
- ✅ Comprehensive error handling
- ✅ OAuth authentication working

### 8.2 Quality Requirements
- ✅ Test coverage ≥ 90%
- ✅ All NOAI tests passing
- ✅ Zero critical security vulnerabilities
- ✅ Type hints for all public API
- ✅ Complete API documentation

### 8.3 Usability Requirements
- ✅ Clear quickstart (< 5 minutes to first API call)
- ✅ Working examples for each resource
- ✅ Helpful error messages
- ✅ Intuitive API design

---

## 9. Risk Management

### 9.1 Identified Risks

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| API documentation incomplete | Medium | High | Web scraping + manual review |
| API changes without notice | Low | High | Version pinning, integration tests |
| Rate limiting too restrictive | Medium | Medium | Adaptive backoff, caching |
| XML parsing edge cases | Medium | Medium | Extensive test coverage |
| Pydantic-xml compatibility issues | Low | Medium | Early prototype, fallback plan |

### 9.2 Contingency Plans

- **If scraping fails:** Manual documentation, community input
- **If pydantic-xml insufficient:** Custom XML serializers
- **If API undocumented features needed:** Reverse engineering, wFirma support

---

## 10. Timeline Estimation

**Note:** Actual timeline depends on API complexity discovered during scraping

| Phase | Estimated Effort | Dependencies |
|-------|-----------------|--------------|
| Phase 0: Setup | 2 hours | None |
| Phase 1: Scraping | 4 hours | Phase 0 |
| Phase 2: Infrastructure | 4 hours | Phase 0 |
| Phase 3: Models | 16 hours | Phase 1, 2 |
| Phase 4: Auth | 6 hours | Phase 2, 3 |
| Phase 5: Client | 8 hours | Phase 3, 4 |
| Phase 6: Company | 4 hours | Phase 5 |
| Phase 7: Contractors | 6 hours | Phase 5, 6 |
| Phase 8: Goods | 6 hours | Phase 5, 6 |
| Phase 9: Invoices | 12 hours | Phase 7, 8 |
| Phase 10: Payments | 6 hours | Phase 9 |
| Phase 11: Warehouse | 6 hours | Phase 8 |
| Phase 12: Employees | 4 hours | Phase 6 |
| Phase 13: Public API | 6 hours | All above |
| Phase 14: Documentation | 8 hours | Phase 13 |
| Phase 15: Examples | 10 hours | Phase 13 |
| Phase 16: CI/CD | 4 hours | Phase 0 |

**Total Estimated Effort:** ~112 hours

---

## 11. Next Steps

1. ✅ User approval of this plan
2. → Execute Phase 0: Project Setup
3. → Execute Phase 1: API Documentation Scraping
4. → Begin TDD cycles starting with Phase 2

---

## Appendix A: Coding Standards

### A.1 Python Style
- Follow PEP 8 (enforced by ruff)
- Maximum line length: 100 characters
- Use type hints (gradual typing)
- Docstring format: Google style

### A.2 Naming Conventions
- Classes: PascalCase
- Functions/methods: snake_case
- Constants: UPPER_SNAKE_CASE
- Private members: _leading_underscore

### A.3 Import Organization
```python
# Standard library
import os
from typing import Optional

# Third-party
import httpx
from pydantic import BaseModel

# Local
from wfirma.exceptions import WFirmaException
from wfirma.models import Invoice
```

### A.4 Test Naming
```python
def test_<feature>_<scenario>_<expected_outcome>():
    """
    Test that <feature> <does something> when <scenario>.
    """
```

---

## Appendix B: Configuration Template

```python
# .env.example
WFIRMA_APP_KEY=your_app_key_here
WFIRMA_SECRET=your_secret_here
WFIRMA_ENVIRONMENT=sandbox  # or production
WFIRMA_TIMEOUT=30
WFIRMA_MAX_RETRIES=3
```

---

**Plan Version:** 1.0  
**Last Updated:** 2026-01-16  
**Status:** AWAITING APPROVAL

