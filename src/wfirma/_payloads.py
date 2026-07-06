"""Internal helpers for extracting payloads from wFirma JSON responses.

wFirma often wraps objects in a "container" key (e.g. "invoices") and then
returns either:

- an indexed mapping: {"0": {"invoice": {...}}, "1": {"invoice": {...}}}
- or a direct mapping: {"invoice": {...}}

These helpers standardize that parsing logic.

Note:
    This module is internal and not part of the public API.
"""

from __future__ import annotations

from typing import Any, cast


def extract_single_object_payload(
    *, data: dict[str, Any], container_key: str, object_key: str
) -> dict[str, Any]:
    """Extract a single object payload from a wFirma JSON response.

    Args:
        data: Parsed JSON response.
        container_key: Top-level container key (e.g. "invoices").
        object_key: Nested object key (e.g. "invoice").

    Returns:
        Object payload mapping.

    Raises:
        KeyError: If the payload cannot be located.
    """
    container = data.get(container_key)
    if isinstance(container, dict):
        first_item = next(iter(container.values()), None)
        if isinstance(first_item, dict):
            inner = first_item.get(object_key)
            if isinstance(inner, dict):
                return cast(dict[str, Any], inner)
        if object_key in container and isinstance(container[object_key], dict):
            return cast(dict[str, Any], container[object_key])

    raise KeyError(
        f"Unable to locate {object_key} payload in response (container={container_key!r})."
    )


def extract_object_list_payloads(
    data: dict[str, Any],
    container_key: str,
    object_key: str,
) -> list[dict[str, Any]]:
    """Extract a list of object payloads from an indexed wFirma container.

    Args:
        data: Parsed JSON response.
        container_key: Top-level container key (e.g. "payments").
        object_key: Nested object key (e.g. "payment").

    Returns:
        List of object payload mappings. Unknown shapes return an empty list.
    """
    container = data.get(container_key)
    if not isinstance(container, dict):
        return []

    payloads: list[dict[str, Any]] = []
    for key, item in container.items():
        if not key.isdigit():
            continue
        if not isinstance(item, dict):
            continue
        inner = item.get(object_key)
        if isinstance(inner, dict):
            payloads.append(inner)

    return payloads


def build_module_payload(
    *, container_key: str, object_key: str, obj: dict[str, Any]
) -> dict[str, Any]:
    """Wrap a single record in wFirma's JSON request envelope.

    Per doc.wfirma.pl ("Format wymiany danych"), request bodies nest records
    under the plural module branch, number each record by key (even a single
    one), and wrap it in the singular object branch::

        {"tags": {"0": {"tag": {...}}}}

    Args:
        container_key: Plural module branch (e.g. "tags").
        object_key: Singular object branch (e.g. "tag").
        obj: Record fields.

    Returns:
        The request body mapping.
    """
    return {container_key: {"0": {object_key: dict(obj)}}}


def build_parameters_payload(parameters: dict[str, Any]) -> dict[str, Any]:
    """Build a name/value ``parameters`` block in wFirma's JSON dialect.

    Used by action endpoints such as ``invoices/download`` and
    ``invoices/send``, whose XML bodies carry repeated ``parameter``
    branches::

        <parameters><parameter><name>page</name><value>all</value></parameter></parameters>

    In JSON, repeated branches must be numbered objects, so this maps to::

        {"parameters": {"0": {"parameter": {"name": "page", "value": "all"}}}}

    Args:
        parameters: Mapping of parameter names to values.

    Returns:
        The ``parameters`` mapping ready to nest under a module branch.
    """
    return {
        "parameters": {
            str(index): {"parameter": {"name": name, "value": value}}
            for index, (name, value) in enumerate(parameters.items())
        }
    }


def build_find_parameters(
    conditions: list[dict[str, Any]] | None,
    *,
    limit: int | None = None,
    page: int | None = None,
) -> dict[str, Any]:
    """Build a find ``parameters`` block in wFirma's JSON dialect.

    Repeated branches in JSON payloads must be numbered objects, not arrays
    (see doc.wfirma.pl, "Format wymiany danych").

    Args:
        conditions: Condition dicts with ``field``/``operator``/``value`` keys.
        limit: Page size.
        page: Page number.

    Returns:
        The ``parameters`` mapping ready to nest under a module branch.
    """
    parameters: dict[str, Any] = {}
    if conditions:
        parameters["conditions"] = {
            str(index): {"condition": dict(condition)} for index, condition in enumerate(conditions)
        }
    if limit is not None:
        parameters["limit"] = limit
    if page is not None:
        parameters["page"] = page
    return parameters
