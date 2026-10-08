#!/usr/bin/python3
"""Unit tests for the create command of the console."""
import io
import unittest
from contextlib import redirect_stdout
from os import getenv
import models
from console import HBNBCommand


def run(line):
    """Run one console command and return what it printed."""
    buf = io.StringIO()
    with redirect_stdout(buf):
        HBNBCommand().onecmd(line)
    return buf.getvalue().strip()


@unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "FileStorage only")
class TestConsoleCreate(unittest.TestCase):
    """Test cases for create with parameters."""

    def test_create_string_param(self):
        """Test that underscores become spaces in strings."""
        new_id = run('create State name="My_little_house"')
        obj = models.storage.all()["State." + new_id]
        self.assertEqual(obj.name, "My little house")

    def test_create_escaped_quote(self):
        """Test that escaped double quotes are kept."""
        new_id = run('create State name="say_\\"hi\\""')
        obj = models.storage.all()["State." + new_id]
        self.assertEqual(obj.name, 'say "hi"')

    def test_create_int_and_float(self):
        """Test integer and float parameters."""
        new_id = run("create Place number_rooms=4 latitude=37.77")
        obj = models.storage.all()["Place." + new_id]
        self.assertEqual(obj.number_rooms, 4)
        self.assertEqual(obj.latitude, 37.77)

    def test_create_skips_bad_params(self):
        """Test that unrecognized parameters are skipped."""
        new_id = run('create State name="a"b" oops age=abc')
        obj = models.storage.all()["State." + new_id]
        self.assertFalse(hasattr(obj, "oops"))
        self.assertNotEqual(getattr(obj, "name", None), 'a"b')

    def test_create_errors(self):
        """Test the error messages."""
        self.assertEqual(run("create"), "** class name missing **")
        self.assertEqual(run("create Nope"), "** class doesn't exist **")


if __name__ == "__main__":
    unittest.main()
