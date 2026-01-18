#!/usr/bin/env python3
"""
Scraper for wFirma API documentation from Postman collection.

This script fetches the public Postman collection for wFirma API,
extracts all endpoints, authentication requirements, and generates
structured documentation.
"""

import json
from pathlib import Path
from typing import Any

import httpx


class WFirmaAPIScraper:
    """Scraper for wFirma API documentation."""

    COLLECTION_URL = (
        "https://doc.wfirma.pl/api/collections/10072824/UVJfkvxJ"
        "?segregateAuth=true&versionTag=latest"
    )
    BASE_URL = "https://api2.wfirma.pl"

    def fetch_collection(self) -> dict[str, Any]:
        """
        Fetch Postman collection from wFirma documentation.

        Returns:
            Dictionary containing the Postman collection structure

        Raises:
            httpx.HTTPError: If fetching fails
        """
        response = httpx.get(self.COLLECTION_URL, timeout=30.0)
        response.raise_for_status()
        return response.json()

    def extract_endpoints(self, collection: dict[str, Any]) -> list[dict[str, Any]]:
        """
        Extract all API endpoints from Postman collection.

        Args:
            collection: Postman collection dictionary

        Returns:
            List of endpoint dictionaries with name, method, path, etc.
        """
        endpoints = []

        def process_item(item: dict[str, Any], parent_path: str = "") -> None:
            """Recursively process collection items."""
            if "item" in item:
                # This is a folder/group
                folder_name = item.get("name", "")
                new_path = f"{parent_path}/{folder_name}" if parent_path else folder_name

                for subitem in item["item"]:
                    process_item(subitem, new_path)
            else:
                # This is an endpoint
                request_data = item.get("request", {})
                if isinstance(request_data, dict):
                    method = request_data.get("method", "GET")
                    url = request_data.get("url", {})

                    if isinstance(url, dict):
                        path = "/".join(url.get("path", []))
                    elif isinstance(url, str):
                        path = url.replace(self.BASE_URL, "")
                    else:
                        path = ""

                    endpoint = {
                        "name": item.get("name", ""),
                        "method": method,
                        "path": f"/{path}" if path and not path.startswith("/") else path,
                        "description": item.get("description", ""),
                        "group": parent_path,
                        "request": request_data,
                    }
                    endpoints.append(endpoint)

        # Process all items in collection
        for item in collection.get("item", []):
            process_item(item)

        return endpoints

    def extract_authentication(self, collection: dict[str, Any]) -> dict[str, Any]:
        """
        Extract authentication requirements from collection.

        Args:
            collection: Postman collection dictionary

        Returns:
            Dictionary with authentication information
        """
        auth_info = {
            "types": [],
            "description": "",
        }

        # Check collection-level auth
        if "auth" in collection:
            auth_type = collection["auth"].get("type")
            if auth_type:
                auth_info["types"].append(auth_type)

        # Extract from description
        description = collection.get("info", {}).get("description", "")

        # Parse authentication methods from description
        if "API Key" in description and "API Key" not in auth_info["types"]:
            auth_info["types"].append("apikey")

        if "OAuth" in description or "oauth" in description.lower():
            if "oauth1" not in auth_info["types"] and "OAuth 1.0a" in description:
                auth_info["types"].append("oauth1")
            if "oauth2" not in auth_info["types"] and "Oauth 2.0" in description:
                auth_info["types"].append("oauth2")

        auth_info["description"] = description

        return auth_info

    def create_api_spec(self, collection: dict[str, Any]) -> dict[str, Any]:
        """
        Create structured API specification from collection.

        Args:
            collection: Postman collection dictionary

        Returns:
            Structured API specification
        """
        endpoints = self.extract_endpoints(collection)
        auth = self.extract_authentication(collection)

        spec = {
            "name": collection.get("info", {}).get("name", "wFirma API"),
            "description": collection.get("info", {}).get("description", ""),
            "base_url": self.BASE_URL,
            "authentication": auth,
            "endpoints": endpoints,
            "version": collection.get("info", {}).get("schema", ""),
        }

        return spec

    def save_spec(self, spec: dict[str, Any], output_path: Path) -> None:
        """
        Save structured API specification to JSON file.

        Args:
            spec: API specification dictionary
            output_path: Path to output JSON file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(spec, f, indent=2, ensure_ascii=False)

    def generate_markdown(self, spec: dict[str, Any], output_path: Path) -> None:
        """
        Generate human-readable markdown documentation.

        Args:
            spec: API specification dictionary
            output_path: Path to output markdown file
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)

        lines = [
            f"# {spec['name']} Reference",
            "",
            "## Overview",
            "",
            f"**Base URL:** `{spec['base_url']}`",
            "",
            "## Authentication",
            "",
            f"Supported authentication methods: {', '.join(spec['authentication']['types'])}",
            "",
        ]

        # Group endpoints by group
        grouped_endpoints: dict[str, list[dict[str, Any]]] = {}
        for endpoint in spec["endpoints"]:
            group = endpoint["group"] or "General"
            if group not in grouped_endpoints:
                grouped_endpoints[group] = []
            grouped_endpoints[group].append(endpoint)

        lines.append("## Endpoints")
        lines.append("")

        for group, endpoints in sorted(grouped_endpoints.items()):
            lines.append(f"### {group}")
            lines.append("")

            for endpoint in endpoints:
                lines.append(f"#### {endpoint['name']}")
                lines.append("")
                lines.append(f"**Method:** `{endpoint['method']}`")
                lines.append("")
                lines.append(f"**Path:** `{endpoint['path']}`")
                lines.append("")

                if endpoint.get("description"):
                    lines.append(f"**Description:** {endpoint['description']}")
                    lines.append("")

                lines.append("---")
                lines.append("")

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def main() -> None:
    """Main entry point for the scraper script."""
    scraper = WFirmaAPIScraper()

    print("Fetching wFirma API collection...")
    collection = scraper.fetch_collection()
    print(f"✓ Fetched collection: {collection['info']['name']}")

    print("\nCreating API specification...")
    spec = scraper.create_api_spec(collection)
    print(f"✓ Found {len(spec['endpoints'])} endpoints")
    print(f"✓ Authentication methods: {', '.join(spec['authentication']['types'])}")

    # Save structured spec
    docs_dir = Path(__file__).parent.parent / "docs"
    spec_path = docs_dir / "api_spec.json"

    print(f"\nSaving specification to {spec_path}...")
    scraper.save_spec(spec, spec_path)
    print("✓ Saved api_spec.json")

    # Generate markdown documentation
    md_path = docs_dir / "api_reference.md"
    print(f"\nGenerating markdown documentation to {md_path}...")
    scraper.generate_markdown(spec, md_path)
    print("✓ Saved api_reference.md")

    print("\n✅ API documentation scraping completed successfully!")


if __name__ == "__main__":
    main()
