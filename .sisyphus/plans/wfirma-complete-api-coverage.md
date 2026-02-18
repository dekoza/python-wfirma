# Complete wFirma API Coverage

## TL;DR

> **Quick Summary**: Implement all 33 missing resource endpoint groups from the wFirma API specification, plus add missing endpoints to the existing Invoices resource (download, send, fiscalize, unfiscalize). This includes prerequisite infrastructure (PATCH method, binary response support), Pydantic models for new entities, sync + async resource classes, client properties, and comprehensive tests.
> 
> **Deliverables**:
> - 3 infrastructure changes (PATCH method, binary download support, XML POST support)
> - ~20 new Pydantic models
> - 33 new sync resource classes + 33 async mirrors
> - 66 client properties (33 sync + 33 async)
> - 4 new endpoints on existing InvoicesResource
> - ~200+ new test files
> - All existing tests still passing, >90% coverage maintained
> 
> **Estimated Effort**: XL
> **Parallel Execution**: YES - 6 waves
> **Critical Path**: Task 1 (PATCH) → Task 34 (webhooks) | Task 2 (binary) → Task 35 (downloads)

---

## Context

### Original Request
Complete the python-wfirma library's API coverage by implementing all missing resource endpoints from the wFirma API specification at https://doc.wfirma.pl/. The scraped API reference at `docs/api_reference.md` is the source of truth.

### Interview Summary
**Key Discussions**:
- Project follows TDD with >90% coverage, both sync and async implementations required
- Existing 7 resources (Company, Contractors, Goods, Invoices, Payments, WarehouseDocumentPW, Tags) establish the implementation pattern
- All remaining ~33 resource groups from `docs/api_reference.md` need implementation

**Research Findings**:
- API spec contains path typos: `notes/edit` shows as `/goods/notes/{id}`, `series/edit` as `/series/notes/ID`, `tags/edit` as `/tags/notes/{id}`, `term_groups/edit` as `/term_groups/notes/{id}`, `terms/edit` as `/terms/notes/{id}` — all should use `/edit/` pattern (confirmed by working Tags implementation)
- `vehicles/delete` uses GET method (not DELETE) per API spec
- `webhooks/edit` uses PATCH method — client currently lacks `patch()`/`patch_json()`
- `invoices/download` and `documents/download` return binary (PDF) data — client `_handle_response()` only handles JSON/text
- `user_companies` endpoints don't include `company_id` parameter — user-scoped not company-scoped
- `series/del` uses `/del/` path segment, not `/delete/`
- `ledger_accountant_years/get` has hardcoded ID `625` in spec — should be parameterized
- Payload wrapping varies: some use list-wrapped `{"resource": [{"object": data}]}`, others use direct `{"object": data}`

### Metis Review
**Identified Gaps** (addressed):
- PATCH method blocker for webhooks → Added as prerequisite Task 1
- Binary download support blocker → Added as prerequisite Task 2
- Payload wrapping inconsistency → Each task instructs executor to check `docs/api_spec.json`
- API spec typos → Documented correct paths in each affected task
- `user_companies` URL exception → Documented in Task 25
- Model-vs-dict decision → Guardrail: use raw dict for ≤3 simple fields, model otherwise
- No abstract base classes → Guardrail: standalone classes only

---

## Work Objectives

### Core Objective
Achieve 100% API endpoint coverage for the wFirma API by implementing all resource groups listed in `docs/api_reference.md`.

### Concrete Deliverables
- All 33 missing resource endpoint groups implemented (sync + async)
- Missing Invoice endpoints (download, send, fiscalize, unfiscalize) added
- New Pydantic models for entities with typed fields
- Full test coverage for every new resource
- Client properties for every new resource on both sync and async clients

### Definition of Done
- [ ] `uv run pytest` → ALL tests pass (0 failures)
- [ ] `uv run pytest --cov=wfirma --cov-report=term-missing` → >90% coverage
- [ ] `uv run ruff check src tests` → 0 lint errors
- [ ] `uv run mypy src` → 0 type errors
- [ ] Every resource group from `docs/api_reference.md` has a corresponding resource class
- [ ] Every resource is accessible via `client.{resource_name}` property

### Must Have
- Both sync and async implementations for every resource
- Tests for every resource method (get, find, add, edit, delete as applicable)
- Tests for client property registration
- Pydantic models where response has ≥3 typed fields
- Correct endpoint paths (fixing known spec typos)

### Must NOT Have (Guardrails)
- **No abstract base classes or mixins** — each resource is a standalone class following existing pattern
- **No modifications to existing 7 resources** (Company, Contractors, Goods, Invoices, Payments, WarehouseDocumentPW, Tags) except adding download/send/fiscalize/unfiscalize to Invoices
- **No retry logic, pagination helpers, or rate limiting** — out of scope
- **No custom validators on Pydantic models** — existing models use simple field definitions
- **No stubs for unsupported operations** — read-only resources only get `find()`/`get()` methods
- **No `__all__` changes to resource `__init__.py`** — add imports + exports following existing pattern
- **No refactoring of `_payloads.py`** — use existing helpers as-is
- **No inline imports except in client.py properties** — circular dependency workaround only for client

---

## Verification Strategy (MANDATORY)

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: YES
- **Automated tests**: YES (TDD — tests first, then implementation)
- **Framework**: pytest (via `uv run pytest`)
- **TDD workflow**: RED (failing test) → GREEN (minimal impl) → REFACTOR

### QA Policy
Every task MUST include agent-executed QA scenarios.
Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

| Deliverable Type | Verification Tool | Method |
|------------------|-------------------|--------|
| Resource methods | Bash (uv run pytest) | Run specific test file, assert all pass |
| Client properties | Bash (uv run pytest) | Run client property tests |
| Import correctness | Bash (python -c) | Import and verify no errors |
| Lint/type check | Bash (uv run ruff/mypy) | Run linters, zero errors |

---

## Execution Strategy

### Parallel Execution Waves

