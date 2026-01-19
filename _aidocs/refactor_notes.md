# Refactor Notes - Auth Tokens and Timestamp Mixin

## Summary
- Introduced shared token utilities in `src/wfirma/auth/common.py` (TokenStore, MemoryTokenStore, FileTokenStore, OAuthToken).
- Sync/async auth modules now alias shared `OAuthToken` to preserve equality; `APIKeyAuth` remains per-module.
- Added `TimestampedFieldsMixin` in `wfirma.models.base` and applied across models to deduplicate `created`/`modified` fields.
- Added tests for the mixin; ensured model exports include the mixin.
- Full test suite passing via `uv run pytest`.

## Files touched (key)
- `src/wfirma/auth/common.py`, `src/wfirma/auth/__init__.py`
- `src/wfirma/sync/auth.py`, `src/wfirma/async_/auth.py`
- `src/wfirma/models/base.py` (+ mixin), `src/wfirma/models/__init__.py`
- Models updated to use mixin: company, contractor, good, invoice, payment, warehouse, employee.
- Tests updated: `tests/models/test_base.py` (mixin coverage); token store tests continue to pass.

## Rationale
- Removes duplicated token store and OAuth token definitions between sync/async modules.
- Centralizes timestamp field definitions to reduce repeated declarations across models.

## Next steps
- If future auth workflows require async-specific token refresh, extend common module with shared logic and keep interface stable.
- Consider documenting token storage usage in user-facing docs once OAuth flows are implemented.

