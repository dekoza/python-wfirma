# 📦 Phase 4.3: Migrate OAuth implementation to Authlib (Plan)

**Project:** python-wfirma  
**Status:** 🟡 PLANNED  
**Owner:** Maintainers / AI agent  
**Last Updated:** 2026-01-19  

> This document describes the plan to migrate OAuth support from the current
> in-house implementation to an Authlib-based implementation.
>
> Backwards compatibility is **not required** because the library is in early
> development and has no real users yet.

---

## 1. Goals

1. Use **Authlib** as the OAuth implementation backend.
2. Keep sync/async support.
3. Keep the public API of `WFirmaClient` clean and consistent.
4. Provide a robust **OAuth2** story:
   - Authorization Code flow
   - Refresh tokens
   - Concurrency-safe refresh in async contexts
5. Keep **OAuth1 PLAINTEXT** support for wFirma (required by the upstream API).

Non-goals:
- Supporting multiple OAuth providers (wFirma only).
- Preserving the exact current public API shape in `wfirma.sync.auth` / `wfirma.async_.auth`.

---

## 2. Current State (Baseline)

### 2.1 In-house OAuth modules

- `src/wfirma/auth/common.py`
  - `TokenStore` protocol
  - `MemoryTokenStore`, `FileTokenStore`
  - `OAuthToken` dataclass
  - OAuth1 helpers:
    - `sign_oauth1_plaintext()`
    - `build_oauth1_authorization_header()`

- `src/wfirma/sync/auth.py` and `src/wfirma/async_/auth.py`
  - `OAuth1Auth` and `OAuth2Auth`
  - Authorization URL builder
  - Code exchange and refresh

### 2.2 Why migrate

Authlib provides:
- RFC-based OAuth1 and OAuth2 implementations.
- First-class `httpx` integrations:
  - `authlib.integrations.httpx_client.OAuth2Client` / `AsyncOAuth2Client`
  - `authlib.integrations.httpx_client.OAuth1Client` / `AsyncOAuth1Client`
- Built-in concurrency guard for async token refresh (`anyio.Lock`).

---

## 3. Target Design (Authlib-based)

### 3.1 New internal OAuth layer

Create a new internal module:

- `src/wfirma/oauth/_authlib.py`

Responsibilities:
- Wrap Authlib types and normalize them to our library's needs.
- Provide small, testable helpers:
  - Build OAuth2 authorization URL for wFirma
  - Exchange authorization code for token
  - Refresh access token
  - Provide an `httpx.Auth` (or header dict) for `WFirmaClient`

### 3.2 Token storage

Keep our own `TokenStore` protocol and implementations:
- `MemoryTokenStore`
- `FileTokenStore`

Reason:
- Our store abstraction is small and already tested.
- Authlib expects an `update_token` callback, which we can implement as an adapter
  that persists tokens using `TokenStore`.

### 3.3 Token model

Replace `wfirma.auth.common.OAuthToken` with an Authlib-compatible representation.

Options:
1. **Use Authlib dict tokens** internally (canonical in Authlib client API).
2. Provide a thin Pydantic model (or dataclass) for serialization and validation
   at the edges:
   - parse response dict -> validated model
   - store model -> dict

Preferred:
- Internally use a dict token in Authlib format, but keep a small validated model
  for persistence and stable typing.

### 3.4 Sync/Async public API

Create new public-facing auth helpers:

- `wfirma.sync.auth`:
  - `APIKeyAuth` stays as-is
  - `OAuth2Auth` becomes a thin wrapper over Authlib
  - `OAuth1Auth` becomes a thin wrapper over Authlib

- `wfirma.async_.auth`:
  - Same surface as sync, but using Authlib async clients

Notes:
- We are allowed to break backwards compatibility.
- We should aim for direct and explicit constructors.

---

## 4. Migration Steps (Incremental)

### Step 0 — Preparation

- Add `authlib` to runtime dependencies in `pyproject.toml`.
- Ensure `tox` environments install it (via project deps).

### Step 1 — Add Authlib adapters (new modules)

- Implement `wfirma.oauth._authlib` (internal).
- Implement conversion between:
  - stored token payload (our format)
  - Authlib token dict

### Step 2 — Rebuild OAuth2 on Authlib

- Build authorization URL for wFirma.
- Implement code exchange and refresh using Authlib OAuth2 client.
- Implement `update_token` callback that writes to our `TokenStore`.
- Provide `get_token()` which:
  - returns current token from store if valid
  - refreshes if expired

### Step 3 — Rebuild OAuth1 on Authlib

- Verify OAuth1 PLAINTEXT signing for wFirma.
- Implement OAuth1 request signing with Authlib httpx integration.

### Step 4 — Wire into `WFirmaClient`

- Ensure `_get_auth_headers()` supports:
  - APIKeyAuth
  - Authlib-based OAuth2Auth
  - Authlib-based OAuth1Auth (if we support it for main API calls)

### Step 5 — Remove old in-house OAuth flows

- Deprecate and then remove:
  - OAuth helpers that are fully replaced by Authlib.
- Keep `TokenStore` implementations if still used.

---

## 5. Testing Strategy

### 5.1 Unit tests

- Token parsing/validation.
- `update_token` callback writes to our `TokenStore`.
- Authorization URL generation.

### 5.2 Integration tests (HTTP mocked)

- Use `respx` to mock:
  - `/oauth2/token` exchange
  - refresh token responses
- Validate:
  - correct request body (grant_type, code, redirect_uri)
  - correct exceptions mapping

### 5.3 OAuth1 signature tests

- Create deterministic test vectors:
  - fixed nonce, timestamp
  - known consumer key/secret and token secret
- Compare the produced Authorization header to expected output.

---

## 6. Risk Register

| Risk | Impact | Mitigation |
|------|--------|------------|
| OAuth1 PLAINTEXT mismatch vs wFirma requirements | High | Add header-level golden tests; keep our current OAuth1 helper as fallback until verified |
| Authlib token dict shape differs from our persistence format | Medium | Introduce explicit token model + adapters |
| Async refresh concurrency issues | Medium | Use Authlib's lock + add tests to ensure single refresh |
| Increased dependency footprint | Medium | Keep Authlib as single OAuth dependency; watch CVEs |

---

## 7. Definition of Done

- ✅ All existing non-OAuth functionality still passes tests.
- ✅ OAuth2 flow covered by unit + mocked integration tests (sync + async).
- ✅ OAuth1 PLAINTEXT signing tested.
- ✅ Lint (`tox -e lint`) and typecheck (`tox -e type`) pass.
- ✅ Docs updated:
  - user docs (`docs/`) mention Authlib-based OAuth
  - internal docs (`_aidocs/`) include this migration phase


