# AI Agent Working Instructions

**Project**: python-wfirma  
**Last Updated**: 2026-01-18

---

## Quick Reference

### Current Status
- **Phase**: Phase 3 (Data Models - NEXT)
- **Version**: 0.1.0-dev
- **Tests**: 74/74 passing, 98% coverage
- **NOAI Tests**: 0
- **AICOMPLETE Tests**: 72 (5 scraper + 25 exceptions + 42 config)

### Essential Files to Check Before Starting
1. `PROJECT_STATUS.md` - Current phase and todos
2. `IMPLEMENTATION_PLAN.md` - Detailed phase breakdown
3. `NOAI_PROBLEMS_REPORT.md` - Any blocked tests
4. `tests/` - Look for NOAI and AICOMPLETE tags

---

## Development Commands

### Testing
```bash
# Run all tests
uv run pytest

# Run specific test
uv run pytest tests/path/to/test_file.py::test_name -v

# Run with coverage
uv run pytest --cov=wfirma --cov-report=html

# Run without coverage (faster)
uv run pytest --no-cov
```

### Code Quality
```bash
# Lint
uv run ruff check src tests

# Format
uv run ruff format src tests

# Type check
uv run mypy src

# All checks
uv run tox -e lint,type
```

### Package Management
```bash
# Install dependencies
uv pip install -e ".[dev]"

# Add new dependency
# 1. Edit pyproject.toml
# 2. uv pip install -e ".[dev]"

# Update dependencies
uv pip install --upgrade -e ".[dev]"
```

---

## TDD Workflow (MANDATORY)

### For Each Feature:

1. **Write Test First** (MUST fail initially)
   ```python
   # tests/path/to/test_feature.py
   def test_new_feature_does_something():
       """Test that new feature does X when Y."""
       # Arrange
       ...
       # Act
       result = new_feature()
       # Assert
       assert result == expected
   ```

2. **Run Test** (verify it fails)
   ```bash
   uv run pytest tests/path/to/test_feature.py::test_new_feature_does_something -v
   ```

3. **Implement Minimal Code**
   ```python
   # src/wfirma/path/to/feature.py
   def new_feature():
       # Minimal implementation
       pass
   ```

4. **Run Test Again** (should pass)
   ```bash
   uv run pytest tests/path/to/test_feature.py::test_new_feature_does_something -v
   ```

5. **Refactor** (keep tests green)

6. **Mark as AICOMPLETE** (when fully implemented)
   ```python
   # AICOMPLETE: Feature X fully implemented with all edge cases - ready for review
   def test_new_feature_does_something():
       ...
   ```

7. **Run All Tests**
   ```bash
   uv run pytest
   ```

8. **Check Coverage**
   ```bash
   uv run pytest --cov=wfirma --cov-report=term-missing
   ```

---

## NOAI System Rules

### AICOMPLETE Tag
- **When**: Feature is fully implemented and tested
- **Format**: `# AICOMPLETE: Brief description - ready for review`
- **Action**: Mark test for human review

### NOAI Tag (Applied by Human)
- **Meaning**: Test is IMMUTABLE to AI
- **Format**: `# NOAI: Brief description - verified YYYY-MM-DD`
- **AI Actions**:
  - ❌ CANNOT modify test
  - ❌ CANNOT delete test
  - ❌ CANNOT refactor test
  - ✅ CAN read test
  - ✅ CAN use test as reference
  - ✅ CAN implement code to pass test

### If NOAI Test Fails
1. **DO NOT** modify the test
2. **Document** in `NOAI_PROBLEMS_REPORT.md`:
   ```markdown
   ### [YYYY-MM-DD HH:MM] Issue in test_file.py::test_name
   
   **Problem**: Brief description
   **Test Tagged NOAI**: Yes
   **Attempted Change**: What I wanted to do
   **Reason Blocked**: NOAI protection
   **Recommendation**: Suggested human action
   **Priority**: High
   **Status**: Open
   ```
3. **Notify** user about the blocker
4. **Continue** with other work if possible

---

## Terminal Fallback Strategy

If terminal hangs or doesn't respond:

```bash
# Instead of running directly:
command

# Use output redirection:
command > /tmp/wfirma_output.txt 2>&1

# Then read the file:
# Use read_file tool on /tmp/wfirma_output.txt
```

### Example:
```bash
# Instead of: uv run pytest
uv run pytest > /tmp/pytest_output.txt 2>&1
# Then: read_file("/tmp/pytest_output.txt")
```

---

## Import Organization (Mandatory)

Always organize imports in this order:

```python
# Standard library
import os
from typing import Optional

# Third-party (alphabetical)
import httpx
from pydantic import BaseModel

# Local (alphabetical)
from wfirma.exceptions import WFirmaException
from wfirma.models import Invoice
```

Use `uv run ruff check --fix` to auto-organize.

