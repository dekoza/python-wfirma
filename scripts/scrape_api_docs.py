#!/usr/bin/env python3
"""Fetch and save a local snapshot of the public wFirma API docs."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from wfirma.tools import WFirmaAPIScraper


def main() -> None:
    """Run the scraper and write JSON and Markdown outputs."""
    scraper = WFirmaAPIScraper()

    collection = scraper.fetch_collection()
    spec = scraper.create_api_spec(collection)
    docs_dir = PROJECT_ROOT / "docs"
    spec_path = docs_dir / "api_spec.json"
    scraper.save_spec(spec, spec_path)
    md_path = docs_dir / "api_reference.md"
    scraper.generate_markdown(spec, md_path)


if __name__ == "__main__":
    main()
