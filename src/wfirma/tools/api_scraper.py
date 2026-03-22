"""Utilities for scraping the public wFirma API documentation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import httpx


class WFirmaAPIScraper:
    """Scrape and normalize the public wFirma Postman collection."""

    COLLECTION_URL = (
        "https://doc.wfirma.pl/api/collections/10072824/UVJfkvxJ"
        "?segregateAuth=true&versionTag=latest"
    )
    BASE_URL = "https://api2.wfirma.pl"

    def fetch_collection(self) -> dict[str, Any]:
        """Fetch the public Postman collection."""
        response = httpx.get(self.COLLECTION_URL, timeout=30.0)
        response.raise_for_status()
        collection = response.json()
        if not isinstance(collection, dict):
            raise ValueError("Expected the Postman collection payload to be a JSON object.")
        return collection

    def extract_endpoints(self, collection: dict[str, Any]) -> list[dict[str, Any]]:
        """Extract endpoints from a Postman collection payload."""
        endpoints: list[dict[str, Any]] = []

        def process_item(item: dict[str, Any], parent_path: str = "") -> None:
            if "item" in item:
                folder_name = item.get("name", "")
                group_path = f"{parent_path}/{folder_name}" if parent_path else folder_name
                for subitem in item["item"]:
                    process_item(subitem, group_path)
                return

            request_data = item.get("request", {})
            if not isinstance(request_data, dict):
                return

            url = request_data.get("url", {})
            if isinstance(url, dict):
                path = "/".join(url.get("path", []))
            elif isinstance(url, str):
                path = url.replace(self.BASE_URL, "")
            else:
                path = ""

            endpoints.append(
                {
                    "name": item.get("name", ""),
                    "method": request_data.get("method", "GET"),
                    "path": f"/{path}" if path and not path.startswith("/") else path,
                    "description": item.get("description", ""),
                    "group": parent_path,
                    "request": request_data,
                }
            )

        for item in collection.get("item", []):
            process_item(item)

        return endpoints

    def extract_authentication(self, collection: dict[str, Any]) -> dict[str, Any]:
        """Extract authentication hints from the collection metadata."""
        auth_types: list[str] = []

        def add_auth_type(auth_type: str) -> None:
            if auth_type not in auth_types:
                auth_types.append(auth_type)

        collection_auth = collection.get("auth")
        if isinstance(collection_auth, dict):
            auth_type = collection_auth.get("type")
            if isinstance(auth_type, str) and auth_type:
                add_auth_type(auth_type)

        description = collection.get("info", {}).get("description", "")
        description_lower = description.lower()

        if "api key" in description_lower:
            add_auth_type("apikey")
        if "oauth 1.0a" in description_lower or "oauth1" in description_lower:
            add_auth_type("oauth1")
        if "oauth 2.0" in description_lower or "oauth2" in description_lower:
            add_auth_type("oauth2")

        return {
            "types": auth_types,
            "description": description,
        }

    def create_api_spec(self, collection: dict[str, Any]) -> dict[str, Any]:
        """Create a normalized API specification from the collection."""
        return {
            "name": collection.get("info", {}).get("name", "wFirma API"),
            "description": collection.get("info", {}).get("description", ""),
            "base_url": self.BASE_URL,
            "authentication": self.extract_authentication(collection),
            "endpoints": self.extract_endpoints(collection),
            "version": collection.get("info", {}).get("schema", ""),
        }

    def save_spec(self, spec: dict[str, Any], output_path: Path) -> None:
        """Save a structured API specification as JSON."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(
            json.dumps(spec, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def generate_markdown(self, spec: dict[str, Any], output_path: Path) -> None:
        """Generate a human-readable Markdown reference from the spec."""
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
            "## Endpoints",
            "",
        ]

        grouped_endpoints: dict[str, list[dict[str, Any]]] = {}
        for endpoint in spec["endpoints"]:
            group = endpoint["group"] or "General"
            grouped_endpoints.setdefault(group, []).append(endpoint)

        for group, endpoints in sorted(grouped_endpoints.items()):
            lines.extend([f"### {group}", ""])
            for endpoint in endpoints:
                lines.extend(
                    [
                        f"#### {endpoint['name']}",
                        "",
                        f"**Method:** `{endpoint['method']}`",
                        "",
                        f"**Path:** `{endpoint['path']}`",
                        "",
                    ]
                )
                if endpoint.get("description"):
                    lines.extend([f"**Description:** {endpoint['description']}", ""])
                lines.extend(["---", ""])

        output_path.write_text("\n".join(lines), encoding="utf-8")


__all__ = ["WFirmaAPIScraper"]