---

## Coding Standards

### Type Hints (Gradual Typing)
```python
# Public API - MUST have type hints
def create_invoice(invoice: Invoice) -> CreatedInvoice:
    ...

# Internal functions - SHOULD have type hints
def _validate_data(data: dict[str, Any]) -> bool:
    ...

# Tests - type hints optional
def test_something():
    ...
```

### Docstrings (Google Style)
```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.

    Longer description if needed.

    Args:
        param1: Description of param1.
        param2: Description of param2.

    Returns:
        Description of return value.

    Raises:
        ValueError: When something is invalid.

    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

### Error Handling
```python
# Use specific exceptions from wfirma.exceptions
from wfirma.exceptions import ValidationError, ResourceNotFoundError

def process_data(data):
    if not data:
        raise ValidationError("Data cannot be empty")
    
    try:
        result = api_call(data)
    except httpx.HTTPStatusError as e:
        if e.response.status_code == 404:
            raise ResourceNotFoundError(f"Resource not found: {data}")
        raise
```

---

## File Creation Rules

### When to Create New File
1. **Test file**: Always before implementation file
2. **Implementation file**: Only after test exists
3. **Model file**: When data structure is defined
4. **Documentation**: When feature is complete

### File Naming
- Tests: `test_<feature>.py`
- Implementation: `<feature>.py`
- Models: `<entity>.py` (singular)
- Resources: `<resource_plural>.py`

---

## Phase-Specific Instructions

### Current Phase: Phase 1 - API Documentation Scraping

**Location**: `scripts/scrape_api_docs.py`

**Steps**:
1. Create scraper script with Beautiful Soup
2. Target URL: https://doc.wfirma.pl/
3. Extract:
   - All endpoints (URLs, methods)
   - Authentication details
   - Request/response schemas
   - Error codes
   - Pagination info
4. Output:
   - `docs/api_reference.md` (human-readable)
   - `docs/api_spec.json` (structured data)
5. Write tests for scraper (if complex)
6. Run scraper
7. Verify output
8. Mark phase as complete

**Important**: If documentation is incomplete, ask user before proceeding!

---

## Quality Gates (Before Moving to Next Phase)

- [ ] All tests pass: `uv run pytest`
- [ ] Coverage ≥ 90%: `uv run pytest --cov=wfirma --cov-report=term`
- [ ] No lint errors: `uv run ruff check src tests`
- [ ] No type errors: `uv run mypy src`
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] Phase completion report created
- [ ] PROJECT_STATUS.md updated

---

## Emergency Contacts

If stuck or unsure:
1. Check `IMPLEMENTATION_PLAN.md` for detailed guidance
2. Check `CONTRIBUTING.md` for development guidelines
3. Check `NOAI_PROBLEMS_REPORT.md` for existing issues
4. **ASK USER** - Don't make assumptions!

---

## Remember

- ✅ **Tests before code** (TDD is mandatory)
- ✅ **NOAI tests are sacred** (never modify)
- ✅ **Small steps** (implement incrementally)
- ✅ **Ask when unsure** (no assumptions)
- ✅ **Document everything** (comments, docstrings, reports)
- ✅ **Quality over speed** (this is a professional library)

---

## Project-Specific Guidelines (python-wfirma)

### DateTime Handling

**IMPORTANT**: W tym projekcie **NIE używamy biblioteki `pendulum`**.

Zamiast tego używamy wbudowanego modułu `datetime` z biblioteki standardowej Python:

```python
# ✅ CORRECT - use standard library datetime
from datetime import datetime, timezone

def parse_wfirma_datetime(value: str) -> datetime | None:
    """Parse wFirma datetime format."""
    if not value or value == "0000-00-00 00:00:00":
        return None
    return datetime.strptime(value, "%Y-%m-%d %H:%M:%S")

def format_wfirma_datetime(dt: datetime) -> str:
    """Format datetime for wFirma API."""
    return dt.strftime("%Y-%m-%d %H:%M:%S")
```

```python
# ❌ WRONG - do not use pendulum
import pendulum  # FORBIDDEN in this project
```

**Powód**: `pydantic-xml` ma problemy z integracją `pendulum.DateTime` i wymaga skomplikowanej konfiguracji. Standardowy `datetime` działa out-of-the-box z Pydantic.

### XML Serialization (pydantic-xml)

Używając `pydantic-xml`, pamiętaj o jawnym oznaczaniu pól jako elementy XML:

```python
from pydantic_xml import BaseXmlModel, element

class Invoice(BaseXmlModel, tag="invoice"):
    # ✅ CORRECT - explicitly mark as XML element
    id: int = element()
    date: str = element()
    
    # ❌ WRONG - without element(), field becomes text content
    # name: str  # This will NOT be serialized as <name>value</name>
```

---

**Good luck with Phase 3!** 🚀