```
Wave 1 (Prerequisites — must complete first):
├── Task 1: Add PATCH method to sync+async clients [quick]
├── Task 2: Add binary response support to sync+async clients [quick]
└── Task 3: Add missing Invoice endpoints (download, send, fiscalize, unfiscalize) [unspecified-high]

Wave 2 (Read-only resources — no new models needed, MAX PARALLEL):
├── Task 4: company_accounts (find, get) [quick]
├── Task 5: company_packs (get) [quick]
├── Task 6: declaration_countries (find, get) [quick]
├── Task 7: expenses (find, get) [quick]
├── Task 8: interests (find) [quick]
├── Task 9: invoice_descriptions (find, get) [quick]
├── Task 10: ledger_accountant_years (find, get) [quick]
├── Task 11: ledger_operation_schemas (find, get) [quick]
├── Task 12: payment_cashboxes (find, get) [quick]
├── Task 13: translation_languages (find, get) [quick]
├── Task 14: user_companies (find, get) [quick]
├── Task 15: users (get) [quick]
├── Task 16: vat_codes (find, get) [quick]
├── Task 17: vehicle_run_rates (find) [quick]
└── Task 18: warehouses (find, get) [quick]

Wave 3 (Parameterized-path read-only resources):
├── Task 19: declaration_body_jpkvat (get by year/month) [quick]
├── Task 20: declaration_body_pit (get by type/year) [quick]
└── Task 21: taxregisters (get by year/month) [quick]

Wave 4 (CRUD resources — new models needed, MAX PARALLEL):
├── Task 22: documents (add, find, get, download, delete) [unspecified-high]
├── Task 23: invoice_deliveries (add, find, get, delete) [quick]
├── Task 24: notes (add, find, get, edit, delete) [quick]
├── Task 25: series (add, find, get, edit, delete) [quick]
├── Task 26: term_groups (add, find, get, edit, delete) [quick]
├── Task 27: terms (add, find, get, edit, delete) [quick]
└── Task 28: vehicles (add, find, get, edit, delete) [unspecified-high]

Wave 5 (Warehouse document types — all share WarehouseDocument model, MAX PARALLEL):
├── Task 29: warehouse_document_p_z [quick]
├── Task 30: warehouse_document_r [quick]
├── Task 31: warehouse_document_r_w [quick]
├── Task 32: warehouse_document_w_z [quick]
├── Task 33: warehouse_document_z_d [quick]
├── Task 34: warehouse_document_z_p_d [quick]
└── Task 35: warehouse_document_z_p_m [quick]

Wave 6 (Special cases — depends on PATCH method from Wave 1):
└── Task 36: webhooks (add, find, get, trigger, edit, delete) [unspecified-high]

Wave FINAL (After ALL tasks — independent review, 4 parallel):
├── Task F1: Plan compliance audit (oracle)
├── Task F2: Code quality review (unspecified-high)
├── Task F3: Full test suite + coverage verification (unspecified-high)
└── Task F4: Scope fidelity check (deep)

Critical Path: Task 1 → Task 36 (PATCH blocker for webhooks)
                Task 2 → Task 3 (binary support → invoice download)
                Task 2 → Task 22 (binary support → documents download)
Parallel Speedup: ~80% faster than sequential
Max Concurrent: 15 (Wave 2)
```

### Dependency Matrix

| Task | Depends On | Blocks | Wave |
|------|------------|--------|------|
| 1 (PATCH method) | — | 36 | 1 |
| 2 (Binary response) | — | 3, 22 | 1 |
| 3 (Invoice extras) | 2 | — | 1 |
| 4-18 (Read-only) | — | — | 2 |
| 19-21 (Parameterized) | — | — | 3 |
| 22 (Documents) | 2 | — | 4 |
| 23-27 (CRUD simple) | — | — | 4 |
| 28 (Vehicles) | — | — | 4 |
| 29-35 (Warehouse) | — | — | 5 |
| 36 (Webhooks) | 1 | — | 6 |
| F1-F4 (Final) | ALL | — | FINAL |

### Agent Dispatch Summary

| Wave | # Parallel | Tasks → Agent Category |
|------|------------|----------------------|
| 1 | **3** | T1 → `quick`, T2 → `quick`, T3 → `unspecified-high` |
| 2 | **15** | T4-T18 → `quick` |
| 3 | **3** | T19-T21 → `quick` |
| 4 | **7** | T22 → `unspecified-high`, T23-T27 → `quick`, T28 → `unspecified-high` |
| 5 | **7** | T29-T35 → `quick` |
| 6 | **1** | T36 → `unspecified-high` |
| FINAL | **4** | F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep` |

---

## TODOs

### Wave 1: Prerequisites

- [x] 1. Add PATCH method to sync and async HTTP clients

  **What to do**:
  - Add `patch()` and `patch_json()` methods to `src/wfirma/sync/client.py` (class `WFirmaClient`)
  - Add `patch()` and `patch_json()` methods to `src/wfirma/async_/client.py` (class `WFirmaClient`)
  - Follow the exact pattern of existing `post()` / `post_json()` methods
  - Write tests for both sync and async PATCH methods in existing client test files

  **Must NOT do**:
  - Do not modify any resource classes
  - Do not change existing method signatures

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Simple method additions following established pattern in 2 files
  - **Skills**: []
    - No special skills needed — straightforward Python

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 2)
  - **Parallel Group**: Wave 1 (with Tasks 2, 3)
  - **Blocks**: Task 36 (webhooks)
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `src/wfirma/sync/client.py:post_json()` — Exact pattern to follow for `patch_json()`; copy method signature, replace `self._http_client.post` with `self._http_client.patch`
  - `src/wfirma/async_/client.py:post_json()` — Async mirror pattern

  **Test References**:
  - `tests/sync/test_client.py::TestWFirmaClientHTTPMethods` — Add PATCH tests here following POST test pattern
  - `tests/async_/test_client.py::TestWFirmaClientHTTPMethods` — Async mirror

  **Acceptance Criteria**:

  - [ ] `uv run pytest tests/sync/test_client.py -v -k patch` → PASS
  - [ ] `uv run pytest tests/async_/test_client.py -v -k patch` → PASS
  - [ ] `uv run ruff check src/wfirma/sync/client.py src/wfirma/async_/client.py` → 0 errors
  - [ ] `uv run mypy src/wfirma/sync/client.py src/wfirma/async_/client.py` → 0 errors

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: PATCH method sends correct HTTP request (sync)
    Tool: Bash (uv run pytest)
    Preconditions: Tests written with httpx mock
    Steps:
      1. Run `uv run pytest tests/sync/test_client.py -v -k "test_patch"` 
      2. Verify all PATCH-related tests pass
    Expected Result: All PATCH tests pass, 0 failures
    Failure Indicators: Any test failure or ImportError
    Evidence: .sisyphus/evidence/task-1-patch-sync.txt

  Scenario: PATCH method sends correct HTTP request (async)
    Tool: Bash (uv run pytest)
    Preconditions: Async tests written with httpx mock
    Steps:
      1. Run `uv run pytest tests/async_/test_client.py -v -k "test_patch"`
      2. Verify all PATCH-related tests pass
    Expected Result: All PATCH tests pass, 0 failures
    Failure Indicators: Any test failure or ImportError
    Evidence: .sisyphus/evidence/task-1-patch-async.txt
  ```

  **Commit**: YES
  - Message: `feat(client): add PATCH/patch_json methods to sync and async clients`
  - Files: `src/wfirma/sync/client.py`, `src/wfirma/async_/client.py`, `tests/sync/test_client.py`, `tests/async_/test_client.py`
  - Pre-commit: `uv run pytest tests/sync/test_client.py tests/async_/test_client.py`

