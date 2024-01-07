import sqlite3
import bisect
from GetPrice import get_current_price
from datetime import date, timedelta
from SupportResistance import support_resistance

class Notification:
    def __init__(self, symbol, days, touches, sensitivity):
        """
        Initializes the Notification instance.

        Args:
            symbol (str): The stock symbol.
            days (int): The number of days for historical data retrieval.
            touches (int): The number of touches for support/resistance calculation.
            sensitivity (int): The sensitivity factor for support/resistance calculation.
            srArray (list): All support and resistance values for one stock
            upperboundDate (date): Upperbound on support and resistance calculations
            lowerboundDate (date): Lowerbound on support and resistance calculations
            currentPrice (float): Current price of stock
        """
        self._symbol = symbol
        self._days = days
        self._touches = touches
        self._sensitivity = sensitivity
        self._srArray = []
        self._upperboundDate = date.today()
        self._lowerboundDate = self._upperboundDate - timedelta(self._days)
        self._currentPrice = get_current_price(self._symbol)

    def calculate_sr(self):
        """
        Calculates support/resistance values based on historical data and updates database.

        """
        # Calculate support/resistance values using the specified parameters
        srArrayRaw = support_resistance(self._symbol, self._lowerboundDate, self._upperboundDate, '1d', self._touches, self._sensitivity)
        
        # Process and append the calculated values to the internal list
        self._srArray.extend(round((sr[0] + sr[1]) / 2, 2) for sr in srArrayRaw)

        try:
            with sqlite3.connect('stock_data.db') as conn:
                cursor = conn.cursor()

                # Insert notification details into the support_resistance table
                cursor.execute("INSERT INTO support_resistance (symbol, day_range, touches, sensitivity) VALUES (?, ?, ?, ?)",
                            (self._symbol, self._days, self._touches, self._sensitivity))

        except sqlite3.IntegrityError:
            print("Symbol already present in the database. Please insert a new symbol.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        finally:
            # Process and append manual support and resistance additions
            cursor.execute('SELECT value, binary FROM modify_sr WHERE symbol = ?', (self._symbol,))
            modifications = cursor.fetchall()

            for modification in modifications:
                if modification[1] == 1: # binary value of 1 and 0 are addition and removal, respectively
                    self._srArray.append(modification[0])

        # Sort the list of support/resistance values
        self._srArray.sort()

        with sqlite3.connect('stock_data.db') as conn:
            cursor = conn.cursor()

            # Update support_resistance table with modified support/resistance values
            for idx, sr_value in enumerate(self._srArray):
                cursor.execute("SELECT binary FROM modify_sr WHERE symbol = ? AND value = ?", (self._symbol, sr_value))
                result = cursor.fetchall()

                # update only when no modifications are present or the modification is adding the support/resistance
                if not result or result[0][0] == 1:
                    cursor.execute(f"UPDATE support_resistance SET sr{idx} = ? WHERE symbol = ?",
                                (sr_value, self._symbol))
                    conn.commit()

    def boundary_setup(self):
        """
        Sets up stock boundaries based on support/resistance values and updates the database.

        """
        try:
            with sqlite3.connect('stock_data.db') as conn:
                cursor = conn.cursor()

                # Retrieve information about the columns in the support_resistance table
                cursor.execute("PRAGMA table_info(support_resistance)")
                columns_info = cursor.fetchall()

                # Extract column names for 'sr0', 'sr1', ..., excluding the last 4 columns
                maximumSR = ', '.join([f"sr{idx}" for idx in range(len(columns_info) - 4)])

                # Retrieve support/resistance values for the specified symbol
                cursor.execute(f'SELECT {maximumSR} FROM support_resistance WHERE symbol=?', (self._symbol,))
                srRaw = cursor.fetchall()

                # Filter out None values from the list of support/resistance values
                srNotNone = [sr for sr in srRaw[0] if sr is not None]

                # Calculate support, resistance, support distance, and resistance distance
                support = round(srNotNone[bisect.bisect(srNotNone, self._currentPrice) - 1], 2)
                resistance = round(srNotNone[bisect.bisect(srNotNone, self._currentPrice)], 2)
                support_distance = round((self._currentPrice - support) / self._currentPrice, 3)
                resistance_distance = round((resistance - self._currentPrice) / self._currentPrice, 3)

                # Insert calculated values into the stock_boundaries table
                cursor.execute('INSERT INTO stock_boundaries (symbol, support, resistance, support_distance, resistance_distance) '
                            'VALUES (?, ?, ?, ?, ?)',
                            (self._symbol, support, resistance, support_distance, resistance_distance))

        except sqlite3.IntegrityError:
            print("Symbol already present in the database. Please insert a new symbol.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        else:
            conn.commit()

        finally:
            conn.close()

    def delete_notification(self):
        """
        Deletes a notification's data from the database.

        """
        try:
            with sqlite3.connect('stock_data.db') as conn:
                cursor = conn.cursor()

                # Delete entries related to the symbol from support_resistance and stock_boundaries tables
                cursor.execute("DELETE FROM support_resistance WHERE symbol=?", (self._symbol,))
                cursor.execute("DELETE FROM stock_boundaries WHERE symbol=?", (self._symbol,))

        except sqlite3.OperationalError:
            print("Symbol is not present in the database. Please create a new notification first.")

        except Exception as e:
            print(f"An unexpected error occurred: {e}")

        else:
            conn.commit()
