from datetime import datetime, timedelta
import yfinance as yf


def get_last_close_price(symbol):
    """
    Retrieves the last available closing price for a given stock symbol within the last 30 days.

    Args:
        symbol (str): The stock symbol.

    Returns:
        float or None: The last closing price if successful, None otherwise.
    """
    try:
        # Get historical data for the last 30 days
        end_date = datetime.now().strftime('%Y-%m-%d')  # Current date
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')  # 30 days ago
        historical_data = yf.download(symbol, start=start_date, end=end_date)

        # Extract the last available closing price
        last_close_price = historical_data['Close'].iloc[-1]

        return last_close_price
    
    except yf.YFinanceError as yfe:
        print(f"Error while retrieving data for {symbol}: {yfe}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_current_price(symbol):
    """
    Retrieves the current or the most recent closing price for a given stock symbol.

    Args:
        symbol (str): The stock symbol.

    Returns:
        float or None: The current or the most recent closing price if successful, None otherwise.
    """
    try:
        company = yf.Ticker(symbol)
        current_price = company.info.get("regularMarketPrice") or company.info.get("previous_close")

        if current_price is not None:
            return round(current_price, 2)
        else:
            # If current price is not available, fallback to the last close price
            return round(get_last_close_price(symbol), 2)
        
    except yf.YFinanceError as yfe:
        print(f"Error while retrieving data for {symbol}: {yfe}")
        return None
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

if __name__ == "__main__":
    get_last_close_price("AMC")