---

- [x] 2. Add binary response support to sync and async HTTP clients

  **What to do**:
  - Add `get_binary()` method to `src/wfirma/sync/client.py` that returns `bytes` (uses `response.content` instead of `response.json()`)
  - Add `post_binary()` method to `src/wfirma/sync/client.py` that POSTs and returns `bytes`
  - Add corresponding async methods to `src/wfirma/async_/client.py`
  - These methods should still handle HTTP errors (status codes) but skip JSON parsing
  - Write tests for both sync and async binary methods

  **Must NOT do**:
  - Do not change existing `_handle_response()` behavior
  - Do not modify JSON response handling

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Adding new methods to existing client, following established patterns
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Task 1)
  - **Parallel Group**: Wave 1 (with Tasks 1, 3)
  - **Blocks**: Task 3 (invoice download), Task 22 (documents download)
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `src/wfirma/sync/client.py:get_json()` — Base pattern; binary version uses same URL construction but returns `response.content` (bytes)
  - `src/wfirma/sync/client.py:_handle_response()` (lines 276–283) — HTTP status error handling logic (429→RateLimitError, 5xx→ServerError/ServiceUnavailableError); replicate the same status checks in the new `get_binary()` method before returning bytes (do NOT call `_handle_response()` directly since it tries to parse JSON)
  - `src/wfirma/async_/client.py:get_json()` — Async mirror pattern

  **Test References**:
  - `tests/sync/test_client.py::TestWFirmaClientHTTPMethods` — Add binary tests following same mock pattern

  **Acceptance Criteria**:

  - [ ] `uv run pytest tests/sync/test_client.py -v -k binary` → PASS
  - [ ] `uv run pytest tests/async_/test_client.py -v -k binary` → PASS
  - [ ] `uv run ruff check src/wfirma/sync/client.py src/wfirma/async_/client.py` → 0 errors

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Binary GET returns raw bytes (sync)
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks httpx to return binary content
    Steps:
      1. Run `uv run pytest tests/sync/test_client.py -v -k "test_get_binary"`
      2. Assert test passes and verifies return type is bytes
    Expected Result: Test passes, binary content correctly returned
    Failure Indicators: TypeError or JSON parsing attempted on binary data
    Evidence: .sisyphus/evidence/task-2-binary-sync.txt

  Scenario: Binary GET handles HTTP errors (sync)
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks httpx to return 404/500 for binary endpoint
    Steps:
      1. Run `uv run pytest tests/sync/test_client.py -v -k "test_get_binary_error"`
      2. Assert appropriate exception raised
    Expected Result: ResourceNotFoundError or ServerError raised
    Failure Indicators: Raw bytes returned instead of exception
    Evidence: .sisyphus/evidence/task-2-binary-error.txt
  ```

  **Commit**: YES
  - Message: `feat(client): add binary response methods (get_binary, post_binary) for download endpoints`
  - Files: `src/wfirma/sync/client.py`, `src/wfirma/async_/client.py`, `tests/sync/test_client.py`, `tests/async_/test_client.py`
  - Pre-commit: `uv run pytest tests/sync/test_client.py tests/async_/test_client.py`

---

- [x] 3. Add missing Invoice endpoints (download, send, fiscalize, unfiscalize)

  **What to do**:
  - Add `download(invoice_id: int) -> bytes` to `InvoicesResource` (sync + async) — uses `post_binary()` from Task 2
  - Add `send(invoice_id: int) -> dict[str, Any]` to `InvoicesResource` (sync + async) — POST endpoint
  - Add `fiscalize(invoice_id: int) -> dict[str, Any]` to `InvoicesResource` (sync + async) — GET endpoint
  - Add `unfiscalize(invoice_id: int) -> dict[str, Any]` to `InvoicesResource` (sync + async) — GET endpoint
  - Check `docs/api_spec.json` for exact request/response shapes of each endpoint
  - Write tests for all 4 new methods (sync + async)

  **Must NOT do**:
  - Do not change existing `get()`, `find()`, `add()`, `edit()`, `delete()` methods
  - Do not change existing tests

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 4 new methods with different patterns (binary download, POST actions, GET actions) — more complex than a single-pattern resource
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO — depends on Task 2
  - **Parallel Group**: Wave 1 (sequential after Task 2)
  - **Blocks**: None
  - **Blocked By**: Task 2 (binary response support)

  **References**:

  **Pattern References**:
  - `src/wfirma/sync/resources/invoices.py` — Existing resource to extend (add methods, don't change existing)
  - `src/wfirma/async_/resources/invoices.py` — Async mirror to extend
  - `docs/api_reference.md:330-401` — Invoice endpoint paths: download (POST), send (POST), fiscalize (GET), unfiscalize (GET)

  **API References**:
  - `docs/api_spec.json` — Check request body format for `invoices/download` and `invoices/send`

  **Test References**:
  - `tests/sync/resources/test_sync_invoices_resource.py` — Add new test methods here
  - `tests/async_/resources/test_async_invoices_resource.py` — Async mirror

  **Acceptance Criteria**:

  - [ ] `uv run pytest tests/sync/resources/test_sync_invoices_resource.py -v` → ALL pass (existing + new)
  - [ ] `uv run pytest tests/async_/resources/test_async_invoices_resource.py -v` → ALL pass
  - [ ] `python -c "from wfirma.sync.resources.invoices import InvoicesResource; assert hasattr(InvoicesResource, 'download')"` → no error
  - [ ] `python -c "from wfirma.sync.resources.invoices import InvoicesResource; assert hasattr(InvoicesResource, 'send')"` → no error

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: Invoice download returns bytes
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks post_binary to return PDF-like bytes
    Steps:
      1. Run `uv run pytest tests/sync/resources/test_sync_invoices_resource.py -v -k "test_download"`
      2. Verify test asserts return type is bytes
    Expected Result: Test passes, bytes returned
    Failure Indicators: JSON parsing error or wrong return type
    Evidence: .sisyphus/evidence/task-3-invoice-download.txt

  Scenario: Invoice fiscalize/unfiscalize call correct endpoints
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks get_json for fiscalize/unfiscalize paths
    Steps:
      1. Run `uv run pytest tests/sync/resources/test_sync_invoices_resource.py -v -k "fiscalize or unfiscalize"`
      2. Verify tests assert correct URL paths used
    Expected Result: Tests pass, correct GET endpoints called
    Failure Indicators: Wrong HTTP method or path
    Evidence: .sisyphus/evidence/task-3-invoice-fiscalize.txt
  ```

  **Commit**: YES
  - Message: `feat(invoices): add download, send, fiscalize, unfiscalize endpoints`
  - Files: `src/wfirma/sync/resources/invoices.py`, `src/wfirma/async_/resources/invoices.py`, `tests/sync/resources/test_sync_invoices_resource.py`, `tests/async_/resources/test_async_invoices_resource.py`
  - Pre-commit: `uv run pytest tests/sync/resources/test_sync_invoices_resource.py tests/async_/resources/test_async_invoices_resource.py`

