"""Unit tests for wFirma API payload extraction helpers.

These utilities standardize how we locate nested objects/lists inside wFirma
JSON responses.
"""

from __future__ import annotations

import pytest


@pytest.mark.aicomplete
class TestExtractSingleObjectPayload:
    def test_extracts_from_indexed_container(self) -> None:
        from wfirma._payloads import extract_single_object_payload

        data = {
            "status": {"code": "OK"},
            "invoices": {"0": {"invoice": {"id": 1, "fullnumber": "FV/1"}}},
        }

        assert extract_single_object_payload(
            data=data, container_key="invoices", object_key="invoice"
        ) == {
            "id": 1,
            "fullnumber": "FV/1",
        }

    def test_extracts_from_direct_container(self) -> None:
        from wfirma._payloads import extract_single_object_payload

        data = {
            "status": {"code": "OK"},
            "invoices": {"invoice": {"id": 1}},
        }

        assert extract_single_object_payload(
            data=data, container_key="invoices", object_key="invoice"
        ) == {"id": 1}

    def test_raises_key_error_when_payload_missing(self) -> None:
        from wfirma._payloads import extract_single_object_payload

        with pytest.raises(KeyError, match="Unable to locate"):
            extract_single_object_payload(
                data={"status": {"code": "OK"}, "invoices": {"0": {"not_invoice": {}}}},
                container_key="invoices",
                object_key="invoice",
            )


@pytest.mark.aicomplete
class TestExtractObjectListPayloads:
    def test_extracts_list_from_indexed_items(self) -> None:
        from wfirma._payloads import extract_object_list_payloads

        data = {
            "status": {"code": "OK"},
            "payments": {
                "0": {"payment": {"id": 1}},
                "1": {"payment": {"id": 2}},
                "parameters": {"page": 1},
            },
        }

        assert extract_object_list_payloads(
            data,
            container_key="payments",
            object_key="payment",
        ) == [{"id": 1}, {"id": 2}]

    def test_skips_non_numeric_keys_and_non_dict_items(self) -> None:
        from wfirma._payloads import extract_object_list_payloads

        data = {
            "status": {"code": "OK"},
            "goods": {
                "0": {"good": {"id": 1}},
                "parameters": {"page": 1},
                "x": {"good": {"id": 999}},
                "2": "not-a-dict",
            },
        }

        assert extract_object_list_payloads(data, container_key="goods", object_key="good") == [
            {"id": 1}
        ]

    def test_returns_empty_list_when_container_missing_or_not_dict(self) -> None:
        from wfirma._payloads import extract_object_list_payloads

        assert extract_object_list_payloads({"status": {"code": "OK"}}, "goods", "good") == []
        assert (
            extract_object_list_payloads({"status": {"code": "OK"}, "goods": []}, "goods", "good")
            == []
        )
