from __future__ import annotations

import json
from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from wfirma.exceptions import MissingConfigurationError


def test_company_show_prints_id_and_name_table(capsys: pytest.CaptureFixture[str]) -> None:
    from wfirma.cli import main

    client = Mock()
    client.company.get.return_value = SimpleNamespace(id=321, name="Acme Sp. z o.o.")

    exit_code = main(["company", "show"], client_factory=lambda _: client)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "ID" in captured.out
    assert "Name" in captured.out
    assert "321" in captured.out
    assert "Acme Sp. z o.o." in captured.out


def test_company_show_supports_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    from wfirma.cli import main

    client = Mock()
    client.company.get.return_value = SimpleNamespace(id=321, name="Acme Sp. z o.o.", nip="123")

    exit_code = main(["company", "show", "--json"], client_factory=lambda _: client)

    captured = capsys.readouterr()
    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload["id"] == 321
    assert payload["name"] == "Acme Sp. z o.o."
    assert payload["nip"] == "123"


def test_list_command_prints_id_and_label_table(capsys: pytest.CaptureFixture[str]) -> None:
    from wfirma.cli import main

    client = Mock()
    client.tags.find.return_value = [
        {"id": 1, "name": "Alpha"},
        {"id": 2, "name": "Beta"},
    ]

    exit_code = main(["tags", "list"], client_factory=lambda _: client)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "ID" in captured.out
    assert "Label" in captured.out
    assert "Alpha" in captured.out
    assert "Beta" in captured.out


def test_list_command_falls_back_to_description_for_label(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from wfirma.cli import main

    client = Mock()
    client.terms.find.return_value = [
        {"id": 10, "description": "14 days"},
    ]

    exit_code = main(["terms", "list"], client_factory=lambda _: client)

    captured = capsys.readouterr()
    assert exit_code == 0
    assert "Label" in captured.out
    assert "14 days" in captured.out


def test_list_command_supports_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    from wfirma.cli import main

    client = Mock()
    client.vat_codes.find.return_value = [
        {"id": 1, "name": "VAT 23%", "rate": 23},
    ]

    exit_code = main(["vat-codes", "list", "--json"], client_factory=lambda _: client)

    captured = capsys.readouterr()
    assert exit_code == 0
    payload = json.loads(captured.out)
    assert payload[0]["id"] == 1
    assert payload[0]["name"] == "VAT 23%"


def test_company_show_uses_company_id_override() -> None:
    from wfirma.cli import main

    client = Mock()
    client.company.get.return_value = SimpleNamespace(id=321, name="Acme Sp. z o.o.")

    exit_code = main(
        ["company", "show", "--company-id", "999"],
        client_factory=lambda _: client,
    )

    assert exit_code == 0
    client.company.get.assert_called_once_with(company_id=999)


def test_cli_raises_clear_error_when_api_key_env_is_missing() -> None:
    from wfirma.cli import build_client_from_env

    with pytest.raises(MissingConfigurationError, match="WFIRMA_APP_KEY"):
        build_client_from_env(env={})


def test_build_client_from_env_uses_api_key_auth() -> None:
    from wfirma.cli import build_client_from_env

    client = build_client_from_env(
        env={
            "WFIRMA_APP_KEY": "app",
            "WFIRMA_ACCESS_KEY": "access",
            "WFIRMA_SECRET_KEY": "secret",
            "WFIRMA_COMPANY_ID": "123",
        }
    )

    try:
        assert client.company_id == 123
        assert client.auth.app_key == "app"
        assert client.auth.access_key == "access"
        assert client.auth.secret_key == "secret"
    finally:
        client.close()


def test_main_returns_error_code_and_message_for_missing_label(
    capsys: pytest.CaptureFixture[str],
) -> None:
    from wfirma.cli import main

    client = Mock()
    client.warehouses.find.return_value = [{"id": 1, "created": "2026-01-01"}]

    exit_code = main(["warehouses", "list"], client_factory=lambda _: client)

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "No usable label field found" in captured.err