---

### Wave 2: Read-Only Resources (No New Models — dict returns)

> **PATTERN FOR ALL WAVE 2 TASKS**: These resources return raw `dict[str, Any]` (like Tags) because we don't have API response schemas for these entities. Each task creates:
> - `src/wfirma/sync/resources/{resource}.py` (sync resource class)
> - `src/wfirma/async_/resources/{resource}.py` (async resource class)
> - Adds property to `src/wfirma/sync/client.py`
> - Adds property to `src/wfirma/async_/client.py`
> - Updates `src/wfirma/sync/resources/__init__.py` and `src/wfirma/async_/resources/__init__.py`
> - Tests: `tests/sync/resources/test_sync_{resource}_resource.py`, `tests/async_/resources/test_async_{resource}_resource.py`, `tests/sync/test_client_{resource}_property.py`, `tests/async_/test_client_{resource}_property.py`
>
> **EVERY executor MUST**: Read `docs/api_spec.json` to find the exact container_key and object_key for their resource before implementing `_extract_*` methods.

- [x] 4. Implement company_accounts resource (find, get)

  **What to do**:
  - Create sync resource class `CompanyAccountsResource` with `find()` → `list[dict]` and `get(company_account_id: int)` → `dict`
  - Create async mirror
  - Add `company_accounts` property to both clients
  - Update `__init__.py` exports
  - Endpoint paths: `GET /company_accounts/find`, `GET /company_accounts/get/{companyAccountId}`
  - Container key likely: `company_accounts`, object key: `company_account` — **verify in `docs/api_spec.json`**
  - Write TDD tests

  **Must NOT do**:
  - No Pydantic model — return raw dict
  - No add/edit/delete methods (API only supports find + get)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 2-endpoint read-only resource following Tags pattern
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2 (with Tasks 5-18)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:

  **Pattern References**:
  - `src/wfirma/sync/resources/tags.py` — Read-only dict-returning resource pattern (follow for `find()` and `get()` structure)
  - `src/wfirma/async_/resources/tags.py` — Async mirror pattern
  - `src/wfirma/sync/client.py:199-213` — Client property pattern (lazy init with `_resources` cache)

  **API References**:
  - `docs/api_reference.md:23-38` — company_accounts/find and company_accounts/get endpoint paths
  - `docs/api_spec.json` — Search for `company_accounts` to find container/object keys and response shape

  **Test References**:
  - `tests/sync/resources/test_sync_tags_resource.py` — Test pattern for dict-returning resources
  - `tests/sync/test_client_warehouse_documents_pw_property.py` — Client property test pattern

  **Acceptance Criteria**:

  - [ ] `uv run pytest tests/sync/resources/test_sync_company_accounts_resource.py -v` → ALL pass
  - [ ] `uv run pytest tests/async_/resources/test_async_company_accounts_resource.py -v` → ALL pass
  - [ ] `uv run pytest tests/sync/test_client_company_accounts_property.py -v` → ALL pass
  - [ ] `uv run pytest tests/async_/test_client_company_accounts_property.py -v` → ALL pass
  - [ ] `python -c "from wfirma.sync.resources import CompanyAccountsResource"` → no error
  - [ ] `python -c "from wfirma.async_.resources import CompanyAccountsResource"` → no error
  - [ ] `uv run ruff check src/wfirma/sync/resources/company_accounts.py src/wfirma/async_/resources/company_accounts.py` → 0 errors

  **QA Scenarios (MANDATORY)**:

  ```
  Scenario: company_accounts find returns list of dicts
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks get_json to return wFirma-style indexed container
    Steps:
      1. Run `uv run pytest tests/sync/resources/test_sync_company_accounts_resource.py -v -k "test_find"`
      2. Assert returns list[dict] with expected keys
    Expected Result: Test passes, list of dicts returned
    Failure Indicators: KeyError in payload extraction or wrong return type
    Evidence: .sisyphus/evidence/task-4-company-accounts-find.txt

  Scenario: company_accounts get returns single dict
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks get_json to return single object
    Steps:
      1. Run `uv run pytest tests/sync/resources/test_sync_company_accounts_resource.py -v -k "test_get"`
      2. Assert returns dict with expected keys
    Expected Result: Test passes
    Failure Indicators: KeyError or wrong container/object key
    Evidence: .sisyphus/evidence/task-4-company-accounts-get.txt
  ```

  **Commit**: YES (groups with other Wave 2 tasks if same agent)
  - Message: `feat(resources): add company_accounts resource (find, get)`
  - Files: `src/wfirma/sync/resources/company_accounts.py`, `src/wfirma/async_/resources/company_accounts.py`, `src/wfirma/sync/client.py`, `src/wfirma/async_/client.py`, `src/wfirma/sync/resources/__init__.py`, `src/wfirma/async_/resources/__init__.py`, tests
  - Pre-commit: `uv run pytest tests/sync/resources/test_sync_company_accounts_resource.py tests/async_/resources/test_async_company_accounts_resource.py`

---

