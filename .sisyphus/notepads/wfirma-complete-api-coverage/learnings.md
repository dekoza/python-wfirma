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
