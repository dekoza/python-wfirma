#!/bin/bash
# Phase 0 Verification Script
# Run this to verify that Phase 0 setup is complete

# Change to project root if running from _aidocs
if [[ $(basename "$PWD") == "_aidocs" ]]; then
    cd ..
fi

echo "=================================================="
echo "Phase 0 Verification - python-wfirma"
echo "Working directory: $(pwd)"
echo "=================================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# Function to check command
check_command() {
    if eval "$1" > /dev/null 2>&1; then
        echo -e "${GREEN}✅${NC} $2"
    else
        echo -e "${RED}❌${NC} $2"
        FAILED=$((FAILED + 1))
    fi
}

# Check Python version
echo "Checking Python version..."
check_command "python --version | grep -q 'Python 3.1[2-9]'" "Python 3.12+"

# Check uv installation
echo "Checking uv installation..."
check_command "uv --version" "uv package manager"

# Check virtual environment
echo "Checking virtual environment..."
check_command "test -d .venv" "Virtual environment exists"

# Check package installation
echo "Checking package installation..."
check_command "uv run python -c 'import wfirma'" "Package importable"

# Check dependencies
echo "Checking dependencies..."
check_command "uv run python -c 'import httpx'" "httpx installed"
check_command "uv run python -c 'import anyio'" "anyio installed"
check_command "uv run python -c 'import pydantic'" "pydantic installed"
check_command "uv run python -c 'import pydantic_xml'" "pydantic-xml installed"
check_command "uv run python -c 'import pytest'" "pytest installed"

# Run tests
echo "Running tests..."
if uv run pytest tests/test_setup.py -q > /tmp/pytest_verify.txt 2>&1; then
    echo -e "${GREEN}✅${NC} Tests passing ($(grep -o '[0-9]* passed' /tmp/pytest_verify.txt))"
else
    echo -e "${RED}❌${NC} Tests failing"
    FAILED=$((FAILED + 1))
fi

# Check linting
echo "Checking code quality..."
if uv run ruff check src tests > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} Ruff linting (0 errors)"
else
    echo -e "${RED}❌${NC} Ruff linting (has errors)"
    FAILED=$((FAILED + 1))
fi

# Check type checking
echo "Checking type hints..."
if uv run mypy src > /dev/null 2>&1; then
    echo -e "${GREEN}✅${NC} Mypy type checking (0 errors)"
else
    echo -e "${RED}❌${NC} Mypy type checking (has errors)"
    FAILED=$((FAILED + 1))
fi

# Check documentation files
echo "Checking documentation..."
check_command "test -f README.md" "README.md"
check_command "test -f CONTRIBUTING.md" "CONTRIBUTING.md"
check_command "test -f _aidocs/IMPLEMENTATION_PLAN.md" "IMPLEMENTATION_PLAN.md (in _aidocs)"
check_command "test -f ROADMAP.md" "ROADMAP.md"
check_command "test -f CHANGELOG.md" "CHANGELOG.md"
check_command "test -f LICENSE" "LICENSE"
check_command "test -f _aidocs/NOAI_PROBLEMS_REPORT.md" "NOAI_PROBLEMS_REPORT.md (in _aidocs)"
check_command "test -f _aidocs/PROJECT_STATUS.md" "PROJECT_STATUS.md (in _aidocs)"
check_command "test -f _aidocs/AI_WORKING_INSTRUCTIONS.md" "AI_WORKING_INSTRUCTIONS.md (in _aidocs)"

# Check configuration files
echo "Checking configuration files..."
check_command "test -f pyproject.toml" "pyproject.toml"
check_command "test -f tox.ini" "tox.ini"
check_command "test -f .gitignore" ".gitignore"
check_command "test -f .pre-commit-config.yaml" ".pre-commit-config.yaml"
check_command "test -f .env.example" ".env.example"

# Check directory structure
echo "Checking directory structure..."
check_command "test -d src/wfirma" "src/wfirma/"
check_command "test -d src/wfirma/sync" "src/wfirma/sync/"
check_command "test -d src/wfirma/async_" "src/wfirma/async_/"
check_command "test -d src/wfirma/models" "src/wfirma/models/"
check_command "test -d tests" "tests/"
check_command "test -d docs" "docs/"
check_command "test -d examples" "examples/"
check_command "test -d scripts" "scripts/"
check_command "test -d .github/workflows" ".github/workflows/"
check_command "test -d _aidocs" "_aidocs/"

echo ""
echo "=================================================="
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Phase 0 Complete - All checks passed!${NC}"
    echo ""
    echo "Next steps:"
    echo "  1. Read _aidocs/START_HERE.md for overview"
    echo "  2. Review _aidocs/IMPLEMENTATION_PLAN.md for Phase 1"
    echo "  3. Begin Phase 1: API Documentation Scraping"
    echo ""
    echo "Ready to start Phase 1! 🚀"
else
    echo -e "${RED}❌ Phase 0 Incomplete - $FAILED check(s) failed${NC}"
    echo ""
    echo "Please fix the failed checks before proceeding."
fi
echo "=================================================="