- [x] 5. Implement company_packs resource (get)

  **What to do**:
  - Create `CompanyPacksResource` with only `get(company_pack_id: int)` → `dict`
  - Create async mirror
  - Add `company_packs` property to both clients
  - Update `__init__.py` exports
  - Endpoint: `GET /company_packs/get/{companyPackId}`
  - Container/object keys: verify in `docs/api_spec.json`
  - Write TDD tests

  **Must NOT do**:
  - No find/add/edit/delete — API only supports `get`

  **Recommended Agent Profile**:
  - **Category**: `quick`
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 2
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - `src/wfirma/sync/resources/tags.py` — Dict-returning pattern
  - `docs/api_reference.md:50-58` — company_packs/get endpoint
  - `docs/api_spec.json` — Search for `company_packs`

  **Acceptance Criteria**:
  - [ ] `uv run pytest tests/sync/resources/test_sync_company_packs_resource.py -v` → ALL pass
  - [ ] `uv run pytest tests/async_/resources/test_async_company_packs_resource.py -v` → ALL pass
  - [ ] `python -c "from wfirma.sync.resources import CompanyPacksResource"` → no error

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: company_packs get returns single dict
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks get_json
    Steps:
      1. Run `uv run pytest tests/sync/resources/test_sync_company_packs_resource.py -v`
    Expected Result: All tests pass
    Evidence: .sisyphus/evidence/task-5-company-packs.txt

  Scenario: company_packs get raises on not found
    Tool: Bash (uv run pytest)
    Preconditions: Test mocks 404 response
    Steps:
      1. Run `uv run pytest tests/sync/resources/test_sync_company_packs_resource.py -v -k "not_found"`
    Expected Result: ResourceNotFoundError raised
    Evidence: .sisyphus/evidence/task-5-company-packs-error.txt
  ```

  **Commit**: YES
  - Message: `feat(resources): add company_packs resource (get)`

---

- [ ] 6. Implement declaration_countries resource (find, get)

  **What to do**:
  - Create `DeclarationCountriesResource` with `find()` → `list[dict]` and `get(declaration_country_id: int)` → `dict`
  - Create async mirror, client properties, exports, TDD tests
  - Endpoints: `GET /declaration_countries/find`, `GET /declaration_countries/get/{declarationCountryId}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel | **Blocks**: None | **Blocked By**: None

  **References**:
  - `src/wfirma/sync/resources/tags.py` — Pattern
  - `docs/api_reference.md:123-138` — Endpoints

  **Acceptance Criteria**:
  - [ ] All sync+async resource tests pass
  - [ ] All client property tests pass
  - [ ] Imports work

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: declaration_countries find+get work correctly
    Tool: Bash (uv run pytest)
    Steps: 1. Run all declaration_countries tests
    Expected Result: All pass
    Evidence: .sisyphus/evidence/task-6-declaration-countries.txt
  ```

  **Commit**: YES — `feat(resources): add declaration_countries resource (find, get)`

---

- [ ] 7. Implement expenses resource (find, get)

  **What to do**:
  - Create `ExpensesResource` with `find()` and `get(expense_id: int)`
  - Both return `dict[str, Any]`
  - Endpoints: `GET /expenses/find`, `GET /expenses/get/{expenseId}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel | **Blocks**: None | **Blocked By**: None

  **References**:
  - `src/wfirma/sync/resources/tags.py` — Pattern
  - `docs/api_reference.md:183-198` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **QA Scenarios**: Same pattern as Task 4

  **Commit**: YES — `feat(resources): add expenses resource (find, get)`

---

- [ ] 8. Implement interests resource (find)

  **What to do**:
  - Create `InterestsResource` with only `find()` → `list[dict]`
  - Endpoint: `GET /interests/find`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel | **Blocks**: None | **Blocked By**: None

  **References**:
  - `docs/api_reference.md:243-250` — Endpoint

  **Acceptance Criteria**: Same pattern as Task 4 (but only find, no get)
  **QA Scenarios**: Same pattern (find only)

  **Commit**: YES — `feat(resources): add interests resource (find)`

---

- [ ] 9. Implement invoice_descriptions resource (find, get)

  **What to do**:
  - Create `InvoiceDescriptionsResource` with `find()` and `get(invoice_description_id: int)`
  - Endpoints: `GET /invoice_descriptions/find`, `GET /invoice_descriptions/get/{invoiceDescriptionsId}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:287-302` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add invoice_descriptions resource (find, get)`

---

- [ ] 10. Implement ledger_accountant_years resource (find, get)

  **What to do**:
  - Create `LedgerAccountantYearsResource` with `find()` and `get(ledger_accountant_year_id: int)`
  - Endpoints: `GET /ledger_accountant_years/find`, `GET /ledger_accountant_years/get/{id}`
  - NOTE: API spec shows hardcoded `625` in path — use parameter instead

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:439-455` — Endpoints (note hardcoded 625, use parameter)

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add ledger_accountant_years resource (find, get)`

---

- [ ] 11. Implement ledger_operation_schemas resource (find, get)

  **What to do**:
  - Create `LedgerOperationSchemasResource` with `find()` and `get(schema_id: int)`
  - Endpoints: `GET /ledger_operation_schemas/find`, `GET /ledger_operation_schemas/get/{id}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:457-472` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add ledger_operation_schemas resource (find, get)`

---

- [ ] 12. Implement payment_cashboxes resource (find, get)

  **What to do**:
  - Create `PaymentCashboxesResource` with `find()` and `get(payment_cashbox_id: int)`
  - Endpoints: `GET /payment_cashboxes/find`, `GET /payment_cashboxes/get/{paymentCashboxId}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:517-532` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add payment_cashboxes resource (find, get)`

---

- [ ] 13. Implement translation_languages resource (find, get)

  **What to do**:
  - Create `TranslationLanguagesResource` with `find()` and `get(translation_language_id: int)`
  - Endpoints: `GET /translation_languages/find`, `GET /translation_languages/get/{translationLanguageId}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:755-769` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add translation_languages resource (find, get)`

---

- [ ] 14. Implement user_companies resource (find, get)

  **What to do**:
  - Create `UserCompaniesResource` with `find()` and `get(user_company_id: int)`
  - **IMPORTANT**: These endpoints do NOT use `company_id` parameter — they are user-scoped
  - Endpoints: `GET /user_companies/find`, `GET /user_companies/get/{userCompanyId}`
  - The existing `UserCompany` model from `src/wfirma/models/company.py` can be used as the return type
  - Verify how the client constructs URLs without company_id — may need to pass a different base path or skip company_id injection

  **Must NOT do**:
  - Do not add/edit/delete methods

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:773-788` — Note: no `company_id` in URLs
  - `src/wfirma/models/company.py:UserCompany` — Existing model to return
  - `src/wfirma/sync/client.py:_build_url()` — Check how company_id is injected; may need to bypass

  **Acceptance Criteria**: Same pattern as Task 4, plus verify UserCompany model returned
  **Commit**: YES — `feat(resources): add user_companies resource (find, get)`

---

- [ ] 15. Implement users resource (get)

  **What to do**:
  - Create `UsersResource` with only `get(user_id: int)` → `User` model
  - Endpoint: `GET /users/get/{userCompanyId}`
  - Use existing `User` model from `src/wfirma/models/employee.py`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:793-798` — Endpoint
  - `src/wfirma/models/employee.py:User` — Existing model to return

  **Acceptance Criteria**: Same pattern, verify User model returned
  **Commit**: YES — `feat(resources): add users resource (get)`

---

- [ ] 16. Implement vat_codes resource (find, get)

  **What to do**:
  - Create `VatCodesResource` with `find()` and `get(vat_code_id: int)`
  - Endpoints: `GET /vat_codes/find`, `GET /vat_codes/get/{vatCodeId}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:801-816` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add vat_codes resource (find, get)`

---

- [ ] 17. Implement vehicle_run_rates resource (find)

  **What to do**:
  - Create `VehicleRunRatesResource` with only `find()` → `list[dict]`
  - Endpoint: `GET /vehicle_run_rates/find`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:819-826` — Endpoint

  **Acceptance Criteria**: Same pattern (find only)
  **Commit**: YES — `feat(resources): add vehicle_run_rates resource (find)`

