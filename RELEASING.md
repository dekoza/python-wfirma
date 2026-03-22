# Releasing python-wfirma

This project does not earn a release by passing a single local test run. Every release must follow the same checklist, or the version number is fiction.

## Release Levels

### Beta blockers

- Packaging or installation is broken.
- Documentation contradicts shipped behavior.
- Any supported auth mode is broken.
- The packaged `wfirma` CLI does not work after install.

### RC blockers

- Any public API rename or incompatible behavior change after the RC cut.
- Sync and async clients behave differently without documentation.
- Any release checklist step fails.
- Examples or docs drift from shipped code.

### Stable blockers

- Any known auth ambiguity remains unresolved.
- Packaging or install behavior is still ambiguous.
- Docs still push users into risky production writes without warning.
- Manual verification procedure is missing or has not been run.

## Release Checklist

Run all commands from a clean working tree.

### 1. Quality gates

```bash
uv run pytest -q
uv run ruff check src tests
uv run mypy src
```

### 2. Packaging

```bash
rm -f dist/*
uv build
uv tool run twine check dist/*
```

### 3. Fresh install verification

Verify both artifacts outside the active development environment.

```bash
python -m venv .venv-release-check
. .venv-release-check/bin/activate
pip install dist/python_wfirma-*.whl
python -m wfirma.cli --help
deactivate
rm -rf .venv-release-check

python -m venv .venv-release-check
. .venv-release-check/bin/activate
pip install dist/python_wfirma-*.tar.gz
python -m wfirma.cli --help
deactivate
rm -rf .venv-release-check
```

### 4. Manual live verification

Use least-privilege production credentials only. These checks are read-only and manual by design.

Required environment variables:

```bash
export WFIRMA_APP_KEY='...'
export WFIRMA_ACCESS_KEY='...'
export WFIRMA_SECRET_KEY='...'
export WFIRMA_COMPANY_ID='123'
```

Run:

```bash
wfirma company show
wfirma tags list
wfirma terms list
wfirma warehouses list
```

Success criteria:

- commands exit with status `0`
- the API returns readable tables or valid JSON when requested
- no write operation is required

### 5. Metadata and release notes

Before tagging:

- `README.md` matches shipped behavior
- `CHANGELOG.md` reflects the upcoming release
- `ROADMAP.md` reflects the next milestone, not the one already shipped
- release notes summarize user-visible changes and known limits

## Release Policy

- `1.0b2`: hardening only, no broad new feature work
- `1.0rc1`: API freeze starts here
- `1.0.0`: publish only if RC validation is clean and no blockers remain

## Public API freeze scope

The `1.0rc1` freeze covers these public surfaces:

- import paths under `wfirma`, `wfirma.sync`, and `wfirma.async_`
- auth constructors and required parameters
- exception classes and their intended semantics
- client defaults and production-only environment model
- CLI command names and flags

After `1.0rc1`, changes to these surfaces are blockers unless they fix a release-critical defect.
