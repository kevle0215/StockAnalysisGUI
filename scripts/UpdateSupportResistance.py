import tkinter as tk
import sqlite3
from NotificationWindow import NotificationWindow
from Notification import Notification

def update_sr():
    """
    Update support and resistance levels for stocks stored in the 'support_resistance' table.
    
    """
    try:
        # Use a context manager for database operations
        with sqlite3.connect('stock_data.db') as conn:
            cursor = conn.cursor()

            # Fetch stock data from the 'support_resistance' table
            cursor.execute('SELECT symbol, day_range, touches, sensitivity FROM support_resistance')
            stock_data = cursor.fetchall()

            for stock in stock_data:
                try:
                    # Extract stock information
                    symbol, day_range, touches, sensitivity = stock

                    # Create a Notification instance for the stock
                    notification = Notification(symbol, day_range, touches, sensitivity)

                    # Delete existing notifications for the stock
                    notification.delete_notification()

                    # Calculate and set new support/resistance levels
                    notification.calculate_sr()
                    
                    # Set up new boundaries for the stock
                    notification.boundary_setup()

                except Exception as inner_exc:
                    print(f"An unexpected error occurred while processing stock {symbol}: {inner_exc}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

if __name__ == "__main__":
    update_sr()
