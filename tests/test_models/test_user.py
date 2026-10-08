#!/usr/bin/python3
"""Unit tests for the User class."""
import unittest
from models.base_model import BaseModel
from models.user import User


class TestUser(unittest.TestCase):
    """Test cases for User."""

    def test_inheritance(self):
        """Test that User inherits from BaseModel."""
        self.assertIsInstance(User(), BaseModel)

    def test_attributes(self):
        """Test the default public attributes of User."""
        obj = User()
        attrs = [
            ("email", str, ""),
            ("password", str, ""),
            ("first_name", str, ""),
            ("last_name", str, ""),
        ]
        for name, typ, default in attrs:
            self.assertTrue(hasattr(obj, name))

    def test_to_dict(self):
        """Test that to_dict reports the right class name."""
        self.assertEqual(User().to_dict()["__class__"], "User")

    def test_from_dict(self):
        """Test recreating User from a dictionary."""
        a = User()
        b = User(**a.to_dict())
        self.assertEqual(a.id, b.id)
        self.assertIsNot(a, b)

    def test_table_mapping(self):
        """Test the SQLAlchemy table name and column names."""
        self.assertEqual(User.__tablename__, "users")
        expected = [
            "id",
            "created_at",
            "updated_at",
            "email",
            "password",
            "first_name",
            "last_name",
        ]
        names = sorted(c.name for c in User.__table__.columns)
        self.assertEqual(names, sorted(expected))


if __name__ == "__main__":
    unittest.main()
