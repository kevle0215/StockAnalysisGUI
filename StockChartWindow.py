import tkinter as tk
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from mplfinance.original_flavor import candlestick_ohlc
import matplotlib.dates as mdates
import mplcursors
from matplotlib.patches import Rectangle
import SupportResistance
import matplotlib.colors as mcolors

class StockChartWindow:
    def __init__(self, master, symbol, startDate, endDate, interval, touches, sensitivity):
        """
        Initializes the StockChartWindow.

        Args:
            master (Tk): The root Tkinter window.
            symbol (str): The stock symbol.
            startDate (str): The start date for retrieving stock data.
            endDate (str): The end date for retrieving stock data.
            interval (str): The time interval for stock data (e.g., '1d' for daily).
            touches (int): Number of touches for support and resistance calculation.
            sensitivity (int): Sensitivity level for support and resistance calculation.
        """
        self.master = master
        self.StockChartWindow = tk.Toplevel(self.master)
        self.StockChartWindow.title(f"{symbol} Stock Chart")

        self.symbol = symbol
        self.startDate = startDate
        self.endDate = endDate
        self.interval = interval
        self.touches = touches
        self.sensitivity = sensitivity
    
    def create_stock_chart(self):
        """
        Creates and displays a candlestick chart with support and resistance zones.
        """
        # Blank stock chart creation
        fig, ax = plt.subplots()
        fig.subplots_adjust(bottom=0.2)
        chart_canvas = FigureCanvasTkAgg(fig, master=self.StockChartWindow)
        chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Create toolbar
        toolbar = NavigationToolbar2Tk(chart_canvas, self.StockChartWindow)
        toolbar.update()
        chart_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        # Place cursor on stock chart
        cursor = mplcursors.cursor(hover=True)
        cursor.connect("add", lambda sel: sel.annotation.set_text(
            f"{mdates.num2date(sel.target[0]).strftime('%Y-%m-%d %H:%M:%S')}\nPrice: {sel.target[1]:.2f}"))
        
        # Price data
        data = yf.download(self.symbol, start=self.startDate, end=self.endDate, interval=self.interval)
        ohlc = data[['Open', 'High', 'Low', 'Close']].copy()
        ohlc.reset_index(inplace=True)
        ohlc['Date'] = ohlc['Date'].map(mdates.date2num)

        # Candlestick chart setup
        candlestick_ohlc(ax, ohlc.values, width=0.6, colorup='g', colordown='r')
        ax.set_xlabel("Date")
        ax.set_ylabel("Price")
        ax.set_title(f"Candlestick Chart for {self.symbol}")

        # Format x-axis as dates
        ax.xaxis_date()
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        plt.xticks(rotation=45)

        # Salculate supports and resistances
        srArray = SupportResistance.support_resistance(self.symbol, self.startDate, self.endDate, self.interval, self.touches, self.sensitivity)

        for sr in srArray:
            
            # Support and resistance date boundaries
            date_1 = find_date(ohlc, sr[0])
            date_2 = find_date(ohlc, sr[1])

            # Create rectangle to denote all supports and resistances
            zone = Rectangle((min(date_1, date_2), sr[0]), max(date_1, date_2) - min(date_1, date_2),
                            sr[1]-sr[0], fc=mcolors.to_rgba('red', 0.5))
            ax.add_patch(zone)


def find_date(data, target_price):
    """
    Finds the date corresponding to a given target price in the stock data.

    Args:
        data (DataFrame): Stock price data.
        target_price (float): Target price for which the date needs to be found.

    Returns:
        datetime: The date corresponding to the target price.
    """

    filtered_data = data[(data['Close'] == target_price) |
                         (data['Open'] == target_price) |
                         (data['High'] == target_price) |
                         (data['Low'] == target_price)]
    
    # Chooses the lowest possible date
    price_date = min(filtered_data['Date'].values)

    return price_date

if __name__ == "__main__":
    root = tk.Tk()
    app = StockChartWindow(root, "AMC", "2023-08-11", "2023-12-11", "1d", "3", "1")
    root.mainloop()