---

- [ ] 18. Implement warehouses resource (find, get)

  **What to do**:
  - Create `WarehousesResource` with `find()` and `get(warehouse_id: int)`
  - Endpoints: `GET /warehouses/find`, `GET /warehouses/get/{id}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 2, parallel

  **References**:
  - `docs/api_reference.md:1207-1222` — Endpoints

  **Acceptance Criteria**: Same pattern as Task 4
  **Commit**: YES — `feat(resources): add warehouses resource (find, get)`

---

### Wave 3: Parameterized-Path Read-Only Resources

- [ ] 19. Implement declaration_body_jpkvat resource (get by year/month)

  **What to do**:
  - Create `DeclarationBodyJpkvatResource` with `get(year: int, month: int)` → `dict`
  - Endpoint: `GET /declaration_body_jpkvat/get/{year}/{month}`
  - Note: path uses two parameters, not a single ID

  **Must NOT do**:
  - No find/add/edit/delete — API only supports parameterized get

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 3, parallel

  **References**:
  - `docs/api_reference.md:103-111` — Endpoint with `{year}/{month}` pattern

  **Acceptance Criteria**:
  - [ ] Test verifies correct URL construction: `/declaration_body_jpkvat/get/2025/1`
  - [ ] All sync+async tests pass

  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: jpkvat get constructs correct year/month URL
    Tool: Bash (uv run pytest)
    Steps: 1. Run test asserting URL includes /get/2025/6
    Expected Result: Correct URL path
    Evidence: .sisyphus/evidence/task-19-jpkvat.txt
  ```

  **Commit**: YES — `feat(resources): add declaration_body_jpkvat resource (get by year/month)`

---

- [ ] 20. Implement declaration_body_pit resource (get by type/year)

  **What to do**:
  - Create `DeclarationBodyPitResource` with `get(pit_type: str, year: int)` → `dict`
  - Endpoint: `GET /declaration_body_pit/get/{type}/{year}`
  - Note: first param is a string type, second is year

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 3, parallel

  **References**:
  - `docs/api_reference.md:113-120` — Endpoint

  **Acceptance Criteria**: Test verifies correct URL construction
  **Commit**: YES — `feat(resources): add declaration_body_pit resource (get by type/year)`

---

- [ ] 21. Implement taxregisters resource (get by year/month)

  **What to do**:
  - Create `TaxregistersResource` with `get(year: int, month: int)` → `dict`
  - Endpoint: `GET /taxregisters/get/{year}/{month}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 3, parallel

  **References**:
  - `docs/api_reference.md:661-668` — Endpoint

  **Acceptance Criteria**: Test verifies correct URL construction
  **Commit**: YES — `feat(resources): add taxregisters resource (get by year/month)`

---

### Wave 4: CRUD Resources (Some Need New Models)

- [ ] 22. Implement documents resource (add, find, get, download, delete)

  **What to do**:
  - Create `DocumentsResource` with `add()`, `find()`, `get()`, `download()`, `delete()`
  - `download(document_id: int) -> bytes` — uses `get_binary()` from Task 2
  - Other methods return `dict[str, Any]` (no model needed initially)
  - Check `docs/api_spec.json` for payload wrapping pattern
  - Endpoints: `/documents/add` (POST), `/documents/find` (GET), `/documents/get/{id}` (GET), `/documents/download/{id}` (GET), `/documents/delete/{id}` (DELETE)

  **Must NOT do**:
  - Do not create a Pydantic model — use raw dict

  **Recommended Agent Profile**: `unspecified-high` | **Skills**: []
  **Parallelization**: Wave 4, parallel | **Blocked By**: Task 2 (binary)

  **References**:
  - `docs/api_reference.md:141-180` — All document endpoints
  - `src/wfirma/sync/resources/invoices.py` — CRUD pattern
  - `docs/api_spec.json` — Check request body for documents/add

  **Acceptance Criteria**: All tests pass, download returns bytes
  **Commit**: YES — `feat(resources): add documents resource (add, find, get, download, delete)`

---

- [ ] 23. Implement invoice_deliveries resource (add, find, get, delete)

  **What to do**:
  - Create `InvoiceDeliveriesResource` with `add()`, `find()`, `get()`, `delete()` (no edit)
  - Return `dict[str, Any]`
  - Check `docs/api_spec.json` for payload wrapping
  - Endpoints: `/invoice_deliveries/add` (POST), `/invoice_deliveries/find` (GET), `/invoice_deliveries/get/{id}` (GET), `/invoice_deliveries/delete/{id}` (DELETE)

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 4, parallel

  **References**:
  - `docs/api_reference.md:253-284` — Endpoints

  **Acceptance Criteria**: All tests pass
  **Commit**: YES — `feat(resources): add invoice_deliveries resource (add, find, get, delete)`

---

- [ ] 24. Implement notes resource (add, find, get, edit, delete)

  **What to do**:
  - Create `NotesResource` with full CRUD
  - Return `dict[str, Any]`
  - **IMPORTANT**: `notes/edit` path in spec shows `/goods/notes/{noteId}` — this is a TYPO. Use `/notes/edit/{noteId}` (following same pattern as tags where spec shows `/tags/notes/` but actual code uses `/tags/edit/`)
  - Check `docs/api_spec.json` for payload wrapping

  **Must NOT do**:
  - Do not use the wrong `/goods/notes/` path from the spec

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 4, parallel

  **References**:
  - `docs/api_reference.md:475-514` — Endpoints (note typo at line 505)
  - `src/wfirma/sync/resources/tags.py:105` — Tags edit uses `/tags/edit/` not `/tags/notes/` — proof the spec typo pattern

  **Acceptance Criteria**: All tests pass, edit uses `/notes/edit/` path
  **Commit**: YES — `feat(resources): add notes resource (add, find, get, edit, delete)`

---

- [ ] 25. Implement series resource (add, find, get, edit, delete)

  **What to do**:
  - Create `SeriesResource` with full CRUD
  - Return `dict[str, Any]`
  - **IMPORTANT**: `series/edit` path shows `/series/notes/ID` — TYPO, use `/series/edit/{id}`
  - **IMPORTANT**: `series/del` uses `/series/del/{id}` NOT `/series/delete/{id}` — this is NOT a typo, it's a different path segment. Use `/series/del/{id}`
  - Check `docs/api_spec.json` for payload wrapping

  **Must NOT do**:
  - Do not use `/series/notes/` path for edit
  - Do not use `/series/delete/` — the API uses `/series/del/`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 4, parallel

  **References**:
  - `docs/api_reference.md:577-617` — Endpoints (note edit typo at line 607, del path at line 613)

  **Acceptance Criteria**: All tests pass, edit uses `/series/edit/`, delete uses `/series/del/`
  **Commit**: YES — `feat(resources): add series resource (add, find, get, edit, delete)`

---

- [ ] 26. Implement term_groups resource (add, find, get, edit, delete)

  **What to do**:
  - Create `TermGroupsResource` with full CRUD
  - Return `dict[str, Any]`
  - **IMPORTANT**: `term_groups/edit` path shows `/term_groups/notes/{id}` — TYPO, use `/term_groups/edit/{id}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 4, parallel

  **References**:
  - `docs/api_reference.md:671-709` — Endpoints (note edit typo at line 701)

  **Acceptance Criteria**: All tests pass, edit uses `/term_groups/edit/`
  **Commit**: YES — `feat(resources): add term_groups resource (add, find, get, edit, delete)`

