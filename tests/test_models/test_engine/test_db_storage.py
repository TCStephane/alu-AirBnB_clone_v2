#!/usr/bin/python3
"""Unit tests for DBStorage (run only with HBNB_TYPE_STORAGE=db)."""
import unittest
from os import getenv
import io
from contextlib import redirect_stdout
import models
from console import HBNBCommand

DB = getenv("HBNB_TYPE_STORAGE") == "db"


def count_rows(table):
    """Count the rows of table using MySQLdb, not SQLAlchemy."""
    import MySQLdb
    conn = MySQLdb.connect(host=getenv("HBNB_MYSQL_HOST"),
                           user=getenv("HBNB_MYSQL_USER"),
                           passwd=getenv("HBNB_MYSQL_PWD"),
                           db=getenv("HBNB_MYSQL_DB"))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM {}".format(table))
    total = cur.fetchone()[0]
    cur.close()
    conn.close()
    return total


@unittest.skipIf(not DB, "DBStorage only")
class TestDBStorage(unittest.TestCase):
    """Test cases for DBStorage."""

    def test_create_state_adds_row(self):
        """Test that create State adds one row to states."""
        before = count_rows("states")
        with redirect_stdout(io.StringIO()):
            HBNBCommand().onecmd('create State name="California"')
        self.assertEqual(count_rows("states"), before + 1)

    def test_all_with_class(self):
        """Test that all(cls) returns only that class."""
        from models.state import State
        st = State(name="Arizona")
        st.save()
        found = models.storage.all(State)
        self.assertIn("State." + st.id, found)
        for obj in found.values():
            self.assertIsInstance(obj, State)

    def test_delete_removes_row(self):
        """Test that delete plus save removes the row."""
        from models.state import State
        st = State(name="Nevada")
        st.save()
        before = count_rows("states")
        st.delete()
        models.storage.save()
        self.assertEqual(count_rows("states"), before - 1)

    def test_cascade_state_cities(self):
        """Test that deleting a State deletes its cities."""
        from models.state import State
        from models.city import City
        st = State(name="Texas")
        st.save()
        City(name="Austin", state_id=st.id).save()
        before = count_rows("cities")
        st.delete()
        models.storage.save()
        self.assertEqual(count_rows("cities"), before - 1)


if __name__ == "__main__":
    unittest.main()
