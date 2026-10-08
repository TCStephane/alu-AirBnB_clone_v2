#!/usr/bin/python3
"""Unit tests for the Review class."""
import unittest
from models.base_model import BaseModel
from models.review import Review


class TestReview(unittest.TestCase):
    """Test cases for Review."""

    def test_inheritance(self):
        """Test that Review inherits from BaseModel."""
        self.assertIsInstance(Review(), BaseModel)

    def test_attributes(self):
        """Test the default public attributes of Review."""
        obj = Review()
        attrs = [
            ("place_id", str, ""),
            ("user_id", str, ""),
            ("text", str, ""),
        ]
        for name, typ, default in attrs:
            self.assertTrue(hasattr(obj, name))

    def test_to_dict(self):
        """Test that to_dict reports the right class name."""
        self.assertEqual(Review().to_dict()["__class__"], "Review")

    def test_from_dict(self):
        """Test recreating Review from a dictionary."""
        a = Review()
        b = Review(**a.to_dict())
        self.assertEqual(a.id, b.id)
        self.assertIsNot(a, b)

    def test_table_mapping(self):
        """Test the SQLAlchemy table name and column names."""
        self.assertEqual(Review.__tablename__, "reviews")
        expected = [
            "id",
            "created_at",
            "updated_at",
            "text",
            "place_id",
            "user_id",
        ]
        names = sorted(c.name for c in Review.__table__.columns)
        self.assertEqual(names, sorted(expected))


if __name__ == "__main__":
    unittest.main()
