import sys
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '..'))

from src.AddSR import AddSR
import unittest
import sqlite3


class TestAddSRMethods(unittest.TestCase):

    @unittest.skip("Cleaner method")
    def cleanup_database(self):
        
        """
        Cleans up the in-memory SQLite database from previous testing cycles.
        """
        try:
            self.cursor.execute('DELETE FROM modify_sr WHERE symbol = ?;', ("AMC",))
        except sqlite3.Error:
            pass

    def test_add_method(self):
        
        """
        Test the 'add' method in the AddSR class.
        """
        with sqlite3.connect(":memory:") as memoryDatabase:
            self.cursor = memoryDatabase.cursor()

            # Remove rows from previous testing sessions
            self.cleanup_database()

            # Instance setup
            self.add_sr_instance = AddSR(master=None, db_connection=memoryDatabase)
            self.add_sr_instance.symbol_var.set("AMC")
            self.add_sr_instance.value_var.set("100")

            # Memory database setup
            self.cursor.execute('CREATE TABLE IF NOT EXISTS modify_sr (symbol TEXT, value TEXT, binary INTEGER)')

            # Call and retrieve results from add method
            self.add_sr_instance.add()
            self.cursor.execute('SELECT binary FROM modify_sr WHERE symbol=? AND value=?',
                                (self.add_sr_instance.symbol_var.get(), self.add_sr_instance.value_var.get()))
            result = self.cursor.fetchall()

            # Assertion
            self.assertEqual(result[0][0], 1)

    def test_delete_method(self):
        
        """
        Test the 'delete' method in the AddSR class.
        """
        with sqlite3.connect(":memory:") as memoryDatabase:
            self.cursor = memoryDatabase.cursor()

            # Remove rows from previous testing sessions
            self.cleanup_database()

            # Instance setup
            self.delete_sr_instance = AddSR(master=None, db_connection=memoryDatabase)
            self.delete_sr_instance.symbol_var.set("AMC")
            self.delete_sr_instance.value_var.set("100")

            # Memory database setup
            self.cursor.execute('CREATE TABLE IF NOT EXISTS modify_sr (symbol TEXT, value TEXT, binary INTEGER)')

            # Call and retrieve results from delete method
            self.delete_sr_instance.delete()
            self.cursor.execute('SELECT binary FROM modify_sr WHERE symbol=? AND value=?',
                                (self.delete_sr_instance.symbol_var.get(), self.delete_sr_instance.value_var.get()))
            result = self.cursor.fetchall()

            # Assertion
            self.assertEqual(result[0][0], 0)

    def test_add_delete(self):
        
        """
        Test the combination of 'add' and 'delete' methods in the AddSR class.
        """
        with sqlite3.connect(":memory:") as memoryDatabase:
            self.cursor = memoryDatabase.cursor()

            # Remove rows from previous testing sessions
            self.cleanup_database()

            # Instance setup
            self.add_delete_instance = AddSR(master=None, db_connection=memoryDatabase)
            self.add_delete_instance.symbol_var.set("AMC")
            self.add_delete_instance.value_var.set("100")

            # Memory database setup
            self.cursor.execute('CREATE TABLE IF NOT EXISTS modify_sr (symbol TEXT, value TEXT, binary INTEGER)')

            # Call and retrieve results from delete method
            self.add_delete_instance.add()
            self.add_delete_instance.delete()

            self.cursor.execute('SELECT binary FROM modify_sr WHERE symbol=? AND value=?',
                                (self.add_delete_instance.symbol_var.get(), self.add_delete_instance.value_var.get()))
            result = self.cursor.fetchall()

            # Assertion
            self.assertEqual(result, [])

    def test_delete_add(self):
        
        """
        Test the combination of 'delete' and 'add' methods in the AddSR class.
        """
        with sqlite3.connect(":memory:") as memoryDatabase:
            self.cursor = memoryDatabase.cursor()

            # Remove rows from previous testing sessions
            self.cleanup_database()

            # Instance setup
            self.delete_add_instance = AddSR(master=None, db_connection=memoryDatabase)
            self.delete_add_instance.symbol_var.set("AMC")
            self.delete_add_instance.value_var.set("100")

            # Memory database setup
            self.cursor.execute('CREATE TABLE IF NOT EXISTS modify_sr (symbol TEXT, value TEXT, binary INTEGER)')

            # Call and retrieve results from delete method
            self.delete_add_instance.delete()
            self.delete_add_instance.add()

            self.cursor.execute('SELECT binary FROM modify_sr WHERE symbol=? AND value=?',
                                (self.delete_add_instance.symbol_var.get(), self.delete_add_instance.value_var.get()))
            result = self.cursor.fetchall()

            # Assertion
            self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()