---

- [ ] 27. Implement terms resource (add, find, get, edit, delete)

  **What to do**:
  - Create `TermsResource` with full CRUD
  - Return `dict[str, Any]`
  - **IMPORTANT**: `terms/edit` path shows `/terms/notes/{id}` — TYPO, use `/terms/edit/{id}`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 4, parallel

  **References**:
  - `docs/api_reference.md:713-752` — Endpoints (note edit typo at line 741)

  **Acceptance Criteria**: All tests pass, edit uses `/terms/edit/`
  **Commit**: YES — `feat(resources): add terms resource (add, find, get, edit, delete)`

---

- [ ] 28. Implement vehicles resource (add, find, get, edit, delete)

  **What to do**:
  - Create `VehiclesResource` with full CRUD
  - Return `dict[str, Any]`
  - **IMPORTANT**: `vehicles/delete` uses GET method (not DELETE!) per the API spec. The `delete()` method must call `self._client.get_json()` NOT `self._client.delete_json()`. Add a clear code comment explaining this API quirk.
  - Check `docs/api_spec.json` for payload wrapping

  **Must NOT do**:
  - Do not use DELETE HTTP method for the delete endpoint

  **Recommended Agent Profile**: `unspecified-high` | **Skills**: []
    - Reason: Non-standard HTTP method for delete requires extra attention
  **Parallelization**: Wave 4, parallel

  **References**:
  - `docs/api_reference.md:829-868` — Endpoints (note vehicles/delete uses GET at line 841)

  **Acceptance Criteria**: All tests pass, delete uses GET method
  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: vehicles delete uses GET not DELETE
    Tool: Bash (uv run pytest)
    Steps: 1. Test asserts get_json called (not delete_json) for delete endpoint
    Expected Result: GET method used
    Evidence: .sisyphus/evidence/task-28-vehicles-delete.txt
  ```

  **Commit**: YES — `feat(resources): add vehicles resource (add, find, get, edit, delete)`

---

### Wave 5: Warehouse Document Types (All Share WarehouseDocument Model)

> **PATTERN FOR ALL WAVE 5 TASKS**: These resources are nearly identical to the existing `WarehouseDocumentPWResource`. Each has full CRUD (add, find, get, edit, delete) and returns `WarehouseDocument` model. Only the endpoint prefix differs.
>
> Follow `src/wfirma/sync/resources/warehouse_documents_pw.py` EXACTLY — copy and change the URL prefix.

- [ ] 29. Implement warehouse_document_p_z resource

  **What to do**:
  - Copy `warehouse_documents_pw.py` pattern, change URL prefix to `warehouse_document_p_z`
  - Class name: `WarehouseDocumentPZResource`
  - Client property: `warehouse_documents_pz`
  - Container key: `warehouse_documents`, object key: `warehouse_document`

  **Recommended Agent Profile**: `quick` | **Skills**: []
  **Parallelization**: Wave 5, parallel

  **References**:
  - `src/wfirma/sync/resources/warehouse_documents_pw.py` — EXACT pattern to copy
  - `docs/api_reference.md:913-952` — PZ endpoints

  **Acceptance Criteria**: All tests pass, model returned is WarehouseDocument
  **Commit**: YES — `feat(resources): add warehouse_document_p_z resource`

---

- [ ] 30. Implement warehouse_document_r resource

  **What to do**:
  - Same pattern as Task 29 with URL prefix `warehouse_document_r`
  - Class: `WarehouseDocumentRResource`, property: `warehouse_documents_r`

  **References**: `docs/api_reference.md:955-994`
  **Commit**: YES — `feat(resources): add warehouse_document_r resource`

---

- [ ] 31. Implement warehouse_document_r_w resource

  **What to do**:
  - Same pattern with URL prefix `warehouse_document_r_w`
  - Class: `WarehouseDocumentRWResource`, property: `warehouse_documents_rw`

  **References**: `docs/api_reference.md:997-1036`
  **Commit**: YES — `feat(resources): add warehouse_document_r_w resource`

---

- [ ] 32. Implement warehouse_document_w_z resource

  **What to do**:
  - Same pattern with URL prefix `warehouse_document_w_z`
  - Class: `WarehouseDocumentWZResource`, property: `warehouse_documents_wz`

  **References**: `docs/api_reference.md:1039-1078`
  **Commit**: YES — `feat(resources): add warehouse_document_w_z resource`

---

- [ ] 33. Implement warehouse_document_z_d resource

  **What to do**:
  - Same pattern with URL prefix `warehouse_document_z_d`
  - Class: `WarehouseDocumentZDResource`, property: `warehouse_documents_zd`

  **References**: `docs/api_reference.md:1081-1120`
  **Commit**: YES — `feat(resources): add warehouse_document_z_d resource`

---

- [ ] 34. Implement warehouse_document_z_p_d resource

  **What to do**:
  - Same pattern with URL prefix `warehouse_document_z_p_d`
  - Class: `WarehouseDocumentZPDResource`, property: `warehouse_documents_zpd`

  **References**: `docs/api_reference.md:1123-1162`
  **Commit**: YES — `feat(resources): add warehouse_document_z_p_d resource`

---

- [ ] 35. Implement warehouse_document_z_p_m resource

  **What to do**:
  - Same pattern with URL prefix `warehouse_document_z_p_m`
  - Class: `WarehouseDocumentZPMResource`, property: `warehouse_documents_zpm`

  **References**: `docs/api_reference.md:1165-1204`
  **Commit**: YES — `feat(resources): add warehouse_document_z_p_m resource`

---

### Wave 6: Special Cases

- [ ] 36. Implement webhooks resource (add, find, get, trigger, edit, delete)

  **What to do**:
  - Create `WebhooksResource` with `add()`, `find()`, `get()`, `trigger()`, `edit()`, `delete()`
  - Return `dict[str, Any]`
  - **IMPORTANT**: `webhooks/edit` uses PATCH method — use `self._client.patch_json()` from Task 1
  - `trigger(webhook_id: int)` is a GET endpoint
  - Check `docs/api_spec.json` for payload wrapping

  **Must NOT do**:
  - Do not use POST for edit — must use PATCH

  **Recommended Agent Profile**: `unspecified-high` | **Skills**: []
    - Reason: Non-standard HTTP methods (PATCH for edit, GET for trigger)
  **Parallelization**: Wave 6, sequential | **Blocked By**: Task 1 (PATCH method)

  **References**:
  - `docs/api_reference.md:1225-1272` — All webhook endpoints (note PATCH at line 1261)
  - `src/wfirma/sync/resources/tags.py` — Base CRUD pattern for dict-returning resources

  **Acceptance Criteria**: All tests pass, edit uses PATCH method, trigger uses GET method
  **QA Scenarios (MANDATORY)**:
  ```
  Scenario: webhooks edit uses PATCH
    Tool: Bash (uv run pytest)
    Steps: 1. Test asserts patch_json called for edit
    Expected Result: PATCH method used
    Evidence: .sisyphus/evidence/task-36-webhooks-patch.txt

  Scenario: webhooks trigger uses GET
    Tool: Bash (uv run pytest)
    Steps: 1. Test asserts get_json called for trigger
    Expected Result: GET method used
    Evidence: .sisyphus/evidence/task-36-webhooks-trigger.txt
  ```

  **Commit**: YES — `feat(resources): add webhooks resource (add, find, get, trigger, edit, delete)`

---

### Wave FINAL: Verification

- [ ] F1. **Plan Compliance Audit** — `oracle`
  Read the plan end-to-end. For each "Must Have": verify implementation exists (read file, import resource). For each "Must NOT Have": search codebase for forbidden patterns — reject with file:line if found. Check evidence files exist in `.sisyphus/evidence/`. Compare deliverables against plan.
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  Run `uv run mypy src` + `uv run ruff check src tests` + `uv run pytest --cov=wfirma --cov-report=term-missing`. Review all new files for: `as Any` overuse, empty catches, console.log equivalent (`print()`), commented-out code, unused imports. Check AI slop: excessive comments, over-abstraction, generic variable names.
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Tests [N pass/N fail] | Coverage [N%] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Full Test Suite + Coverage Verification** — `unspecified-high`
  Run `uv run pytest --cache-clear -v` to execute the ENTIRE test suite. Verify no regressions in existing tests. Verify >90% coverage. For each new resource: verify import works (`python -c "from wfirma.sync.resources import X"`). Save output to `.sisyphus/evidence/final-qa/`.
  Output: `Total Tests [N pass/N fail] | Coverage [N%] | Regressions [CLEAN/N] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  For each resource in `docs/api_reference.md`: verify a corresponding resource class exists. For each task: read "What to do", verify actual implementation matches. Check "Must NOT do" compliance — no abstract base classes, no modifications to existing 7 resources (except invoices Task 3). Detect any unaccounted changes.
  Output: `API Coverage [N/N endpoints] | Tasks [N/N compliant] | Unaccounted [CLEAN/N] | VERDICT`

