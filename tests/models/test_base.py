"""
Tests for base Pydantic models.

These tests verify the base model classes that provide XML/JSON
serialization support for all wFirma API entities.
"""

from datetime import datetime

import pytest
from pydantic import ValidationError
from pydantic_xml import element

from wfirma.models.base import (
    BaseXMLModel,
    DateTimeField,
    OptionalDateTimeField,
    ResponseParameters,
    ResponseStatus,
    TimestampedFieldsMixin,
    WFirmaBaseModel,
    format_wfirma_datetime,
    parse_wfirma_datetime,
)


class TestWFirmaBaseModel:
    """Tests for WFirmaBaseModel base class."""

    # AICOMPLETE: Base model validation tests - ready for review

    def test_base_model_is_immutable(self) -> None:
        """Test that base model instances are immutable (frozen)."""

        class SampleModel(WFirmaBaseModel):
            name: str = element()

        instance = SampleModel(name="test")
        with pytest.raises(ValidationError):
            instance.name = "new_value"

    def test_base_model_allows_extra_fields_on_parse(self) -> None:
        """Test that extra fields from API are ignored during parsing."""

        class SampleModel(WFirmaBaseModel, tag="sample"):
            name: str = element()

        # Extra fields should be ignored (API may add new fields)
        xml_str = b"<sample><name>test</name><unknown>ignored</unknown></sample>"
        instance = SampleModel.from_xml(xml_str)
        assert instance.name == "test"

    def test_base_model_to_dict(self) -> None:
        """Test model serialization to dictionary."""

        class SampleModel(WFirmaBaseModel):
            name: str = element()
            value: int = element()

        instance = SampleModel(name="test", value=42)
        result = instance.model_dump()
        assert result == {"name": "test", "value": 42}

    def test_base_model_to_dict_excludes_none(self) -> None:
        """Test that None values are excluded by default."""

        class SampleModel(WFirmaBaseModel):
            name: str = element()
            optional_value: int | None = element(default=None)

        instance = SampleModel(name="test")
        result = instance.model_dump(exclude_none=True)
        assert result == {"name": "test"}

    def test_base_model_from_dict(self) -> None:
        """Test model creation from dictionary."""

        class SampleModel(WFirmaBaseModel):
            name: str = element()
            value: int = element()

        data = {"name": "test", "value": 42}
        instance = SampleModel.model_validate(data)
        assert instance.name == "test"
        assert instance.value == 42

    def test_base_model_optional_fields(self) -> None:
        """Test that optional fields default to None."""

        class SampleModel(WFirmaBaseModel):
            name: str = element()
            description: str | None = element(default=None)

        instance = SampleModel(name="test")
        assert instance.name == "test"
        assert instance.description is None


class TestBaseXMLModel:
    """Tests for BaseXMLModel with XML serialization support."""

    # AICOMPLETE: XML model serialization tests - ready for review

    def test_xml_model_to_xml_string(self) -> None:
        """Test XML serialization."""

        class SampleXMLModel(BaseXMLModel, tag="sample"):
            name: str = element()
            value: int = element()

        instance = SampleXMLModel(name="test", value=42)
        xml_bytes = instance.to_xml()
        xml_str = xml_bytes.decode("utf-8")
        assert "<sample>" in xml_str
        assert "<name>test</name>" in xml_str
        assert "<value>42</value>" in xml_str

    def test_xml_model_from_xml_string(self) -> None:
        """Test XML deserialization."""

        class SampleXMLModel(BaseXMLModel, tag="sample"):
            name: str = element()
            value: int = element()

        xml_str = b"<sample><name>test</name><value>42</value></sample>"
        instance = SampleXMLModel.from_xml(xml_str)
        assert instance.name == "test"
        assert instance.value == 42

    def test_xml_model_ignores_unknown_elements(self) -> None:
        """Test that unknown XML elements are ignored during parsing."""

        class SampleXMLModel(BaseXMLModel, tag="sample"):
            name: str = element()

        xml_str = b"<sample><name>test</name><unknown>ignored</unknown></sample>"
        instance = SampleXMLModel.from_xml(xml_str)
        assert instance.name == "test"

    def test_xml_model_handles_nested_elements(self) -> None:
        """Test nested XML element handling."""

        class InnerModel(BaseXMLModel, tag="inner"):
            value: int = element()

        class OuterModel(BaseXMLModel, tag="outer"):
            name: str = element()
            inner: InnerModel

        outer = OuterModel(name="test", inner=InnerModel(value=42))
        xml_bytes = outer.to_xml()
        xml_str = xml_bytes.decode("utf-8")
        assert "<outer>" in xml_str
        assert "<inner>" in xml_str
        assert "<value>42</value>" in xml_str

    def test_xml_model_round_trip(self) -> None:
        """Test that XML serialization and deserialization are consistent."""

        class SampleXMLModel(BaseXMLModel, tag="sample"):
            name: str = element()
            value: int = element()

        original = SampleXMLModel(name="test", value=42)
        xml_bytes = original.to_xml()
        restored = SampleXMLModel.from_xml(xml_bytes)
        assert restored.name == original.name
        assert restored.value == original.value


