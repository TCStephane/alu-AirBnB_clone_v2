#!/usr/bin/python3
"""Unit tests for the City class."""
import unittest
from models.base_model import BaseModel
from models.city import City


class TestCity(unittest.TestCase):
    """Test cases for City."""

    def test_inheritance(self):
        """Test that City inherits from BaseModel."""
        self.assertIsInstance(City(), BaseModel)

    def test_attributes(self):
        """Test the default public attributes of City."""
        obj = City()
        for name, typ, default in [("state_id", str, ""), ("name", str, "")]:
            self.assertTrue(hasattr(obj, name))

    def test_to_dict(self):
        """Test that to_dict reports the right class name."""
        self.assertEqual(City().to_dict()["__class__"], "City")

    def test_from_dict(self):
        """Test recreating City from a dictionary."""
        a = City()
        b = City(**a.to_dict())
        self.assertEqual(a.id, b.id)
        self.assertIsNot(a, b)

    def test_table_mapping(self):
        """Test the SQLAlchemy table name and column names."""
        self.assertEqual(City.__tablename__, "cities")
        expected = [
            "id",
            "created_at",
            "updated_at",
            "name",
            "state_id",
        ]
        names = sorted(c.name for c in City.__table__.columns)
        self.assertEqual(names, sorted(expected))


if __name__ == "__main__":
    unittest.main()
