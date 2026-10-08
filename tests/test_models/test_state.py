#!/usr/bin/python3
"""Unit tests for the State class."""
import unittest
from models.base_model import BaseModel
from models.state import State


class TestState(unittest.TestCase):
    """Test cases for State."""

    def test_inheritance(self):
        """Test that State inherits from BaseModel."""
        self.assertIsInstance(State(), BaseModel)

    def test_attributes(self):
        """Test the default public attributes of State."""
        obj = State()
        for name in ["name"]:
            self.assertTrue(hasattr(obj, name))

    def test_to_dict(self):
        """Test that to_dict reports the right class name."""
        self.assertEqual(State().to_dict()["__class__"], "State")

    def test_from_dict(self):
        """Test recreating State from a dictionary."""
        a = State()
        b = State(**a.to_dict())
        self.assertEqual(a.id, b.id)
        self.assertIsNot(a, b)

    def test_table_mapping(self):
        """Test the SQLAlchemy table name and column names."""
        self.assertEqual(State.__tablename__, "states")
        expected = [
            "id",
            "created_at",
            "updated_at",
            "name",
        ]
        names = sorted(c.name for c in State.__table__.columns)
        self.assertEqual(names, sorted(expected))


if __name__ == "__main__":
    unittest.main()