class TestDateTimeFunctions:
    """Tests for datetime parsing and formatting functions."""

    # AICOMPLETE: DateTime function tests - ready for review

    def test_parse_wfirma_datetime_standard_format(self) -> None:
        """Test parsing wFirma datetime format (YYYY-MM-DD HH:MM:SS)."""
        result = parse_wfirma_datetime("2024-01-15 10:30:45")
        assert isinstance(result, datetime)
        assert result.year == 2024
        assert result.month == 1
        assert result.day == 15
        assert result.hour == 10
        assert result.minute == 30
        assert result.second == 45

    def test_parse_wfirma_datetime_null_format(self) -> None:
        """Test handling of wFirma null datetime (0000-00-00 00:00:00)."""
        result = parse_wfirma_datetime("0000-00-00 00:00:00")
        assert result is None

    def test_parse_wfirma_datetime_empty_string(self) -> None:
        """Test handling of empty datetime string."""
        result = parse_wfirma_datetime("")
        assert result is None

    def test_parse_wfirma_datetime_none(self) -> None:
        """Test handling of None value."""
        result = parse_wfirma_datetime(None)
        assert result is None

    def test_parse_wfirma_datetime_invalid_format(self) -> None:
        """Test that invalid format raises ValueError."""
        with pytest.raises(ValueError, match="Invalid datetime format"):
            parse_wfirma_datetime("invalid-date")

    def test_parse_wfirma_datetime_invalid_type(self) -> None:
        """Test that invalid type raises ValueError."""
        with pytest.raises(ValueError, match="Expected datetime string or datetime object"):
            parse_wfirma_datetime(12345)  # type: ignore[arg-type]

    def test_format_wfirma_datetime(self) -> None:
        """Test datetime formatting to wFirma format."""
        dt = datetime(2024, 1, 15, 10, 30, 45)
        result = format_wfirma_datetime(dt)
        assert result == "2024-01-15 10:30:45"

    def test_format_wfirma_datetime_none(self) -> None:
        """Test formatting None returns None."""
        result = format_wfirma_datetime(None)
        assert result is None


class TestDateTimeField:
    """Tests for DateTimeField annotated type."""

    # AICOMPLETE: DateTimeField tests - ready for review

    def test_datetime_field_parsing_in_model(self) -> None:
        """Test DateTimeField parsing in a model."""

        class SampleModel(WFirmaBaseModel):
            created: DateTimeField = element()

        instance = SampleModel.model_validate({"created": "2024-01-15 10:30:45"})
        assert isinstance(instance.created, datetime)
        assert instance.created.year == 2024
        assert instance.created.month == 1
        assert instance.created.day == 15

    def test_datetime_field_accepts_datetime_object(self) -> None:
        """Test that datetime objects are accepted."""

        class SampleModel(WFirmaBaseModel):
            created: DateTimeField = element()

        dt = datetime(2024, 1, 15, 10, 30, 45)
        instance = SampleModel(created=dt)
        assert instance.created == dt

    def test_datetime_field_serialization(self) -> None:
        """Test datetime serialization to wFirma format."""

        class SampleModel(WFirmaBaseModel):
            created: DateTimeField = element()

        dt = datetime(2024, 1, 15, 10, 30, 45)
        instance = SampleModel(created=dt)
        result = instance.model_dump(mode="json")
        assert result["created"] == "2024-01-15 10:30:45"

    def test_datetime_field_optional_with_null(self) -> None:
        """Test optional datetime field handles null/empty values."""

        class SampleModel(WFirmaBaseModel):
            created: OptionalDateTimeField = element(default=None)

        instance = SampleModel.model_validate({"created": "0000-00-00 00:00:00"})
        assert instance.created is None

    def test_datetime_field_optional_with_empty(self) -> None:
        """Test optional DateTimeField with empty string."""

        class SampleModel(WFirmaBaseModel):
            created: OptionalDateTimeField = element(default=None)

        instance = SampleModel.model_validate({"created": ""})
        assert instance.created is None


