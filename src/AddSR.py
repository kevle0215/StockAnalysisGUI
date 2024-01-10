import sqlite3
import tkinter as tk
from tkinter import messagebox

class AddSR:
    """
    AddSR - GUI window for manually adding or deleting support/resistance levels.

    Attributes:
        symbol_var (StringVar): Variable to store stock symbol input.
        value_var (StringVar): Variable to store support/resistance value input.
    """

    def __init__(self, master, db_connection = None):
        """
        Initializes the AddSR window.
        
        """
        self.master = master
        self.addSR = tk.Toplevel(self.master)
        self.addSR.title("Add support/resistance")

        self.symbol_var = tk.StringVar()
        self.value_var = tk.StringVar()

        self.create_widgets()

        # testing purposes
        self.db_connection = db_connection or sqlite3.connect('stock_data.db')

    def create_widgets(self):
        """
        Configures graphical elements of the AddSR window.

        """
        # Label setup
        stock_label = tk.Label(self.addSR, text="Stock Symbol")
        value_label = tk.Label(self.addSR, text="New Value")

        # Entry setup
        stock_entry = tk.Entry(self.addSR, textvariable=self.symbol_var)
        value_entry = tk.Entry(self.addSR, textvariable=self.value_var)

        # Button setup
        addButton = tk.Button(self.addSR, text="Add Support/Resistance", command=lambda: self.add())
        deleteButton = tk.Button(self.addSR, text="Delete Support/Resistance", command=lambda: self.delete())

        # Label locations
        stock_label.grid(column=0, row=0)
        value_label.grid(column=0, row=1)

        # Entry locations
        stock_entry.grid(column=1, row=0)
        value_entry.grid(column=1, row=1)

        # Button locations
        addButton.grid(column=0, row=2)
        deleteButton.grid(column=1, row=2)

    def add(self):
        """
        Adds a support/resistance level based on user input.

        Raises:
            Warning: If the support/resistance level already exists or has been deleted.
        """
        try:
            with self.db_connection as conn:
                cursor = conn.cursor()

                # Fetch existing values for the specified stock symbol
                cursor.execute('SELECT value, binary FROM modify_sr WHERE symbol = ?', (self.symbol_var.get(),))
                existing_values = cursor.fetchall()

                # Check for duplication or opposite pair
                duplication = any(float(old_value[0]) == float(self.value_var.get()) and float(old_value[1]) == 1 for old_value in existing_values)
                oppositePair = any(float(old_value[0]) == float(self.value_var.get()) and float(old_value[1]) == 0 for old_value in existing_values)

                # Handle cases of duplication or opposite pair
                if duplication:
                    messagebox.showwarning("Support/Resistance already added!")
                elif oppositePair:
                    cursor.execute('DELETE FROM modify_sr WHERE symbol=? AND value=? AND binary=0', (self.symbol_var.get(), self.value_var.get()))
                else:
                    cursor.execute('INSERT INTO modify_sr (symbol, value, binary) VALUES (?, ?, 1)', (self.symbol_var.get(), self.value_var.get()))

                conn.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")

    def delete(self):
        """
        Deletes a support/resistance level based on user input.

        Raises:
            Warning: If the support/resistance level already deleted or has been added.
        """
        try:
            with self.db_connection as conn:
                cursor = conn.cursor()

                # Fetch existing values for the specified stock symbol
                cursor.execute('SELECT value, binary FROM modify_sr WHERE symbol = ?', (self.symbol_var.get(),))
                existing_values = cursor.fetchall()

                # Check for duplication or opposite pair
                duplication = any(float(old_value[0]) == float(self.value_var.get()) and float(old_value[1]) == 0 for old_value in existing_values)
                oppositePair = any(float(old_value[0]) == float(self.value_var.get()) and float(old_value[1]) == 1 for old_value in existing_values)

                # Handle cases of duplication or opposite pair
                if duplication:
                    messagebox.showwarning("Support/Resistance already deleted!")
                elif oppositePair:
                    cursor.execute('DELETE FROM modify_sr WHERE symbol=? AND value=? AND binary=1', (self.symbol_var.get(), self.value_var.get()))
                else:
                    cursor.execute('INSERT INTO modify_sr (symbol, value, binary) VALUES (?, ?, 0)', (self.symbol_var.get(), self.value_var.get()))

                conn.commit()

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
