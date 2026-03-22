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


def test_fixture_availability(wfirma_config_data, api_key_auth_data):
    """Test that pytest fixtures are available."""
    assert wfirma_config_data["app_key"] == "test_app_key"
    assert wfirma_config_data["app_secret"] == "test_app_secret"
    assert wfirma_config_data["environment"] == "sandbox"

    assert api_key_auth_data["access_key"] == "test_access_key"
    assert api_key_auth_data["secret_key"] == "test_secret_key"
    assert api_key_auth_data["app_key"] == "test_app_key"
