#!/usr/bin/python3
"""Unit tests for the FileStorage class."""
import json
import os
import unittest
from os import getenv
import models
from models.base_model import BaseModel
from models.user import User
from models.engine.file_storage import FileStorage


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage only")
class TestFileStorage(unittest.TestCase):
    """Test cases for FileStorage."""

    def setUp(self):
        """Back up and clear storage state before each test."""
        self.backup = dict(FileStorage._FileStorage__objects)
        FileStorage._FileStorage__objects.clear()
        if os.path.exists("file.json"):
            os.rename("file.json", "file.json.bak")

    def tearDown(self):
        """Restore storage state after each test."""
        if os.path.exists("file.json"):
            os.remove("file.json")
        if os.path.exists("file.json.bak"):
            os.rename("file.json.bak", "file.json")
        FileStorage._FileStorage__objects.clear()
        FileStorage._FileStorage__objects.update(self.backup)

    def test_storage_instance(self):
        """Test that storage is a FileStorage instance."""
        self.assertIsInstance(models.storage, FileStorage)

    def test_all_returns_dict(self):
        """Test that all returns the objects dictionary."""
        self.assertIsInstance(models.storage.all(), dict)

    def test_new_adds_object(self):
        """Test that creating an object registers it under its key."""
        a = BaseModel()
        self.assertNotIn("BaseModel." + a.id, models.storage.all())
        a.save()
        self.assertIs(models.storage.all()["BaseModel." + a.id], a)

    def test_save_writes_json(self):
        """Test that save writes the JSON file."""
        a = BaseModel()
        a.save()
        with open("file.json") as f:
            data = json.load(f)
        self.assertEqual(data["BaseModel." + a.id], a.to_dict())

    def test_reload(self):
        """Test that reload restores saved objects."""
        u = User()
        u.first_name = "Betty"
        u.save()
        FileStorage._FileStorage__objects.clear()
        models.storage.reload()
        obj = models.storage.all()["User." + u.id]
        self.assertIsInstance(obj, User)
        self.assertEqual(obj.first_name, "Betty")

    def test_reload_without_file(self):
        """Test that reload does nothing when the file is missing."""
        models.storage.reload()
        self.assertEqual(models.storage.all(), {})

    def test_all_with_class(self):
        """Test that all(cls) only returns instances of cls."""
        from models.state import State
        s1 = State(name="A")
        s1.save()
        BaseModel().save()
        found = models.storage.all(State)
        self.assertEqual(list(found.keys()), ["State." + s1.id])

    def test_delete(self):
        """Test that delete removes an object."""
        u = User()
        u.save()
        models.storage.delete(u)
        self.assertNotIn("User." + u.id, models.storage.all())

    def test_delete_none(self):
        """Test that delete(None) changes nothing."""
        BaseModel().save()
        before = dict(models.storage.all())
        models.storage.delete(None)
        self.assertEqual(before, models.storage.all())

    def test_delete_missing(self):
        """Test that deleting an unknown object does not fail."""
        models.storage.delete(User())


if __name__ == "__main__":
    unittest.main()
