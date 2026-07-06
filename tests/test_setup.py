"""Basic sanity tests to verify project setup."""

from __future__ import annotations

import importlib.util
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]


def _load_docs_conf():
    conf_path = REPO_ROOT / "docs" / "conf.py"
    spec = importlib.util.spec_from_file_location("wfirma_docs_conf", conf_path)
    assert spec is not None
    assert spec.loader is not None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_project_setup():
    """Test that package version metadata stays aligned."""
    import wfirma

    docs_conf = _load_docs_conf()

    assert wfirma.__version__ == "1.0.0"
    assert docs_conf.release == wfirma.__version__


def test_pyproject_uses_dynamic_beta_version_metadata():
    """Test that build metadata reads the version from the package."""
    pyproject = tomllib.loads((REPO_ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    assert "version" not in pyproject["project"]
    assert "version" in pyproject["project"]["dynamic"]
    assert pyproject["tool"]["hatch"]["version"]["path"] == "src/wfirma/__init__.py"
    assert "Development Status :: 4 - Beta" in pyproject["project"]["classifiers"]


def test_gitignore_excludes_temporary_virtualenvs():
    """Test that local smoke-test virtualenvs do not leak into sdists."""
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

    assert ".venv*/" in gitignore or ".venv-smoke/" in gitignore


def test_integration_readme_describes_rc_smoke_scope():
    """Test that the integration readme reflects the current rc contract."""
    readme = (REPO_ROOT / "tests" / "integration" / "README.md").read_text(encoding="utf-8")

    assert "1.0rc2" in readme
    assert "WFIRMA_RUN_INTEGRATION=1 pytest" in readme
    assert "WFIRMA_OAUTH2_ACCESS_TOKEN" in readme


def test_authentication_docs_match_rc_public_api() -> None:
    """Test that authentication docs describe the real 1.0rc2 API surface."""
    docs = (REPO_ROOT / "docs" / "authentication.rst").read_text(encoding="utf-8")

    assert "uses OAuth for authentication" not in docs
    assert "from wfirma import WFirmaClient" not in docs
    assert 'secret="your_secret"' not in docs
    assert "WFIRMA_ACCESS_KEY" in docs
    assert "WFIRMA_SECRET_KEY" in docs
    assert "``WFirmaClient`` supports API Key, OAuth 2.0, and OAuth 1.0a in ``1.0rc2``." in docs
    assert "first-class ``WFirmaClient`` support is deferred" not in docs


def test_quickstart_docs_use_production_for_default_client_examples() -> None:
    """Test that quickstart mocks match the production default client environment."""
    docs = (REPO_ROOT / "docs" / "quickstart.rst").read_text(encoding="utf-8")

    assert "https://api2.wfirma.pl/users/get/123" in docs
    assert "https://sandbox-api2.wfirma.pl/users/get/123" not in docs


def test_troubleshooting_docs_do_not_claim_missing_features() -> None:
    """Test that troubleshooting docs do not promise behavior the library lacks."""
    docs = (REPO_ROOT / "docs" / "troubleshooting.rst").read_text(encoding="utf-8")

    assert "automatic retry with backoff" not in docs
    assert "last_response" not in docs
    assert "client.company.get_info()" not in docs
    assert "client.company.switch(company_id)" not in docs
    assert "Version 0.1.x" not in docs
    assert "1.0rc2" in docs


def test_releasing_guide_covers_release_checks_and_manual_verification() -> None:
    """Test that the release process is documented explicitly."""
    guide = (REPO_ROOT / "RELEASING.md").read_text(encoding="utf-8")

    assert "uv run pytest -q" in guide
    assert "uv run ruff check src tests" in guide
    assert "uv run mypy src" in guide
    assert "uv build" in guide
    assert "uv tool run twine check dist/*" in guide
    assert "python -m wfirma.cli --help" in guide
    assert "wfirma --help" not in guide
    assert "wfirma company show" in guide
    assert "wfirma tags list" in guide
    assert "Stable blockers" in guide
    assert "Public API freeze scope" in guide
    assert "## 1.0.0 Go/No-Go Checklist" in guide
    assert "No public API changes since `v1.0rc1` except blocker-class fixes." in guide
    assert "No known P0/P1 defects remain open." in guide
    assert "Tag and publish `1.0.0` only if every item above is a hard yes." in guide


def test_readme_prioritizes_safe_readonly_usage_and_release_hardening() -> None:
    """Test that the README reflects post-1.0b1 hardening priorities."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "## Production Use Checklist" in readme
    assert "## Choosing Auth Mode" in readme
    assert "## Handling API Errors" in readme
    assert "wfirma company show" in readme
    assert "mutate real production data" in readme


def test_release_metadata_reflects_rc_preparation_state() -> None:
    """Test that roadmap and changelog are ready for the rc release cut."""
    roadmap = (REPO_ROOT / "ROADMAP.md").read_text(encoding="utf-8")
    changelog = (REPO_ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    assert "Current target version: **1.0.0**." in roadmap
    assert "## 1.0b2 — Released" in roadmap
    assert "## 1.0rc1 — Released" in roadmap
    assert "## 1.0rc2 — Released" in roadmap
    assert "This branch is preparing the `1.0b1` beta release." not in changelog
    assert "## [1.0.0] - 2026-07-07" in changelog
    assert (
        "[Unreleased]: https://github.com/dekoza/python-wfirma/compare/v1.0.0...HEAD" in changelog
    )


def test_contributing_points_to_release_workflow() -> None:
    """Test that contributor docs link to the release process."""
    contributing = (REPO_ROOT / "CONTRIBUTING.md").read_text(encoding="utf-8")

    assert "RELEASING.md" in contributing


def test_docs_index_includes_migration_guide() -> None:
    """Test that published docs expose migration guidance."""
    index = (REPO_ROOT / "docs" / "index.rst").read_text(encoding="utf-8")

    assert "migration_guide" in index


def test_migration_guide_covers_beta_to_rc_changes() -> None:
    """Test that migration guidance exists for post-beta users."""
    guide = (REPO_ROOT / "docs" / "migration_guide.rst").read_text(encoding="utf-8")

    assert "1.0b1" in guide
    assert "1.0b2" in guide
    assert "production-only environment model" in guide
    assert "OAuth1Auth" in guide
    assert "wfirma company show" in guide


def test_readme_mentions_rc_freeze_scope() -> None:
    """Test that the README tells users what remains frozen for rc2."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "> **Status**: Release candidate (`1.0rc2`)." in readme
    assert "## Stability Policy" in readme
    assert "1.0rc2" in readme
    assert "CLI command names and flags" in readme


def test_readme_does_not_advertise_unconfigured_parallel_pytest() -> None:
    """Test that the README only documents supported test commands."""
    readme = (REPO_ROOT / "README.md").read_text(encoding="utf-8")

    assert "pytest -n auto" not in readme
    assert "WFIRMA_ACCESS_KEY" in readme
    assert "WFIRMA_SECRET_KEY" in readme


def test_fixture_availability(wfirma_config_data, api_key_auth_data):
    """Test that pytest fixtures are available."""
    assert wfirma_config_data["app_key"] == "test_app_key"
    assert wfirma_config_data["app_secret"] == "test_app_secret"
    assert wfirma_config_data["environment"] == "production"

    assert api_key_auth_data["access_key"] == "test_access_key"
    assert api_key_auth_data["secret_key"] == "test_secret_key"
    assert api_key_auth_data["app_key"] == "test_app_key"
