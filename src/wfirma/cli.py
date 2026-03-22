"""Minimal read-only CLI for manual wFirma API verification."""

from __future__ import annotations

import argparse
import json
import os
import sys
from collections.abc import Callable, Sequence
from contextlib import suppress
from dataclasses import asdict, is_dataclass
from typing import Any, Protocol, cast

from pydantic import BaseModel

from wfirma.exceptions import MissingConfigurationError, WFirmaException
from wfirma.sync import APIKeyAuth, WFirmaClient

LIST_RESOURCE_MAP = {
    "tags": "tags",
    "terms": "terms",
    "term-groups": "term_groups",
    "warehouses": "warehouses",
    "vat-codes": "vat_codes",
}

LABEL_FIELD_PRIORITY = (
    "name",
    "company_name",
    "description",
    "login",
    "code",
    "symbol",
)

LABEL_FIELD_DENYLIST = {
    "created",
    "modified",
    "url",
    "token",
    "nip",
    "email",
    "id",
}


class SupportsModelDump(Protocol):
    def model_dump(self, *, mode: str = "python") -> dict[str, Any]: ...


ClientFactory = Callable[[Any], Any]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wfirma")
    subparsers = parser.add_subparsers(dest="resource", required=True)

    company_parser = subparsers.add_parser("company")
    company_subparsers = company_parser.add_subparsers(dest="action", required=True)
    company_show = company_subparsers.add_parser("show")
    company_show.add_argument("--company-id", type=int)
    company_show.add_argument("--json", action="store_true", dest="json_output")

    for resource_name in LIST_RESOURCE_MAP:
        resource_parser = subparsers.add_parser(resource_name)
        resource_subparsers = resource_parser.add_subparsers(dest="action", required=True)
        list_parser = resource_subparsers.add_parser("list")
        list_parser.add_argument("--json", action="store_true", dest="json_output")

    return parser


def _to_plain_data(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if is_dataclass(value) and not isinstance(value, type):
        return asdict(value)
    if hasattr(value, "model_dump") and not isinstance(value, type):
        model_like = cast(SupportsModelDump, value)
        return model_like.model_dump(mode="json")
    if hasattr(value, "__dict__") and not isinstance(value, dict):
        return dict(vars(value))
    return value


def _extract_label(item: dict[str, Any]) -> str:
    for key in LABEL_FIELD_PRIORITY:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value

    for key, value in item.items():
        if key in LABEL_FIELD_DENYLIST:
            continue
        if isinstance(value, str) and value.strip():
            return value

    raise ValueError(f"No usable label field found for item with id={item.get('id')!r}.")


def _format_table(headers: Sequence[str], rows: Sequence[Sequence[str]]) -> str:
    widths = [len(header) for header in headers]
    for row in rows:
        for index, cell in enumerate(row):
            widths[index] = max(widths[index], len(cell))

    def format_row(row: Sequence[str]) -> str:
        return "  ".join(cell.ljust(widths[index]) for index, cell in enumerate(row))

    lines = [format_row(headers), format_row(["-" * width for width in widths])]
    lines.extend(format_row(row) for row in rows)
    return "\n".join(lines)


def _print_company(company: Any, *, json_output: bool) -> None:
    payload = _to_plain_data(company)
    if json_output:
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return

    rows = [[str(payload["id"]), str(payload["name"])]]
    print(_format_table(("ID", "Name"), rows))


def _print_list(items: list[dict[str, Any]], *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(items, indent=2, ensure_ascii=False))
        return

    rows = [[str(item.get("id", "")), _extract_label(item)] for item in items]
    print(_format_table(("ID", "Label"), rows))


def build_client_from_env(env: dict[str, str] | None = None) -> WFirmaClient:
    values = env if env is not None else dict(os.environ)
    required = [
        "WFIRMA_APP_KEY",
        "WFIRMA_ACCESS_KEY",
        "WFIRMA_SECRET_KEY",
    ]
    missing = [name for name in required if not values.get(name)]
    if missing:
        missing_list = ", ".join(missing)
        raise MissingConfigurationError(
            f"Missing required API key environment variables: {missing_list}."
        )

    company_id_raw = values.get("WFIRMA_COMPANY_ID")
    company_id = int(company_id_raw) if company_id_raw else None

    auth = APIKeyAuth(
        access_key=values["WFIRMA_ACCESS_KEY"],
        secret_key=values["WFIRMA_SECRET_KEY"],
        app_key=values["WFIRMA_APP_KEY"],
    )
    return WFirmaClient(auth=auth, company_id=company_id)


def main(
    argv: Sequence[str] | None = None,
    *,
    client_factory: ClientFactory | None = None,
) -> int:
    parser = _build_parser()
    args = parser.parse_args(list(argv) if argv is not None else None)

    if client_factory is None:
        client_creator = cast(ClientFactory, build_client_from_env)
        env_payload: dict[str, str] | argparse.Namespace = dict(os.environ)
    else:
        client_creator = client_factory
        env_payload = args

    try:
        client = client_creator(env_payload)
        try:
            if args.resource == "company" and args.action == "show":
                company = client.company.get(company_id=args.company_id)
                _print_company(company, json_output=args.json_output)
                return 0

            resource_name = LIST_RESOURCE_MAP[args.resource]
            resource = getattr(client, resource_name)
            items = [_to_plain_data(item) for item in resource.find()]
            _print_list(items, json_output=args.json_output)
            return 0
        finally:
            with suppress(AttributeError):
                client.close()
    except (WFirmaException, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
