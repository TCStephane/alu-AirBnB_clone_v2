#!/usr/bin/python3
"""Tests for FileStorage.delete and FileStorage.all(cls)."""
import unittest
from os import getenv
from models.engine.file_storage import FileStorage
from models.state import State
from models.city import City


@unittest.skipIf(getenv('HBNB_TYPE_STORAGE') == 'db', "FileStorage only")
class TestFileStorageDelete(unittest.TestCase):
    """Test delete and filtered all."""

    def test_delete_removes_object(self):
        """delete removes the object from all()."""
        fs = FileStorage()
        state = State(name="Test")
        fs.new(state)
        self.assertIn("State." + state.id, fs.all(State))
        fs.delete(state)
        self.assertNotIn("State." + state.id, fs.all(State))

    def test_delete_none(self):
        """delete(None) does nothing."""
        fs = FileStorage()
        before = len(fs.all())
        fs.delete(None)
        self.assertEqual(before, len(fs.all()))

    def test_all_filters_by_class(self):
        """all(cls) returns only that class."""
        fs = FileStorage()
        fs.new(City(name="X", state_id="1"))
        for obj in fs.all(City).values():
            self.assertIsInstance(obj, City)


if __name__ == '__main__':
    unittest.main()
