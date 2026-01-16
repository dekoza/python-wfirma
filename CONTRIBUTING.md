# Contributing to python-wfirma

Thank you for your interest in contributing to python-wfirma! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Workflow](#development-workflow)
- [Testing Guidelines](#testing-guidelines)
- [Code Style](#code-style)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [NOAI System](#noai-system)

---

## Code of Conduct

This project follows a standard code of conduct:

- Be respectful and inclusive
- Welcome newcomers and help them get started
- Accept constructive criticism gracefully
- Focus on what is best for the community
- Show empathy towards other community members

---

## Getting Started

### Prerequisites

- Python 3.12 or higher
- Git
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer

### Setting Up Development Environment

1. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   # or: pip install uv
   ```

2. **Fork and clone the repository**:
   ```bash
   git clone https://github.com/yourusername/python-wfirma.git
   cd python-wfirma
   ```

3. **Create virtual environment and install dependencies**:
   ```bash
   uv venv
   uv pip install -e ".[dev,docs,examples]"
   ```

   Note: `uv` automatically manages the virtual environment. To activate manually:
   ```bash
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```


4. **Install pre-commit hooks**:
   ```bash
   uv run pre-commit install
   ```

5. **Verify installation**:
   ```bash
   uv run pytest
   uv run ruff check src
   uv run mypy src
   ```

---

## Development Workflow

This project follows **Test-Driven Development (TDD)**:

1. **Write a failing test** for the new feature or bug fix
2. **Run tests** to confirm the test fails
3. **Implement** the minimal code to make the test pass
4. **Run tests** to confirm they pass
5. **Refactor** if needed while keeping tests green
6. **Mark test as AICOMPLETE** when feature is fully implemented
7. **Request review** from maintainers

### Branch Naming

- Feature: `feature/short-description`
- Bug fix: `fix/short-description`
- Documentation: `docs/short-description`
- Refactoring: `refactor/short-description`

### Example Workflow

```bash
# Create feature branch
git checkout -b feature/add-invoice-filtering

# Write failing test
# Edit: tests/sync/resources/test_invoices.py

# Run test (should fail)
pytest tests/sync/resources/test_invoices.py::test_filter_invoices_by_date

# Implement feature
# Edit: src/wfirma/sync/resources/invoices.py

# Run test (should pass)
pytest tests/sync/resources/test_invoices.py::test_filter_invoices_by_date

# Run all tests
pytest

# Check code quality
ruff check src tests
mypy src

# Commit changes
git add .
git commit -m "feat: add invoice filtering by date range"

# Push and create PR
git push origin feature/add-invoice-filtering
```

---

## Testing Guidelines

### Test Structure

Tests are organized by implementation type:

```
tests/
├── models/           # Pydantic model tests
├── sync/             # Synchronous implementation tests
├── async_/           # Asynchronous implementation tests
└── integration/      # Integration tests (optional)
```

### Writing Tests

1. **Use descriptive names**:
   ```python
   def test_create_invoice_with_multiple_line_items_calculates_total_correctly():
       ...
   ```

2. **Follow AAA pattern** (Arrange, Act, Assert):
   ```python
   def test_example():
       # Arrange
       client = WFirmaClient(...)
       invoice = Invoice(...)
       
       # Act
       result = client.invoices.create(invoice)
       
       # Assert
       assert result.id is not None
       assert result.total == expected_total
   ```

3. **Use fixtures** for common setup:
   ```python
   @pytest.fixture
   def mock_client():
       return MockWFirmaClient()
   ```

4. **Mock external calls** with respx:
   ```python
   def test_api_call(respx_mock):
       respx_mock.post("https://api.wfirma.pl/invoices").mock(
           return_value=httpx.Response(200, json={"id": "123"})
       )
       ...
   ```

### Test Markers

- `@pytest.mark.slow`: Slow-running tests
- `@pytest.mark.integration`: Integration tests requiring API access
- `@pytest.mark.aicomplete`: Tests ready for NOAI tagging
- `@pytest.mark.noai`: Immutable tests (protected from AI modifications)

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/sync/test_client.py

# Specific test
pytest tests/sync/test_client.py::test_authentication

# With coverage
pytest --cov=wfirma --cov-report=html

# Exclude slow tests
pytest -m "not slow"

# Only integration tests
pytest -m integration

# Parallel execution
pytest -n auto
```

---

## Code Style

### Python Style Guide

- Follow **PEP 8**
- Maximum line length: **100 characters**
- Use **type hints** for all functions
- Write **docstrings** for public API (Google style)

### Formatting

Code is automatically formatted with **ruff**:

```bash
# Format code
ruff format src tests examples

# Check formatting
ruff format --check src tests examples
```

### Linting

```bash
# Lint and auto-fix
ruff check --fix src tests examples

# Lint only
ruff check src tests examples
```

### Type Checking

```bash
# Type check source code
mypy src

# Type check specific file
mypy src/wfirma/sync/client.py
```

### Import Organization

Imports should be organized in three groups:
1. Standard library
2. Third-party packages
3. Local modules

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

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

### Examples

```
feat(invoices): add filtering by date range

Implemented date range filtering for invoice listing.
Supports both start_date and end_date parameters.

Closes #42
```

```
fix(auth): handle token expiration correctly

Fixed bug where expired tokens were not refreshed
automatically, causing authentication failures.

Fixes #58
```

---

## Pull Request Process

### Before Submitting

1. ✅ All tests pass (`pytest`)
2. ✅ Code is formatted (`ruff format`)
3. ✅ No linting errors (`ruff check`)
4. ✅ Type checks pass (`mypy src`)
5. ✅ Documentation updated (if applicable)
6. ✅ CHANGELOG.md updated
7. ✅ Commit messages follow conventions

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
Describe testing performed

## Checklist
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
- [ ] All tests pass
- [ ] Code formatted and linted
- [ ] Type checks pass
```

### Review Process

1. Automated checks run (CI)
2. Maintainer reviews code
3. Address feedback
4. Approval and merge

---

## NOAI System

### Overview

This project uses a **NOAI protection system** to ensure test stability:

- Tests marked with `# AICOMPLETE` are candidates for protection
- Tests marked with `# NOAI` are **immutable** to AI agents
- AI agents **cannot modify** NOAI tests
- Conflicts are logged in `_aidocs/NOAI_PROBLEMS_REPORT.md`

### AICOMPLETE Tag

When a test is fully implemented and verified:

```python
# AICOMPLETE: Invoice creation with validation - ready for review
def test_create_invoice_with_full_validation():
    ...
```

### NOAI Tag

After human review and approval:

```python
# NOAI: Invoice creation with validation - verified 2026-01-16
def test_create_invoice_with_full_validation():
    ...
```

### Important Notes

- **Only maintainers** should add NOAI tags
- NOAI tests should only be modified by humans
- If NOAI test needs changes, remove tag first
- Document reasons for removing NOAI protection

---

## Questions?

- 📫 Open an issue for questions
- 💬 Join discussions in GitHub Discussions
- 📖 Check documentation at [python-wfirma.readthedocs.io](https://python-wfirma.readthedocs.io)

---

Thank you for contributing to python-wfirma! 🎉

