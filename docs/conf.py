# Configuration file for the Sphinx documentation builder.

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

import wfirma

# -- Project information -----------------------------------------------------

project = "python-wfirma"
copyright = "2026, Python wFirma Contributors"
author = "Python wFirma Contributors"
release = wfirma.__version__

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "myst_parser",
]

templates_path = ["_templates"]
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "api_reference.md",
]

# -- Options for HTML output -------------------------------------------------

html_theme = "sphinx_rtd_theme"

# Keep static path empty to avoid warnings when `_static` directory is missing.
html_static_path: list[str] = []

# -- Extension configuration -------------------------------------------------

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Intersphinx
# NOTE: Documentation builds for this repo may run in restricted/offline
# environments. Keep mappings that are reliable, and avoid ones that cause
# hard failures when `-W` is enabled.
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
}

# MyST parser
myst_enable_extensions = [
    "colon_fence",
    "deflist",
]
