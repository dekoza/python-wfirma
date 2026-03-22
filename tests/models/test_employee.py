"""
Tests for employee/user models.

This module tests the User model which represents users in wFirma API.
"""

from __future__ import annotations

import importlib
import warnings
from datetime import datetime

import pytest
from pydantic import ValidationError

import wfirma.models.employee as employee_module
from wfirma.models.employee import User


class TestUser:
    """Tests for User model."""

    def test_create_user_with_required_fields(self) -> None:
        """Test creating user with only required fields."""
        user = User(id=124233, login="jan@kowalski.com")

        assert user.id == 124233
        assert user.login == "jan@kowalski.com"
        assert user.created is None
        assert user.modified is None

    def test_create_user_with_all_fields(self) -> None:
        """Test creating user with all fields."""
        created = datetime(2024, 1, 15, 10, 30, 0)
        modified = datetime(2024, 2, 20, 14, 45, 0)

        user = User(
            id=124233,
            login="jan@kowalski.com",
            created=created,
            modified=modified,
        )

        assert user.id == 124233
        assert user.login == "jan@kowalski.com"
        assert user.created == created
        assert user.modified == modified

    def test_user_to_xml_serialization(self) -> None:
        """Test that user can be serialized to XML."""
        user = User(id=124233, login="jan@kowalski.com")

        xml_bytes = user.to_xml()
        xml_str = xml_bytes.decode("utf-8")

        assert "<user>" in xml_str
        assert "<id>124233</id>" in xml_str
        assert "<login>jan@kowalski.com</login>" in xml_str
        assert "</user>" in xml_str

    def test_user_from_xml_deserialization(self) -> None:
        """Test that user can be deserialized from XML."""
        xml_str = """
        <user>
            <id>124233</id>
            <login>jan@kowalski.com</login>
            <created>2024-01-15 10:30:00</created>
            <modified>2024-02-20 14:45:00</modified>
        </user>
        """

        user = User.from_xml(xml_str.encode("utf-8"))

        assert user.id == 124233
        assert user.login == "jan@kowalski.com"
        assert user.created == datetime(2024, 1, 15, 10, 30, 0)
        assert user.modified == datetime(2024, 2, 20, 14, 45, 0)

    def test_user_from_xml_with_zero_datetime(self) -> None:
        """Test that user handles wFirma's '0000-00-00 00:00:00' datetime."""
        xml_str = """
        <user>
            <id>124233</id>
            <login>jan@kowalski.com</login>
            <created>0000-00-00 00:00:00</created>
            <modified>0000-00-00 00:00:00</modified>
        </user>
        """

        user = User.from_xml(xml_str.encode("utf-8"))

        assert user.id == 124233
        assert user.login == "jan@kowalski.com"
        # Zero datetime should be parsed as None
        assert user.created is None
        assert user.modified is None

    def test_user_roundtrip_serialization(self) -> None:
        """Test that user survives roundtrip serialization."""
        original = User(
            id=999,
            login="test@example.com",
            created=datetime(2025, 6, 1, 12, 0, 0),
            modified=datetime(2025, 6, 2, 18, 30, 0),
        )

        xml_bytes = original.to_xml()
        restored = User.from_xml(xml_bytes)

        assert restored.id == original.id
        assert restored.login == original.login
        assert restored.created == original.created
        assert restored.modified == original.modified

    def test_user_model_is_immutable(self) -> None:
        """Test that user model is immutable (frozen config)."""
        user = User(id=1, login="test@example.com")

        with pytest.raises(ValidationError):
            user.login = "changed@example.com"

    def test_user_equality(self) -> None:
        """Test user equality based on fields."""
        user1 = User(id=1, login="test@example.com")
        user2 = User(id=1, login="test@example.com")
        user3 = User(id=2, login="test@example.com")

        assert user1 == user2
        assert user1 != user3

    def test_user_xml_tag(self) -> None:
        """Test that user uses correct XML tag."""
        user = User(id=1, login="test@example.com")
        xml_str = user.to_xml().decode("utf-8")

        # Should start with <user> tag
        assert xml_str.strip().startswith("<user>") or xml_str.strip().startswith("<?xml")


class TestEmployeeModuleExports:
    """Tests for module exports."""

    def test_user_is_exported(self) -> None:
        """Test that User is exported from employee module."""
        from wfirma.models.employee import User

        assert User is not None

    def test_user_is_exported_from_models(self) -> None:
        """Test that User is exported from wfirma.models."""
        from wfirma.models import User

        assert User is not None

    def test_reloading_employee_module_emits_no_shadowing_warnings(self) -> None:
        """Test that the User model does not redefine timestamp fields from the mixin."""
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            importlib.reload(employee_module)

        shadow_warnings = [
            warning
            for warning in caught
            if "shadows an attribute in parent" in str(warning.message)
        ]

        assert not shadow_warnings