---

## Commit Strategy

| After Task(s) | Message | Verification |
|--------------|---------|--------------|
| 1 | `feat(client): add PATCH/patch_json methods` | `uv run pytest tests/sync/test_client.py tests/async_/test_client.py` |
| 2 | `feat(client): add binary response methods` | Same as above |
| 3 | `feat(invoices): add download, send, fiscalize, unfiscalize` | `uv run pytest tests/*/resources/test_*invoices*` |
| 4-18 | Individual commits per resource | Per-resource test files |
| 19-21 | Individual commits | Per-resource test files |
| 22-28 | Individual commits | Per-resource test files |
| 29-35 | Individual commits | Per-resource test files |
| 36 | `feat(resources): add webhooks resource` | Per-resource test files |
| FINAL | No commit — verification only | `uv run pytest --cov=wfirma` |

---

## Success Criteria

### Verification Commands
```bash
# All tests pass
uv run pytest --cache-clear -v  # Expected: ALL PASS, 0 failures

# Coverage maintained
uv run pytest --cov=wfirma --cov-report=term-missing  # Expected: >90%

# Lint clean
uv run ruff check src tests  # Expected: 0 errors

# Type check clean
uv run mypy src  # Expected: 0 errors

# All resources importable
python -c "from wfirma.sync.resources import CompanyAccountsResource, CompanyPacksResource, DeclarationCountriesResource, ExpensesResource, InterestsResource, InvoiceDescriptionsResource, LedgerAccountantYearsResource, LedgerOperationSchemasResource, PaymentCashboxesResource, TranslationLanguagesResource, UserCompaniesResource, UsersResource, VatCodesResource, VehicleRunRatesResource, WarehousesResource, DeclarationBodyJpkvatResource, DeclarationBodyPitResource, TaxregistersResource, DocumentsResource, InvoiceDeliveriesResource, NotesResource, SeriesResource, TermGroupsResource, TermsResource, VehiclesResource, WarehouseDocumentPZResource, WarehouseDocumentRResource, WarehouseDocumentRWResource, WarehouseDocumentWZResource, WarehouseDocumentZDResource, WarehouseDocumentZPDResource, WarehouseDocumentZPMResource, WebhooksResource"

# All client properties accessible
python -c "
from wfirma.sync.client import WFirmaClient
from wfirma.sync.auth import APIKeyAuth
auth = APIKeyAuth(access_key='x', secret_key='y', app_key='z')
c = WFirmaClient(auth=auth, company_id=1)
for attr in ['company_accounts', 'company_packs', 'declaration_countries', 'expenses', 'interests', 'invoice_descriptions', 'ledger_accountant_years', 'ledger_operation_schemas', 'payment_cashboxes', 'translation_languages', 'user_companies', 'users', 'vat_codes', 'vehicle_run_rates', 'warehouses', 'declaration_body_jpkvat', 'declaration_body_pit', 'taxregisters', 'documents', 'invoice_deliveries', 'notes', 'series', 'term_groups', 'terms', 'vehicles', 'warehouse_documents_pz', 'warehouse_documents_r', 'warehouse_documents_rw', 'warehouse_documents_wz', 'warehouse_documents_zd', 'warehouse_documents_zpd', 'warehouse_documents_zpm', 'webhooks']:
    assert hasattr(c, attr), f'Missing property: {attr}'
print('All properties present')
"
```

### Final Checklist
- [ ] All "Must Have" present — every API endpoint group has a resource class
- [ ] All "Must NOT Have" absent — no abstract base classes, no unauthorized modifications
- [ ] All tests pass — 0 failures
- [ ] Coverage >90%
- [ ] 0 lint errors
- [ ] 0 type errors
