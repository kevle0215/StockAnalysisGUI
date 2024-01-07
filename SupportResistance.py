import yfinance as yf
import numpy as np


def support_resistance(symbol, start_date, end_date, interval, touches, sensitivity):
    """
    Detect support and resistance levels in the historical stock price data.

    Args:
        symbol (str): Stock symbol.
        start_date (str): Start date for historical data retrieval (YYYY-MM-DD).
        end_date (str): End date for historical data retrieval (YYYY-MM-DD).
        interval (str): Data interval for stock prices (e.g., '1d' for daily).
        touches (int): Minimum number of touches to consider a level.
        sensitivity (int): Sensitivity factor for level detection.

    Returns:
        list: List of support and resistance levels detected in the form of [min_level, max_level].
    """
    try:
        # Download and sort historical highs and lows of stock data
        data = yf.download(symbol, start=start_date, end=end_date, interval=interval)
        prices = np.concatenate((data['Low'].values, data['High'].values))
        prices.sort()

        # Stores all supports and resistances
        sr_total_array = []

        # Iterates through all prices once
        i = 0
        while i < len(prices) - 1:

            # Bottom of support/resistance range
            bottom = prices[i]
            sr_array = [bottom]

            # Assumes the top is one element above the bottom
            j = i + 1
            top = prices[j]

            # Iterates through the top until the top is greater than (0.04*(0.5^sensitivity)) away or all prices have been iterated through
            while top <= bottom * (1 + 0.04 * (0.5 ** sensitivity)) and j < len(prices):
                top = prices[j]

                if top <= bottom * (1 + 0.04 * (0.5 ** sensitivity)):
                    sr_array.append(top)
                    j += 1
                else:
                    break

            # Check if the detected level has enough touches
            if len(sr_array) >= float(touches):

                # Store the detected level as [min_level, max_level]
                sr_array = [min(sr_array), max(sr_array)]
                sr_total_array.append(sr_array)
                
                i = j + 1

            else:
                i += 1

        return sr_total_array

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []