# Learnings

> Conventions, patterns, and best practices discovered during implementation.


## Task 2: Binary Response Support (get_binary, post_binary)

### Implementation Pattern
- **HTTP Error Handling**: Binary methods replicate exact HTTP status code checks from `_handle_response()` lines 276-283:
  - 429 → RateLimitError
  - 503 → ServiceUnavailableError  
  - ≥500 → ServerError
- **Helper Method**: Created `_handle_binary_response()` that mirrors JSON response handler but returns `response.content` (bytes) instead of parsing JSON
- **Async Compatibility**: Both sync and async clients use identical error handling logic in `_handle_binary_response()`
- **Async Auth Headers**: Async client must use `await self._get_auth_headers()` (discovered via LSP errors)

### Binary Method Signatures
- `get_binary(path, params=None) -> bytes`
- `post_binary(path, data=None, params=None) -> bytes`

### Test Coverage
- ✅ Basic binary return (sync & async)
- ✅ HTTP error handling (429, 500, 503)
- ✅ POST with JSON data payload
- ✅ Query parameter support

### Key Insights
- Do NOT call `_handle_response()` for binary (it tries JSON parsing)
- Binary methods handle ONLY HTTP errors, not wFirma API status codes (binary formats may not have JSON status wrapper)
- Created separate helper to keep concerns separated: JSON vs binary response handling


## Task 1: PATCH Method Implementation

### Implementation Pattern
- **Exact POST Pattern Replication**: Both `patch()` and `patch_json()` follow the EXACT signature and behavior of `post()` and `post_json()`
- **Method Placement**: PATCH methods inserted BEFORE `delete()` method in both sync and async clients (logical grouping with other modifying methods)
- **Signature**: `patch(path, *, json=None, content=None, content_type="application/json", params=None) -> dict[str, Any]`
- **JSON Convenience**: `patch_json(path, *, data, params=None) -> dict[str, Any]` adds `inputFormat=json` and `outputFormat=json` params

### HTTP Client Integration
- Uses `self._http_client.patch()` (httpx library)
- Error handling identical to POST:
  - `httpx.TimeoutException` → `TimeoutError`
  - `httpx.ConnectError` → `ConnectionError`
  - `httpx.RequestError` → `ConnectionError`
- Response parsing via `_handle_response()` (reuses existing error handler)
- Parameters processed via `_add_default_params()` (includes company_id when set)

### Async Implementation
- Same signatures with `async def` and `await` keywords
- Must `await self._get_auth_headers()` for auth headers

### Test Coverage (8 tests total)
**Sync tests** (4 in `TestWFirmaClientHTTPMethods`):
- `test_patch_request_sends_json_body`: Verifies JSON body is sent correctly
- `test_patch_request_sends_xml_body`: Verifies XML body is sent correctly  
- `test_patch_json_sets_format_params`: Verifies format parameters are set
- `test_patch_xml_sends_request`: Verifies raw PATCH request with custom content-type

**Async tests** (4 in `TestWFirmaClientHTTPMethods`):
- `test_patch_request_sends_json_body`: Async variant
- `test_patch_request_sends_xml_body`: Async variant
- `test_patch_json_adds_format_parameters`: Async variant
- `test_patch_xml_sends_request`: Async variant

### Verification
- ✅ All 97 client tests pass (existing + new PATCH tests)
- ✅ Ruff linter: No issues
- ✅ MyPy type checker: No issues
- ✅ Commit: f8397c4 - "feat(client): add PATCH/patch_json methods to sync and async clients"

### Key Insights
- PATCH methods are **exact mirrors** of POST (same error handling, response parsing, parameter handling)
- httpx library handles PATCH HTTP method natively (like POST, GET, DELETE)
- Respx mock library supports `respx.patch()` just like other HTTP methods
- Methods should be placed logically near related verbs (PATCH after POST, before DELETE)

## Task 3: Invoice Endpoints (download, send, fiscalize, unfiscalize)

### Implementation Pattern
- **Binary Download**: `download()` uses `post_binary()` — returns PDF bytes, not JSON
- **JSON Endpoints**: `send()`, `fiscalize()`, `unfiscalize()` all return `dict[str, Any]` (raw JSON response)
- **Optional Parameters**: `download()` and `send()` accept optional `parameters` dict for API-specific options (email, subject, page, duplicate, etc.)

### Endpoint Details (from API spec)
- `invoices/download` — POST `/invoices/download/{invoiceId}`, returns binary PDF
  - Optional parameters wrapped: `{"invoices": [{"parameters": {...}}]}`
- `invoices/send` — POST `/invoices/send/{invoiceId}`, returns JSON
  - Optional parameters wrapped: `{"invoices": [{"parameters": {...}}]}`
- `invoices/fiscalize` — GET `/invoices/fiscalize/{invoiceId}`, returns JSON
  - No body, just invoice_id in path
- `invoices/unfiscalize` — GET `/invoices/unfiscalize/{invoiceId}`, returns JSON
  - No body, just invoice_id in path

### Method Signatures
- `download(invoice_id: int, *, parameters: dict[str, Any] | None = None) -> bytes`
- `send(invoice_id: int, *, parameters: dict[str, Any] | None = None) -> dict[str, Any]`
- `fiscalize(invoice_id: int) -> dict[str, Any]`
- `unfiscalize(invoice_id: int) -> dict[str, Any]`

### Test Coverage (12 tests total: 6 sync + 6 async)
**Sync tests**:
- `test_download_calls_expected_endpoint_and_returns_bytes`: Verifies PDF download returns bytes
- `test_download_with_parameters`: Verifies optional parameters are sent
- `test_send_calls_expected_endpoint_and_returns_dict`: Verifies email sending returns JSON
- `test_send_with_parameters`: Verifies email parameters (subject, body, etc.)
- `test_fiscalize_calls_expected_endpoint_and_returns_dict`: Verifies fiscalize returns JSON
- `test_unfiscalize_calls_expected_endpoint_and_returns_dict`: Verifies unfiscalize returns JSON

**Async tests**: Same 6 tests with async/await

### Binary Method Query Parameters
- **Key Finding**: `post_binary()` does NOT add `inputFormat`/`outputFormat` parameters
- Binary methods only add `company_id` via `_add_default_params()`
- Tests must NOT expect `inputFormat`/`outputFormat` for binary endpoints (unlike `post_json()`)
- Pattern verified from existing `test_client.py::test_post_binary_returns_bytes` (lines 250-259)

### Verification
- ✅ All 24 invoice tests pass (12 new + 12 existing)
- ✅ 100% coverage on both sync and async InvoicesResource
- ✅ Evidence saved: `.sisyphus/evidence/task-3-invoice-endpoints.txt`

### Key Insights
- `download()` is the FIRST binary endpoint in resources layer (all others were JSON)
- Payload wrapping for parameters: `{"invoices": [{"parameters": {...}}]}`
- GET endpoints (fiscalize/unfiscalize) have no body — just path parameter
- POST endpoints (download/send) can have optional body parameters
- Binary downloads must use `post_binary()`, not `post_json()` (different response type)


## Task 4: company_accounts Resource (Read-Only, Dict-Returning)

### Implementation Pattern
- **Resource Type**: Read-only resource with only `find()` and `get()` methods (no add/edit/delete)
- **Return Type**: Raw `dict[str, Any]` (no Pydantic model — following Task pattern for resources without schemas)
- **Container/Object Keys**: Determined from `docs/api_spec.json` — `company_accounts` (container), `company_account` (object, singular)
- **Payload Extraction**: Uses existing helpers from `wfirma._payloads`:
  - `extract_object_list_payloads()` for `find()` → returns list
  - `extract_single_object_payload()` for `get()` → returns dict
  - Both require `container_key` and `object_key` parameters

### TDD Workflow
1. **RED Phase**: Wrote all tests FIRST (4 test files, 10 test methods total)
   - Sync resource tests: `test_sync_company_accounts_resource.py` (3 tests: get, find, find_empty)
   - Async resource tests: `test_async_company_accounts_resource.py` (3 tests: same as sync with async/await)
   - Sync client property tests: `test_client_company_accounts_property.py` (2 tests: returns_resource, is_cached)
   - Async client property tests: `test_client_company_accounts_property.py` (2 tests: same with async)
2. **GREEN Phase**: Implemented minimal code to pass tests
   - Sync resource: `src/wfirma/sync/resources/company_accounts.py`
   - Async resource: `src/wfirma/async_/resources/company_accounts.py`
   - Client properties added to both sync and async clients
   - Exports added to both `__init__.py` files
3. **Verification**: All 10 tests passed, 0 lint errors, 100% coverage on new resources

### Client Property Pattern
- **Lazy Initialization**: Property checks `self._resources` cache first
- **Local Import**: Import resource class INSIDE property to avoid circular dependencies (all client properties use this pattern)
- **Cache Storage**: Store instantiated resource in `self._resources["{resource_name}"]`
- **Docstring Pattern**: All client properties have identical docstring structure:
  ```python
  """Convenience accessor for {resource} endpoints.
  
  Returns:
      {ResourceClass} instance bound to this client.
  """
  ```

### File Structure for Wave 2 Resources
Each read-only resource requires exactly 6 files:
1. `src/wfirma/sync/resources/{resource}.py` — Sync resource class
2. `src/wfirma/async_/resources/{resource}.py` — Async resource class (mirror with async/await)
3. `tests/sync/resources/test_sync_{resource}_resource.py` — Sync resource tests
4. `tests/async_/resources/test_async_{resource}_resource.py` — Async resource tests
5. `tests/sync/test_client_{resource}_property.py` — Sync client property tests
6. `tests/async_/test_client_{resource}_property.py` — Async client property tests

Plus 2 updates:
- `src/wfirma/sync/resources/__init__.py` — Add import + export
- `src/wfirma/async_/resources/__init__.py` — Add import + export

### API Spec Investigation
- **Critical Step**: ALWAYS check `docs/api_spec.json` for exact container/object keys before implementing `_extract_*` methods
- **Search Pattern**: `grep -i "resource_name" docs/api_spec.json` to find endpoint definitions
- **Response Structure**: wFirma uses indexed containers like:
  ```json
  {
    "status": {"code": "OK"},
    "company_accounts": {
      "0": {"company_account": {...}},
      "1": {"company_account": {...}}
    }
  }
  ```

### Test Patterns
- **Mock Structure**: All tests use `respx.mock` with `httpx.Response` mocking
- **Expected Params**: GET requests expect `outputFormat=json` and `company_id={company_id}` query params
- **Empty Result Handling**: Always include test for empty result (empty dict `{}` in container)
- **Client Property Tests**: Always test both "returns correct type" and "caches instance" (ensures `first is second`)

### Key Insights
- Wave 2 resources are intentionally simple (read-only, dict-returning) → perfect for parallel execution
- Exact pattern replication from Tags resource ensures consistency
- Container/object key discovery from API spec is non-negotiable (can't guess or assume)
- TDD approach caught import/export issues before running implementation

## Task 3: Invoice Methods Implementation (2026-02-18)

### What We Did
Implemented 4 missing invoice methods in both sync and async InvoicesResource:
- `download(invoice_id, parameters=None) -> bytes` - Download invoice as PDF
- `send(invoice_id, parameters=None) -> dict[str, Any]` - Send invoice via email
- `fiscalize(invoice_id) -> dict[str, Any]` - Mark invoice as fiscalized
- `unfiscalize(invoice_id) -> dict[str, Any]` - Remove fiscalization

### Key Technical Discoveries

#### 1. Client Method Signatures Matter
- `post_binary(path, data=None)` - `data` is **optional** (`dict[str, Any] | None`)
- `post_json(path, data)` - `data` is **required** (`dict[str, Any]`)
- `get_json(path)` - No data payload needed

This difference caused the initial mypy error:
```python
# ❌ WRONG - mypy error because payload could be None
payload: dict[str, Any] | None = None
if parameters:
    payload = {"invoices": [{"parameters": parameters}]}
return self._client.post_json(path, data=payload)  # ERROR: None not assignable to dict[str, Any]

# ✅ CORRECT - initialize to empty dict instead
payload: dict[str, Any] = {}
if parameters:
    payload = {"invoices": [{"parameters": parameters}]}
return self._client.post_json(path, data=payload)  # OK: always dict[str, Any]
```

#### 2. Method Classification by Return Type
- **Binary methods** (`download`): Use `post_binary()`, return `bytes`
- **JSON methods** (`send`, `fiscalize`, `unfiscalize`): Use `post_json()`/`get_json()`, return `dict[str, Any]`

#### 3. Parameter Wrapping Pattern
When optional parameters are provided:
```python
{"invoices": [{"parameters": parameters}]}
```

When no parameters (for `post_json` which requires data):
```python
{}  # Empty dict, not None
```

#### 4. Endpoint HTTP Methods
Not all invoice endpoints use POST:
- `POST /invoices/download/{id}` - Binary download (requires POST for payload)
- `POST /invoices/send/{id}` - Email send (requires POST for payload)
- `GET /invoices/fiscalize/{id}` - Simple state change (no payload needed)
- `GET /invoices/unfiscalize/{id}` - Simple state change (no payload needed)

### Code Pattern Established

**For binary downloads:**
```python
def download(self, invoice_id: int, *, parameters: dict[str, Any] | None = None) -> bytes:
    payload: dict[str, Any] | None = None
    if parameters:
        payload = {"invoices": [{"parameters": parameters}]}
    return self._client.post_binary(f"/invoices/download/{invoice_id}", data=payload)
```

**For POST returning JSON with optional parameters:**
```python
def send(self, invoice_id: int, *, parameters: dict[str, Any] | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {}  # Initialize to empty dict, NOT None
    if parameters:
        payload = {"invoices": [{"parameters": parameters}]}
    return self._client.post_json(f"/invoices/send/{invoice_id}", data=payload)
```

**For simple GET endpoints:**
```python
def fiscalize(self, invoice_id: int) -> dict[str, Any]:
    return self._client.get_json(f"/invoices/fiscalize/{invoice_id}")
```

### Test Results
- ✅ 24/24 tests passed (12 sync + 12 async)
- ✅ 100% coverage on both invoice resource files (50 statements each, 0 missed)
- ✅ Zero mypy errors
- ✅ Zero ruff lint issues

### Files Modified
1. `src/wfirma/sync/resources/invoices.py` - Added 4 methods (lines 90-157)
2. `src/wfirma/async_/resources/invoices.py` - Added 4 async methods (lines 90-157)

### Verification Commands Used
```bash
# Type checking
uv run mypy src/wfirma/sync/resources/invoices.py src/wfirma/async_/resources/invoices.py --show-error-codes

# Tests
uv run pytest tests/sync/resources/test_sync_invoices_resource.py tests/async_/resources/test_async_invoices_resource.py -v

# Linting
uv run ruff check src/wfirma/sync/resources/invoices.py src/wfirma/async_/resources/invoices.py
```

### Evidence
Saved to: `.sisyphus/evidence/task-3-invoice-methods-complete.txt`

### Next Steps
Task 3 (Invoice endpoints) is now complete. Ready to move to Wave 2 (Tasks 4-18: read-only resources).

