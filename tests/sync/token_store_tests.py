"""Sync token store tests.

This file exists to avoid pytest import-mismatch issues caused by having
multiple test modules with the same basename across different folders.

Pytest will still collect tests from this module.
"""

from __future__ import annotations

from .test_sync_token_store import TestMemoryTokenStore  # noqa: F401

