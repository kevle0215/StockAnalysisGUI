import sqlite3
import os
import time
import datetime
import yfinance as yf
import sys
import os

# Get the directory of the script
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(script_dir, '..'))

from src.GetPrice import get_current_price
from datetime import timedelta, datetime

def send_notification(title, message):
    """
    Sends a desktop notification.

    Args:
        title (str): The title of the notification.
        message (str): The content of the notification.

    """
    os.system(f"osascript -e 'display notification \"{message}\" with title \"{title}\"'")


def get_support_resistance_values(symbol):
    """
    Retrieves the support/resistance values for a given symbol from the database.

    Args:
        symbol (str): The stock symbol.

    Returns:
        List[float]: A list of support/resistance values.
    """

    try:
        with sqlite3.connect('stock_data.db') as conn:
            cursor = conn.cursor()

            # Get column names excluding the last 4 columns
            cursor.execute("PRAGMA table_info(support_resistance)")
            columns_info = cursor.fetchall()
            column_names = [f"sr{idx}" for idx in range(len(columns_info) - 4)]
            maximumSR = ', '.join(column_names)

            # Fetch support/resistance values for the specified symbol
            cursor.execute(f'SELECT {maximumSR} FROM support_resistance WHERE symbol=?', (symbol,))
            sr_values = cursor.fetchone()

            # Filter out None values from the list of support/resistance values
            sr_not_none = [round(sr, 2) for sr in sr_values if sr is not None]

        return sr_not_none

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
        return []

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []


def update_value(symbol, column_name, new_value):
    """
    Updates a specific value in the stock_boundaries table for a given symbol.

    Args:
        symbol (str): The stock symbol.
        column_name (str): The name of the column to be updated.
        new_value: The new value to be set.

    """
    try:
        with sqlite3.connect('stock_data.db') as conn:
            cursor = conn.cursor()

            # update new value in specified column
            cursor.execute(f'UPDATE stock_boundaries SET {column_name}=? WHERE symbol=?', (new_value, symbol))

        print(f"Updated {column_name} for {symbol} to {new_value}")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def notification_setup():
    """
    Performs the setup for stock notifications based on support and resistance boundaries.

    """
    try:
        # Connect to the SQL database
        with sqlite3.connect('stock_data.db') as conn:
            cursor = conn.cursor()

            # Fetch stock symbols
            cursor.execute('SELECT symbol FROM stock_boundaries')
            symbolList_raw = cursor.fetchall()

            # Clean up excess parentheses in the stock list
            symbolList = [symbol[0] for symbol in symbolList_raw]

            for symbol in symbolList:
                # Get the current stock price
                currentPrice = get_current_price(symbol)

                # Fetch support and resistance boundaries for the stock
                cursor.execute('SELECT support, resistance, support_distance, resistance_distance '
                               'FROM stock_boundaries WHERE symbol=?', (symbol,))
                sr = cursor.fetchone()

                # Calculate distances from current price to support and resistance
                supportDistance_new = round((currentPrice - sr[0]) / currentPrice, 3)
                resistanceDistance_new = round((sr[1] - currentPrice) / currentPrice, 3)

                # Current price close to support
                if supportDistance_new < sr[2]:
                    supportPercent = supportDistance_new * 100
                    message = f"{symbol} is {supportPercent}% away from the support {sr[0]}"
                    send_notification(f'{symbol} Stock Notification', message)

                    # Update the support distance value
                    update_value(symbol, 'support_distance', sr[2])

                # Current price close to resistance
                elif resistanceDistance_new < sr[3]:
                    resistancePercent = resistanceDistance_new * 100
                    message = f"{symbol} is {resistancePercent}% away from the resistance {sr[1]}"
                    send_notification(f'{symbol} Stock Notification', message)

                    # Update the resistance distance value
                    update_value(symbol, 'resistance_distance', sr[3])

                # Current price below support
                elif supportDistance_new < 0:
                    broken_support(symbol, sr[0])

                # Current price above resistance
                elif resistanceDistance_new < 0:
                    broken_resistance(symbol, sr[1])

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


def broken_support(symbol, old_value, db_connection = None):
    """
    Adjusts support and resistance values when the current price falls below the support level.

    Args:
        symbol (str): Stock symbol.
        old_value (float): The old support value.
    """
    try:
        # Get the filtered support/resistance values
        sr_filtered = get_support_resistance_values(symbol)

        # Try to find the new support value
        new_value = sr_filtered[sr_filtered.index(old_value) - 1]

    except IndexError:
        # If IndexError occurs, fetch historical stock data from the last 365 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Find the lowest closing price in the last 365 days
        lowest_price = stock_data['Close'].min()

        new_value = lowest_price
    
    db_connection = db_connection or sqlite3.connect('stock_data.db')
    with db_connection as conn:

        # Update the support and resistance values
        update_value(conn, symbol, 'support', new_value)
        update_value(conn, symbol, 'resistance', old_value)

        # Get the current price
        current_price = get_current_price(symbol)

        # Update the support and resistance distances
        support_distance = (current_price - new_value) / current_price
        resistance_distance = (old_value - current_price) / current_price

        update_value(conn, symbol, 'support_distance', support_distance)
        update_value(conn, symbol, 'resistance_distance', resistance_distance)

def broken_resistance(symbol, old_value):
    """
    Adjusts support and resistance values when the current price rises above the resistance level.

    Args:
        symbol (str): Stock symbol.
        old_value (float): The old resistance value.
    """
    try:
        # Get the filtered support/resistance values
        sr_filtered = get_support_resistance_values(symbol)

        # Try to find the new resistance value
        new_value = sr_filtered[sr_filtered.index(old_value) + 1]

    except IndexError:
        # If IndexError occurs, fetch historical stock data from the last 365 days
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')

        stock_data = yf.download(symbol, start=start_date, end=end_date)

        # Find the highest closing price from the last 365 days
        highest_price = stock_data['Close'].max()

        new_value = highest_price

    with sqlite3.connect('stock_data.db') as conn:
        # Update the resistance and support values
        update_value(conn, symbol, 'resistance', new_value)
        update_value(conn, symbol, 'support', old_value)

        # Get the current price
        current_price = get_current_price(symbol)

        # Update the resistance and support distances
        resistance_distance = (new_value - current_price) / current_price
        support_distance = (current_price - old_value) / current_price

        update_value(conn, symbol, 'support_distance', support_distance)
        update_value(conn, symbol, 'resistance_distance', resistance_distance)

def main_loop():
    """
    Main loop to continuously check and process notifications based on the running_var value in the database.

    """
    while True:

        with sqlite3.connect('stock_data.db') as conn:
            cursor = conn.cursor()

            # Fetch the running_var value from the script_state table
            cursor.execute('SELECT running_var FROM script_state WHERE id=0')
            truth_value = cursor.fetchone()[0]

            # Check if notifications should be on or off based on the running_var value
            if truth_value == "True":
                notification_setup()
        
        # sleep the while loop for 60 (seconds)
        time.sleep(60)

if __name__ == "__main__":
    main_loop()
    