class TestTimestampedFieldsMixin:
    """Tests for shared timestamp fields mixin."""

    def test_mixin_provides_created_and_modified(self) -> None:
        class SampleModel(TimestampedFieldsMixin, BaseXMLModel, tag="sample"):
            name: str = element()

        model = SampleModel(name="x")
        assert model.created is None
        assert model.modified is None

    def test_mixin_serializes_datetime_fields(self) -> None:
        dt = datetime(2024, 1, 1, 12, 0, 0)

        class SampleModel(TimestampedFieldsMixin, BaseXMLModel, tag="sample"):
            name: str = element()

        model = SampleModel(name="x", created=dt, modified=dt)
        payload = model.model_dump(mode="json")
        assert payload["created"] == "2024-01-01 12:00:00"
        assert payload["modified"] == "2024-01-01 12:00:00"


class TestResponseStatus:
    """Tests for ResponseStatus model."""

    # AICOMPLETE: Response status tests - ready for review

    def test_response_status_ok(self) -> None:
        """Test OK status parsing."""
        status = ResponseStatus(code="OK")
        assert status.code == "OK"
        assert status.is_success

    def test_response_status_error(self) -> None:
        """Test ERROR status parsing."""
        status = ResponseStatus(code="ERROR")
        assert status.code == "ERROR"
        assert not status.is_success

    def test_response_status_auth_error(self) -> None:
        """Test AUTH error status."""
        status = ResponseStatus(code="AUTH")
        assert status.code == "AUTH"
        assert not status.is_success

    def test_response_status_not_found(self) -> None:
        """Test NOT FOUND status."""
        status = ResponseStatus(code="NOT FOUND")
        assert status.code == "NOT FOUND"
        assert not status.is_success

    def test_response_status_from_xml(self) -> None:
        """Test ResponseStatus parsing from XML."""
        xml_str = b"<status><code>OK</code></status>"
        status = ResponseStatus.from_xml(xml_str)
        assert status.code == "OK"
        assert status.is_success


class TestResponseParameters:
    """Tests for API response pagination parameters."""

    # AICOMPLETE: Response parameters tests - ready for review

    def test_response_parameters_parsing(self) -> None:
        """Test parsing pagination parameters."""
        params = ResponseParameters(limit=20, page=1, total=100)
        assert params.limit == 20
        assert params.page == 1
        assert params.total == 100

    def test_response_parameters_from_dict(self) -> None:
        """Test parameters from dictionary."""
        data = {"limit": 20, "page": 2, "total": 50}
        params = ResponseParameters.model_validate(data)
        assert params.limit == 20
        assert params.page == 2
        assert params.total == 50

    def test_response_parameters_from_xml(self) -> None:
        """Test parameters parsing from XML."""
        xml_str = b"<parameters><limit>20</limit><page>1</page><total>11</total></parameters>"
        params = ResponseParameters.from_xml(xml_str)
        assert params.limit == 20
        assert params.page == 1
        assert params.total == 11

    def test_response_parameters_has_more_pages(self) -> None:
        """Test has_more_pages calculation."""
        # Page 1 of 5 pages (100 items, 20 per page)
        params = ResponseParameters(limit=20, page=1, total=100)
        assert params.has_more_pages

        # Last page
        params = ResponseParameters(limit=20, page=5, total=100)
        assert not params.has_more_pages

    def test_response_parameters_total_pages(self) -> None:
        """Test total_pages calculation."""
        # 100 items, 20 per page = 5 pages
        params = ResponseParameters(limit=20, page=1, total=100)
        assert params.total_pages == 5

        # 101 items, 20 per page = 6 pages
        params = ResponseParameters(limit=20, page=1, total=101)
        assert params.total_pages == 6

        # 0 items = 0 pages
        params = ResponseParameters(limit=20, page=1, total=0)
        assert params.total_pages == 0
