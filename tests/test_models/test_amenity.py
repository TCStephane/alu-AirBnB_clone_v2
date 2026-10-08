#!/usr/bin/python3
"""Unit tests for the Amenity class."""
import unittest
from models.base_model import BaseModel
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """Test cases for Amenity."""

    def test_inheritance(self):
        """Test that Amenity inherits from BaseModel."""
        self.assertIsInstance(Amenity(), BaseModel)

    def test_attributes(self):
        """Test the default public attributes of Amenity."""
        obj = Amenity()
        for name in ["name"]:
            self.assertTrue(hasattr(obj, name))

    def test_to_dict(self):
        """Test that to_dict reports the right class name."""
        self.assertEqual(Amenity().to_dict()["__class__"], "Amenity")

    def test_from_dict(self):
        """Test recreating Amenity from a dictionary."""
        a = Amenity()
        b = Amenity(**a.to_dict())
        self.assertEqual(a.id, b.id)
        self.assertIsNot(a, b)

    def test_table_mapping(self):
        """Test the SQLAlchemy table name and column names."""
        self.assertEqual(Amenity.__tablename__, "amenities")
        expected = [
            "id",
            "created_at",
            "updated_at",
            "name",
        ]
        names = sorted(c.name for c in Amenity.__table__.columns)
        self.assertEqual(names, sorted(expected))


if __name__ == "__main__":
    unittest.main()
