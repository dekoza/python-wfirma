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

    assert wfirma.__version__ == "1.0b1"
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


def test_integration_readme_describes_beta_smoke_scope():
    """Test that the integration readme reflects the current beta contract."""
    readme = (REPO_ROOT / "tests" / "integration" / "README.md").read_text(encoding="utf-8")

    assert "1.0b1" in readme
    assert "WFIRMA_RUN_INTEGRATION=1 pytest" in readme
    assert "WFIRMA_OAUTH2_ACCESS_TOKEN" in readme


def test_authentication_docs_match_beta_public_api() -> None:
    """Test that authentication docs describe the real 1.0b1 API surface."""
    docs = (REPO_ROOT / "docs" / "authentication.rst").read_text(encoding="utf-8")

    assert "uses OAuth for authentication" not in docs
    assert "from wfirma import WFirmaClient" not in docs
    assert 'secret="your_secret"' not in docs
    assert "WFIRMA_ACCESS_KEY" in docs
    assert "WFIRMA_SECRET_KEY" in docs
    assert "``WFirmaClient`` supports API Key and OAuth 2.0 in 1.0b1" in docs
    assert "OAuth 1.0a helper flows remain available" in docs


def test_quickstart_docs_use_sandbox_for_default_client_examples() -> None:
    """Test that quickstart mocks match the sandbox default client environment."""
    docs = (REPO_ROOT / "docs" / "quickstart.rst").read_text(encoding="utf-8")

    assert "https://sandbox-api2.wfirma.pl/users/get/123" in docs
    assert "https://api2.wfirma.pl/users/get/123" not in docs


def test_troubleshooting_docs_do_not_claim_missing_features() -> None:
    """Test that troubleshooting docs do not promise behavior the library lacks."""
    docs = (REPO_ROOT / "docs" / "troubleshooting.rst").read_text(encoding="utf-8")

    assert "automatic retry with backoff" not in docs
    assert "last_response" not in docs
    assert "client.company.get_info()" not in docs
    assert "client.company.switch(company_id)" not in docs
    assert "Version 0.1.x" not in docs
    assert "1.0b1" in docs


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
    assert wfirma_config_data["environment"] == "sandbox"

    assert api_key_auth_data["access_key"] == "test_access_key"
    assert api_key_auth_data["secret_key"] == "test_secret_key"
    assert api_key_auth_data["app_key"] == "test_app_key"
