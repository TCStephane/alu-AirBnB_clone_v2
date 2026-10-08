#!/usr/bin/python3
"""Unit tests for the Place class."""
import unittest
from os import getenv
from models.base_model import BaseModel
from models.place import Place


class TestPlace(unittest.TestCase):
    """Test cases for Place."""

    def test_inheritance(self):
        """Test that Place inherits from BaseModel."""
        self.assertIsInstance(Place(), BaseModel)

    def test_attributes(self):
        """Test the default public attributes of Place."""
        obj = Place()
        attrs = [
            ("city_id", str, ""),
            ("user_id", str, ""),
            ("name", str, ""),
            ("description", str, ""),
            ("number_rooms", int, 0),
            ("number_bathrooms", int, 0),
            ("max_guest", int, 0),
            ("price_by_night", int, 0),
            ("latitude", float, 0.0),
            ("longitude", float, 0.0),
        ]
        for name, typ, default in attrs:
            self.assertTrue(hasattr(obj, name))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage only")
    def test_amenity_ids(self):
        """Test that each Place has its own amenity_ids list."""
        a, b = Place(), Place()
        self.assertEqual(a.amenity_ids, [])
        a.amenity_ids.append("x")
        self.assertEqual(b.amenity_ids, [])

    def test_to_dict(self):
        """Test that to_dict reports the right class name."""
        self.assertEqual(Place().to_dict()["__class__"], "Place")

    def test_from_dict(self):
        """Test recreating Place from a dictionary."""
        a = Place()
        b = Place(**a.to_dict())
        self.assertEqual(a.id, b.id)
        self.assertIsNot(a, b)

    def test_table_mapping(self):
        """Test the SQLAlchemy table name and column names."""
        self.assertEqual(Place.__tablename__, "places")
        expected = [
            "id",
            "created_at",
            "updated_at",
            "city_id",
            "user_id",
            "name",
            "description",
            "number_rooms",
            "number_bathrooms",
            "max_guest",
            "price_by_night",
            "latitude",
            "longitude",
        ]
        names = sorted(c.name for c in Place.__table__.columns)
        self.assertEqual(names, sorted(expected))


if __name__ == "__main__":
    unittest.main()
