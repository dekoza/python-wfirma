"""(Disabled) Sync token store tests.

This file is intentionally NOT collected by pytest.

Reason:
    Having both tests/sync/test_token_store.py and tests/async_/test_token_store.py
    causes a pytest "import file mismatch" error due to identical module names.

Actual tests live in:
    - tests/sync/test_sync_token_store.py
    - tests/async_/test_token_store.py
"""

from __future__ import annotations

__test__ = False
